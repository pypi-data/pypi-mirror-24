"""
Copyright (C) 2011, 2012, 2013 Michal Goral.

This file is part of Subconvert

Subconvert is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Subconvert is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Subconvert. If not, see <http://www.gnu.org/licenses/>.
"""
import os
import re
import collections
from enum import Enum
from html.parser import HTMLParser

from subconvert.parsing.FrameTime import FrameTime
from subconvert.parsing.Core import Subtitle, SubManager
from subconvert.utils.SubException import SubAssert
from subconvert.utils.Locale import _

_Tag = collections.namedtuple('Tag', ('text', 'start', 'end'))

def _find_nested_pair(string, open_ch, close_ch, start):
    '''Finds a pair of tag characters. This handles nested tags in a form:
        [tag1[tag2]]

    In above example, when searched from the first character, this function
    returns first and last position, not first and second to last.'''
    pos_start = None
    opened = []
    found = []
    min_found = len(string) + 1, len(string) + 1
    for pos, ch in enumerate(string[start:], start=start):
        if ch == open_ch:
            opened.append(pos)

        if ch == close_ch:
            if opened:
                found.append((opened.pop(), pos))
                if len(opened) == 0:
                    return found[-1]
                else:
                    min_found = min(min_found, found[-1])

    if found:
        return min_found

    # Same value as str.find
    return -1, -1


def find_tag(string, open_ch, close_ch, start=0):
    '''Finds a first tag in string, delimited with given characters, starting at
    position `start`'''
    open, close = _find_nested_pair(string, open_ch, close_ch, start)
    if open != -1 and close != -1:
        return _Tag(string[open+1:close], open, close)
    return _Tag(None, None, None)


def find_all_tags(string, open_ch, close_ch):
    '''Finds all level-0 (not nested) tags.'''
    ret = []
    start = 0
    while True:
        found = find_tag(string, open_ch, close_ch, start)
        if found.start is None:
            break
        ret.append(found)
        start = found.end + 1
    return ret


# https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
class _Stripper(HTMLParser):
    '''Strips HTML tags from any given input'''
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

class SubFormat:
    """A general description of subtitle format. Should be specialized for each format."""
    NAME = 'Generic'
    EXTENSION = 'sub'
    OPT = None

    def __init__(self, fps=None, subtitles=None):
        self._fps = fps
        self._parsing_error = ''

        if subtitles:
            self._subtitles = subtitles
        else:
            self._subtitles = SubManager()

    #
    # Below are methods which can be reimplemented by specific formats
    ############################################################################

    def feed(self, line):
        '''Parse next lines of subtitles. Should return True if line is accepted
        and False if it's not (current format is unable to parse it).'''
        raise NotImplementedError

    def eof(self):
        '''Indicate to SubFormat that there's nothing more to be parsed. Returns
        True if current format accepts this information and False if it would
        mean that it's irrecoverable situation or all or some data would be lost
        due to this situation.'''
        return True

    @property
    def formatting(self):
        '''Returns a string describing Format's formatting. This string is
        formatted by performing a string substitution with named parameters:

            %(subno)s: subtitle number (starting from 0)
            %(t_start)s, %(t_end): formatted start and end time of subtitle
            %(text)s: styled subtitle text
            %(lf)s: newline character'''
        raise NotImplementedError

    def to_frametime(self, text):
        '''Convert format-specific time to FrameTime. If format accepts such
        values, received text can be empty, None or whatever is suitable.'''
        raise NotImplementedError

    def from_frametime(self, ft):
        '''Convert FrameTime to format-specific formatted time. Received ft may
        be None if format accepts such values.'''
        raise NotImplementedError

    def to_common_format(self, text):
        '''Convert a format-specific styled text to a common style
        understandable by all formats (HTML-like one). By default, it doesn't
        change anything.'''
        return text

    def style_text(self, text):
        '''Convert common (HTML-styling) to format-specific one. By default it
        removes all styling information.'''
        strp = _Stripper()
        strp.feed(text)
        return strp.get_data()

    @property
    def output(self):
        '''Generator which returns formatted (converted) subtitles, one by
        one.

        If this method is reimplemented, it's recommended to call the original
        one at some point, like that:

            @property
            def output(self):
                # some format-specific code
                yield sth

                yield from super().output
        '''
        for no, sub in enumerate(self.subtitles):
            fmt_d = dict(lf=os.linesep,
                         subno=no,
                         t_start=self.from_frametime(sub.start),
                         t_end=self.from_frametime(sub.end),
                         text=self.style_text(sub.text))
            yield self.formatting % fmt_d

    #
    # End of reimplementable methods. Below are some public and private helper
    # methods which should be used as-is.
    ############################################################################

    @property
    def fps(self):
        '''FPS of subtitles'''
        return self._fps

    @property
    def subtitles(self):
        '''A list of parsed (or loaded) subtitles'''
        return self._subtitles

    @property
    def error(self):
        '''An error produced by a specific format during subtitles parsing'''
        return self._parsing_error

    def _add_subtitle(self, start, end, text):
        sub = Subtitle(self.to_frametime(start),
                       self.to_frametime(end),
                       self.to_common_format(text))

        if start and text:
            self.subtitles.append(sub)
        elif start and not text:
            pass
        else:
            raise SubException(_('Incorrect subtitle'))

    def _error(self, txt='', ret=False):
        self._parsing_error = txt
        return ret

    def __hash__(self):
        return self.NAME.__hash__()


