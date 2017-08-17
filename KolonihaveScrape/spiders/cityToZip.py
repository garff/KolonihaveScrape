# -*- coding: utf-8 -*-
import csv
import codecs
import sys

class cityToZip():

    def __init__(self, ):
        self.cityToZipCode = {}
        self.ktsCity = []
        self.ktsCityAsZips = []

    ## Map city into a zip code HashMap - allows for returning of zip code from city name
    def readZipCodesAndCitiesIntoHashMap(self, ):
        with open('/Users/whateverisforever/Desktop/All/Coding/MyScripts/KolonihaveScrape/KolonihaveScrape/spiders/postnumre.txt', 'r') as csvFile:
            rowReader = csv.reader(csvFile, delimiter=',', quotechar='\n')
            for row in rowReader:
                self.cityToZipCode[row[1]] = row[0]

    ## Reads kts.txt - appends the city to a list 
    def readScrapedZipCodesFromTxt(self, ): 
        with open('/Users/whateverisforever/Desktop/All/Coding/MyScripts/KolonihaveScrape/KolonihaveScrape/spiders/kts.txt', 'r') as csvFile:
            rowReader = csv.reader(csvFile, delimiter=',', quotechar='\n')
            for row in rowReader:
                self.ktsCity.append(row[0])

    ## Saves the city as zip in ktsCityAsZips
    def changeCitiesToZipCodes(self, ):
        for x in self.ktsCity:
            try: ## Only happens if citys zip-code is <= 3670 - the cities of interest 
                self.ktsCityAsZips.append(self.cityToZipCode[x])
            except: 
                pass

    ## Substitues the city name for the zip code
    def writeNewZipCodesToTxt(self, ):
        with open('/Users/whateverisforever/Desktop/All/Coding/MyScripts/KolonihaveScrape/KolonihaveScrape/spiders/kts.txt', 'r') as csvfile:
            txtFileWithCityNameAsList = [] 
            rowReader = csv.reader(csvfile, delimiter=',', quotechar='\n')
            for row in rowReader:
                for x in row:
                    txtFileWithCityNameAsList.append(x)

            ## Swap city for zip
            print txtFileWithCityNameAsList
            print self.ktsCityAsZips
            try: ## Sets the zip-code if it is <= 3670
                txtFileWithCityNameAsList[0] = self.ktsCityAsZips[0]
            except: txtFileWithCityNameAsList[0] = '0000'

            ## Write is out 
            ktsTxt = codecs.open('/Users/whateverisforever/Desktop/All/Coding/MyScripts/KolonihaveScrape/KolonihaveScrape/spiders/kts.txt', 'r+', 'utf-8')
            ktsTxt.truncate()

            cityName = txtFileWithCityNameAsList[0]
            price = txtFileWithCityNameAsList[1]
            sqMtr = txtFileWithCityNameAsList[2]
            date = txtFileWithCityNameAsList[3]
            relativeUrl = txtFileWithCityNameAsList[4]

            ktsTxt.write(cityName + ',' + price + ',' + sqMtr + ',' + date + ',' + relativeUrl + '\n')
