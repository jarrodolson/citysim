########################################################################
## Population synthesizer for Corvallis in Housing Forecast Model
## By: Jarrod Olson for Soc 519, Edwards Group, Spr 2012
##      at Oregon State University
########################################################################

from random import random
import os
import math

def initializeHouseLi(houseFi):
    houseLi = []
    houseDic = {}
    fi = open(houseFi)
    fiObj = fi.read()
    fi.close()
    fiObjLi = fiObj.split("\n")
    rowCount = 0
    for row in fiObjLi:
        rowLi = row.split("\t")
        if len(rowLi)>2 & rowCount>0:
            houseLi.append(rowLi)
            houseDic[str(rowLi[0])]=rowLi
            ##print rowLi[0]
        rowCount = rowCount+1
    return houseLi,houseDic

def createHousehold(subAreaStatsDic,householdID,householdDic):
    ##list: Name, Age, Married(0=No,1=Yes,2=Widowed), kidAgeList, StudentD,
    ##          Income, housetype(0:homeless,1:apt,2:th,3:house),nRoomsHouse
        ##      jobVariable (0:Unemployed,1=Employed,2=Retired)
    householdLi = [householdID]
    householdLi.append(findAge(subAreaStatsDic["AvgAge"]))
    householdLi.append(findMarriage(subAreaStatsDic["perMarried"]))
    householdLi.append(findKids(subAreaStatsDic["avgFamSize"]))
    student = []
    prStud = random()
    if prStud>.2937:##Probability of not being a household w/ students (survey data)
        student = []
    if prStud<=.2937:##Probability of being a household w/ students (survey data)
        nStudent = int(random()*4)##NOTE: Assumes a linear pr(choosing 1:4 roommates)
        while len(student)<=nStudent:
            student = findStudent(subAreaStatsDic["perStudents"],householdLi[1],student)
    householdLi.append(student)
    if len(student)>2:
        householdLi[2]=0
        householdLi[3]=[]
    householdLi.append(findIncome(subAreaStatsDic["avgIncome"],householdLi[4],householdLi[2]))
    householdLi.append(findHousetype(subAreaStatsDic["perBeds"],subAreaStatsDic["houseTypes"]))
    householdLi.append(findRooms(householdLi[6],subAreaStatsDic["perBeds"]))
    ##householdLi.append(findHousetype(subAreaStatsDic["perBeds"],subAreaStatsDic["houseTypes"])[1])
    if householdLi[1]>65:
        householdLi.append(2)##Retired
    if householdLi[1]<=65:
        householdLi.append(findJob(subAreaStatsDic["areaUnemployment"]))
    householdLi.append(findEth(subAreaStatsDic["PerWhite"]))
    #########################################
    ##TEMPORARY TO CHECK STUDENT LIST DISTRO
    ##householdLi.append(len(student))
    #########################################
    address = findHousing(householdLi,householdDic)
    householdLi.append(address)
    if address!="999999999":
        ##print householdDic[address]
        del householdDic[address]
        ##print"Found"

    ##print householdLi
    return householdLi,householdDic

def findEth(avgEth):
    eth = 0##0=White
    if random()>avgEth:
        eth=1##1=NotWhite
    return eth

def findAge(avgAge):
    ##AvgAge = 18-25,26-35,36-45,46-55,56-65,66-75,75+
    ageGroupRand = random()
    ageDifRand = random()
    if ageGroupRand<=avgAge[0]:
        difTopBot = 26-18
        age = int(ageDifRand*difTopBot)+18
        return age
    if ageGroupRand<=avgAge[1]+avgAge[0]:
        difTopBot = 36-26
        age = int(ageDifRand*difTopBot)+26
        return age
    if ageGroupRand<=avgAge[2]+avgAge[0]+avgAge[1]:
        difTopBot = 46-36
        age = int(ageDifRand*difTopBot)+36
        return age
    if ageGroupRand<=avgAge[3]+avgAge[0]+avgAge[1]+avgAge[2]:
        difTopBot = 56-46
        age = int(ageDifRand*difTopBot)+46
        return age
    if ageGroupRand<=avgAge[4]+avgAge[0]+avgAge[1]+avgAge[2]+avgAge[3]:
        difTopBot = 66-56
        age = int(ageDifRand*difTopBot)+56
        return age
    if ageGroupRand<=avgAge[5]+avgAge[0]+avgAge[1]+avgAge[2]+avgAge[3]+avgAge[4]:
        difTopBot = 76-66
        age = int(ageDifRand*difTopBot)+66
        return age
    if ageGroupRand<=avgAge[6]+avgAge[0]+avgAge[1]+avgAge[2]+avgAge[3]+avgAge[4]+avgAge[5]:
        difTopBot = 91-76
        age = int(ageDifRand*difTopBot)+76
        return age

