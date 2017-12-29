#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, sys
import datetime, time
import commands
import logging
import ConfigParser
import pandas as pd
import numpy as np
import MySQLdb
from rwExcel import rwExcel
from rwExcel import position

reload(sys)
sys.setdefaultencoding('utf-8')
from mysqlProcess import mysqlProcess;



class pandasProcess(mysqlProcess):
    def __init__(self):
        mysqlProcess.__init__(self);
        self.fileType = 0;
        self.targetFileName = "../data/test.xlsx";

    def generateMonthDataToExcel(self, pdData, startRow=1):
        print "generateMonthDataToExcel";
        tmpRwExcel = rwExcel();
        tmpPosition = position(0, 0);
        tmpRange = position(pdData.shape.__getitem__(0), pdData.shape.__getitem__(1));
        excelPosition = position(startRow, 0);
        tmpRwExcel.updateExcel(self.targetFileName, self.fileType - 1, pdData, tmpPosition, tmpRange, excelPosition);

    def getMonthData(self, FileName):
        Data1 = pd.DataFrame(columns=["location", 'name'])
        Data = pd.DataFrame({"location": "", "MinValueofOutputOpticalPower": ""}, index=["0"])
        filepath = "/data/vixtel/OtndatasFile"
        path1="/home/OtnDatas/File/"
        if "00050" in FileName:
            Data.drop(Data.index, inplace=True)
            path=filepath+"/00050"
            self.fileType = 1
            cloumnname = "MaxValueofReceivingOpticalPower";
            self.GetPdData(path=path,path1=path1,Data=Data,cloumnname=cloumnname)


        if "04203" in FileName:
            Data.drop(Data.index, inplace=True)
            self.fileType = 2
            path = filepath + "/04203"
            cloumnname = "EthernetPIReceiveerrorframes"
            self.GetPdData(path=path,path1=path1,Data=Data,cloumnname=cloumnname)

    def GetPdData(self,path,path1,Data,cloumnname):
        dirs = os.listdir(path)
        for dir in  dirs:
            print dir
            df = pd.read_csv(path + dir, encoding="gb2312")
            df.rename(columns=lambda x: x.replace('测量对象位置', 'location'), inplace=True)
            df1 = pd.read_csv(path1 + "location.csv", encoding="gb2312")
            con = pd.merge(df, df1, how="inner", on="location", indicator='indicator')
            pdData = con[con.indicator == "both"].reset_index()
            print pdData
            for i in range(len(pdData)):
                val = pdData.ix[i]["location"];
                val2 = pdData.ix[i][cloumnname];
                dataFrame = pd.DataFrame([[val, val2]], columns=["location", 'name'])
                Data = Data.append(dataFrame,ignore_index=True).fillna("")
            print Data
            #self.generateMonthDataToExcel(pdData=Data);
    def mainProcess(self):
        fileNameList = ['00050', '04203']
        for FileName in fileNameList:
            self.getMonthData(FileName);


if __name__ == "__main__":
    while True:
        excelMonthlyData = pandasProcess();
        excelMonthlyData.mainProcess();
        break;
