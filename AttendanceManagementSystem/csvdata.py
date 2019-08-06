#輸出數據寫入CSV文件
import csv
import time
import pandas as pd


def resetKeyData():
    df = pd.DataFrame(columns = ["Name","ID"]) 
    df.to_csv("../data/key.csv",index=False)

def resetdata(ID):
    data = [[0 for i in range(6)] for i in range(31)]
    writedata(ID, data)

def writedata(ID,data):
    path = getPath()
    dataname = path + str(ID) + '.csv'
    with open(dataname, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for list in data:
            csv_writer.writerow(list)


def readdata(ID):
    data = []
    path = getPath()
    dataname = path + str(ID) + '.csv'
    f = open(dataname, 'r', newline='')
    for row in csv.reader(f):
        data.append(row)
    f.close()
    return data

def getPath():
    year = time.localtime().tm_year
    month = time.localtime().tm_mon
    path = '../data/' + str(year) + '/' + str(month) + '/'
    return path 