def findMarriage(percentMarried):
    marriedDraw = random()
    married = 0
    if marriedDraw<=percentMarried:
        married = 1
    return married

def findKids(avgFamilySize):
    nKids = int(random()*5)##Note: Needs to be fixed for actual distribution
    kidLi = []
    if nKids>0:
        countKids = 0
        while countKids<nKids:
            kidLi.append(int(random()*18))
            countKids = countKids+1
    return kidLi

def findStudent(avgStudentsLi,age,student):
    ##perBeds = percent given age: 0=18-25, 1=26-35, 2=36-45,3=46-55,4=55+
    ##student = 0
    moreStudent = True
    studentRand = random()
    if age<=25 and studentRand<=avgStudentsLi[0]:
        student.append(int(random()*5))
        return student
    if age<=35 and studentRand<=avgStudentsLi[1]:
        student.append(int(random()*5))
        return student
    if age<=45 and studentRand<=avgStudentsLi[2]:
        student.append(int(random()*5))
        return student
    if age<=55 and studentRand<=avgStudentsLi[3]:
        student.append(int(random()*5))
        return student
    if age>55 and studentRand<=avgStudentsLi[4]:
        student.append(int(random()*5))
        return student
    return student

##def findIncome(avgIncomeLi,student):##From surveys
##    ##avgIncome = percent within income bracket by student (two lists)
##    ##  = 0:0-25,1:26-45,2:56-60,3:61-80,4:81+
##    if student>0:
##        student = 1
##    incomeRand = random()
##    if incomeRand <= avgIncomeLi[student][0]:
##        rangeDif = 25-0
##        income = int((incomeRand*rangeDif)*1000)
##        ##income = 0
##        return income
##    if incomeRand <= avgIncomeLi[student][1]+avgIncomeLi[student][0]:
##        rangeDif = 56-25
##        income = int((incomeRand*rangeDif)*1000)
##        ##income = 1
##        return income
##    if incomeRand <= avgIncomeLi[student][2]+avgIncomeLi[student][0]+avgIncomeLi[student][1]:
##        rangeDif = 61-56
##        income = int((incomeRand*rangeDif)*1000)
##        ##income = 2
##        return income
##    if incomeRand <= avgIncomeLi[student][3]+avgIncomeLi[student][0]+avgIncomeLi[student][1]+avgIncomeLi[student][2]:
##        rangeDif = 81-61
##        income = int((incomeRand*rangeDif)*1000)
##        ##income = 3
##        return income
##    if incomeRand <= avgIncomeLi[student][4]+avgIncomeLi[student][0]+avgIncomeLi[student][1]+avgIncomeLi[student][2]+avgIncomeLi[student][3]:
##        rangeDif = 201-81
##        income = int((incomeRand*rangeDif)*1000)
##        ##income = 4
##        return income

