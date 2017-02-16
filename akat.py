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

akButtonClicked = 0


def dealPath(pathname=''):
    '''deal with windows file path'''
    if pathname:
        pathname = str(pathname).strip()
    if pathname:
        pathname = r'%s'%pathname
        pathname = string.replace(pathname, r'/', '\\')
        pathname = os.path.abspath(pathname)
        if pathname.find(":\\") == -1:
            pathname = os.path.join(os.getcwd(), pathname)
    return pathname
#The excel operation class:
class EasyExcel(object):
    '''class of easy to deal with excel'''

    def __init__(self):
        '''initial excel application'''
        self.m_filename = ''
        self.m_exists = False
        self.m_excel = win32com.client.DispatchEx('Excel.Application') #也可以用Dispatch，前者开启新进程，后者会复用进程中的excel进程
        self.m_excel.DisplayAlerts = False                             #覆盖同名文件时不弹出确认框
        
    def open(self, filename=''):
        '''open excel file'''
        if getattr(self, 'm_book', False):
            self.m_book.Close()
        self.m_filename = dealPath(filename) or ''
        self.m_exists = os.path.isfile(self.m_filename)
        if not self.m_filename or not self.m_exists:
            self.m_book = self.m_excel.Workbooks.Add()
        else:
            self.m_book = self.m_excel.Workbooks.Open(self.m_filename)

    def reset(self):
        '''reset'''
        self.m_excel = None
        self.m_book = None
        self.m_filename = ''

    def save(self, newfile=''):
        '''save the excel content'''
        assert type(newfile) is str, 'filename must be type string'
        newfile = dealPath(newfile) or self.m_filename
        if not newfile or (self.m_exists and newfile == self.m_filename):
            self.m_book.Save()
            return
        pathname = os.path.dirname(newfile)
        if not os.path.isdir(pathname):
            os.makedirs(pathname)
        self.m_filename = newfile
        self.m_book.SaveAs(newfile)

    def close(self):
        '''close the application'''
        self.m_book.Close(SaveChanges=1)
        self.m_excel.Quit()
        time.sleep(2)
        self.reset()

    def addSheet(self, sheetname=None):
        '''add new sheet, the name of sheet can be modify,but the workbook can't '''
        #print ' in Add sheet'
        sht = self.m_book.Worksheets.Add()
        sht.Name = sheetname if sheetname else sht.Name
        return sht

    def getSheet(self, sheet=1):
        '''get the sheet object by the sheet index'''
        #print 'in get sheet'
        assert sheet > 0, 'the sheet index must bigger then 0'
        return self.m_book.Worksheets(sheet)

    def getSheetByName(self, name):
        '''get the sheet object by the sheet name'''
        #print 'the sheet count is %d'%(self.getSheetCount())
        for i in xrange(1, self.getSheetCount()+1):
            sheet = self.getSheet(i)
            if name == sheet.Name:
                print 'the name is %s'%(sheet.Name)
                return i
        return None

    def getCell(self, sheet=1, row=1, col=1):
        '''get the cell object'''
        assert row>0 and col>0, 'the row and column index must bigger then 0'
        return self.getSheet(sheet).Cells(row, col)

    def getRow(self, sheet=1, row=1):
        '''get the row object'''
        #print 'in get Row'
        assert row>0, 'the row index must bigger then 0'
        return self.getSheet(sheet).Rows(row)

    def getCol(self, sheet, col):
        '''get the column object'''
        assert col>0, 'the column index must bigger then 0'
        return self.getSheet(sheet).Columns(col)

    def getRange(self, sheet, row1, col1, row2, col2):
        '''get the range object'''
        sht = self.getSheet(sheet)
        return sht.Range(self.getCell(sheet, row1, col1), self.getCell(sheet, row2, col2))

    def getCellValue(self, sheet, row, col):
        '''Get value of one cell'''
        return self.getCell(sheet,row, col).Value

    def setCellValue(self, sheet, row, col, value):
        '''set value of one cell'''
        #print 'in set Cell value'
        self.getCell(sheet, row, col).Value = value

    def getRowValue(self, sheet, row):
        '''get the row values'''
        #print 'in get row value'
        return self.getRow(sheet, row).Value

    def setRowValue(self, sheet, row, values):
        '''set the row values'''
        #print 'in SetRowValue'
        self.getRow(sheet, row).Value = values

    def getColValue(self, sheet, col):
        '''get the row values'''
        #print 'in getColValue'
        return self.getCol(sheet, col).Value

    def setColValue(self, sheet, col, values):
        '''set the row values'''
        #print 'in setColValue'
        self.getCol(sheet, col).Value = values

    def getRangeValue(self, sheet, row1, col1, row2, col2):
        '''return a tuples of tuple)'''
        return self.getRange(sheet, row1, col1, row2, col2).Value

    def setRangeValue(self, sheet, row1, col1, data):
        '''set the range values'''
        row2 = row1 + len(data) - 1
        col2 = col1 + len(data[0]) - 1
        range = self.getRange(sheet, row1, col1, row2, col2)
        range.Clear()
        range.Value = data

    def getSheetCount(self):
        '''get the number of sheet'''
        return self.m_book.Worksheets.Count

    def getMaxRow(self, sheet):
        '''get the max row number, not the count of used row number'''
        return self.getSheet(sheet).Rows.Count

    def getMaxCol(self, sheet):
        '''get the max col number, not the count of used col number'''
        return self.getSheet(sheet).Columns.Count

    def clearCell(self, sheet, row, col):
        '''clear the content of the cell'''
        self.getCell(sheet,row,col).Clear()

    def deleteCell(self, sheet, row, col):
        '''delete the cell'''
        self.getCell(sheet, row, col).Delete()

    def clearRow(self, sheet, row):
        '''clear the content of the row'''
        self.getRow(sheet, row).Clear()

    def deleteRow(self, sheet, row):
        '''delete the row'''
        self.getRow(sheet, row).Delete()

    def clearCol(self, sheet, col):
        '''clear the col'''
        self.getCol(sheet, col).Clear()

    def deleteCol(self, sheet, col):
        '''delete the col'''
        self.getCol(sheet, col).Delete()

    def clearSheet(self, sheet):
        '''clear the hole sheet'''
        self.getSheet(sheet).Clear()

    def deleteSheet(self, sheet):
        '''delete the hole sheet'''
        #print 'in delete sheet'
        self.getSheet(sheet).Delete()

    def deleteRows(self, sheet, fromRow, count=1):
        '''delete count rows of the sheet'''
        maxRow = self.getMaxRow(sheet)
        maxCol = self.getMaxCol(sheet)
        endRow = fromRow+count-1
        if fromRow > maxRow or endRow < 1:
            return
        self.getRange(sheet, fromRow, 1, endRow, maxCol).Delete()

    def deleteCols(self, sheet, fromCol, count=1):
        '''delete count cols of the sheet'''
        maxRow = self.getMaxRow(sheet)
        maxCol = self.getMaxCol(sheet)
        endCol = fromCol + count - 1
        if fromCol > maxCol or endCol < 1:
            return
        self.getRange(sheet, 1, fromCol, maxRow, endCol).Delete()