class MicroDVD(SubFormat):
    NAME = 'Micro DVD'
    OPT = 'microdvd'
    EXTENSION = 'sub'

    # XXX: MicroDVD serves also as a base class for one-line-formats, so keep it
    # in mind when modifying it.
    def __init__(self, *a, **kw):
        self._pattern = re.compile(r'''
            ^
            \{(?P<t_start>\d+)\}  # {digits}
            \{(?P<t_end>\d+)\}    # {digits}
            (?P<text>[^\r\n]*)''',
            re.X)

        self._style_pattern = re.compile(r'</?[biu]>|<br/>')

        super().__init__(*a, **kw)

    def feed(self, line):
        m = self._pattern.search(line)
        if m:
            self._add_subtitle(self._group(m, 't_start'),
                               self._group(m, 't_end'),
                               self._group(m, 'text'))
            return True
        elif line.strip() == '':
            return True
        return self._error(_('not a %s format') % self.NAME)

    @property
    def formatting(self):
        return '{%(t_start)s}{%(t_end)s}%(text)s%(lf)s'

    def to_frametime(self, text):
        return FrameTime.InitFrames(text, self.fps)

    def from_frametime(self, frametime):
        SubAssert(frametime.frame >= 0, _("Negative time present."))
        return frametime.frame

    def to_common_format(self, text):
        lines = text.split('|')
        for i, line in enumerate(lines):
            tags = find_all_tags(line, '{', '}')
            for tag in reversed(tags):
                if tag.text == 'y:b':
                    line = '%s<b>%s</b>' % (line[:tag.start], line[tag.end + 1:])
                elif tag.text == 'y:i':
                    line = '%s<i>%s</i>' % (line[:tag.start], line[tag.end + 1:])
                elif tag.text == 'y:u':
                    line = '%s<u>%s</u>' % (line[:tag.start], line[tag.end + 1:])
            lines[i] = line

        return '<br/>'.join(lines)

    def style_text(self, text):
        text = self._style_pattern.sub(self._style_fn, text)
        return super().style_text(text)  # remove any additional styling

    def _style_fn(self, match):
        text = match.group(0)
        if text == '<br/>':
            return '|';
        elif text[1] == '/':  # closing tag
            return ''
        else:
            return '{y:%s}' % text[1]

    def _group(self, m, name, default=None):
        try:
            return m.group(name)
        except IndexError:
            return default

class SubRip(SubFormat):
    NAME = 'Sub Rip'
    OPT = 'subrip'
    EXTENSION = 'srt'

    class _State(Enum):
        # Idle: when not waiting for text (between subtitles)
        # WaitForText: subtitle times parsed
        Idle = 0
        WaitForText = 1

    def __init__(self, *a, **kw):
        self._state = SubRip._State.Idle
        self._curr_start = None
        self._curr_end = None
        self._curr_text = []

        self._time_pattern = re.compile(r'''
            ^
            \d*\s*
            (?P<t_start>\d+:\d{2}:\d{2},\d+)  # 00:00:00,000
            [ \t]*-->[ \t]*
            (?P<t_end>\d+:\d{2}:\d{2},\d+)''',
            re.X)

        super().__init__(*a, **kw)

    def feed(self, line):
        if self._state == self._State.Idle:
            tm = self._time_pattern.search(line)
            if tm:
                self._curr_start = tm.group('t_start')
                self._curr_end = tm.group('t_end')
                self._state = self._State.WaitForText
                return True

            # omit empty lines and lines with subtitle numbers
            line = line.strip()
            if line == '' or line.isnumeric():
                return True
            return self._error(_('expected time header, got: %s') % line)

        elif self._state == self._State.WaitForText:
            if line.strip() == '':
                self._state = self._State.Idle
                self._add_subtitle()
            else:
                self._curr_text.append(line)
            return True

        return self._error(_('unexpected line: %s') % line)

    def eof(self):
        if self._curr_start and not self._curr_text:
            return self._error(_('unexpected end of file; expected subtitle text'))
        elif self._curr_start and self._curr_end and self._curr_text:
            self._add_subtitle()
        return True

    @property
    def formatting(self):
        return '%(subno)s%(lf)s' \
                '%(t_start)s --> %(t_end)s%(lf)s' \
                '%(text)s%(lf)s%(lf)s'

    def to_frametime(self, text):
        timestr = '.'.join(text.rsplit(',', 1))
        return FrameTime.InitTimeStr(timestr, self.fps)

    def from_frametime(self, frametime):
        SubAssert(frametime.ms >= 0, _("Negative time present."))
        t = frametime.time
        return '%02d:%02d:%02d,%03d' % (t['hours'], t['minutes'], t['seconds'],
                                        t['milliseconds'])

    def style_text(self, text):
        text = os.linesep.join(text.split('<br/>'))
        return text  # we'll simply accept all HTML

    def _add_subtitle(self):
        text = '<br/>'.join(self._curr_text)
        super()._add_subtitle(self._curr_start, self._curr_end, text)
        self._clear_curr()

    def _clear_curr(self):
        self._curr_start = None
        self._curr_end = None
        self._curr_text = []