def findIncome(avgIncomeLi,student,married):##From census - http://factfinder2.census.gov/faces/tableservices/jsf/pages/productview.xhtml?src=bkmk
    avgIncomeLi = [.161,.056,.151,.113,.119,.141,.1,.101,.029,.03]
    ## NOTE: Does not assume students have a diff income distro
    married = married+1
    nStudents = len(student)
    nStudents = nStudents+1
    incomeRand = random()
    if incomeRand<=.161:
        rangeDif = 9.9-0
        incomeRand = random()
        income = int((incomeRand*rangeDif)*1000)
        income = income*married
        income = income*nStudents
        return income
    if incomeRand<=.217:
        rangeDif = 14.9-10
        incomeRand = random()
        income = int(((incomeRand*rangeDif)+10)*1000)
        income = income*married
        income = income*nStudents
        return income
    if incomeRand<=.368:
        rangeDif = 24.9-15
        incomeRand = random()
        income = int(((incomeRand*rangeDif)+15)*1000)
        income = income*married
        income = income*nStudents
        return income
    if incomeRand<=.481:
        rangeDif = 34.9-25
        incomeRand = random()
        income = int(((incomeRand*rangeDif)+25)*1000)
        income = income*married
        income = income*nStudents
        return income
    if incomeRand<=.6:
        rangeDif = 49.9-35
        incomeRand = random()
        income = int(((incomeRand*rangeDif)+35)*1000)
        income = income*married
        income = income*nStudents
        return income
    if incomeRand<=.741:
        rangeDif = 74.9-50
        incomeRand = random()
        income = int(((incomeRand*rangeDif)+50)*1000)
        income = income*married
        income = income*nStudents
        return income
    if incomeRand<=.841:
        rangeDif = 99.9-75
        incomeRand = random()
        income = int(((incomeRand*rangeDif)+75)*1000)
        income = income*married
        income = income*nStudents
        return income
    if incomeRand<=.942:
        rangeDif = 149.9-100
        incomeRand = random()
        income = int(((incomeRand*rangeDif)+100)*1000)
        income = income*married
        income = income*nStudents
        return income
    if incomeRand<=.971:
        rangeDif = 199.9-150
        incomeRand = random()
        income = int(((incomeRand*rangeDif)+150)*1000)
        income = income*married
        income = income*nStudents
        return income
    if incomeRand>.971:
        rangeDif = 300-200
        incomeRand = random()
        income = int(((incomeRand*rangeDif)+200)*1000)
        income = income*married
        income = income*nStudents
        return income

def findHousetype(perBedLi,perHouseLi):
    ##0 = homeless, 1=apt, 2=th, 3=house
    ##perHousesLi = 0=apt, 1=th, 2=house
    houseType = 0
##    typeRand = random()
##    if typeRand<=perHouseLi[0]:
##        houseType = 1
##        ##nRooms = findRooms(houseType,perHouseLi)
##        return houseType
##    if typeRand<=perHouseLi[1]+perHouseLi[0]:
##        houseType = 2
##        ##nRooms = findRooms(houseType,perHouseLi)
##        return houseType
##    if typeRand<=perHouseLi[2]+perHouseLi[0]+perHouseLi[1]:
##        houseType = 3
##        ##nRooms = findRooms(houseType,perBedLi)
##        return houseType

def findRooms(houseType,perBedLi):
    ##print perBedLi
##    roomsRand = random()
##    nRooms = 1
##    if roomsRand<=perBedLi[houseType][0]:
##        return nRooms
##    if roomsRand<=perBedLi[houseType][1]+perBedLi[houseType][0]:
##        nRooms = 2
##        return nRooms
##    if roomsRand<=perBedLi[houseType][2]+perBedLi[houseType][0]+perBedLi[houseType][1]:
##        nRooms=3
##        return nRooms
##    if roomsRand<=perBedLi[houseType][3]+perBedLi[houseType][0]+perBedLi[houseType][1]+perBedLi[houseType][2]:
##        nRooms=4
##        return nRooms
##    if roomsRand<=perBedLi[houseType][4]+perBedLi[houseType][0]+perBedLi[houseType][1]+perBedLi[houseType][2]+perBedLi[houseType][3]:
##        nRooms = 5
##        return nRooms
    return 0

def findJob(areaUnemployment):
    jobCode = 0
    if random()>areaUnemployment:
        jobCode = 1
    return jobCode

