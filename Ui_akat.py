# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Work\AKAT\akat.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_akat(object):
    def setupUi(self, akat):
        akat.setObjectName(_fromUtf8("akat"))
        akat.resize(820, 590)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Mincho"))
        akat.setFont(font)
        akat.setSizeGripEnabled(True)
        self.groupBox_2 = QtGui.QGroupBox(akat)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 20, 801, 431))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.groupBox = QtGui.QGroupBox(self.groupBox_2)
        self.groupBox.setGeometry(QtCore.QRect(10, 30, 781, 121))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(60, 80, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEdit_processName = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_processName.setGeometry(QtCore.QRect(160, 30, 611, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_processName.setFont(font)
        self.lineEdit_processName.setObjectName(_fromUtf8("lineEdit_processName"))
        self.dateTimeEdit_end = QtGui.QDateTimeEdit(self.groupBox)
        self.dateTimeEdit_end.setGeometry(QtCore.QRect(160, 80, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dateTimeEdit_end.setFont(font)
        self.dateTimeEdit_end.setDateTime(QtCore.QDateTime(QtCore.QDate(2017, 1, 1), QtCore.QTime(10, 20, 30)))
        self.dateTimeEdit_end.setObjectName(_fromUtf8("dateTimeEdit_end"))
        self.pushButton_start = QtGui.QPushButton(self.groupBox)
        self.pushButton_start.setGeometry(QtCore.QRect(410, 80, 131, 31))
        self.pushButton_start.setObjectName(_fromUtf8("pushButton_start"))
        self.pushButton_stop = QtGui.QPushButton(self.groupBox)
        self.pushButton_stop.setGeometry(QtCore.QRect(570, 80, 131, 31))
        self.pushButton_stop.setObjectName(_fromUtf8("pushButton_stop"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(50, 30, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(40, 170, 111, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit_mmtDirectory = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_mmtDirectory.setGeometry(QtCore.QRect(170, 170, 611, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        self.lineEdit_mmtDirectory.setFont(font)
        self.lineEdit_mmtDirectory.setObjectName(_fromUtf8("lineEdit_mmtDirectory"))
        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(100, 210, 51, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.lineEdit_from = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_from.setGeometry(QtCore.QRect(170, 210, 121, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        self.lineEdit_from.setFont(font)
        self.lineEdit_from.setObjectName(_fromUtf8("lineEdit_from"))
        self.label_10 = QtGui.QLabel(self.groupBox_2)
        self.label_10.setGeometry(QtCore.QRect(400, 210, 51, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.lineEdit_to = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_to.setGeometry(QtCore.QRect(440, 210, 121, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        self.lineEdit_to.setFont(font)
        self.lineEdit_to.setObjectName(_fromUtf8("lineEdit_to"))
        self.label_8 = QtGui.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(10, 250, 161, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.lineEdit_apiReportToolDirectory = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_apiReportToolDirectory.setGeometry(QtCore.QRect(170, 250, 611, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        self.lineEdit_apiReportToolDirectory.setFont(font)
        self.lineEdit_apiReportToolDirectory.setText(_fromUtf8(""))
        self.lineEdit_apiReportToolDirectory.setObjectName(_fromUtf8("lineEdit_apiReportToolDirectory"))
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(80, 300, 81, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.lineEdit_carrierID = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_carrierID.setGeometry(QtCore.QRect(170, 300, 121, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        self.lineEdit_carrierID.setFont(font)
        self.lineEdit_carrierID.setObjectName(_fromUtf8("lineEdit_carrierID"))
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(120, 340, 51, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.lineEdit_api = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_api.setGeometry(QtCore.QRect(170, 340, 121, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        self.lineEdit_api.setFont(font)
        self.lineEdit_api.setObjectName(_fromUtf8("lineEdit_api"))
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(360, 300, 71, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.lineEdit_sectorID = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_sectorID.setGeometry(QtCore.QRect(440, 300, 121, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        self.lineEdit_sectorID.setFont(font)
        self.lineEdit_sectorID.setObjectName(_fromUtf8("lineEdit_sectorID"))
        self.label_7 = QtGui.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(350, 340, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.lineEdit_itemName = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_itemName.setGeometry(QtCore.QRect(440, 340, 341, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        self.lineEdit_itemName.setFont(font)
        self.lineEdit_itemName.setObjectName(_fromUtf8("lineEdit_itemName"))
        self.pushButton_akatStart = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_akatStart.setGeometry(QtCore.QRect(240, 390, 101, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial Black"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_akatStart.setFont(font)
        self.pushButton_akatStart.setObjectName(_fromUtf8("pushButton_akatStart"))
        self.pushButton_akatStop = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_akatStop.setGeometry(QtCore.QRect(450, 390, 91, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial Black"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_akatStop.setFont(font)
        self.pushButton_akatStop.setObjectName(_fromUtf8("pushButton_akatStop"))
        self.checkBox = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox.setGeometry(QtCore.QRect(90, 390, 81, 31))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.groupBox_3 = QtGui.QGroupBox(akat)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 470, 801, 101))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.label_11 = QtGui.QLabel(self.groupBox_3)
        self.label_11.setGeometry(QtCore.QRect(60, 20, 121, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.lineEdit_targetGraphFile = QtGui.QLineEdit(self.groupBox_3)
        self.lineEdit_targetGraphFile.setGeometry(QtCore.QRect(210, 20, 511, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        self.lineEdit_targetGraphFile.setFont(font)
        self.lineEdit_targetGraphFile.setText(_fromUtf8(""))
        self.lineEdit_targetGraphFile.setObjectName(_fromUtf8("lineEdit_targetGraphFile"))
        self.label_12 = QtGui.QLabel(self.groupBox_3)
        self.label_12.setGeometry(QtCore.QRect(130, 60, 81, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.lineEdit_sourceFileId = QtGui.QLineEdit(self.groupBox_3)
        self.lineEdit_sourceFileId.setGeometry(QtCore.QRect(210, 60, 121, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        self.lineEdit_sourceFileId.setFont(font)
        self.lineEdit_sourceFileId.setText(_fromUtf8(""))
        self.lineEdit_sourceFileId.setObjectName(_fromUtf8("lineEdit_sourceFileId"))
        self.label_13 = QtGui.QLabel(self.groupBox_3)
        self.label_13.setGeometry(QtCore.QRect(370, 60, 101, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.lineEdit_graphName = QtGui.QLineEdit(self.groupBox_3)
        self.lineEdit_graphName.setGeometry(QtCore.QRect(480, 60, 121, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        self.lineEdit_graphName.setFont(font)
        self.lineEdit_graphName.setText(_fromUtf8(""))
        self.lineEdit_graphName.setObjectName(_fromUtf8("lineEdit_graphName"))
        self.pushButton_copyStart = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_copyStart.setGeometry(QtCore.QRect(620, 60, 101, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial Black"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_copyStart.setFont(font)
        self.pushButton_copyStart.setObjectName(_fromUtf8("pushButton_copyStart"))

        self.retranslateUi(akat)
        QtCore.QMetaObject.connectSlotsByName(akat)

    def retranslateUi(self, akat):
        akat.setWindowTitle(_translate("akat", "AKAT", None))
        self.groupBox_2.setTitle(_translate("akat", "AKAT", None))
        self.groupBox.setTitle(_translate("akat", "AK", None))
        self.label_2.setText(_translate("akat", "When to Kill:", None))
        self.dateTimeEdit_end.setDisplayFormat(_translate("akat", "yyyy-M-d H:mm:ss", None))
        self.pushButton_start.setText(_translate("akat", "AK Start", None))
        self.pushButton_stop.setText(_translate("akat", "AK Stop", None))
        self.label.setText(_translate("akat", "ProcessName:", None))
        self.label_3.setText(_translate("akat", "MMT Directory:", None))
        self.label_9.setText(_translate("akat", "FROM:", None))
        self.label_10.setText(_translate("akat", "TO:", None))
        self.label_8.setText(_translate("akat", "API Report Tool Dir:", None))
        self.label_4.setText(_translate("akat", "CarrierID:", None))
        self.label_6.setText(_translate("akat", "API:", None))
        self.label_5.setText(_translate("akat", "ScetorID:", None))
        self.label_7.setText(_translate("akat", "Item Name:", None))
        self.pushButton_akatStart.setText(_translate("akat", "AKAT Start", None))
        self.pushButton_akatStop.setText(_translate("akat", "AKAT Stop", None))
        self.checkBox.setText(_translate("akat", "  Copy", None))
        self.groupBox_3.setTitle(_translate("akat", "Copy", None))
        self.label_11.setText(_translate("akat", "TargetGraphFile:", None))
        self.label_12.setText(_translate("akat", "CellID:", None))
        self.label_13.setText(_translate("akat", "Graph Name:", None))
        self.pushButton_copyStart.setText(_translate("akat", "Copy Start", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    akat = QtGui.QDialog()
    ui = Ui_akat()
    ui.setupUi(akat)
    akat.show()
    sys.exit(app.exec_())

