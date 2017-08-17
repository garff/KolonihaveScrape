# -*- coding: utf-8 -*-
import codecs
import scrapy
from allotment import *


class KtsSpider(scrapy.Spider):
    name = 'kts'
    allowed_domains = ['http://kolonihavertilsalg.dk']
    start_urls = ['http://kolonihavertilsalg.dk']

    ## The amount of adds being scraped
    AMOUNT_OF_SCRAPED_ADDS = 1

    ## Scrapes the webpage for information about the allotment; 1) City name, 2) Price, 3) Square meter - m2, 4) Date put up for sale
    ## 4 parameters that tells if the sale is unique for crossreferencing when scraping other sites
    ## The last parameter is the url link from the mainpage to the individual adds
    def parse(self, response):

        allotmentsRawData = []
        
        ## Wrapper containing all 4 parameters 
        allotmentForSale = response.xpath('//tr[@class="annonce_liste_item"]')

        ## Each <span id=""> is unique - first 4 adds are scraped 
        for x in range(0, self.AMOUNT_OF_SCRAPED_ADDS):
            ## City
            cityId = "//span[@id='ctl00_MainContent_AnnonceListe_ListViewAnnonceListe_ctrl" + str(x) + "_by_idLabel']/text()"
            try:
                city = allotmentForSale.xpath(cityId).extract_first()[0:]
            except:
                city = "null"
            allotmentsRawData.append([city,]) ## Appends the city first as a list and the first element 
            
            ## Price
            priceId = "//span[@id='ctl00_MainContent_AnnonceListe_ListViewAnnonceListe_ctrl" + str(x) + "_salgsprisLabel']/text()"
            try:
                price = allotmentForSale.xpath(priceId).extract_first()[4:]
            except:
                price = "null"
            allotmentsRawData[x].append(price) ## Appends the price to the city list 

            ## Squaremeter
            squareMeterID = "//span[@id='ctl00_MainContent_AnnonceListe_ListViewAnnonceListe_ctrl" + str(x) + "_boligarealLabel']/text()"
            try:
                squareMeter = allotmentForSale.xpath(squareMeterID).extract_first()[0:-3]
            except:
                squareMeter = "null"
            allotmentsRawData[x].append(squareMeter) ## Appends the square meter size to the city list

            ## Date
            dateId = "//span[@id='ctl00_MainContent_AnnonceListe_ListViewAnnonceListe_ctrl" + str(x) + "_oprettetLabel']/text()"
            try:
                date = allotmentForSale.xpath(dateId).extract_first()[0:]
            except:
                date = "null"
            allotmentsRawData[x].append(date) ## Appends the date to the city list 

            ## Url
            urlId = "//a[@id='ctl00_MainContent_AnnonceListe_ListViewAnnonceListe_ctrl" + str(x) + "_HyperLinkVisAnnoncen']/@href"
            try:
                relativeUrl = allotmentForSale.xpath(urlId).extract_first()[0:]
            except:
                relativeUrl = "null"
            absoluteUrl = "http://kolonihavertilsalg.dk/" + relativeUrl
            allotmentsRawData[x].append(absoluteUrl) ## Appends the url to the city list        

        self.proccessedAllotments = self.processAllotments(allotmentsRawData)
        self.writeToFile(self.proccessedAllotments)

    ## Processes the allotments and transform the raw data into allotment objects
    def processAllotments(self, allotmentsRawData):
        
        proccessedAllotments = []
        for x in range(0, self.AMOUNT_OF_SCRAPED_ADDS):
            proccessedAllotments.append(allotment(allotmentsRawData, x)) 
        return proccessedAllotments

    ## Write the proccesed allotments out into kts.txt 
    def writeToFile(self, proccessedAllotments):

        ktsTxt = codecs.open('/Users/whateverisforever/Desktop/All/Coding/MyScripts/KolonihaveScrape/KolonihaveScrape/spiders/kts.txt', 'r+', 'utf-8')
        ktsTxt.truncate()

        for x in range(0, self.AMOUNT_OF_SCRAPED_ADDS):

            cityName = proccessedAllotments[x].getCityName()
            price = proccessedAllotments[x].getPrice()
            sqMtr = proccessedAllotments[x].getsqMtr()
            date = proccessedAllotments[x].getDate()
            relativeUrl = proccessedAllotments[x].getRelativeUrl()

            ktsTxt.write(cityName + ',' + price + ',' + sqMtr + ',' + date + ',' + relativeUrl + '\n')
