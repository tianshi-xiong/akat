# -*- coding: utf-8 -*-

"""
Module implementing killer.
"""

from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import QDialog
from PyQt4 import QtCore
from PyQt4 import QtGui
from Ui_akat import Ui_akat
import time
from datetime import datetime
import os
import subprocess

class atThread(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(atThread, self).__init__(parent)
        self.carrierId= ''
        self.sectorId =''
        self.api = ''
        self.itemName = ''
        self.convertedMmtDirectory = ''
        self.apiReportToolDirecotry = ''
        

class killProcessThread(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(list)
    oneCommandSentSignal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(killProcessThread, self).__init__(parent)
        self.expectedTime = ''
    
    def initValues(self, endTime, process):
        self.expectedTime = endTime
        self.processName = process
    
    def run(self):
        currentTime = datetime.now()
        #print currentTime
        # add judgement here to sure the end time is ahead of the current time 
        sleepTime = (self.expectedTime-currentTime).seconds
        #print  ('the sleep time is %d' ,  sleepTime)
        time.sleep(sleepTime)
        exeList = self.processName.split(',')
        processList = []
        for each in exeList:
            wordList = each.split('.')
            if wordList == '':
                continue
            cmd = 'taskkill /F /IM %s.exe' % (wordList[0])
            time.sleep(1)
            os.system(cmd)
            processList.append(wordList[0])
        self.finishSignal.emit(processList)

class killer(QDialog, Ui_akat):
    """
    Class documentation goes here.
    """
    paraForSubThread = QtCore.pyqtSignal(datetime, str)
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setFixedSize(851, 424)
        self.flagKilling = 0
        self.kThread = killProcessThread()
        self.kThread.finishSignal.connect(self.subThreadWorkEndAll)
        self.paraForSubThread.connect(self.kThread.initValues)
        self.dateTimeEdit_end.setDateTime(datetime.now())
        

    @pyqtSignature("")
    def on_pushButton_start_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.pushButton_start.setDisabled(True)
        self.flagKilling = 1
        
        endDate = self.dateTimeEdit_end.date()
        yy = endDate.year()
        mm = endDate.month()
        dd = endDate.day()
        endTime = self.dateTimeEdit_end.time()
        hh = endTime.hour()
        min = endTime.minute()
        ss = endTime.second()
        expectedEndTime = datetime(yy, mm, dd, hh, min, ss, 0)
        #print expectedEndTime
        processName = self.lineEdit_processName.text()
        self.paraForSubThread.emit(expectedEndTime, processName)
        self.kThread.start()    
        
    def subThreadWorkEndAll(self, processList):
        self.pushButton_start.setDisabled(False)
        self.flagKilling = 0
        if processList.isEmpty():
            QtGui.QMessageBox.information(self, "INFO", 'No process will be terminated!!')
        else:
            for each in processList:
                QtGui.QMessageBox.information(self, "INFO", 'Process %s is Terminated' %(each))
        #subprocess.call(r"D:\Work\AutoKiller\api_report_tool_v2.3\api_report_ui.exe")
        
    @pyqtSignature("")
    def on_pushButton_stop_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if self.kThread.isRunning():
            self.kThread.terminate()
            self.pushButton_start.setDisabled(False)
            self.flagKilling = 0
    def on_pushButton_akatStart_clicked(self):
        self.on_pushButton_start_clicked()
    
    def akFinishedToStartAT(self, processList):
        pass
    
    def on_pushButton_akatStop_clicked(self):
        pass
        
        
if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import  QApplication
    app = QApplication(sys.argv)
    dlg = killer()
    dlg.show()
    sys.exit(app.exec_())
    

