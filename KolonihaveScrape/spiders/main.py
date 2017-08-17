
# -*- coding: utf-8 -*-

import sys 
from cityToZip import *
from sendSms import *

class main():

    def main():
        test = cityToZip()
        test.readZipCodesAndCitiesIntoHashMap()
        test.readScrapedZipCodesFromTxt()
        test.changeCitiesToZipCodes()
        test.writeNewZipCodesToTxt()
        # test2 = sendSms()
        # test2.readFromKtsAndDbaTxt()
        # test2.readInLastOneSendKtsAndDba()
        # test2.checkIfAllotmentIsOfInteresetKts()
        # test2.checkIfAllotmentIsOfInteresetDba()

    if __name__ == '__main__':
        main()