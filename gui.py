import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QLabel, QDialog, QVBoxLayout, QGridLayout, QRadioButton, QFileDialog, QLineEdit, QTextEdit, QDoubleSpinBox, QPlainTextEdit
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import pyqtSlot

class FilePicker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('请选择刺激列表文件')
 
    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Excel Files (*.xlsx;*.xls)", options=options)
        return fileName

class App(QDialog):
    
    def __init__(self):
        super().__init__()
        self.title = 'VoiceGenerator 1.7.2 (by Biao)'
        self.filepath = ''
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.createLayout()
        self.setLayout(self.horizontalLayout)
 
        self.show()

    def readStimuli(self):
        selector = FilePicker()
        self.filepath = selector.openFileNameDialog()
        self.label_openFile.setText(self.filepath)
        self.label_openFile.adjustSize() 

    def analyze(self):
        self.bn_analyze.setText('请查看命令行窗口')

        cmd = 'python %s/run.py ' %sys.path[0]

        if self.radio_gender1.isChecked():
            cmd += '--gender=male '
        else:
            cmd += '--gender=female '

        if self.radio_nature1.isChecked():
            cmd += '--nature=0 '
        else:
            cmd += '--nature=1 '

        if self.filepath == '':
            self.readStimuli()
        
        cmd += '--filename="%s" ' %self.filepath
        cmd += '--duration_target=%s ' %self.input_duration.value()
        cmd += '--weaken_duration=%s ' %self.input_weakenD.value()
        cmd += '--output=%s ' %self.input_outputpath.text()

        os.system(cmd)  

    def radio_nature1_clicked(self, enabled):
        if enabled:
            self.layout_duration.setTitle('每个拼音发音的目标长度（秒）')
            self.layout_weakenD.setTitle('每个拼音发音的声音结尾的渐弱时间（秒）')
            self.input_weakenD.setEnabled(True)

    def radio_nature2_clicked(self, enabled):
        if enabled:
            self.layout_duration.setTitle('整段文本发音的目标长度（秒）')
            self.layout_weakenD.setTitle('[不适用自然模式] 每个拼音发音的声音结尾的渐弱时间（秒）')
            self.input_weakenD.setEnabled(False)

    def HLayout(self, obj, items):
        hbox = QHBoxLayout()
        for i in items:
            hbox.addWidget(i)
        hbox.addStretch(1)
        obj.setLayout(hbox)

    def createLayout(self):
        ###
        self.bn_openFile = QPushButton('打开刺激列表', self)
        self.bn_openFile.clicked.connect(self.readStimuli)
        self.label_openFile = QLabel(self)
        ###
        self.layout_gender = QGroupBox('音源')
        self.radio_gender1 = QRadioButton('男')
        self.radio_gender2 = QRadioButton('女')
        self.radio_gender1.setChecked(True) 
        self.HLayout(self.layout_gender,[self.radio_gender1,self.radio_gender2])
        ###
        self.layout_nature = QGroupBox('每个字的发音长度')
        self.radio_nature1 = QRadioButton('相同')
        self.radio_nature2 = QRadioButton('自然')
        self.radio_nature1.setChecked(True) 
        self.radio_nature1.toggled.connect(self.radio_nature1_clicked)
        self.radio_nature2.toggled.connect(self.radio_nature2_clicked)
        self.HLayout(self.layout_nature,[self.radio_nature1,self.radio_nature2])
        ###
        self.layout_duration = QGroupBox('每个拼音发音的目标长度（秒）')
        self.input_duration = QDoubleSpinBox()
        self.input_duration.setValue(0.25)
        self.HLayout(self.layout_duration,[self.input_duration])
        ###
        self.layout_weakenD = QGroupBox('每个拼音发音的声音结尾的渐弱时间（秒）')
        self.input_weakenD = QDoubleSpinBox()
        self.input_weakenD.setValue(0.025)
        self.input_weakenD.singleStep = 0.1
        self.HLayout(self.layout_weakenD,[self.input_weakenD])
        ###
        self.layout_outputpath = QGroupBox('存放生成的wav文件的路径')
        self.input_outputpath = QLineEdit()
        self.input_outputpath.setText(sys.path[0] +'\\output')
        self.HLayout(self.layout_outputpath,[self.input_outputpath])
        ###
        self.bn_analyze = QPushButton('开始分析', self)
        self.bn_analyze.clicked.connect(self.analyze)

        ###
        # self.layout_textbox = QGroupBox('内容')
        # self.textbox = QTextEdit('11')
        # # self.textbox.resize(600,300)
        # self.HLayout(self.layout_textbox,[self.textbox])

        self.verticalLayout1 = QtWidgets.QVBoxLayout()
        self.verticalLayout1.addWidget(self.layout_gender)
        self.verticalLayout1.addWidget(self.layout_nature)
        self.verticalLayout1.addWidget(self.layout_duration)
        self.verticalLayout1.addWidget(self.layout_weakenD)
        self.verticalLayout1.addWidget(self.layout_outputpath)
        self.verticalLayout1.addWidget(self.bn_openFile)
        self.verticalLayout1.addWidget(self.label_openFile)
        self.verticalLayout1.addWidget(self.bn_analyze)
        
        # self.verticalLayout2 = QtWidgets.QVBoxLayout()
        # self.verticalLayout2.addWidget(self.layout_textbox)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.addLayout(self.verticalLayout1)
        # self.horizontalLayout.addLayout(self.verticalLayout2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
