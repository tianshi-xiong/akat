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
import os, shutil, psutil
import re, string
import autopy
import win32com.client, pythoncom
import win32gui
import win32con, win32com

akButtonClicked = 0

class startApiReportToolThread(QtCore.QThread):
    def __init__(self, parent=None):
        super(startApiReportToolThread, self).__init__(parent)
        self.apiReportToolDirecotry = ''
    def initValues(self, apiToolPath):
         self.apiReportToolDirecotry = str(apiToolPath)
    def run(self):
        #self.apiReportToolDirecotry = os.path.join(str(self.apiReportToolDirecotry),r'api_report_ui_2.2.exe')
        os.system(self.apiReportToolDirecotry)
        
class atThread(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(atThread, self).__init__(parent)
        self.carrierId= ''
        self.sectorId =''
        self.api = ''
        self.itemName = ''
        self.convertedMmtDirectory = ''
        self.apiReportToolDirecotry = ''
    
    def initValues(self, processList):
        self.carrierId= processList[0]
        self.sectorId =processList[1]
        self.api = processList[2]
        self.itemName = processList[3]
        self.convertedMmtDirectory = processList[4]
        self.apiReportToolDirecotry = processList[5]

    def find_idxSubHandle(self, pHandle, winClass, index=0):  
        """ 
        """  
        assert type(index) == int and index >= 0  
        handle = win32gui.FindWindowEx(pHandle, 0, winClass, None)  
        while index > 0:  
            handle = win32gui.FindWindowEx(pHandle, handle, winClass, None)  
            index -= 1  
        return handle  
  
  
    def find_subHandle(self, pHandle, winClassList):  
        """ 
        """  
        assert type(winClassList) == list  
        if len(winClassList) == 1:  
            return self.find_idxSubHandle(pHandle, winClassList[0][0], winClassList[0][1])  
        else:  
            pHandle = self.find_idxSubHandle(pHandle, winClassList[0][0], winClassList[0][1])  
            return self.find_subHandle(pHandle, winClassList[1:])  
            
    def moveMouseAndClick(self, parentWH,subWH):
        #restore  the api report tool if it is minimized, seems better to judge if it is minimized firstly
        win32gui.ShowWindow(parentWH,win32con.SW_RESTORE)
        #need to initialize firstly in sub thread.
        pythoncom.CoInitialize()
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(parentWH)
        #win32gui.SetWindowPos(parentWH, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE| win32con.SWP_NOOWNERZORDER|win32con.SWP_SHOWWINDOW)
        rect = win32gui.GetWindowRect(subWH)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        halfW= x+w/2
        halfH = y+ h/2
        posTuple = [halfW,halfH]
        autopy.mouse.move(halfW,halfH)
        autopy.mouse.click()
        return posTuple

    def judgeTheCpuUsageRate(self, processPath):
        processName = os.path.basename(processPath)
        cmd = 'tasklist /fi "imagename eq ' + processName + '"' + ' | findstr.exe ' + processName
        result = os.popen(cmd).read()
        rule= '[a-zA-Z0-9\._-]+'
        patten = re.compile(rule)
        apiToolPid = string.atoi(patten.findall(result)[1])
        p = psutil.Process(apiToolPid)
        #print "subprocess id is %d" % apiToolPid
        while True:
            percentage = p.cpu_percent(interval=1.0)
            print "the cpu percentage is %f" % percentage
            if percentage > 5:
                #print r"the cpu percentage is more than 10%"
                time.sleep(10)
                continue
            else:
                time.sleep(3)
                percentage = p.cpu_percent(interval=1.0)
                if percentage < 5:
                    #print r"the cpu percentage is less than 10%"
                    break
     
    def run(self):
        time.sleep(10)
        os.chdir(os.path.dirname(self.apiReportToolDirecotry))
        Mhandle = win32gui.FindWindow("TkTopLevel", r"SAT 400UE API Report Tool")
        #print "%x" % (Mhandle) 
        #set the window to the top level
        #win32gui.ShowWindow(Mhandle,win32con.SW_RESTORE)
        #shell = win32com.client.Dispatch("WScript.Shell")
        #shell.SendKeys('%')
        #win32gui.SetForegroundWindow(Mhandle)
        
        logDirecotyHandle = self.find_subHandle(Mhandle, [("TkChild", 0),("TkChild", 4),("TkChild", 0),])  
        #print "logDirecotyHandle %x" % (logDirecotyHandle)
        # click the log directory edit line and input the path
        self.moveMouseAndClick(Mhandle,logDirecotyHandle)
        time.sleep(2)
        dirList = self.convertedMmtDirectory.split(":")
       #print  dirList[0]
        time.sleep(1)
        autopy.key.type_string(dirList[0])
        autopy.key.toggle(autopy.key.K_SHIFT,True)
        autopy.key.type_string(":")
        time.sleep(1)
        autopy.key.toggle(autopy.key.K_SHIFT,False)
        autopy.key.type_string(dirList[1])
       # print  dirList[1]
        time.sleep(2)
        #click the generate CVS button and wait for the finish of decode 
        generateCvsLogHandle = self.find_subHandle(Mhandle, [("TkChild", 0),("TkChild", 3),("Button",0)])  
        #print "generateCvsLogHandle %x" % (generateCvsLogHandle) 
        self.moveMouseAndClick(Mhandle,generateCvsLogHandle)
        time.sleep(3)
        self.judgeTheCpuUsageRate(self.apiReportToolDirecotry)
        # get all the handles of the other elements in API report tool
        generalReportHandle = self.find_subHandle(Mhandle, [("TkChild", 0),("TkChild", 0),("Button",0)])  
        #print "generalReportHandle %x" % (generalReportHandle)  
        specificReportHandle = self.find_subHandle(Mhandle, [("TkChild", 0),("TkChild", 1),("Button",0)])  
        #print "specificReportHandle %x" % (specificReportHandle) 
        sectorIdHandle = self.find_subHandle(Mhandle, [("TkChild", 0),("TkChild", 2),("TkChild", 3),("TkChild", 0)])  
        #print "sectorIdHandle %x" % (sectorIdHandle) 
        carrierIdHandle = self.find_subHandle(Mhandle, [("TkChild", 0),("TkChild", 2),("TkChild", 2),("TkChild", 0)])  
        #print "carrierIdHandle %x" % (carrierIdHandle)
        apiIdHandle = self.find_subHandle(Mhandle, [("TkChild", 0),("TkChild", 2),("TkChild", 1),("TkChild", 0)])  
        #print "apiIdHandle %x" % (apiIdHandle)
        itemNameHandle = self.find_subHandle(Mhandle, [("TkChild", 0),("TkChild", 2),("TkChild", 0),("TkChild", 0)])  
        #print "itemNameHandle %x" % (itemNameHandle)
        # if api and itemName is empty, only generate the general report, else both report 
        if self.api != "" and self.itemName != "":
            #generate specific report, all edits will be filled
            self.moveMouseAndClick(Mhandle,sectorIdHandle)
            time.sleep(2)
            autopy.key.type_string(self.sectorId)
            
            self.moveMouseAndClick(Mhandle,carrierIdHandle)
            time.sleep(2)
            autopy.key.type_string(self.carrierId)
            
            self.moveMouseAndClick(Mhandle,apiIdHandle)
            time.sleep(2)
            autopy.key.type_string(self.api)
            
            self.moveMouseAndClick(Mhandle,itemNameHandle)
            time.sleep(2)
            autopy.key.type_string(self.itemName)
            
            self.moveMouseAndClick(Mhandle,specificReportHandle)
            time.sleep(3)
            self.judgeTheCpuUsageRate(self.apiReportToolDirecotry)
            
            self.moveMouseAndClick(Mhandle,generalReportHandle)
            time.sleep(3)
            self.judgeTheCpuUsageRate(self.apiReportToolDirecotry)
            self.finishSignal.emit()
            
        else: #only general report needed
            self.moveMouseAndClick(Mhandle,sectorIdHandle)
            time.sleep(2)
            autopy.key.type_string(self.sectorId)
            
            self.moveMouseAndClick(Mhandle,carrierIdHandle)
            time.sleep(2)
            autopy.key.type_string(self.carrierId)
            
            self.moveMouseAndClick(Mhandle,generalReportHandle)
            time.sleep(4)
            self.judgeTheCpuUsageRate(self.apiReportToolDirecotry)
            self.finishSignal.emit()
        
class killProcessThread(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(list)
    finishSignalForAt = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(killProcessThread, self).__init__(parent)
        self.expectedTime = ''
        self.processName = ''
        self.processList = []
    
    def initValues(self, endTime, process):
        self.expectedTime = endTime
        self.processName = process
    
    def run(self):
        global akButtonClicked
        
        currentTime = datetime.now()
        #print currentTime
        # add judgement here to sure the end time is ahead of the current time 
        sleepTime = (self.expectedTime-currentTime).seconds
        #print  ('the sleep time is %d' ,  sleepTime)
        time.sleep(sleepTime)
        exeList = self.processName.split(',')

        for each in exeList:
            wordList = each.split('.')
            print 'the killed process name is %s' % (wordList[0])
            if wordList[0] == '':
                break
            cmd = 'taskkill /F /IM %s.exe' % (wordList[0])
            time.sleep(1)
            os.system(cmd)
            self.processList.append(wordList[0])
        if akButtonClicked==1:  
            self.finishSignal.emit(self.processList)
        else:   
            self.finishSignal.emit(self.processList)
            self.finishSignalForAt.emit()

class killer(QDialog, Ui_akat):
    """
    Class documentation goes here.
    """
    paraForSubThread = QtCore.pyqtSignal(datetime, str)
    paraForAtThread = QtCore.pyqtSignal(list)
    paraForStartApiToolThread = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setFixedSize(820, 458)
        self.kThread = killProcessThread()
        self.aThread = atThread()
        self.apiThread = startApiReportToolThread()
        
        self.aThread.finishSignal.connect(self.atThreadFinished)
        self.kThread.finishSignal.connect(self.subThreadWorkEndAll)
        self.kThread.finishSignalForAt.connect(self.akFinishedToStartAT)
        self.paraForSubThread.connect(self.kThread.initValues)
        
        self.paraForAtThread.connect(self.aThread.initValues)
        self.paraForStartApiToolThread.connect(self.apiThread.initValues)
        self.dateTimeEdit_end.setDateTime(datetime.now())
        

    @pyqtSignature("")
    def on_pushButton_start_clicked(self):
        """
        Kill the process by name.
        """
        global  akButtonClicked
        akButtonClicked = 1        
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
        if str(processName) =='':
            QtGui.QMessageBox.information(self, "INFO", 'Please input the process name you want to kill')
            return
        else:
            currentTime = datetime.now()
            if currentTime > expectedEndTime:
                QtGui.QMessageBox.information(self, "INFO", 'Make sure the end time is after current time')
                return
            else:
                self.pushButton_start.setDisabled(True)
                self.pushButton_akatStart.setDisabled(True)
                self.pushButton_akatStop.setDisabled(True)
                self.paraForSubThread.emit(expectedEndTime, processName)
                self.flagKilling = 1
                self.kThread.start()    

    def akThreadStartForAT(self):
        """
        Kill the process by name.
        """
        global  akButtonClicked
        akButtonClicked = 0
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
        if str(processName) =='':
            QtGui.QMessageBox.information(self, "INFO", 'Please input the process name you want to kill')
            return 1
            #self.pushButton_akatStop.setDisabled(False)
        else:
            currentTime = datetime.now()
            if currentTime > expectedEndTime:
                QtGui.QMessageBox.information(self, "INFO", 'Make sure the end time is after current time')
                return 1
                #self.pushButton_akatStop.setDisabled(False)
            else:
                self.pushButton_start.setDisabled(True)
                self.flagKilling = 1
                self.paraForSubThread.emit(expectedEndTime, processName)
                self.kThread.start()  
                return 0
    def subThreadWorkEndAll(self, processList):
        '''
        after the killing thread work end, will send signal to main thread, and main thread will popup msg box to notify user
        '''
        
        self.flagKilling = 0
        global akButtonClicked
        #print 'the length of the list is %d' % len(processList)
        if len(processList) == 0:
            QtGui.QMessageBox.information(self, "INFO", 'No process will be terminated!!')
            if akButtonClicked == 1 :
                self.pushButton_akatStart.setDisabled(False)
                self.pushButton_akatStop.setDisabled(False)
            return
        else:
            for each in processList:
                QtGui.QMessageBox.information(self, "INFO", 'Process %s is Terminated' %(each))
            if akButtonClicked == 1:
                self.pushButton_akatStart.setDisabled(False)
                self.pushButton_akatStop.setDisabled(False)
                self.pushButton_start.setDisabled(False)
        #subprocess.call(r"D:\Work\AutoKiller\api_report_tool_v2.3\api_report_ui.exe")
        
    @pyqtSignature("")
    def on_pushButton_stop_clicked(self):
        """
        Stop the killing thread before timeout, no process will be killed.
        """
        if self.kThread.isRunning():
            self.kThread.terminate()
            self.pushButton_start.setDisabled(False)
            self.flagKilling = 0
            self.pushButton_akatStart.setDisabled(False)
            self.pushButton_akatStop.setDisabled(False)
    @pyqtSignature("")       
    def on_pushButton_akatStart_clicked(self):
        startN = str(self.lineEdit_from.text())
        endN = str(self.lineEdit_to.text())
        carrierId = str(self.lineEdit_carrierID.text())
        sectorId = str(self.lineEdit_sectorID.text())
        mmtDirectory = str(self.lineEdit_mmtDirectory.text())
        apiReportToolDirectory =str(self.lineEdit_apiReportToolDirectory.text())
        #apiReportToolDirectory = str(apiReportToolDirectory)
        if startN=='' or endN =='' or carrierId =='' or sectorId=='' or mmtDirectory=='' or apiReportToolDirectory =='':
            QtGui.QMessageBox.information(self, "INFO", 'Must fill all Line edit expect the api and itemName!!')
            return
        else:
            self.pushButton_akatStart.setDisabled(True)
            self.pushButton_stop.setDisabled(True)
            if  self.akThreadStartForAT() ==1:
                self.pushButton_akatStart.setDisabled(False)
                self.pushButton_stop.setDisabled(False)
    
    def akFinishedToStartAT(self):
        '''
        get parameters from gui, and send them to the decode thread, and copy the mmt files from MMT dir to converted dir
        also copy the configuration cvs file in api report tool path to current path, before copy will delete all the cvs files from
        current path.
        '''
        paraList = []
        startN = str(self.lineEdit_from.text())
        #print type(startN)
        endN = str(self.lineEdit_to.text())
        fromNumber = string.atoi(startN)
        toNumber = string.atoi(endN)
        carrierId = self.lineEdit_carrierID.text()
        paraList.append(str(carrierId))
        sectorId = self.lineEdit_sectorID.text()
        paraList.append(str(sectorId))
        api = self.lineEdit_api.text()
        paraList.append(str(api))
        itemName = self.lineEdit_itemName.text()
        paraList.append(str(itemName))
        mmtDirectory = self.lineEdit_mmtDirectory.text()
        convertedMmtDirectory = os.path.join(str(mmtDirectory),'convertedMMT')
        #print  convertedMmtDirectory
        paraList.append(convertedMmtDirectory)
        apiReportToolDirectory =self.lineEdit_apiReportToolDirectory.text()
        apiReportToolDirectory = str(apiReportToolDirectory)
        paraList.append(apiReportToolDirectory)
        if not os.path.exists(convertedMmtDirectory):
            os.mkdir(convertedMmtDirectory)
        fileList = os.listdir(mmtDirectory)
        #print fileList
        for i in range(fromNumber,toNumber+1):
            if i<10:
                rule = '.+_0000%s_.+'%(i)
            elif 10<=i and i<100:
                rule = '.+_000%s_.+'%(i)
            elif 100<=i and i<1000:
                rule = '.+_00%s_.+'%(i)
            elif 1000<=i and i<10000:
                rule = '.+_0%s_.+'%(i) 
            else:
                rule = '.+_%s_.+'%(i)
            for each in fileList:
                if re.search(rule,each):
                    shutil.move(os.path.join(str(mmtDirectory), each),str(convertedMmtDirectory))
        
        #copy csv files from api report tool to current dir
        apiDirPath = os.path.dirname(apiReportToolDirectory)
        filesInApiToolPath = os.listdir(apiDirPath)
        #print filesInApiToolPath
        currentDir = os.getcwd()
        #print currentDir
        rule = '.+\.csv'
        for eachfile in filesInApiToolPath:
            if re.search(rule, eachfile):
                shutil.copy(os.path.join(str(apiDirPath), eachfile),currentDir)
        
        #send parameter to sub threads and start api tool and start the decode 
        self.paraForAtThread.emit(paraList)
        self.paraForStartApiToolThread.emit(apiReportToolDirectory)
        self.apiThread.start()
        #time.sleep(2)
        #Mhandle = win32gui.FindWindow("TkTopLevel", r"SAT 400UE API Report Tool")
        #print "%x" % (Mhandle) 
        #set the window to the top level
        #win32gui.ShowWindow(Mhandle,win32con.SW_RESTORE)
        #shell = win32com.client.Dispatch("WScript.Shell")
        #shell.SendKeys('%')
        #win32gui.SetForegroundWindow(Mhandle)
        
        self.aThread.start() 
        
    def atThreadFinished(self):
        '''
        after decode thread finished, the main thread will kill the api report tool
        '''
        cmd = 'taskkill /F /IM %s' % (os.path.basename(str(self.lineEdit_apiReportToolDirectory.text())))
        #print cmd
        time.sleep(1)
        os.system(cmd)
        self.pushButton_akatStart.setDisabled(False)
        self.pushButton_stop.setDisabled(False)
    @pyqtSignature("")    
    def on_pushButton_akatStop_clicked(self):
        if self.kThread.isRunning():
            self.kThread.terminate()
        self.pushButton_start.setDisabled(False)
        self.pushButton_stop.setDisabled(False)
            
        if self.aThread.isRunning():
            self.aThread.terminate()
        self.pushButton_akatStart.setDisabled(False)    
        
        
if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import  QApplication
    app = QApplication(sys.argv)
    dlg = killer()
    dlg.show()
    sys.exit(app.exec_())
