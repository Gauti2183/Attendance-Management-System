#輸出數據寫入CSV文件
import csv


def resetdata(ID):
    data = [[0 for i in range(6)] for i in range(31)]
    writedata(ID, data)

def writedata(ID,data):
    dataname = str(ID) + '.csv'
    with open(dataname, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for list in data:
            csv_writer.writerow(list)


def readdata(ID):
    data = []
    dataname = str(ID) + '.csv'
    f = open(dataname, 'r', newline='')
    for row in csv.reader(f):
        data.append(row)
    f.close()
    return data