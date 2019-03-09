# -*- coding: utf-8 -*-

SCRIPT_TITLE = 'Add a point road sign'
GENERAL_INFO = u"""
author: Piotr Michałowski, Olsztyn, woj. W-M, Poland
piotrm35@hotmail.com
license: GPL v. 2
work begin: 21.01.2019
"""

# this file version: 0.2

from PyQt5 import QtSvg


#====================================================================================================================

class My_QSvgWidget(QtSvg.QSvgWidget):
    
    def __init__(self, parent, path):
        super(My_QSvgWidget, self).__init__()
        self.parent = parent
        self.path = path

    def mouseReleaseEvent(self, e):  
        self.parent.set_selected_type_QSvgWidget(self.path)


#====================================================================================================================
