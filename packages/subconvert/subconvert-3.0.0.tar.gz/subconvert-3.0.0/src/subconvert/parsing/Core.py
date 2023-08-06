#-*- coding: utf-8 -*-

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
import codecs

from subconvert.parsing.FrameTime import FrameTime
from subconvert.utils.Locale import _
from subconvert.utils.SubException import SubException, SubAssert
from subconvert.utils.Alias import *

#TODO: add comparing Subtitles (i.e. __eq__, __ne__ etc.)
class Subtitle():
    def __init__(self, start = None, end = None, text = None):
        self._start = None
        self._end = None
        self._text = None
        self.change(start, end, text)

    def _validateFps(self, start, end):
        startFps = None
        endFps = None
        if start and end:
            startFps = start.fps
            endFps = end.fps
        elif end and self._start:
            startFps = self._start.fps
            endFps = end.fps
        elif start and self._end:
            startFps = start.fps
            endFps = self._end.fps

        if startFps != endFps:
            raise ValueError("Subtitle FPS values differ: %s != %s" % (startFps, endFps))

    def clone(self):
        other = Subtitle()
        other._start = self._start.clone()
        other._end = self._end.clone()
        other._text = self._text
        return other

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def text(self):
        return self._text

    @property
    def fps(self):
        if self._start:
            return self._start.fps
        return None

    @fps.setter
    def fps(self, value):
        if self._start:
            self._start.fps = value
        if self._end:
            self._end.fps = value

    def change(self, start = None, end = None, text = None):
        self._validateFps(start, end)
        if start is not None:
            self._start = start
        if end is not None:
            self._end = end
        if text is not None:
            self._text = text

    def empty(self):
        return not (bool(self._start) or bool(self._end) or bool(self._text))

class Meta(AliasBase):
    def __init__(self):
        super().__init__()
        self._entries = {}

    def clone(self):
        other = Meta()
        other._aliases = self._aliases.copy()
        other._entries = self._entries.copy()
        return other

    @acceptAlias
    def add(self, entry, value):
        self._entries[entry] = value

    @acceptAlias
    def erase(self, entry):
        if entry in self._entries.keys():
            del self._entries[entry]

    @acceptAlias
    def get(self, entry, default=None):
        return self._entries.get(entry, default)

    def empty(self):
        return len(self._entries) == 0

    def clear(self):
        self._entries.clear()

class SubParsingError(SubException):
    '''Custom parsing error class.'''
    def __init__(self, message, lineNo):
        super().__init__("%d: %s" % (lineNo, message))
        self.lineNo = lineNo

class SubManager:
    def __init__(self):
        self._subs = []
        self._meta = Meta()

        # if sub has been appended without endTime, its auto endTime should be changed once when a
        # new sub is appended again
        self._invalidTime = False

    def _autoSetEnd(self, sub, nextSub = None):
        endTime = None
        if nextSub is None:
            endTime = sub.start + FrameTime(2500, sub.fps)
        else:
            endTime = sub.start + (nextSub.start - sub.start) * 0.85
        sub.change(end = endTime)

    def clone(self):
        other = SubManager()
        other._meta= self._meta.clone()
        other._invalidTime = self._invalidTime
        other._subs = []
        for sub in self._subs:
            other._subs.append(sub.clone())
        return other

    def insert(self, subNo, sub):
        if subNo >= 0:
            if len(self._subs) < subNo:
                self.append(sub)
            else:
                if sub.end is None:
                    self._autoSetEnd(sub, self._subs[subNo + 1])
                self._subs.insert(subNo, sub)
        else:
            raise ValueError("insert only accepts positive indices")

    def append(self, sub):
        if self._invalidTime:
            invalidSub = self._subs[-1]
            self._autoSetEnd(invalidSub, sub)
            self._invalidTime = False

        if sub.end is None:
            self._autoSetEnd(sub)
            self._invalidTime = True
        self._subs.append(sub)

    # TODO: test
    def remove(self, subNo):
        if subNo == self.size() - 1:
            self._invalidTime = False
        del self._subs[subNo]

    def clear(self):
        self._subs = []
        self._invalidTime = False

    # TODO: test
    @property
    def fps(self):
        if self.size() > 0:
            return self._subs[0].fps
        return None

    def changeFps(self, fps):
        if not fps > 0:
            raise ValueError("Incorrect FPS value")

        for sub in self._subs:
            sub.fps = fps
        return self

    # TODO: test
    def changeSubText(self, subNo, newText):
        self._subs[subNo].change(text = newText)
        return self

    # TODO: test
    def changeSubStart(self, subNo, newTime):
        self._subs[subNo].change(start = newTime)
        return self

    # TODO: test
    def changeSubEnd(self, subNo, newTime):
        self._subs[subNo].change(end = newTime)
        if subNo == self.size() - 1:
            self._invalidTime = False
        return self

    # TODO: test
    def offset(self, ft):
        for sub in self._subs:
            sub.change(start=sub.start + ft, end=sub.end + ft)

    @property
    def meta(self):
        return self._meta

    def size(self):
        return len(self._subs)

    def __eq__(self, other):
        return self._subs == other._subs

    def __ne__(self, other):
        return self._subs != other._subs

    def __lt__(self, other):
        return self._subs < other._subs

    def __gt__(self, other):
        return self._subs > other._subs

    # Do not implement __setitem__ as we want to keep explicit control over things that are added
    def __getitem__(self, key):
        return self._subs[key].clone()

    def __iter__(self):
        for sub in self._subs:
            yield sub.clone()

    def __len__(self):
        return len(self._subs)

class SubParser:
    def __init__(self):
        self._supportedFormats = set()

        self._subtitles = None
        self._format = None

    def message(self, lineNo, msg = "parsing error."):
        '''Uniform error message.'''
        return "%d: %s" % (lineNo + 1, msg)

    # TODO: parser should not be aware of the encoding
    def _initialLinePrepare(self, line, lineNo):
        if lineNo == 0 and line.startswith( codecs.BOM_UTF8.decode("utf8") ):
            line = line[1:]
        return line

    def registerFormat(self, fmt):
        self._supportedFormats.add(fmt)

    # TODO: test
    @property
    def formats(self):
        return frozenset(self._supportedFormats)

    # It is not a @property, because calling parser.parsedFormat() by accident would actually
    # return a created instance of SubFormat (i.e. would result in a SubFormat())
    def parsedFormat(self):
        return self._format

    def parse(self, content, fps=25):
        errors = []
        for Format in self._supportedFormats:
            subFormat = Format(fps)
            result = self.__parseFormat(subFormat, content)
            if result:
                self._subtitles = result
                self._format = Format
                return self._subtitles
            elif subFormat.error:
                errors.append('%s: %s' % (subFormat.NAME, subFormat.error))

        msg = _('Not a known subtitle format')
        if errors:
            # Translators: note space after colon
            join_str = os.linesep + '    ' + _('note: ')
            msg = msg + join_str + join_str.join(errors)
        raise SubParsingError(msg, 0)

    def __parseFormat(self, fmt, content):
        failed = False

        for no, line in enumerate(content):
            failed = not fmt.feed(line)
            if failed:
                break
        else:
            failed = not fmt.eof()

        if failed and len(fmt.subtitles):
            msg =_('Subtitles partially parsed as %s.') % fmt.NAME
            if fmt.error:
                # Translators: note space after colon
                msg = msg + os.linesep + '    ' + _('note: ') + fmt.error
            raise SubParsingError(msg, no)
        elif failed:
            return
        return fmt.subtitles

    @property
    def results(self):
        '''Return parsing results which is a list of dictionaries'''
        return self._subtitles
