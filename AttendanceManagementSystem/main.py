#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 02:42:55 2018

@author: uhong
"""

import sys
import get_ID
import main_structure
from UI import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import datetime
import csvdata
import os
import time
import pandas as pd
from PyQt5.QtWidgets import QMessageBox

import csv
last_time = []
header = ["早上上班","早上下班","下午上班","下午下班","晚上加班","晚上下班","上班時數","加班時數","時薪","日薪"]
time_last = {0: 0, 1: 0,2: 0,3: 0,4: 0,5: 0,6: 0,7: 0,8: 0,9: 0,10: 0,11: 0,12: 0,13: 0,14: 0}
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.pushButton_addmember.clicked.connect(self.set_name)
        self.comboBox.activated.connect(self.showcard)
        self.pushButton_2.clicked.connect(self.gettime)
        self.pushButton_addMember.clicked.connect(self.addMember)
        self.timer = QTimer(self)
        self.count = 0
        self.timer.timeout.connect(self.card)
        self.startCount()
        for i in range(len(header)):
            self.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(header[i]))
        self.sysStatus = 0

    def checkCardMember(self,memberNumber,sysStatus):
        df = pd.read_csv('../data/key.csv')
        return df[(df.ID == memberNumber)].index.tolist()

    def addMember(self):
        self.textEdit_State.setText("請感應卡片以增加成員")
        aelf.sysStatus = 1

    def startCount(self):
        self.timer.start(5000)

    def timetostring(self,stime):
        if len(stime) != 1:
            wtime = stime[0:2] + stime[3:5]
        else:
            wtime = stime
        return wtime

    def getminute(self,sminute):
        if len(sminute) != 1:
            wminute = int(sminute[0:2]) * 60 + int(sminute[2:4])
        else:
            wminute = int(sminute)
        return wminute

    def gettime(self):
        currentT = self.comboBox.currentIndex()
        reader = csvdata.readdata(currentT + 1)
        h_salary = self.textEdit_2.toPlainText()

        if len(h_salary) == 0 :
            QMessageBox.question(self, 'Message', '錯誤:尚未輸入時薪', QMessageBox.Yes)
            return
        for i in range(31):

            time1 = self.timetostring(reader[i][0])
            minute1 = self.getminute(time1)
            if (minute1 < 480) & (minute1 != 0)  :
                minute1 = 480
            time2 = self.timetostring(reader[i][1])
            minute2 = self.getminute(time2)
            moringtime = minute2 - minute1

            time3 = self.timetostring(reader[i][2])
            minute3 = self.getminute(time3)
            if (minute3 < 780) & (minute3 != 0):
                minute3 = 780
            time4 = self.timetostring(reader[i][3])
            minute4 = self.getminute(time4)

            time5 = self.timetostring(reader[i][4])
            minute5 = self.getminute(time5)
            time6 = self.timetostring(reader[i][5])
            minute6 = self.getminute(time6)

            if (minute4 != 0) & (minute3 !=0):
                afternoontime = minute4 - minute3
            elif(minute6 != 0) & (minute5 == 0) & (minute4 == 0) & (minute3 != 0):
                afternoontime = 1020 - minute3
                print(afternoontime)
            else:
                afternoontime = 0
                mess = str(i+1) + '日早上可能有誤'
                reply = QMessageBox.question(self, 'Message',  mess, QMessageBox.Yes | QMessageBox.Ignore,
                                             QMessageBox.Ignore)
                if reply == QMessageBox.Ignore:
                    return
            if (minute5 != 0) & (minute6 != 0):
                night = minute6 - minute5
            elif (minute6 != 0) & (minute5 == 0) & (minute4 == 0) & (minute3 != 0):
                night = minute6 - 1020
            else:
                night = 0
                mess = str(i+1) + '日下午可能有誤'
                reply = QMessageBox.question(self, 'Message',  mess, QMessageBox.Yes | QMessageBox.Ignore,
                                             QMessageBox.Ignore)
                if reply == QMessageBox.Ignore:
                    return
            overtime = round((night / 60), 2)
            normaltime = round(((moringtime + afternoontime) / 60), 2)

            money = round(normaltime * float(h_salary) + 1.33 * overtime * float(h_salary),0)

            self.tableWidget.setItem(i, 6, QTableWidgetItem(str(normaltime)))
            self.tableWidget.setItem(i, 7, QTableWidgetItem(str(overtime)))
            self.tableWidget.setItem(i, 8, QTableWidgetItem(h_salary))
            self.tableWidget.setItem(i, 9, QTableWidgetItem(str(money)))

    def showcard(self):
        who = self.comboBox.currentIndex()
        reader = csvdata.readdata(who + 1)
        self.settable(reader)

    def settable(self, timelist):

        for i in range(6):
            for j in range(31):
                self.tableWidget.setItem(j, i, QTableWidgetItem(timelist[j][i]))

    def set_name(self):
        #name = self.textEdit.toPlainText()
        #salary = self.textEdit_2.toPlainText()
        #self.newName = QTableWidgetItem(name)
        #self.newSalary = QTableWidgetItem(salary)
        #self.tableWidget.setItem(0, 0, self.newName)
        #self.tableWidget.setItem(0, 1, self.newSalary)

        self.card()

    def card(self):
        timeAll = str(datetime.datetime.now())

        timeAll = timeAll[0:16]
        time_card = timeAll[11:16]
        hour = timeAll[11:13]

        day = timeAll[8:10]
        if int(day) < 10:
            day = timeAll[9:10]

        test = get_ID.get_ID()
        #hour = 17
        for i in range(15):
            if test[i] == "1":
                if not (os.path.isfile('../data/key.csv')):
                    csvdata.resetKeyData()
                memberIndex = self.checkCardMember(i+1,self.sysStatus)
                if not memberIndex:
                    self.textEdit_Status.setText("未知的卡片號碼\n請先加入卡片")
                    return
                else:
                    df = pd.read_csv('../data/key.csv')
                    memberIndexInt = memberIndex[0]
                    self.textEdit_Status.setText("歡迎 " + df['Name'][memberIndexInt])

                path = csvdata.getPath()
                datafile = path +str(i+1) + '.csv'
                if not (os.path.isfile(datafile)):
                    csvdata.resetdata(i+1)
                reader = csvdata.readdata(i+1)
                time_now = (int(time_card[0:2])) * 60 + int(time_card[3:5])
                #if difference of time under 5 minutes, it won't work
                if (time_now - time_last[i]) < 5 :
                    return
                time_last[i] = time_now
                print(time_last)

                if (reader[int(day) - 1][0] == '0') & (int(hour) < 12) :
                    moment = 0
                elif (reader[int(day) - 1][0] != '0') & (reader[int(day) - 1][1] == '0'):
                    moment = 1
                elif (reader[int(day) - 1][2] == '0') & (int(hour) >= 12) & (int(hour) <= 17):
                    moment = 2
                elif (reader[int(day) - 1][2] != '0') & (reader[int(day) - 1][3] == '0'):
                    moment = 3
                elif (reader[int(day) - 1][4] == '0') & (int(hour) >= 17):
                    moment = 4
                elif (reader[int(day) - 1][5] == '0') & (reader[int(day) - 1][4] != '0'):
                    moment = 5
                else:
                    moment = 5
                reader[int(day) - 1][moment] = str(time_card)
                csvdata.writedata(i+1, reader)
                #self.tableWidget.setItem(1, 0, QTableWidgetItem(time_card))

        fo = open("../data/RawData.txt", "a")
        fo.write(test + " " + timeAll + '\n')
        fo.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