class copyDataAndGraphThread(QtCore.QThread):
    copyFinishSignal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(copyDataAndGraphThread, self).__init__(parent)
    def initValues(self, sourceFilePath, targetExcelPath, name, cellid):
        self.sourceExcelFilePath = sourceFilePath
        self.targetExcelFile = targetExcelPath
        self.graphName = name
        self.CellId = cellid
    def run(self):
        excelRd = EasyExcel()
        #print self.sourceExcelFilePath, self.targetExcelFile, self.graphName, self.CellId
        sourceFileName = os.path.join(str(self.sourceExcelFilePath), (r'general_report_cell'+str(self.CellId)+r'.xlsx'))
        print 'the sourceFileName is %s'%(sourceFileName)
        excelRd.open(sourceFileName)

        generalSheet = excelRd.getSheetByName(r'general')
        aveDataRateSheet = excelRd.getSheetByName(r'aveDataRate')
        pathlossSheet = excelRd.getSheetByName(r'pathloss')
        cqiSheet = excelRd.getSheetByName(r'cqi')
        #sourceContent = excelRd.getRangeValue(generalSheet,1,1,240,61)
       
        targetFileName = self.targetExcelFile
        excelWt = EasyExcel()
        excelWt.open(targetFileName)

        #copy the summary sheet
        sheetSummary= excelWt.getSheetByName('Summary')
        if not sheetSummary:
            count =excelWt.getSheetCount()
            currentSheet = excelWt.getSheet(count)
            currentSheet.Select
            currentSheet.Activate()
            excelWt.addSheet('Summary')
            sheetSummary = excelWt.getSheetByName('Summary')
        else:
            excelWt.deleteSheet(sheetSummary)
            count =excelWt.getSheetCount()
            currentSheet = excelWt.getSheet(count)
            currentSheet.Select
            currentSheet.Activate()
            excelWt.addSheet('Summary')
            sheetSummary = excelWt.getSheetByName('Summary')
        for i in range(1,19):
            data = excelRd.getRowValue(aveDataRateSheet,i)
            excelWt.setRowValue(sheetSummary,i,data)
        
        #copy the pathloss data
        pathlossData = excelRd.getColValue(pathlossSheet,2)
        excelWt.setColValue(sheetSummary,8,pathlossData)
        #copy the cqi data
        cqiData = excelRd.getColValue(cqiSheet,2)
        excelWt.setColValue(sheetSummary,9,cqiData)
    
        #copy the general sheet
        sheetData= excelWt.getSheetByName('Data')
        if not sheetData:
            excelWt.addSheet('Data')
            sheetData = excelWt.getSheetByName('Data')
        else:
            excelWt.deleteSheet(sheetData)
            excelWt.addSheet('Data')
            sheetData = excelWt.getSheetByName('Data')
        for i in range(1,241):
            data = excelRd.getRowValue(generalSheet,i)
            excelWt.setRowValue(sheetData,i,data)
        #Set the graph name
        graphName = str(self.graphName)
        excelWt.setCellValue(9,1,11,graphName)
    
        savedFileName = os.path.join(str(self.sourceExcelFilePath),r'CompareResult.xlsm')
        print 'the saved file name is %s'%(savedFileName)
        excelWt.save(savedFileName)
        excelWt.close()
        excelRd.close()
        
        #run the copy macro 
        xl=win32com.client.Dispatch("Excel.Application")
        mb = xl.Workbooks.Open(Filename=savedFileName)
        xl.Application.Run("Copy")
        time.sleep(40)
        xl.Application.Save()
        mb.Save()
        mb.Close(SaveChanges=1)
        xl.Application.Quit()
        del xl
        self.copyFinishSignal.emit()

