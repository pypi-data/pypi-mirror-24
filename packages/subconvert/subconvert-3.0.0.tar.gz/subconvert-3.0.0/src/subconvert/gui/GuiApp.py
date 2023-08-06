#-*- coding: utf-8 -*-

"""
Copyright (C) 2015 Michal Goral.

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

import sys
import locale
import logging

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QLocale, QTranslator, QLibraryInfo

from subconvert.gui.MainWindow import MainWindow
from subconvert.utils.Locale import _

log = logging.getLogger('Subconvert.%s' % __name__)

class SubApplication:
    def __init__(self, args, parser):
        self._args = args
        self._parser = parser

        self._app = QApplication(sys.argv)

        # This is required by libmpv;
        # Qt changes locale to system default one, but only at the point of
        # initialization of QApplication:
        #
        #       http://doc.qt.io/qt-5/qcoreapplication.html
        #
        # LC_NUMERIC only defines a decimal point character so it won't affect
        # translations.
        locale.setlocale(locale.LC_NUMERIC, 'C')

        # Translate default strings of Qt widgets.
        # There are many, many types of translations inside
        # PyQt5/Qt/translations. For some languages some of these files are
        # "empty" and the others are not. I guess it all depends on translators.
        loc = QLocale.system().name()
        path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
        transbases = ['qt_%s', 'qtbase_%s']
        for base in transbases:
            translator = QTranslator(self._app)
            trans = base % loc
            if translator.load(trans, path):
                self._app.installTranslator(translator)
            else:
                log.debug(_('Failed to load Qt translation: %s') % trans)

        self._gui = MainWindow(self._args, self._parser)

    def cleanup(self):
        self._gui.cleanup()

    def run(self):
        # Let the interpreter run each 500 ms.
        timer = QTimer()
        timer.start(500)
        timer.timeout.connect(lambda: None)

        self._gui.show()
        return self._app.exec_()

