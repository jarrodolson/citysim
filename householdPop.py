import os
from random import random
import math

def initializeHouses(allSubAreaStatsDic,priceDic):
    houseLiLi = []
    count = 0
    for area in allSubAreaStatsDic:
        areaDic = allSubAreaStatsDic[area]
        count2 = 0
        while count2 < areaDic["households"]:
            ##print "Creating household"
            tempLi = []
            address = str(count)
            location = area
            housetype = findHT(areaDic["houseTypes"])
            rentable = findRentable(housetype)
            nBR = findBR(areaDic["perBeds"][housetype])
            forSale = findForSale(rentable)
            forRent = findForRent(areaDic["vacancyRate"],rentable)
            rentPrice = findRentPrice(housetype,rentable,nBR,forRent,priceDic)
            salePrice = findSalePrice(housetype,rentable,nBR)
            tempLi = [address,location,housetype,rentable,nBR,forSale,
                      forRent,rentPrice,salePrice]
            houseLiLi.append(tempLi)
            ##print tempLi
            count = count+1
            count2 = count2+1
    return houseLiLi

def findRentPrice(housetype,rentable,nBR,forRent,priceDic):
    if rentable == 1:
        housetypeLi = ["A","TH","H"]
        key = str(nBR)+"BR"+str(housetypeLi[housetype-1])
        avgPrice = priceDic[1]["RentAvgPrice"][key]
        stDev = priceDic[1]["RentStDev"][key]
        neg = False
        if random()>.5:
            neg = True
        if neg == True:
            price = avgPrice - ((2*stDev)*random())
        if neg == False:
            price = avgPrice + ((2*stDev)*random())
    if rentable != 1:
        price = 0
    ##print avgPrice
    ##print price
    return price

def findConfidenceIntervals (prediction, sef, tCritical):
    CIUp = prediction+(sef*tCritical)
    CILo = prediction-(sef*tCritical)
    return CIUp, CILo

def findPriceAll(price, sef, tCritical):
    CIUp, CILo = findConfidenceIntervals(price, sef, tCritical)
    CIDiff = CIUp-CILo
    normalizedRand = random()*CIDiff
    price = CILo + normalizedRand
    return price

def findSalePrice(housetype,rentable,nBR):
    ## Coefficients
    constant = 203691.5
    cost2BR = 37066.48
    cost3BR = 72322.56
    cost4BR = 138563.4
    cost5BR = 173751.9
    ##For CI
    tCritical = 1.9601672
    sef1 = 93795.93
    sef2 = 93415.57
    sef3 = 93390.31
    sef4 = 93402.06
    sef5 = 93465.52
    if rentable==0:
        price = constant
        if nBR==1:
            price = findPriceAll(price, sef1, tCritical)
        if nBR==2:
            price = price+cost2BR
            price = findPriceAll(price, sef2, tCritical)
        if nBR==3:
            price = price+cost3BR
            price = findPriceAll(price, sef3, tCritical)
        if nBR==4:
            price = price+cost4BR
            price = findPriceAll(price, sef4, tCritical)
        if nBR==5:
            price = price+cost5BR
            price = findPriceAll(price, sef5, tCritical)
    if rentable==1:
        price = 0
    return price

def findRentable(housetype):
    if housetype == 1:##Apartments are rentable, but not neccesarily for rent
        indic = 1
    if housetype == 2:
        indic = 0
        if random()>=.6059:##From SOC519 data
            indic=1
    if housetype == 3:
        indic=0
        if random()>=.3125:##From SOC519 data
            indic=1
    return indic

def findBR(perBedLi):
    brRand = random()
    ##print brRand,perBedLi
    if brRand<=perBedLi[0]:
        br = 1
    if brRand>=perBedLi[0]:
        br = 2
    if brRand>=perBedLi[0]+perBedLi[1]:
        br = 3
    if brRand>=perBedLi[0]+perBedLi[1]+perBedLi[2]:
        br = 4
    if brRand>=perBedLi[0]+perBedLi[1]+perBedLi[2]+perBedLi[3]:
        br = 5
    ##print br
    return br