class SubViewer(SubFormat):
    NAME = 'SubViewer 1.0'
    OPT = 'subviewer'
    EXTENSION = 'sub'

    class _State(Enum):
        # States:
        # Idle: when not waiting for text (in header or between subtitles)
        # WaitForText: subtitle times parsed
        Idle = 1
        WaitForText = 2


    def __init__(self, *a, **kw):
        self._state = SubViewer._State.Idle
        self._curr_start = None
        self._curr_end = None
        self._curr_text = []

        # subtitles will be parsed only when between [SUBTITLE] and [END
        # SUBTITLE] tags
        self._subtitle_opened = 0

        # a flag indicating whether subviewer encountered first [SUBTITLE] tag.
        # Used to early break subtitles parsing (otherwise MPL format could be
        # fully parsed as a format which contains only tags)
        self._subtitle_encountered = False
        self._lines_feeded = 0

        self._time_pattern = re.compile(r'''
            ^
            (?P<t_start>\d{2}:\d{2}:\d{2}.\d{2})
            ,
            (?P<t_end>\d{2}:\d{2}:\d{2}.\d{2})''',
            re.X)

        super().__init__(*a, **kw)

        self.subtitles.meta.registerAlias('prg', 'program')
        self.subtitles.meta.registerAlias('style', 'font_style')
        self.subtitles.meta.registerAlias('size', 'font_size')
        self.subtitles.meta.registerAlias('colf', 'color')

    def feed(self, line):
        self._lines_feeded += 1

        if self._state == self._State.Idle:
            # XXX: start parsing subtitles ONLY if there was previously
            # [SUBTITLE] tag encountered and it wasn't closed
            if self._subtitle_opened:
                tm = self._time_pattern.search(line)
                if tm:
                    self._curr_start = tm.group('t_start')
                    self._curr_end = tm.group('t_end')
                    self._state = self._State.WaitForText
                    return True

            # let's check tags
            tags = self._extract_tags(line)
            if tags:
                for tag, val in tags:
                    if tag == 'subtitle':
                        self._subtitle_opened += 1
                        self._subtitle_encountered = True
                    elif tag == 'end_subtitle':
                        self._subtitle_opened = max(0, self._subtitle_opened-1)
                    elif tag and val:  # only add tags with values
                        self.subtitles.meta.add(tag, val)

                # early break. If there's no [SUBTITLE] yet, it's probably not
                # SubViewer
                if not self._subtitle_encountered and self._lines_feeded > 35:
                    return self._error(
                        _('breaking too long wait for [SUBTITLE] tag'))
                return True

            # allow empty lines
            if line.strip() == '':
                # don't count empty lines to lines_feeded. They're cheap anyway
                self._lines_feeded = max(0, self._lines_feeded - 1)
                return True

            # at this point we only have to decide WHAT error will be reported
            if not self._subtitle_encountered:
                return self._error(
                    _('missing [SUBTITLE] tag before line: %s') % line)
            return self._error(_('expected time or tag, got: %s') % line)

        elif self._state == self._State.WaitForText:
            if line.strip() == '':
                self._state = self._State.Idle
                self._add_subtitle()
            else:
                self._curr_text.append(line)
            return True

        return self._error(_('unexpected line: %s') % line)

    def eof(self):
        if not self._subtitle_encountered:
            return self._error(_('missing [SUBTITLE] tag'))

        if self._curr_start and not self._curr_text:
            return self._error(_('unexpected end of file; expected subtitle text'))
        elif self._curr_start and self._curr_end and self._curr_text:
            self._add_subtitle()
        return True

    @property
    def formatting(self):
        return '%(t_start)s,%(t_end)s%(lf)s' \
                '%(text)s%(lf)s%(lf)s'

    def to_frametime(self, text):
        tstr = text + '0'
        return FrameTime.InitTimeStr(tstr, self.fps)

    def from_frametime(self, frametime):
        SubAssert(frametime.ms >= 0, _("Negative time present."))
        t = frametime.time
        ms = round(t['milliseconds'] / float(10))
        return '%02d:%02d:%02d.%02d' % (t['hours'], t['minutes'], t['seconds'], ms)

    def style_text(self, text):
        text = os.linesep.join(text.split('<br/>'))
        return super().style_text(text)  # remove any additional styling

    def _add_subtitle(self):
        text = '<br/>'.join(self._curr_text)
        super()._add_subtitle(self._curr_start, self._curr_end, text)
        self._clear_curr()

    def _extract_tags(self, string):
        ret = []
        tags = find_all_tags(string, '[', ']')

        def _format_tag(tag):
            return tag.lower().replace(' ', '_').strip()
        def _format_val(val):
            return val.strip(', \n\r\t')

        for i, tag in enumerate(tags):
            if len(tags) > i + 1:
                next_tag = tags[i + 1]
                tagname = _format_tag(tag.text)
                val = _format_val(string[tag.end + 1 : next_tag.start])
                ret.append((tagname, val))
            else:
                tagname = _format_tag(tag.text)
                val = _format_val(string[tag.end + 1:])
                ret.append((tagname, val))
        return ret

    def _clear_curr(self):
        self._curr_start = None
        self._curr_end = None
        self._curr_text = []

    @property
    def output(self):
        meta = self.subtitles.meta
        title = meta.get('title', '')
        author = meta.get('author', '')
        source = meta.get('source', '')
        program = meta.get('program', 'SubConvert')
        filepath = meta.get('filepath', '')
        delay = meta.get('delay', '0')
        cd_track = meta.get('cd_track', '0')
        comment = meta.get('comment', 'Converted to subviewer format with SubConvert')
        color = meta.get('color', '&HFFFFFF')
        font_style = meta.get('font_style', 'no')
        font_size = meta.get('font_size', '24')
        font = meta.get('font', 'Tahoma')
        yield os.linesep.join([ \
            '[INFORMATION]', '[TITLE]%s' % title, '[AUTHOR]%s' % author, \
            '[SOURCE]%s' % source, '[PRG]%s' % program, '[FILEPATH]%s' % filepath, \
            '[DELAY]%s' % delay, '[CD TRACK]%s' % cd_track, '[COMMENT]%s' % comment, \
            '[END INFORMATION]', '[SUBTITLE]',
            '[COLF]%s,[STYLE]%s,[SIZE]%s,[FONT]%s%s' % \
            (color, font_style, font_size, font, os.linesep)])
        yield from super().output