def writeData(fiName,cityHouseholdsByAreaDic):
    fout = open(fiName,"w")
    fout.write("Area\tName\tAge\tMarriageStatus\tkidsAges\tStudentD\tIncome\tHousetype\tnRooms\tJobType\tEthnicity\tAddress\t\n")
    for subArea in cityHouseholdsByAreaDic:
        list1 = cityHouseholdsByAreaDic[subArea]
        for el in list1:
            fout.write(str(subArea)+"\t")
            for item in el:
                fout.write(str(item)+"\t")
            fout.write("\n")
    fout.close()

def countHHAdults(popLi):
    if popLi[2]==1:##Married
        if len(popLi[4])>1:
            nAdults = len(popLi[4])##All students
        if len(popLi[4])<=1:
            nAdults = 1+len(popLi[4])##One student is head of household
    if popLi[2]!=1:##Not married
        if len(popLi[4])>1:
            nAdults = len(popLi[4])
        if len(popLi[4])<=1:
            nAdults = 1+len(popLi[4])
    return nAdults

def createNew(allSubAreaStatsDic,subAreaLi,householdDic):
    cityHouseholdsByAreaDic = {}
    householdID = 0
    for subArea in subAreaLi:
        countInArea = 0
        tempCount = 0
        areaHouseholds = []
        while countInArea <= allSubAreaStatsDic[subArea]["population"]:
            if countInArea/1000 > tempCount:
                print countInArea," Ppl Created"
                tempCount = countInArea/1000
            householdLi, householdDic = createHousehold(allSubAreaStatsDic[subArea],householdID,householdDic)
            areaHouseholds.append(householdLi)
            ##print householdLi
            nAdults = countHHAdults(householdLi)
            nPpl = nAdults+len(householdLi[3])
            householdID = householdID+1
            countInArea = countInArea+nPpl
            del nPpl
        cityHouseholdsByAreaDic[subArea]=areaHouseholds
    return cityHouseholdsByAreaDic

def findHousing(popLi,houseDic):
    address = 999999999## This is the base address, equals "homeless"
    prefLi = findPreferences (popLi)
    income = popLi[5]
    maxRent = popLi[5]/12
    prefLi = findPreferences (popLi)
    buy = False
    if random()<=.5:
        buy=True##50% chance of looking to buy
    saveLi = utilityMaximize(houseDic,prefLi,buy,maxRent,popLi)
    if len(saveLi)!=0:
        address = str(saveLi[0])
        ##print address
    if len(saveLi)==0:
        address = str(999999999)
        ##print "Not found!!"
    return address

def findPreferences (popLi):
    student = 0
    if len(popLi[4])>0:
        student = 1
    age = popLi[2]
    adult = 1
    if popLi[2]==1:
        adult = int(2)
    if len(popLi[4])>0:
        adult = int(adult)+int(len(popLi[4]))
    minors = len(popLi[3])
    ethnicity = popLi[9]
    prefLi = []
    aptModel = 4.800859+(float(student)*.4803235)+(float(age)*-.0328646)+(float(adult)*-1.29605)+(float(minors)*-.5347455)+(float(ethnicity)*-1.600257)
    aptModelProb = math.exp(aptModel)/(1+math.exp(aptModel))
    ##print aptModelProb
    prefLi.append(aptModelProb)
    HT1Model = 9.338695+(float(student)*1.87992)+(float(age)*-.0454925)+(float(adult)*-5.396276)+(float(minors)*-1.602293)+(float(ethnicity)*-1.971297)
    HT2Model = 3.682469+(float(student)*.093984)+(float(age)*-.0202579)+(float(adult)*-1.067024)+(float(minors)*-.3274551)+(float(ethnicity)*-1.251799)
    HT3Model = -1.401758+(float(student)*.5881097)+(float(age)*.0261023)+(float(adult)*.4577689)+(float(minors)*-.3331851)+(float(ethnicity)*-.6014236)
    HT4Model = -7.892151+(float(student)*-.11737)+(float(age)*.083249)+(float(adult)*1.815857)+(float(minors)*.3369356)+(float(ethnicity)*.4513584)
    ##print HT1Model
    HT1ModelProb = math.exp(HT1Model)/(1+math.exp(HT1Model))
    ##print HT1ModelProb
    prefLi.append(HT1ModelProb)
    HT2ModelProb = math.exp(HT2Model)/(1+math.exp(HT2Model))
    prefLi.append(HT2ModelProb)
    HT3ModelProb = math.exp(HT3Model)/(1+math.exp(HT3Model))
    prefLi.append(HT3ModelProb)
    HT4ModelProb = math.exp(HT4Model)/(1+math.exp(HT4Model))
    prefLi.append(HT4ModelProb)
    ##print prefLi
    return prefLi

