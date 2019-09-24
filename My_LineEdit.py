# -*- coding: utf-8 -*-

"""
/***************************************************************************
  My_LineEdit.py

  My QLineEdit QT5 widget with enter pressed event handled.
  --------------------------------------
  Date : 21.01.2019
  Copyright: (C) 2019 by Piotr Michałowski
  Email: piotrm35@hotmail.com
/***************************************************************************
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as published
 * by the Free Software Foundation.
 *
 ***************************************************************************/
"""

SCRIPT_TITLE = 'Add a point road sign'
GENERAL_INFO = u"""
author: Piotr Michałowski, Olsztyn, woj. W-M, Poland
piotrm35@hotmail.com
license: GPL v. 2
work begin: 21.01.2019
"""

# this file version: 0.1

from PyQt5 import QtCore, QtWidgets


#====================================================================================================================

class My_LineEdit(QtWidgets.QLineEdit):

    enter_pressed_signal = QtCore.pyqtSignal()
    
    def __init__(self, *args):
        super(My_LineEdit, self).__init__(*args)
        
    def event(self, event):
        if (event.type() == QtCore.QEvent.KeyPress) and (event.key() == QtCore.Qt.Key_Enter):
            self.enter_pressed_signal.emit()
            return True
        return QtWidgets.QLineEdit.event(self, event)

#====================================================================================================================