class TMP(MicroDVD):
    NAME = 'TMP'
    OPT = 'tmp'
    EXTENSION = 'txt'

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        # TMP inherits from MicroDVD, because parsing is basically the same
        # here, only _pattern differs.
        self._pattern = re.compile(r'''
            ^
            (?P<t_start>\d+:\d{2}:\d{2})
            :
            (?P<text>[^\r\n]+)
            ''',
            re.X)

    @property
    def formatting(self):
        return '%(t_start)s:%(text)s%(lf)s'

    def to_frametime(self, text):
        if text:
            return FrameTime.InitTimeStr(text, self.fps)
        return None

    def from_frametime(self, frametime):
        if frametime:
            SubAssert(frametime.ms >= 0, _("Negative time present."))
            t = frametime.time
            return '%02d:%02d:%02d' % (t['hours'], t['minutes'], t['seconds'])
        return None


class MPL2(MicroDVD):
    NAME = 'MPL2'
    OPT = 'mpl2'
    EXTENSION = 'txt'

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        # MPL2 inherits from MicroDVD, because parsing is basically the same
        # here, only _pattern differs.
        self._pattern = re.compile(r'''
            ^
            \[(?P<t_start>\d+)\]  # {digits}
            \[(?P<t_end>\d+)\]    # {digits}
            (?P<text>[^\r\n]*)''',
            re.X)

    @property
    def formatting(self):
        return "[%(t_start)s][%(t_end)s]%(text)s%(lf)s"

    def to_frametime(self, text):
        text = ''.join(['0', text]) # Parsing "[0][5] sub" would cause an error without this
        ms = int(text[-1]) * 100
        seconds = int(text[:-1])
        return FrameTime(1000 * seconds + ms, self.fps)

    def from_frametime(self, frametime):
        SubAssert(frametime.ms >= 0, _("Negative time present."))
        return round(frametime.ms / 100)

    def to_common_format(self, text):
        lines = text.split('|')
        for i, line in enumerate(lines):
            if line.startswith('/'):
                lines[i] = '<i>' + line[1:] + '</i>'
        return '<br/>'.join(lines)

    def _style_fn(self, match):
        text = match.group(0)
        if text == '<br/>':
            return '|';
        elif text == '<i>':
            return '/'
        return ''
