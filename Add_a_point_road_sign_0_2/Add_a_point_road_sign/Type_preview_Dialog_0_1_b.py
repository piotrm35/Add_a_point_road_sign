# -*- coding: utf-8 -*-

SCRIPT_TITLE = 'Add a point road sign'
GENERAL_INFO = u"""
author: Piotr Michałowski, Olsztyn, woj. W-M, Poland
piotrm35@hotmail.com
license: GPL v. 2
work begin: 21.01.2019
"""

import os
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg, uic


#====================================================================================================================

class Type_preview_Dialog(QtWidgets.QDialog):

    def __init__(self, parent, path):
        super(Type_preview_Dialog, self).__init__()
        self.parent = parent
        uic.loadUi(os.path.join(self.parent.base_path, 'ui', 'Type_preview_Dialog_0_1.ui'), self)
        self.setWindowIcon(self.parent.icon)
        if self.parent.SVG_radioButton.isChecked():
            self.Selected_type_QSvgWidget = QtSvg.QSvgWidget(self)
            self._resize_Selected_type_QSvgWidget()
            self.Selected_type_QSvgWidget.load(path)
        else:
            self.Selected_type_QLabel = QtWidgets.QLabel(self)
            self.raw_image = QtGui.QImage(path)
            self._resize_Selected_type_QLabel()
        self.show()


    def resizeEvent(self, event):       # overriding the method
        QtWidgets.QDialog.resizeEvent(self, event)
        if self.parent.SVG_radioButton.isChecked():
            self._resize_Selected_type_QSvgWidget()
        else:
            self._resize_Selected_type_QLabel()

    def _resize_Selected_type_QSvgWidget(self):
        self.Selected_type_QSvgWidget.setGeometry(QtCore.QRect(0, 0, self.width(), self.height()))
        self.setWindowTitle('Type preview ' + str(self.width()) + ' x ' + str(self.height()))


    def _resize_Selected_type_QLabel(self):
        if self.raw_image:
            image = QtGui.QImage(self.raw_image)
            image = image.scaled(self.width(), self.height(), aspectRatioMode=QtCore.Qt.IgnoreAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
            self.Selected_type_QLabel.setGeometry(QtCore.QRect(0, 0, self.width(), self.height()))
            self.Selected_type_QLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.setWindowTitle('Type preview ' + str(self.width()) + ' x ' + str(self.height()))
        

#====================================================================================================================