def findHT(htLi):
    htRand = random()
    if htRand<=htLi[0]:
        ht = 1##1=Apartment
    if htRand>=htLi[0]:
        ht = 2##2=Townhouse
    if htRand>=htLi[0]+htLi[1]:
        ht = 3##3 = Apartment
    return ht

def findForSale(rentable): ## Note: On 6/8 Zillow reports 373 for sale units, PropClass 101 in GIS assessors_2 there are 8668 houses that are sellable
    ## 373/8668 = 4.3%
    indic = 1##For sale
    if rentable==1:
        indic = 2##Rental
    if rentable!=1:
        indic = 1
    return indic

def findForRent(vacancyRate,rentable):
    indic = 1##Not available... although, that means they won't be available ever
    if rentable==1:##Rentable
        indic = 1
    if rentable==0:
        ##print "Not for rent... sales only!!"
        indic = 2##Owned, not for rent
    return indic

def writeData(houseLiLi):
    fout = open(".\\Development\\TEST2_StartHouses.txt","w")
    fout.write("Address\tLocation\tHousetype\tRentable\tnBR\tforSale\tforRent\trentPrice\tsalePrice\t\n")
    for row in houseLiLi:
        for col in row:
            fout.write(str(col)+"\t")
        fout.write("\n")
    fout.close()

####################################################
allSubAreaStatsDic = {1:{"population":52000,
                         "PerWhite":0.827,
                         "AvgAge":[.29,.18,.12,.12,.11,.09,.09],
                         "households":21000,
                         "avgIncome":{0:[.24,.23,.18,.14,.21],1:[.72,.16,.06,.05,.01]},
                         "perBeds":{0:[0,0,0,0,0],1:[.23,.65,.06,.06,0],2:[0,.15,.7,.15,0],3:[.01,.2,.43,.21,.15]},
                         "houseTypes":[0.25,.06,.69],
                         "perMarried":0.30,
                         "perStudents":[0.76,.17,.04,.02,.01],
                         "avgFamSize":3,
                         "areaUnemployment":0.08,
                         "vacancyRate":0.027}}
priceDic = {1:{"RentAvgPrice":{"1BRH":475,"2BRH":830.91,"3BRH":1121.05,"4BRH":1529.44,"5BRH":1973.125,"6BRH":0,
                               "1BRA":575,"2BRA":747.63,"3BRA":1207.5,"4BRA":1800,
                               "1BRTH":550,"2BRTH":1050,"3BRTH":1237.5,"4BRTH":1900,"5BRTH":0,"6BRTH":0},
               "RentStDev":{"1BRH":100,"2BRH":223.58,"3BRH":174.23,"4BRH":329.23,"5BRH":515.19,"6BRH":0,
                            "1BRA":83.1,"2BRA":160.61,"3BRA":152.03,"4BRA":200,
                            "1BRTH":100,"2BRTH":100,"3BRTH":83.29,"4BRTH":100,"5BRTH":0,"6BRTH":0},
               "SaleAvgPrice":{"1BRH":0,"2BRH":0,"3BRH":0,"4BRH":0,"5BRH":0,"6BRH":0,
                               "1BRA":0,"2BRA":0,"3BRA":0,"4BRA":0,
                               "1BRTH":0,"2BRTH":0,"3BRTH":0,"4BRTH":0,"5BRTH":0,"6BRTH":0},
               "SaleStDev":{"1BRH":0,"2BRH":0,"3BRH":0,"4BRH":0,"5BRH":0,"6BRH":0,
                            "1BRA":0,"2BRA":0,"3BRA":0,"4BRA":0,
                            "1BRTH":0,"2BRTH":0,"3BRTH":0,"4BRTH":0,"5BRTH":0,"6BRTH":0}}}
houseLiLi = initializeHouses(allSubAreaStatsDic,priceDic)
writeData(houseLiLi)
