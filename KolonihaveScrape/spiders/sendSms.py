# -*- coding: utf-8 -*-
import csv
import codecs 
import time 
import smtplib
from sinchsms import SinchSMS
from allotment import *

class sendSms():

    def __init__(self, ):
        self.ktsTxtAsList = []
        self.dbaTxtAsList = []
        self.lastOneSendKts = ""
        self.lastOneSendDba = ""
        self.number = '+4531317204'
        self.client = SinchSMS('5b6dfa69-ac9b-4471-b7b7-7d870b9c3bd3', 'J5CweFNRh0KZlB0OY5+nAw==')
        self.server = smtplib.SMTP('smtp.gmail.com', 587)    

    ## Reads in kts.txt and dba.txt
    def readFromKtsAndDbaTxt(self, ):
        with open('/Users/whateverisforever/Desktop/All/Coding/MyScripts/KolonihaveScrape/KolonihaveScrape/spiders/kts.txt', 'r') as csvFile:
            rowReader = csv.reader(csvFile, delimiter=',', quotechar='\n')
            for row in rowReader:
                for x in row:
                    self.ktsTxtAsList.append(x)

        with open('/Users/whateverisforever/Desktop/All/Coding/MyScripts/KolonihaveScrape/KolonihaveScrape/spiders/dba.txt', 'r') as csvFile:
            rowReader = csv.reader(csvFile, delimiter=',', quotechar='\n')
            for row in rowReader:
                for x in row:
                    self.dbaTxtAsList.append(x)

    ## Reads in lastOneSendKts.txt and lastOneSendDba.txt
    def readInLastOneSendKtsAndDba(self, ):
        with open('/Users/whateverisforever/Desktop/All/Coding/MyScripts/KolonihaveScrape/KolonihaveScrape/spiders/lastOneSendKts.txt', 'r') as csvFile:
            rowReader = csv.reader(csvFile, delimiter=',', quotechar='\n')
            for row in rowReader:
                self.lastOneSendKts = row[0]

        with open('/Users/whateverisforever/Desktop/All/Coding/MyScripts/KolonihaveScrape/KolonihaveScrape/spiders/lastOneSendDba.txt', 'r') as csvFile:
            rowReader = csv.reader(csvFile, delimiter=',', quotechar='\n')
            for row in rowReader:
                self.lastOneSendDba = row[0]

    ## Checks both self.ktsTxtAsList and self.dbaTxtAsList
    def checkIfAllotmentIsOfInteresetKts(self, ):

# How it looks in kts.txt / dba.txt
# ['2750', '43.000', '20', 'I dag', 'http://www.dba.dk/flot-lysthave-tilhoerende/id-1035127733/']

        if (len(self.ktsTxtAsList) > 0) and (self.lastOneSendKts != self.ktsTxtAsList[4]):
            if (float(self.ktsTxtAsList[1]) < 700.0) and (int(self.ktsTxtAsList[2]) > 35) and (self.ktsTxtAsList[3] == 'I dag'):

                ## Sends sms 
                message = 'You got mail from kts!'
                self.sendSmsAfterConfirmation(message)

                ## Sends email
                emailMsg = self.ktsTxtAsList[0] + ' , ' + self.ktsTxtAsList[1] + ' , ' + self.ktsTxtAsList[2] + ' , ' + self.ktsTxtAsList[3] + ' , ' + self.ktsTxtAsList[4]
                self.sendEmailAfterConfirmation(emailMsg)

                ## Write to lastOneSendKts
                self.lastOneSendKts = codecs.open('/Users/whateverisforever/Desktop/All/Coding/MyScripts/KolonihaveScrape/KolonihaveScrape/spiders/lastOneSendKts.txt', 'r+', 'utf-8')
                self.lastOneSendKts.truncate()
                self.lastOneSendKts.write(self.ktsTxtAsList[4])

    def checkIfAllotmentIsOfInteresetDba(self, ): 

        if (len(self.dbaTxtAsList) > 0) and (self.lastOneSendDba != self.dbaTxtAsList[4]):
            if (float(self.dbaTxtAsList[1]) < 700.0) and (int(self.dbaTxtAsList[2]) > 35) and (self.dbaTxtAsList[3] == 'I dag'):

                ## Sends sms
                message = 'You got mail from dba!' 
                self.sendSmsAfterConfirmation(message)

                ## Sends email
                emailMsg = self.dbaTxtAsList[0] + ' , ' + self.dbaTxtAsList[1] + ' , ' + self.dbaTxtAsList[2] + ' , ' + self.dbaTxtAsList[3] + ' , ' + self.ktsTxtAsList[4]
                self.sendEmailAfterConfirmation(emailMsg)

                ## Write to lastOneSendKts
                self.lastOneSendDba = codecs.open('/Users/whateverisforever/Desktop/All/Coding/MyScripts/KolonihaveScrape/KolonihaveScrape/spiders/lastOneSendDba.txt', 'r+', 'utf-8')
                self.lastOneSendDba.truncate()
                self.lastOneSendDba.write(self.dbaTxtAsList[4])

    ## Sends the sms
    def sendSmsAfterConfirmation(self, txtMsg):

        response = self.client.send_message(self.number, txtMsg)
        message_id = response['messageId']
        response = self.client.check_status(message_id)

        while response['status'] != 'Successful':
            print(response['status'])
            time.sleep(1)
            response = self.client.check_status(message_id)
            print(response['status'])

    ## Sends the email
    def sendEmailAfterConfirmation(self, emailMsg):   

        self.server.starttls()  
        self.server.login('kolonihavescrap@gmail.com', 'Madsha171131') 
        self.server.sendmail('kolonihavescrap@gmail.com', 'madsgarff@hotmail.com', emailMsg)