#Class used to start api report tool 
class startApiReportToolThread(QtCore.QThread):
    def __init__(self, parent=None):
        super(startApiReportToolThread, self).__init__(parent)
        self.apiReportToolDirecotry = ''
    def initValues(self, apiToolPath):
         self.apiReportToolDirecotry = str(apiToolPath)
    def run(self):
        #kill the api tool firstly, if it is in open status
        cmd = 'taskkill /F /IM %s' % (os.path.basename(str(self.apiReportToolDirecotry)))
        os.system(cmd)
        time.sleep(1)
        #self.apiReportToolDirecotry = os.path.join(str(self.apiReportToolDirecotry),r'api_report_ui_2.2.exe')
        os.system(self.apiReportToolDirecotry)

#class used to automatically transform the MMT log        
class atThread(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal()
    foregroundSignal = QtCore.pyqtSignal()
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
        #win32gui.ShowWindow(parentWH,win32con.SW_RESTORE)
        #need to initialize firstly in sub thread. set the api tool to the foreground, emit signal to let main thread make the api tool to foreground.
        self.foregroundSignal.emit()
        # for simple, just sleep to wait, but better to use signal to notify sub thread 
        time.sleep(6)
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
            percentage = abs(p.cpu_percent(interval=1.0))
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
    def inputUnderLine(self):
        autopy.key.toggle(autopy.key.K_SHIFT,True)
        autopy.key.type_string("_")
        time.sleep(1)
        autopy.key.toggle(autopy.key.K_SHIFT,False) 
        
    def run(self):
        time.sleep(10)
        #os.chdir(os.path.dirname(self.apiReportToolDirecotry))
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
        #if there is ":" and "_" in direcotry, need to input them separately
        autopy.key.toggle(autopy.key.K_SHIFT,True)
        autopy.key.type_string(":")
        time.sleep(1)
        autopy.key.toggle(autopy.key.K_SHIFT,False)
        #if there are "_" in file name need to input them separately 
        #autopy.key.type_string("\\")
        strList = dirList[1].split("\\")
        rule = "_"
        for each in strList:
            #if re.match(rule, each):
            #    self.inputUnderLine()
            if re.search(rule, each):
                wdList = each.split("_")
                #print wdList
                #print len(wdList)
                for i in range(len(wdList)):
                    autopy.key.type_string(wdList[i])
                    #print i, 
                    if i == (len(wdList)-1) and wdList[i] == '':
                        break
                    else:
                        if i ==(len(wdList)-1):
                            break
                        self.inputUnderLine()
            else:
                autopy.key.type_string(each)
            autopy.key.type_string("\\")
        #autopy.key.type_string(dirList[1])
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
            self.moveMouseAndClick(Mhandle,apiIdHandle)
            time.sleep(2)
            autopy.key.type_string(self.api)
             
            self.moveMouseAndClick(Mhandle,itemNameHandle)
            time.sleep(2)
            autopy.key.type_string(self.itemName)

            self.sectorId = str(self.sectorId).strip()
            self.carrierId = str(self.carrierId).strip()
            sectorList = self.sectorId.split(',')
            carrierList = self.carrierId.split(',')            
            for i in range(len(sectorList)):
                self.moveMouseAndClick(Mhandle,sectorIdHandle)
                autopy.mouse.click()
                autopy.key.tap(autopy.key.K_DELETE)
                time.sleep(2)
                autopy.key.type_string(sectorList[i])
                    
                self.moveMouseAndClick(Mhandle,carrierIdHandle)
                autopy.mouse.click()
                autopy.key.tap(autopy.key.K_DELETE)
                time.sleep(2)
                autopy.key.type_string(carrierList[i])
                
                self.moveMouseAndClick(Mhandle,specificReportHandle)
                time.sleep(3)
                self.judgeTheCpuUsageRate(self.apiReportToolDirecotry)
                
                self.moveMouseAndClick(Mhandle,generalReportHandle)
                time.sleep(3)
                self.judgeTheCpuUsageRate(self.apiReportToolDirecotry)
            self.finishSignal.emit()
            
        else: #only general report needed
            self.sectorId = str(self.sectorId).strip()
            self.carrierId = str(self.carrierId).strip()
            sectorList = self.sectorId.split(',')
            carrierList = self.carrierId.split(',')
            for i in range(len(sectorList)):             
                self.moveMouseAndClick(Mhandle,sectorIdHandle)
                autopy.mouse.click()
                autopy.key.tap(autopy.key.K_DELETE)
                time.sleep(2)
                autopy.key.type_string(sectorList[i])
            
                self.moveMouseAndClick(Mhandle,carrierIdHandle)
                autopy.mouse.click()
                autopy.key.tap(autopy.key.K_DELETE)
                time.sleep(2)
                autopy.key.type_string(carrierList[i])
            
                self.moveMouseAndClick(Mhandle,generalReportHandle)
                time.sleep(4)
                self.judgeTheCpuUsageRate(self.apiReportToolDirecotry)
            self.finishSignal.emit()

#Class used to Kill processes        
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
        self.processList = []
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

#Main Class
class killer(QDialog, Ui_akat):
    """
    Class documentation goes here.
    """
    paraForSubThread = QtCore.pyqtSignal(datetime, str)
    paraForAtThread = QtCore.pyqtSignal(list)
    paraForStartApiToolThread = QtCore.pyqtSignal(str)
    paraForCopyThread = QtCore.pyqtSignal(str,str,  str, str)
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setFixedSize(820, 600)
        self.kThread = killProcessThread()
        self.aThread = atThread()
        self.apiThread = startApiReportToolThread()
        self.copyThread = copyDataAndGraphThread()
        
        self.aThread.finishSignal.connect(self.atThreadFinished)
        self.aThread.foregroundSignal.connect(self.makeForeGround)
        self.kThread.finishSignal.connect(self.subThreadWorkEndAll)
        self.kThread.finishSignalForAt.connect(self.akFinishedToStartAT)
        self.copyThread.copyFinishSignal.connect(self.copyThreadFinished)
        self.paraForSubThread.connect(self.kThread.initValues)
        
        self.paraForCopyThread.connect(self.copyThread.initValues)
        
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
            QtGui.QMessageBox.information(self, "INFO", 'Must fill all Line edit except the api and itemName!!')
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
        #remove all the csv files in current dir 
        rule = '.+\.csv'
        filesInCurDir = os.listdir(currentDir)
        for eachfile in filesInCurDir:
            if re.search(rule, eachfile):
               os.remove(os.path.join(str(currentDir), eachfile)) 
        #print currentDir
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
        after decode thread finished, the main thread will kill the api report tool, and if check button 'copy' checked, will start the copy thread
        '''
        cmd = 'taskkill /F /IM %s' % (os.path.basename(str(self.lineEdit_apiReportToolDirectory.text())))
        #print cmd
        time.sleep(1)
        os.system(cmd)
        #set all button enabled
        self.pushButton_akatStart.setDisabled(False)
        self.pushButton_stop.setDisabled(False)
        self.pushButton_start.setDisabled(False)
        if self.checkBox.isChecked():
            #disable the copy button, after finished copy, need to enable it
            self.startCopyAndGraph()
            
    def startCopyAndGraph(self):
        self.pushButton_copyStart.setDisabled(True)
        #initialize the value
        mmtDirectory = self.lineEdit_mmtDirectory.text()
        convertedMmtDirectory = os.path.join(str(mmtDirectory),'convertedMMT')
        targetFile = str(self.lineEdit_targetGraphFile.text())
        Cellid = str(self.lineEdit_sourceFileId.text())
        graphname = str(self.lineEdit_graphName.text())   
        self.paraForCopyThread.emit(convertedMmtDirectory, targetFile, graphname,Cellid)
        time.sleep(1)
        self.copyThread.run()
    
    @pyqtSignature("")
    def on_pushButton_copyStart_clicked(self):
        """
        Slot documentation goes here.
        """
        # after click the copy button, call the startCopyAndGraph function
        self.startCopyAndGraph()
        
    @pyqtSignature("")    
    def on_pushButton_akatStop_clicked(self):
        if self.kThread.isRunning():
            self.kThread.terminate()
        self.pushButton_start.setDisabled(False)
        self.pushButton_stop.setDisabled(False)
            
        if self.aThread.isRunning():
            self.aThread.terminate()
        self.pushButton_akatStart.setDisabled(False)    
        
    def makeForeGround(self):
        Mhandle = win32gui.FindWindow("TkTopLevel", r"SAT 400UE API Report Tool")
        pythoncom.CoInitialize()
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(Mhandle)
    # when copy thread work end, enable the copy button and show a msg window
    def copyThreadFinished(self):
        self.pushButton_copyStart.setDisabled(False)
        QtGui.QMessageBox.information(self, "INFO", 'Copy and Graph Finished')
        print "Copy and generate Graph Successful"
        
if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import  QApplication
    app = QApplication(sys.argv)
    dlg = killer()
    dlg.show()
    sys.exit(app.exec_())
