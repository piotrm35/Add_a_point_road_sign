# -*- coding: utf-8 -*-

"""
/***************************************************************************
  My_QLabel.py

  My QLabel QT5 widget with mouseReleaseEvent handled.
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

from PyQt5 import QtWidgets


#====================================================================================================================

class My_QLabel(QtWidgets.QLabel):
    
    def __init__(self, parent, path):
        super(My_QLabel, self).__init__()
        self.parent = parent
        self.path = path

    def mouseReleaseEvent(self, e):  
        self.parent.set_selected_type_QLabel(self.path)


#====================================================================================================================