def findWeights (prefLi,houseLi,refPrice):
    HTWeightValue = prefLi[0]
    ##print HTWeightValue
    if int(houseLi[2])==1:
        HTWeight = 1.0-float(HTWeightValue)
    if int(houseLi[2])==2 or int(houseLi[2])==3:
        HTWeight = float(HTWeightValue)
    ##print "\t",HTWeight
    BRWeightLocator = int(houseLi[2])
    BRWeightValue = prefLi[BRWeightLocator]
    BRWeight = 1.0-float(BRWeightValue)
    try:
        priceWeighted = ((float(houseLi[refPrice])*HTWeight)+(float(houseLi[refPrice])*BRWeight))/2.0##Weighted price is price weight of HT and price weight of BR count combined
    except UnboundLocalError:
        print prefLi
        print houseLi
        print refPrice
    return priceWeighted

def utilityMaximize (houseDic,prefLi,buy,maxRent,popLi):
    ##Weight by price by preference, so if I have an 8 percent chance of picking an apt,
    ##  then the price of the house will be discounted by 8%, so that it's more expensive than
    ##  the house option (discounted by 92%)
    ##print "Into UtilityMaximize"
    price2 = 1000000000000000000000000.0
    saveLi = []
    refPrice = 7
    searchPattern = 1##For rent
    found = False
    if buy == True:
        refPrice = 8
        searchPattern = 0
    while found==False and searchPattern<2:
        if searchPattern == 1:
            refPrice = 7## If couldn't find house to buy, look again for house to rent
        for house in houseDic:
            ##print "Into houseDic Loop"
            houseLi = houseDic[house]
            if float(houseLi[refPrice])>0:
                ##print houseLi[refPrice]
                if refPrice == 8:
                    priceWeighted = findWeights(prefLi,houseLi,refPrice)
                if refPrice == 7 and float(houseLi[refPrice])<=float(maxRent):
                    priceWeighted = findWeights(prefLi,houseLi,refPrice)
                    ##print priceWeighted
                if refPrice == 7 and float(houseLi[refPrice])>float(maxRent):
                    priceWeighted = 100000000000000000000000000000000.0##Don't even try
                if float(priceWeighted)<float(price2):
                    ##print "Property found: ", refPrice
                    ##print priceWeighted, price2
                    price2 = priceWeighted
                    saveLi = houseLi
        if len(saveLi)!=0:
            found=True
        if len(saveLi)==0:
            searchPattern = searchPattern + 1
    ##fout2 = open("CheckPreferences.txt","a")
    ##fout2.write(str(popLi[0])+"\t"+str(prefLi)+"\t"+str(HTWeight)+"\t"+str(BRWeight)+"\t"+str(priceWeighted)+"\t"+str(price2)+"\t"+str(len(houseDic))+"\t"+str(found)+"\t"+str(saveLi[refPrice])+"\t"+str(buy)+"\n")
    ##fout2.close()
    return saveLi

########################################################################3

##houseTypes = percentage of each house type: Apt, TH, House
##AvgAge = 18-25,26-35,36-45,46-55,56-65,66-75,75+
##perBeds = 1,2,3,4,5+
##perStudents = percent given age: 0=18-25, 1=26-35, 2=36-45,3=46-55,4=55+
##avgIncome = percent within income bracket by student/nonstudent (2 lists) = 0:0-25,1:26-45,2:56-60,3:61-80,4:81+

##cityHouseholdsByAreaDic = createNew()
##writeData("testPop2.txt",cityHouseholdsByAreaDic)
