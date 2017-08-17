# -*- coding: utf-8 -*-
import scrapy

class allotment():

    def __init__(self, allotments, allotmentNumber):
        self.cityName = allotments[allotmentNumber][0]
        self.price = allotments[allotmentNumber][1]
        self.sqMtr = allotments[allotmentNumber][2]
        self.date = allotments[allotmentNumber][3]
        self.relativeUrl = allotments[allotmentNumber][4]

    def getAllVarsOfAllotment(self,):
        allotmentVars = []
        allotmentVars.append(self.cityName)
        allotmentVars.append(self.price)
        allotmentVars.append(self.sqMtr)
        allotmentVars.append(self.date)
        allotmentVars.append(self.relativeUrl)
        return allotmentVars

    def getCityName(self,):
        return self.cityName

    def getsqMtr(self,):
        return self.sqMtr

    def getPrice(self,):
        return self.price

    def getDate(self,):
        return self.date

    def getRelativeUrl(self,):
        return self.relativeUrl