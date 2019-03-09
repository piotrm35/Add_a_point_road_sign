# -*- coding: utf-8 -*-

SCRIPT_TITLE = 'Add a point road sign'
SCRIPT_NAME = 'Add_a_point_road_sign'
SCRIPT_VERSION = '0.2.2'
GENERAL_INFO = u"""
author: Piotr Michałowski, Olsztyn, woj. W-M, Poland
piotrm35@hotmail.com
license: GPL v. 2
work begin: 21.01.2019
"""

import os, math
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg, uic
from PyQt5.QtGui import QTextCursor
from qgis.core import *
from qgis.utils import iface
from .Setup import Setup
from .Mouse_point_tool import Mouse_point_tool
from .My_QSvgWidget import My_QSvgWidget
from .My_QLabel import My_QLabel
from .Type_preview_Dialog import Type_preview_Dialog
from .My_LineEdit import My_LineEdit




#====================================================================================================================

class Add_a_point_road_sign(QtWidgets.QMainWindow):

    def __init__(self, iface):
        super(Add_a_point_road_sign, self).__init__()
        self.iface = iface
        self.base_path = os.path.realpath(__file__).split(os.sep + SCRIPT_NAME + os.sep)[0] + os.sep + SCRIPT_NAME
        self.icon = QtGui.QIcon(os.path.join(self.base_path, 'img', 'Add_a_point_road_sign_ICON.png'))
        self.mouse_point_tool = None
        self.setup = Setup()
        self.start_date = None
        self.pt_width = None
        self.pt_height = None
        self.angle = None
        self.comments = None
        self.selected_type = None
        self.selected_type_path = None
        self.type_groups_folder = None
        self.type_folders = None
        self.type_preview_Dialog = None
        self.type_groups_comboBox_currentIndexChanged_LOCK = True
        self.memory_list = [[None] * 5, [None] * 5, [None] * 5]
        self.memory_X_pushButtons_list = None
        self.set_angle_mode = False
        self.svg_extension_list = ['.SVG']
        self.raster_extension_list = ['.PNG', '.JPG']
        self.selected_type_file_name_label_default_text = None
        self.type_groups_folder_label_default_text = None
        


    def closeEvent(self, event):        # overriding the method
        self.mouse_point_tool_del()
        event.accept()


    #----------------------------------------------------------------------------------------------------------------
    # plugin methods:

    def initGui(self):
        self.action = QtWidgets.QAction(self.icon, SCRIPT_TITLE, self.iface.mainWindow())
        self.action.setObjectName(SCRIPT_NAME + '_action')
        self.iface.addToolBarIcon(self.action)
        self.action.triggered.connect(self.run)
        uic.loadUi(os.path.join(self.base_path, 'ui', 'Add_a_point_road_sign.ui'), self)
        self.selected_type_file_name_label_default_text = self.Selected_type_file_name_label.text()
        self.type_groups_folder_label_default_text = self.Type_groups_folder_label.text()
        self.setWindowTitle(SCRIPT_TITLE + ' v. ' + SCRIPT_VERSION)
        self.Graphics_type_groupBox.setEnabled(self._raster_enabled())
        self.Selected_type_QSvgWidget = QtSvg.QSvgWidget(self)
        self.Selected_type_QSvgWidget.setGeometry(QtCore.QRect(5, 5, 71, 71))
        self.Selected_type_QLabel = QtWidgets.QLabel(self)
        self.Selected_type_QLabel.setGeometry(QtCore.QRect(5, 5, 71, 71))
        self.Selected_type_QLabel.setVisible(False)
        self.Type_filter_lineEdit = My_LineEdit(self)
        self.Type_filter_lineEdit.setGeometry(QtCore.QRect(515, 60, 113, 20))
        self.Type_filter_lineEdit.setObjectName("Type_filter_lineEdit")
        self.memory_X_pushButtons_list = [self.Memory_1_pushButton, self.Memory_2_pushButton, self.Memory_3_pushButton]
        self.set_default_pushButton_clicked()
        self.Set_type_groups_folder_pushButton.clicked.connect(self.set_type_groups_folder_pushButton_clicked)
        self.About_pushButton.clicked.connect(self.about_pushButton_clicked)
        self.Width_lineEdit.textChanged.connect(self.width_lineEdit_textChanged)
        self.Height_lineEdit.textChanged.connect(self.height_lineEdit_textChanged)
        self.Angle_lineEdit.textChanged.connect(self.angle_lineEdit_textChanged)
        self.Start_dateTimeEdit.dateTimeChanged.connect(self.start_dateTimeEdit_dateTimeChanged)
        self.Comments_textEdit.textChanged.connect(self.comments_textEdit_textChanged)
        self.Type_groups_comboBox.currentIndexChanged.connect(self.type_groups_comboBox_currentIndexChanged)
        self.Type_preview_pushButton.clicked.connect(self.type_preview_pushButton_clicked)
        self.Type_filter_pushButton.clicked.connect(self.type_filter_pushButton_clicked)
        self.Type_filter_lineEdit.enter_pressed_signal.connect(self.type_filter_pushButton_clicked)
        self.Manual_pushButton.clicked.connect(self.manual_pushButton_clicked)
        self.Set_default_pushButton.clicked.connect(self.set_default_pushButton_clicked)
        self.Memory_1_pushButton.clicked.connect(self.memory_1_pushButton_clicked)
        self.Memory_2_pushButton.clicked.connect(self.memory_2_pushButton_clicked)
        self.Memory_3_pushButton.clicked.connect(self.memory_3_pushButton_clicked)
        self.Del_memory_1_pushButton.clicked.connect(self.del_memory_1_pushButton_clicked)
        self.Del_memory_2_pushButton.clicked.connect(self.del_memory_2_pushButton_clicked)
        self.Del_memory_3_pushButton.clicked.connect(self.del_memory_3_pushButton_clicked)
        self.Set_angle_pushButton.clicked.connect(self.set_angle_pushButton_clicked)
        self.Copy_data_pushButton.clicked.connect(self.copy_data_pushButton_clicked)
        self.SVG_radioButton.toggled.connect(self.svg_radioButton_toggled)
        
        
    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        self.action.triggered.disconnect(self.run)
        self.Set_type_groups_folder_pushButton.clicked.disconnect(self.set_type_groups_folder_pushButton_clicked)
        self.About_pushButton.clicked.disconnect(self.about_pushButton_clicked)
        self.Width_lineEdit.textChanged.disconnect(self.width_lineEdit_textChanged)
        self.Height_lineEdit.textChanged.disconnect(self.height_lineEdit_textChanged)
        self.Angle_lineEdit.textChanged.disconnect(self.angle_lineEdit_textChanged)
        self.Start_dateTimeEdit.dateTimeChanged.disconnect(self.start_dateTimeEdit_dateTimeChanged)
        self.Comments_textEdit.textChanged.disconnect(self.comments_textEdit_textChanged)
        self.Type_groups_comboBox.currentIndexChanged.disconnect(self.type_groups_comboBox_currentIndexChanged)
        self.Type_preview_pushButton.clicked.disconnect(self.type_preview_pushButton_clicked)
        self.Type_filter_pushButton.clicked.disconnect(self.type_filter_pushButton_clicked)
        self.Type_filter_lineEdit.enter_pressed_signal.disconnect(self.type_filter_pushButton_clicked)
        self.Manual_pushButton.clicked.disconnect(self.manual_pushButton_clicked)
        self.Set_default_pushButton.clicked.disconnect(self.set_default_pushButton_clicked)
        self.Memory_1_pushButton.clicked.disconnect(self.memory_1_pushButton_clicked)
        self.Memory_2_pushButton.clicked.disconnect(self.memory_2_pushButton_clicked)
        self.Memory_3_pushButton.clicked.disconnect(self.memory_3_pushButton_clicked)
        self.Del_memory_1_pushButton.clicked.disconnect(self.del_memory_1_pushButton_clicked)
        self.Del_memory_2_pushButton.clicked.disconnect(self.del_memory_2_pushButton_clicked)
        self.Del_memory_3_pushButton.clicked.disconnect(self.del_memory_3_pushButton_clicked)
        self.Set_angle_pushButton.clicked.disconnect(self.set_angle_pushButton_clicked)
        self.Copy_data_pushButton.clicked.disconnect(self.copy_data_pushButton_clicked)
        self.SVG_radioButton.toggled.disconnect(self.svg_radioButton_toggled)
        

    def run(self):
        self.mouse_point_tool_del()
        self.mouse_point_tool_init()
        

    #----------------------------------------------------------------------------------------------------------------
    # input widget methods


    def set_type_groups_folder_pushButton_clicked(self):
        self.type_groups_comboBox_currentIndexChanged_LOCK = True
        _type_groups_folder = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a type groups folder:', self.type_groups_folder, QtWidgets.QFileDialog.ShowDirsOnly)
        if _type_groups_folder and os.path.exists(_type_groups_folder) and os.path.isdir(_type_groups_folder):
            self.type_groups_folder = _type_groups_folder
            self.Type_groups_folder_label.setText(self.type_groups_folder)
            self.Type_groups_comboBox.clear()
            self.type_folders = [f for f in os.listdir(self.type_groups_folder) if os.path.isdir(os.path.join(self.type_groups_folder, f))]
            self.Type_groups_comboBox.addItems(self.type_folders)
            if self.type_folders is None or len(self.type_folders) <= 0:
                self.type_folders = ['']
            self._show_type_group(self.type_folders[0])
            self.type_groups_comboBox_currentIndexChanged_LOCK = False


    def _show_type_group(self, folder_name, filter_mask = None):
        self._remove_widgets_from_gridLayout()
        if folder_name and len(folder_name) > 0:
            _folder = os.path.join(self.type_groups_folder, folder_name)
        else:
            _folder = self.type_groups_folder
        if self.SVG_radioButton.isChecked():
            _tmp_extension_list = self.svg_extension_list
        else:
            _tmp_extension_list = self.raster_extension_list
        if filter_mask and len(filter_mask) > 0:
            _type_file_names = [f for f in os.listdir(_folder) if os.path.isfile(os.path.join(_folder, f)) and os.path.splitext(f)[1].upper() in _tmp_extension_list and os.path.splitext(f)[0].upper().rfind(filter_mask.upper()) >= 0]
        else:
            _type_file_names = [f for f in os.listdir(_folder) if os.path.isfile(os.path.join(_folder, f)) and os.path.splitext(f)[1].upper() in _tmp_extension_list]
        n = len(_type_file_names)
        if n > 0:
            MAX_COL = 8
            IMG_WIDTH = 71
            IMG_HEIGHT = 71
            row = n // MAX_COL
            if n % MAX_COL != 0:
                row += 1
            col = min(n, MAX_COL)
            _new_rect = QtCore.QRect(0, 0, col * (IMG_WIDTH + 8), row * (IMG_HEIGHT + 8))
            self.scrollAreaWidgetContents.setGeometry(_new_rect)
            self.gridLayoutWidget.setGeometry(_new_rect)
            r = 0
            c = -1
            for _type_file_name in _type_file_names:
                c += 1
                if c >= MAX_COL:
                    c = 0
                    r += 1
                if self.SVG_radioButton.isChecked():
                    self.gridLayout.addWidget(self._get_QSvgWidget(os.path.join(_folder, _type_file_name), IMG_WIDTH, IMG_HEIGHT), r, c)
                else:
                    self.gridLayout.addWidget(self._get_QLabel(os.path.join(_folder, _type_file_name), IMG_WIDTH, IMG_HEIGHT), r, c)


    def _remove_widgets_from_gridLayout(self):
        for i in reversed(range(self.gridLayout.count())):
            _widget_to_remove = self.gridLayout.itemAt(i).widget()
            self.gridLayout.removeWidget(_widget_to_remove)
            _widget_to_remove.setParent(None)
            del _widget_to_remove
                

    def _get_QSvgWidget(self, file_path, width, height):
        _tmp_QSvgWidget = My_QSvgWidget(self, file_path)
        _tmp_QSvgWidget.setGeometry(QtCore.QRect(0, 0, width, height))
        _tmp_QSvgWidget.setMinimumSize(width, height)
        _tmp_QSvgWidget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        _tmp_QSvgWidget.load(file_path)
        return _tmp_QSvgWidget


    def _get_QLabel(self, file_path, width, height):
        _tmp_label = My_QLabel(self, file_path)
        _tmp_label.setGeometry(QtCore.QRect(0, 0, width, height))
        _tmp_label.setMinimumSize(width, height)
        _tmp_label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self._show_image_on_label(_tmp_label, file_path, width, height)
        return _tmp_label


    def _show_image_on_label(self, label, file_path, width, height):
        if label and file_path and os.path.exists(file_path):
            try:
                _image = QtGui.QImage(file_path)
                if _image:
                    _image = _image.scaled(width, height, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
                    label.setPixmap(QtGui.QPixmap.fromImage(_image))
            except:
                print("_show_image_on_label - ERROR.")
        
    
    def _raster_enabled(self):
        try:
            ver_str = Qgis.QGIS_VERSION
            if ver_str and len(ver_str) > 0:
                ver_major = int(ver_str[0])
                if ver_major >= 4:
                    return True
                elif ver_major == 3:
                    ver_minor = int(ver_str[2])
                    if ver_minor >= 6:
                        return True
        except:
            pass
        return False


    def svg_radioButton_toggled(self):
        if self.SVG_radioButton.isChecked():
            self.Selected_type_QSvgWidget.setVisible(True)
            self.Selected_type_QLabel.setVisible(False)
        else:
            self.Selected_type_QSvgWidget.setVisible(False)
            self.Selected_type_QLabel.setVisible(True)
        self.Type_groups_comboBox.clear()
        self._remove_widgets_from_gridLayout()
        self.Selected_type_file_name_label.setText(self.selected_type_file_name_label_default_text)
        self.Type_groups_folder_label.setText(self.type_groups_folder_label_default_text)
        self.selected_type = None
        self.selected_type_path = None
        self.Selected_type_QSvgWidget.load(None)
        self.Selected_type_QLabel.clear()
        
        
    def type_groups_comboBox_currentIndexChanged(self, new_idx):
        if not self.type_groups_comboBox_currentIndexChanged_LOCK:
            if self.type_folders and len(self.type_folders) >= new_idx + 1:
                self._show_type_group(self.type_folders[new_idx])
            

    def set_selected_type_QSvgWidget(self, path):
        self.Selected_type_QSvgWidget.load(path)
        self.selected_type = os.path.basename(path).split('.')[0]
        self.Selected_type_file_name_label.setText(self.selected_type)
        self.selected_type_path = path


    def set_selected_type_QLabel(self, path):
        self._show_image_on_label(self.Selected_type_QLabel, path, self.Selected_type_QLabel.width(), self.Selected_type_QLabel.height())
        self.selected_type = os.path.basename(path).split('.')[0]
        self.Selected_type_file_name_label.setText(self.selected_type)
        self.selected_type_path = path


    def start_dateTimeEdit_dateTimeChanged(self, dateTime):
        self.start_date = dateTime.toString("yyyy'-'MM'-'dd'T'hh':'mm")


    def width_lineEdit_textChanged(self, tx):
        if tx is None or len(tx) == 0 or self.is_float(tx):
            self.pt_width = tx.strip()
        else:
            self.Width_lineEdit.setText(self.pt_width)


    def height_lineEdit_textChanged(self, tx):
        if tx is None or len(tx) == 0 or self.is_float(tx):
            self.pt_height = tx.strip()
        else:
            self.Height_lineEdit.setText(self.pt_height)
            

    def angle_lineEdit_textChanged(self, tx):
        if tx is None or len(tx) == 0 or self.is_float(tx):
            self.angle = tx.strip()
        else:
            self.Angle_lineEdit.setText(self.angle)


    def comments_textEdit_textChanged(self):
        tx = self.Comments_textEdit.toPlainText()
        len_tx = len(tx)
        if len_tx <= Setup.COMMENTS_MAX_LENGTH:
            self.comments = tx.strip()
        else:
            self.Comments_textEdit.setText(self.comments)
            self.Comments_textEdit.moveCursor(QTextCursor.End)
            print("Comments' len = " + str(len_tx) + " > " + str(Setup.COMMENTS_MAX_LENGTH))

        
    def about_pushButton_clicked(self):
        QtWidgets.QMessageBox.information(self, SCRIPT_TITLE, SCRIPT_TITLE + ' v. ' + SCRIPT_VERSION + '\n' + GENERAL_INFO + "\n( QGIS v. " + Qgis.QGIS_VERSION + " )")


    def type_preview_pushButton_clicked(self):
        if self.selected_type_path:
            self.type_preview_Dialog = Type_preview_Dialog(self, self.selected_type_path)


    def type_filter_pushButton_clicked(self):
        self._show_type_group(self.type_folders[self.Type_groups_comboBox.currentIndex()], self.Type_filter_lineEdit.text())


    def manual_pushButton_clicked(self):
        if Setup.MANUAL_FILE_NAME and len(Setup.MANUAL_FILE_NAME) > 0 and Setup.MANUAL_FILE_NAME.upper().endswith('.PDF'):
            try:
                os.startfile(os.path.join(self.base_path, 'doc', Setup.MANUAL_FILE_NAME))
            except:
                pass


    def set_default_pushButton_clicked(self):
        self.start_date = Setup.START_DATE
        self.pt_width = str(Setup.WIDTH).strip()
        self.pt_height = str(Setup.HEIGHT).strip()
        self.angle = None
        self.comments = Setup.COMMENTS.strip()
        self._show_data()


    def memory_1_pushButton_clicked(self):
        self.memory_X_pushButton_clicked(0)


    def memory_2_pushButton_clicked(self):
        self.memory_X_pushButton_clicked(1)


    def memory_3_pushButton_clicked(self):
        self.memory_X_pushButton_clicked(2)
        

    def del_memory_1_pushButton_clicked(self):
        self.Memory_1_pushButton.setText('')


    def del_memory_2_pushButton_clicked(self):
        self.Memory_2_pushButton.setText('')


    def del_memory_3_pushButton_clicked(self):
        self.Memory_3_pushButton.setText('')


    def memory_X_pushButton_clicked(self, idx):
        if self.memory_X_pushButtons_list[idx].text() and self.memory_X_pushButtons_list[idx].text() == 'M' + str(idx + 1):
            self.start_date = self.memory_list[idx][0]
            self.pt_width = self.memory_list[idx][1]
            self.pt_height = self.memory_list[idx][2]
            self.angle = self.memory_list[idx][3]
            self.comments = self.memory_list[idx][4]
            self._show_data()
        else:
            self.memory_list[idx][0] = self.start_date
            self.memory_list[idx][1] = self.pt_width
            self.memory_list[idx][2] = self.pt_height
            self.memory_list[idx][3] = self.angle
            self.memory_list[idx][4] = self.comments
            self.memory_X_pushButtons_list[idx].setText('M' + str(idx + 1))
        

    def _show_data(self):
        if self.start_date and len(self.start_date) > 0:
            try:
                self.Start_dateTimeEdit.setDateTime(QtCore.QDateTime.fromString(self.start_date, "yyyy'-'MM'-'dd'T'hh':'mm"))
            except:
                print("setDateTime - ERROR")
        if self.pt_width:
            self.Width_lineEdit.setText(self.pt_width)
        else:
            self.Width_lineEdit.setText('')
        if self.pt_height:
            self.Height_lineEdit.setText(self.pt_height)
        else:
            self.Height_lineEdit.setText('')
        if self.angle:
            self.Angle_lineEdit.setText(self.angle)
        else:
            self.Angle_lineEdit.setText('')
        if self.comments:
            self.Comments_textEdit.setText(self.comments)
        else:
            self.Comments_textEdit.setText('')


    def set_angle_pushButton_clicked(self):
        self.Set_angle_pushButton.setEnabled(False)
        self.set_angle_mode = True


    def set_angle(self, angle):
        self.angle = math.floor(angle)
        self.Angle_lineEdit.setText(str(self.angle))
        self.Set_angle_pushButton.setEnabled(True)
        self.set_angle_mode = False


    def copy_data_pushButton_clicked(self):
        layer = self.get_active_point_layer()
        if layer:
            selection = layer.selectedFeatures()
            if selection and len(selection) > 0:
                try:
                    self.start_date = selection[0][self.setup.DB_FIELD_NAMES_MAPPING_DICT['START_DATE']].toString("yyyy'-'MM'-'dd'T'hh':'mm")
                except:
                    pass
                try:
                    self.pt_width = str(selection[0][self.setup.DB_FIELD_NAMES_MAPPING_DICT['WIDTH']])
                except:
                    pass
                try:
                    self.pt_height = str(selection[0][self.setup.DB_FIELD_NAMES_MAPPING_DICT['HEIGHT']])
                except:
                    pass
                try:
                    self.angle = str(selection[0][self.setup.DB_FIELD_NAMES_MAPPING_DICT['ANGLE']])
                except:
                    pass
                try:
                    self.comments = selection[0][self.setup.DB_FIELD_NAMES_MAPPING_DICT['COMMENTS']]
                except:
                    pass
                self._show_data()
            else:
                QtWidgets.QMessageBox.critical(self.iface.mainWindow(), SCRIPT_TITLE, 'Please select a POINT in selected layer.')

        
    #----------------------------------------------------------------------------------------------------------------
    # work methods:

    def mouse_point_tool_del(self):
        if self.mouse_point_tool:
            try:
                iface.mapCanvas().unsetMapTool(self.mouse_point_tool)
            except:
                pass
            finally:
                self.mouse_point_tool.setParent(None)
                del self.mouse_point_tool
                self.mouse_point_tool = None
            print("mouse_point_tool_del - OK")
                

    def mouse_point_tool_init(self):
        self.mouse_point_tool = Mouse_point_tool(iface.mapCanvas(), self)
        iface.mapCanvas().setMapTool(self.mouse_point_tool)
        self._show_data()
        self.show()
        print("mouse_point_tool_init - OK")


    def get_active_point_layer(self):
        res = False
        try:
            layer = self.iface.activeLayer()
            if layer and layer.type() == QgsMapLayer.VectorLayer:
                features = layer.getFeatures()
                n = 0
                for feature in features:
                    n += 1
                    geom = feature.geometry()
                    if geom and geom.type() == QgsWkbTypes.PointGeometry:
                        if QgsWkbTypes.isSingleType(geom.wkbType()):
                            res = True
                    break
                if n == 0:
                    res = True
        except:
            pass
        if not res:
            QtWidgets.QMessageBox.critical(self.iface.mainWindow(), SCRIPT_TITLE, 'Please select a POINT LAYER.')
            return None
        else:
            return layer


    def is_float(self, x_str):
        try:
            float(x_str)
            return True
        except:
            pass
        return False
    

#====================================================================================================================



