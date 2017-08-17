# -*- coding: utf-8 -*-
import codecs
import scrapy
from allotment import *

class DbaSpider(scrapy.Spider):
    name = 'dba'
    allowed_domains = ['http://www.dba.dk/boliger/fritidsbolig/kolonihaver/?soeg=kolonihave&sort=listingdate-desc']
    start_urls = ['http://www.dba.dk/boliger/fritidsbolig/kolonihaver/?soeg=kolonihave&sort=listingdate-desc']

    ## The amount of adds being scraped
    AMOUNT_OF_SCRAPED_ADDS = 1

    ## Scrapes the webpage for information about the allotment; 1) City name, 2) Price, 3) Square meter - m2, 4) Date put up for sale
    ## 4 parameters that tells if the sale is unique for crossreferencing when scraping other sites
    ## The last parameter is the url link from the mainpage to the individual adds
    def parse(self, response):
    	
        allotmentsRawData = []

        ## Wrapper containing city
        allotmentForSaleCity = response.xpath('//td[@class="mainContent"]/ul[@class="details"]')

        ## Wrapper containing price 
        allotmentForSalePrice = response.xpath('//td[@title="Pris"]')

        ## Wrapper containing squareMeter 
        allotmentForSaleSqmtr = response.xpath('//div[@class="expandable-box expandable-box-collapsed"]')

        ## Wrapper containing date
        allotmentForSaleDate = response.xpath('//td[@title="Dato"]')

        ## Wrapoper containing the url
        allotmentForSaleUrl = response.xpath('//div[@class="expandable-box expandable-box-collapsed"]')

        for x in range(0, self.AMOUNT_OF_SCRAPED_ADDS):

            ## City
            try:
                city = allotmentForSaleCity[x].xpath('li/span/a/text()').extract_first()[6:10]
            except:
                city = "null"
            allotmentsRawData.append([city, ]) ## Appends the city as a list and the first element

            ## Price
            try:
                price = allotmentForSalePrice[x].xpath('text()').extract_first()[6:-6]
            except:
                price = "null"
            allotmentsRawData[x].append(price) ## Appends the price to the list 

            ## Square meter
            try:
                squareMeter = allotmentForSaleSqmtr[x].xpath('a/text()').extract_first()[12:14]
            except:
                squareMeter = "null"
            allotmentsRawData[x].append(squareMeter) ## Appends tbe squaremeter price to the list 
            
            ## Date
            try:
                date = allotmentForSaleDate[x].xpath('text()').extract_first()[6:-2]
            except:
                date = "null"
            allotmentsRawData[x].append(date) ## Appends the date to the list 

            ## Url
            try: 
                url = allotmentForSaleUrl[x].xpath('a/@href').extract_first()[0:]
            except:
                url = "null"
            allotmentsRawData[x].append(url) ## Appends the url to the list 

        self.processedAllotments = self.processAllotments(allotmentsRawData)
        self.writeToFile(self.processedAllotments)

    ## Processes the allotments and transform the raw data into allotment objects
    def processAllotments(self, allotmentsRawData):

        processedAllotments = []
        for x in range(0, self.AMOUNT_OF_SCRAPED_ADDS):
            processedAllotments.append(allotment(allotmentsRawData,x))
        return processedAllotments

    ## Write the proccesed allotments out into kts.txt 
    def writeToFile(self, processedAllotments):

        dbaTxt = codecs.open('/Users/whateverisforever/Desktop/All/Coding/MyScripts/KolonihaveScrape/KolonihaveScrape/spiders/dba.txt', 'r+', 'utf-8')
        dbaTxt.truncate()

        for x in range(0, self.AMOUNT_OF_SCRAPED_ADDS):

            cityName = processedAllotments[x].getCityName()
            price = processedAllotments[x].getPrice()
            sqMtr = processedAllotments[x].getsqMtr()
            date = processedAllotments[x].getDate()
            url = processedAllotments[x].getRelativeUrl() ## In this case its just the url

            dbaTxt.write(cityName + ',' + price + ',' + sqMtr + ',' + date + ',' + url + '\n')
