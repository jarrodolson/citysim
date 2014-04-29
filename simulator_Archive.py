## DRAFT VERSION OF Willamette Neighborhood Housing Association Price
###############################################################################
## Housing Price Indicator Simulator
## By: Jarrod Olson for Soc 519, Edwards Group, Spr 2012
##     at Oregon State University
###############################################################################

import os
import math
from random import random
import time
import PopulationCreator as newPop

#############################
##Initialize
#############################

def findUnmatchedPpl(popDic):
    unmatchedPplLi = []
    for ppl in popDic:
        popLi = popDic[ppl]
        if int(popLi[11])==999999999:
            unmatchedPplLi.append(popLi[0])
    return unmatchedPplLi

def initializeHouseLi(houseFi):
    houseLi = []
    houseDic = {}
    fi = open(houseFi)
    fiObj = fi.read()
    fi.close()
    fiObjLi = fiObj.split("\n")
    ##print "Number of entries in house file: ",len(fiObjLi)
    rowCount = 0
    for row in fiObjLi:
        rowLi = row.split("\t")
        if len(rowLi)>1 and rowCount>0:
            houseLi.append(rowLi)
            try:
                houseDic[str(rowLi[0])]
                print "OVERWRITING!!!"
            except KeyError:
                houseDic[str(rowLi[0])]=rowLi
            ##print rowLi[0]
        rowCount = rowCount+1
    return houseLi,houseDic

def createNewHouseholds (popPath,allSubAreaStatsDic,subAreaLi,householdDic):

    ##houseTypes = percentage of each house type: Apt, TH, House
    ##AvgAge = 18-25,26-35,36-45,46-55,56-65,66-75,75+
    ##perBeds = 1,2,3,4,5+
    ##perStudents = percent given age: 0=18-25, 1=26-35, 2=36-45,3=46-55,4=55+
    ##avgIncome = percent within income bracket by student/nonstudent (2 lists) = 0:0-25,1:26-45,2:56-60,3:61-80,4:81+
    cityHouseholdsByAreaDic = newPop.createNew(allSubAreaStatsDic,subAreaLi,householdDic)
    ##print len(cityHouseholdsByAreadic)
    date = time.asctime()
    dateSave = date.replace(" ","-")
    dateSave = dateSave.replace(":","")
    dateSave = dateSave.replace(".","")
    newPop.writeData(popPath+"\\test_"+str(dateSave)+".txt",cityHouseholdsByAreaDic)

def initializeDeathRate(popDir):
    deathDic = {}
    data = open(popDir+"\\deathRate.txt")
    dataObj = data.read()
    data.close()
    dataObjLi = dataObj.split("\n")
    for age in dataObjLi:
        ageLi = age.split("\t")
        if len(ageLi)>1:
            deathDic[ageLi[0]]=float(ageLi[1])
    return deathDic

def initializeDevelop(developDic,developPath):
    return developDic

def createInitialHouseholdLiLi (popPath):
    householdLiLi = []
    print "Population: ",popPath
    data = open(popPath)
    dataObj = data.read()
    data.close()
    dataObjLi = dataObj.split("\n")
    print "Population Size of Households",len(dataObjLi)-1
    header = []
    for household in dataObjLi:
        householdLi = household.split("\t")
        householdLiLi.append(householdLi)
        ##print householdLi[11]
    return householdLiLi
    

def initializePop(popDic,popPath):
    unmatchedPplLi = []
    householdLiLi = createInitialHouseholdLiLi(popPath)
    householdCount = 0
    for householdLi in householdLiLi:
        if len(householdLi)>1:
            if householdCount==0:
                header = householdLi
                print header
            if householdCount!=0:
                area = householdLi[0]
                name = householdLi[1]
                age = int(householdLi[2])
                ##print age
                marriageStatus = householdLi[3]
                kidsAges = householdLi[4]
                kidsAges = kidsAges.replace("[","")
                kidsAges = kidsAges.replace("]","")
                kidsAges = kidsAges.replace("'","")
                kidsAges = kidsAges.replace(" ","")
                kidsAgesLi = kidsAges.split(",")
                ##print kidsAgesLi
                count1 = 0
                newKidsAgesLi = []
                if kidsAgesLi[count1]=="":
                    del kidsAgesLi[count1]
                for el in kidsAgesLi:
                    kidsAgesLi[count1]=int(kidsAgesLi[count1])
                    count1 = count1+1##This is what we want
                ##print kidsAgesLi
                studentD = householdLi[5]
                studentD = studentD.replace("[","")
                studentD = studentD.replace("]","")
                studentD = studentD.replace("'","")
                studentD = studentD.replace(" ","")
                studentD2 = studentD.split(",")
                studentD = []
                for el in studentD2:
                    try:
                        studentD.append(int(el))
                    except ValueError:
                        pass
                income = householdLi[6]
                housetype = householdLi[7]
                nRooms = householdLi[8]
                jobType = householdLi[9]
                ethnic = householdLi[10]
                address = householdLi[11]
                if int(address) == int(999999999):
                    ##print "homeless"
                    unmatchedPplLi.append(name)
                try:
                    popDic[name]
                    print "Duplicate input name", name
                except KeyError:
                    popDic[name]=[name,int(age),int(marriageStatus),kidsAgesLi,studentD,
                                  int(income),housetype,int(jobType),int(area),
                                  int(nRooms),int(ethnic),int(address)]
        householdCount = householdCount+1
    ##Incomeing: Area;Name;Age;MarriageStatus;kidsAges;StudentD;Income;
        ##      Housetype;nRooms;JobType
    ##Outgoing: Name, Age, Married(0=No,1=Yes,2=Widowed), kidAgeList, StudentD, Income, housetype(0:homeless,1:apt,2:th,3:house),
        ##      jobVariable (0:Unemployed,1=Employed,2=Retired),area,nRooms,ethnicity(0=white,1=minority)
    return popDic,unmatchedPplLi

def openScenario(scenPath,scenarioFiName):
    scenarioDic = {}
    data = open(scenPath+"\\"+scenarioFiName+".txt")
    dataObj = data.read()
    data.close()
    dataObjLi = dataObj.split("\n")
    count = 0
    for line in dataObjLi:
        lineLi = line.split("\t")
        if len(lineLi)>1 and count>0:
            tempStr = lineLi[1].replace("[","")
            tempStr = tempStr.replace("]","")
            dataLi = tempStr.split(",")
            if len(dataLi)>1:
                scenarioDic[lineLi[0]] = dataLi
            if len(dataLi)<=1:
                scenarioDic[lineLi[0]] = float(lineLi[1])
        count += 1
    return scenarioDic

def yearlyNewFamilies(nPeople,subAreaStatsDic,subAreaLi,year,availableUnitsDic,newTakenUnitsLi,houseDic,scenarioDic):
    ##list: Name, Age, Married(0=No,1=Yes,2=Widowed), kidAgeList, StudentD, Income, housetype(0:homeless,1:apt,2:th,3:house),
    ##      jobVariable (0:Unemployed,1=Employed,2=Retired),area,housetype,nRooms
    newFamLi = []
    countNames = 0
    count = 0
    countKids = 0
    while count<nPeople:
        area = 1##Should be random number giving us range among different areas
        areaDic = subAreaStatsDic[area]
        name = "newFam_"+str(year)+"_"+str(countNames)
        ##print name
        age = newPop.findAge(areaDic["AvgAge"])
        marriage = newPop.findMarriage(areaDic["perMarried"])
        if marriage == 0 or marriage == 2:
            count = count+1
        if marriage == 1:
            count = count+2
        kidLi = newPop.findKids(areaDic["avgFamSize"])
        nKids = len(kidLi)
        countKids += nKids
        count = count+nKids
        studentYr = []
        income = newPop.findIncome(areaDic["avgIncome"],studentYr,marriage)
        houseType = 0
        rooms = 0
        if age>65:
            jobCode = 2
        if age<=65:
            jobCode = newPop.findJob(areaDic["areaUnemployment"])
        ethnicity = newPop.findEth(areaDic["PerWhite"])
        popLi = [name,age,marriage,kidLi,studentYr,income,houseType,jobCode,area,rooms,ethnicity,999999999]##Starter
        moveIndic, popLi, availableUnitsDic, newTakenUnitsLi,unassigned,unassigned2 = moveOrNo(popLi, availableUnitsDic, houseDic, newTakenUnitsLi,[],{})##Find house (Not able to room)
        ##print "New household!"
        newFamLi.append(popLi)
        countNames += 1
    return newFamLi,count,availableUnitsDic,newTakenUnitsLi,count, countKids

def yearlyNewStudents(totalExpectStudGrowth,subAreaStatsDic,subAreaLi,year,availableUnitsDic,newTakenUnitsLi,houseDic,scenarioDic,newFamLi):
    ##list: Name, Age, Married(0=No,1=Yes,2=Widowed), kidAgeList, StudentD, Income, housetype(0:homeless,1:apt,2:th,3:house),
    ##      jobVariable (0:Unemployed,1=Employed,2=Retired),area,housetype,nRooms
    ##newFamLi = []
    count = 0
    while count<totalExpectStudGrowth:
        area = 1##Should be random number giving us range among different areas
        areaDic = subAreaStatsDic[area]
        name = "new_"+str(year)+"_"+str(count)
        age = 18
        marriage = 0
        if marriage == 0 or marriage == 2:
            count = count+1
        if marriage == 1:
            count = count+2
        kidLi = []
        nKids = len(kidLi)
        count = count+nKids
        studentYr = [1,1]
        count += len(studentYr)
        income = newPop.findIncome(areaDic["avgIncome"],studentYr,marriage)
        houseType = 0
        rooms = 0
        if age>65:
            jobCode = 2
        if age<=65:
            jobCode = newPop.findJob(areaDic["areaUnemployment"])
        ethnicity = newPop.findEth(areaDic["PerWhite"])
        popLi = [name,age,marriage,kidLi,studentYr,income,houseType,jobCode,area,rooms,ethnicity,999999998]
        ## Assumes that all new students live in dorms (999999998)
        ##moveIndic, popLi, availableUnitsDic, newTakenUnitsLi = moveOrNo(popLi, availableUnitsDic, houseDic, newTakenUnitsLi)
        ##print "New household!"
        newFamLi.append(popLi)
    return newFamLi,count,availableUnitsDic,newTakenUnitsLi,count

#########################################
## Decision making for developers
#########################################
def adjustPrices (houseDic,globalStatDic,availableUnitsDic):
    htLi = ["homeless","A","TH","H"]
    for house in availableUnitsDic:
        if house!="999999999" and house!="999999998":
            houseLi = houseDic[house]
            key = str(houseLi[4])+"BR"+str(htLi[int(houseLi[2])])
            avgPrice = globalStatDic["rentAvgPriceDic"][key]
            stDev = globalStatDic["rentStDev"][key]
            stDev_2 = 2*stDev
            neg = False
            if random()>.5:
                neg = True
            if neg == False:
                newPrice = avgPrice+(random()*stDev_2)
            if neg == True:
                newPrice = avgPrice+(random()*stDev_2)
            houseLi[7] = str(newPrice)
            houseDic[house]=houseLi
    return houseDic

def developOrNot(developLi):
    coinToss = random()
    if coinToss>.5:
        ##print "New Development"
        pass
    return developLi

def whatToMake(developLi):
    return developLi

def developSuccess(developLi):
    return developLi

def findRent(globalStatDic,ht,nBR):
    htLi = ["HOMELESS","A","TH","H"]
    rentPriceDic = globalStatDic["rentAvgPriceDic"]
    rentStDevDic = globalStatDic["rentStDev"]
    baselineRent = rentPriceDic[str(nBR)+"BR"+str(htLi[ht])]
    StDev = rentStDevDic[str(nBR)+"BR"+str(htLi[ht])]
    rand = random()
    premium = (rand*(2*StDev))
    rentPrice = baselineRent+premium
    ##print ht,":",nBR
    ##print baselineRent,"+(",StDev,"*",rand,")=",rentPrice
    return rentPrice

def scenarioDev(scenarioDic,year,globalStatDic):
    newHouseLi = []
    nNewHouses = scenarioDic["nNewHouses"]
    nNewApts = scenarioDic["nNewApts"]
    nNewTH = scenarioDic["nNewTH"]
    totalNewDev = nNewHouses+nNewApts+nNewTH
    countH = 0
    for houseC in nNewHouses:
        countMadeH = 0
        ##print houseC
        while countMadeH < int(houseC):
            addy = str(year)+"_"+str(countMadeH)
            location = 1
            ht = 3
            rentable = 1##Need to decide how this will work
            nBR = countH+1
            forSale = 0
            forRent = 1
            rentPrice = findRent(globalStatDic,ht,nBR)
            salePrice = 0
            newHouseLi.append([addy,location,ht,rentable,nBR,forSale,forRent,rentPrice,salePrice])
            countMadeH+=1
            ##print countMadeH
        countH += 1
    countA = 0
    for aptC in nNewApts:
        countMadeA = 0
        while countMadeA < int(aptC):
            addy = str(year)+"_"+str(countMadeA+countMadeH)
            location = 1
            ht = 1
            rentable = 1
            nBR = countA+1
            forSale = 0
            forRent = 1
            rentPrice = findRent(globalStatDic,ht,nBR)
            salePrice = 0
            newHouseLi.append([addy,location,ht,rentable,nBR,forSale,forRent,rentPrice,salePrice])
            countMadeA+=1
        countA+=1
    countTH = 0
    for THC in nNewTH:
        countMadeTH = 0
        while countMadeTH < int(THC):
            addy = str(year)+"_"+str(countMadeTH+countMadeA+countMadeH)
            location = 1
            ht = 2
            rentable = 1
            nBR = countTH+1
            forSale = 0
            forRent = 1
            rentPrice = findRent(globalStatDic,ht,nBR)
            salePrice = 0
            newHouseLi.append([addy,location,ht,rentable,nBR,forSale,forRent,rentPrice,salePrice])
            countMadeTH+=1
        countTH+=1
    return newHouseLi

#########################################
## Decision making for consumers
#########################################
def lifeChanges(popLi,popDic,marriageLi,popChangeLi,deathDic,choiceLi,houseDic):##Takes data from popLi, which has already been pulled out
    ##list: Name, Age, MarriedDummy, NKids, StudentD, Income
    ##PopChangeLi = 0:Birth,1:Death,2:Marriage,3:Immigrate,4:Emigrate,5:MoveOutHome-StayInTown
    ##                6:GradCol-StayInTown,7:GradCol-Emigrate,8:divorce,9:MoveOutHome-Emigrate
    masterLi = []
    hhSurvival = True
    partner = "None"
    ##################
    ## Age adults
    #################
    if survival(int(popLi[1]),deathDic)==True:## Lived: Age 1 year
        popLi[1]=popLi[1]+1
    if survival(int(popLi[1]),deathDic)==False:## Died
        if popLi[2]+len(popLi[4])==0:## If unmarried with no students, household is deleteted
            ##print "\nHousehold died",popLi
            nPeopleDead = 1+len(popLi[3])
            popChangeLi[1]=popChangeLi[1]+nPeopleDead
            choiceLi[14]=2
            hhSurvival = False
        if popLi[2]==0:##If married, just make household widowed
            popLi[2]=2
            popChangeLi[1]=popChangeLi[1]+1
            choiceLi[14]=1
            ##print "\nHead of household died",popLi
    ##################
    ## Age kids
    ##################
    countKids = 0
    nDeadKids = 0
    if hhSurvival==True:## If the household died off, do not run through this section
        ##print popLi
        while countKids<len(popLi[3]):## Loop through once for each child in household
            kid = popLi[3][countKids]
            survivalBool = survival(kid,deathDic)##Did the kid live?
            if survivalBool==True:## Kid lived
                kid = kid+1 ## Childs new age
                if kid<18:
                    popLi[3][countKids]=kid##Age each kid
                if kid>=18:
                    ##print popLi
                    ## If over 18, child moves out and makes choice (method "moveAt18")
                    popLi,popLi2,popChangeLi,toCollege = moveAt18(popLi,kid,countKids,popChangeLi)
                    choiceLi[16]=2
                    choiceLi[17] = choiceLi[17]+toCollege
                    ##print "Moved out",popLi2
                    if len(popLi2)>1:## If moved out, popLi2 is longer than 1
                        masterLi.append(popLi2)## Save to "new households list"
                        choiceLi[16]=1
                        del popLi2## to avoid overwrites/mis-writes, delete popLi2
            if survivalBool==False:## If the kid died...
                ##print "One of the kids died... bummer.", popLi
                popChangeLi[1]=popChangeLi[1]+1
                choiceLi[15]=choiceLi[15]+1
            countKids = countKids+1## For the while loop
    ##print hhSurvival,popLi[2]

    #######################
    ## Marriage (if household is unmarried)
    #######################


    ##If someone marries outside of corvallis... can they move out of corvallis (yes... fix it)
    if hhSurvival==True and popLi[2]==int(0):##Once widowed, you are out of luck
        marriageRand = random()
        ageMarriageProb = findMarriageProb(popLi)##Uses equation to find probability of marriage given age
        ##print ageMarriageProb
        choiceLi[18]=ageMarriageProb
        if marriageRand<=ageMarriageProb:##Made prob up... ***NEEDS CONFIRMING
            ## If random draw is within prob distribution, goes through marriage
            ## process method: "marriage"
            choiceLi[19]=1
            marImmigCount = popChangeLi[3]
            preNKids = len(popLi[3])
            popLi,partner,marriageLi,popChangeLi = marriage(popLi,popDic,marriageLi,popChangeLi,houseDic)
            if marImmigCount!=popChangeLi[3]:
                choiceLi[20]=1## Married Immigrant
            choiceLi[21]=popLi[0]## Married Name
            choiceLi[22]=len(popLi[3])-preNKids##Number new kids
            ##print "\n marriage:",partner
            ##print "We got married!!",popLi

    #############################
    ## Divorce (If household is married)
    #############################
    
    if hhSurvival and popLi[2]==int(1):
        ##print "Entered divorce if"
        probDivorce = .0036##http://www.nber.org/digest/nov07/w12944.html
        choiceLi[23]=probDivorce
        divorceRand = random()
        if divorceRand<=probDivorce:
            ## If the divorce random draw is under the probability distribution
            ## then they go through the divorce process method: "divorce"
            ##print "Divorce", popLi
            choiceLi[24]=1
            popChangeLi[8]=popChangeLi[8]+1
            popLi,popLi2 = divorce(popLi,popDic)
            choiceLi[25]=popLi[0]
            choiceLi[26]=popLi2[0]
            if len(popLi[3])==0:##If party 2 has the kids
                choiceLi[27]=2
            if len(popLi2[3])==0:##If party 1 has the kids
                choiceLi[27]=1
            if len(popLi2)>1:
                masterLi.append(popLi2)## New household added to "new households list"
                del popLi2## To avoid over-writes or other problems, deletes popLi2

    ##################################
    ## Having kids
    #################################

    if hhSurvival == True:
        popLi,popChangeLi,choiceLi = haveKidsOrNo(popLi,popChangeLi,choiceLi)


    #################################
    ## College graduation
    #################################
    countStudents = 0
    delLi = []
    while countStudents<len(popLi[4]):
        if hhSurvival==True and popLi[4][countStudents]>=int(1):
            if popLi[4][countStudents]>1:
                popLi[11]=999999999##If a second year is in the house, need to prepare for move
            popLi[4][countStudents]=int(popLi[4][countStudents])+1
            if popLi[4][countStudents]==5:## After 4 (5-1) years, graduates from college
                ##print "I graduated from college!", popLi
                popChangeLi[6]=popChangeLi[6]+1
                delLi.append(countStudents)
                popLi[4][countStudents]=0
                choiceLi[29]=1
                if stayInTown(popLi,popLi[1])==False:## If graduating, makes decision whether to stay in town or not
                    ##print "We're leaving town!!",popLi
                    choiceLi[30]=1
                    popChangeLi[6]=popChangeLi[6]-1
                    popChangeLi[7]= popChangeLi[7]+1
                    if (len(popLi[4])-len(delLi))<1:
                        hhSurvival=False## If decides not to stay in town, graduate household does not survive
        countStudents = countStudents+1
    count2 = 0
    for student in popLi[4]:
        if student==0:
            del popLi[4][count2]
        count2 = count2+1

    ################################
    ## Employment
    ################################

    if hhSurvival==True:
        ## If decides to stay in town, then finds (or doesn't find) a job/salary
        preJobCode = popLi[7]
        preIncome = popLi[5]
        popLi,popChangeLi,leaveAreaTest = jobDynamics(popLi,popChangeLi)
        if leaveAreaTest == True:
            hhSurvival = False
            popChangeLi[4]=popChangeLi[4]+1
        if preJobCode != popLi[7]:##If there was a change...
            if popLi[7]==2:##Retired
                choiceLi[31]=3
            if preJobCode==0 and popLi[7]==1:##Hired (didn't have, now has)
                choiceLi[31]=2
            if preJobCode==1 and popLi[7]==0:##Fired (had, no longer has)
                choiceLi[31]=1
        choiceLi[32]=popLi[5]-preIncome
        choiceLi[33]=popLi[5]
    return popLi, masterLi, hhSurvival,partner,marriageLi,popChangeLi,choiceLi

##############################
##Marriage Calls
#############################

def haveKidsOrNo(popLi,popChangeLi,choiceLi):
    ##http://www.cdc.gov/nchs/data/statab/t991x07.pdf
    ##NOTE: Need to also determine if they want a bigger family
    haveKid = False
    kidRand = random()
    age = popLi[1]
    if age>10 and age<=14 and kidRand<=0.0009:
        haveKid = True
    if age>14 and age<=17 and kidRand<=.0287:
        haveKid = True
    if age>17 and age<=19 and kidRand<=.0803:
        haveKid = True
    if age>19 and age<=24 and kidRand<=.111:
        haveKid = True
    if age>24 and age<=29 and kidRand<=.1178:
        haveKid = True
    if age>29 and age<=34 and kidRand<=.0896:
        haveKid = True
    if age>34 and age<=39 and kidRand<=.0383:
        haveKid = True
    if age>39 and age<=44 and kidRand<=.0074:
        haveKid = True
    if age>44 and age<=49 and kidRand<=.0004:
        haveKid = True
    if haveKid == True:
        popLi = haveKid2(popLi)
        popChangeLi[0]=popChangeLi[0]+1
        choiceLi[28]=choiceLi[28]+1
        ##print "We had hids!!",popLi
    return popLi, popChangeLi,choiceLi

def checkMarriages(popDic):
    bachelorLi = []
    for el in popDic:
        popLi = popDic[el]
        if popLi[2]>0:
            bachelorLi.append(popLi)
    return bachelorLi

def divorce(popLi,popDic):
    popLi[2]=0 ##Not married
    popLi[5]=popLi[5]/2##Income is split
    popLi2 = []
    count = 0
    for el in popLi:##Makes carbon copy of popLi (called popLi2)
        popLi2.append(el)
    popLi2[0]=str(popLi[0])+"_2"##New name for new divorcee
    if len(popLi[3])>=1:
        kidsRand = random()
        if kidsRand>=.5:##2 gets the kids, so 1 has none
            ##popLi2[3]=popLi[3]
            popLi[3]=[]
            ##print "2 gets the kids"
        if kidsRand < .5:##1 gets the kids, so 2 has none
            popLi2[3]=[]
            ##print "1 gets the kids"
    popLi2[11]=999999999
    return popLi,popLi2

def findMarriageProb(popLi):
    age = popLi[1]
    if age<=30:
        prob = .25
    if age>30:
        prob = .25-((age/200.0)**2.0)
    if prob < 0:
        prob = 0
    ##print prob
    return prob

def marriage (popLi,popDic,marriageLi,popChangeLi,houseDic):
    inHouseProb = .5
    ##PopChangeLi = 0:Birth,1:Death,2:Marriage,3:Marriage-Immigrate,4:Emigrate,5:MoveOutHome-StayInTown
    ##            6:GradCol-StayInTown,7:GradCol-Emigrate
    ##print "Marriage!!!!"
    popChangeLi[2]=popChangeLi[2]+1
    probEa = 0.0
    partner = "None"
    father1 = popLi[0][0].split("_")[0]
    ##print father
    if len(marriageLi)>0:
        randInOrOut = random()
        if randInOrOut<=inHouseProb and len(marriageLi)>0:##If less than value, marry in house
            ##print "marrying in house"
            choiceMade = False
            while choiceMade==False:
                choice = int(len(marriageLi)*random())
                ##print choice
                partnerLi = marriageLi[choice]
                ##print person2
                if partnerLi[0].split("_")[0]!=father1:
                    choiceMade = True
                    del marriageLi[choice]
            marriedName = str(popLi[0])+"_M_"+str(partnerLi[0])
            newLi = combineHH(popLi,partnerLi,marriedName)
            if houseDic[str(popLi[11])][2]> houseDic[str(partnerLi[11])][2]:
                address=str(popLi[11])
                area = houseDic[address][1]
            if houseDic[str(popLi[11])][2]<=houseDic[str(partnerLi[11])][2]:
                address=str(partnerLi[11])
                area = houseDic[address][1]
            del popLi
            popLi = newLi
        if randInOrOut>inHouseProb:
            popLi[2]=1
            partner = "New"
            popChangeLi[3]=popChangeLi[3]+1
    if len(marriageLi)==0:
        ##print "Length of marriage list is 0"
        popLi[2]=1
        partner = "New"
        popChangeLi[3]=popChangeLi[3]+1
    return popLi,partner,marriageLi,popChangeLi

def combineHH(popLi,partnerLi,name):
    newLi = []
    if int(popLi[1])>int(partnerLi[1]):
        marriedAge = popLi[1]
    if int(popLi[1])<=int(partnerLi[1]):
        marriedAge = partnerLi[1]
    married = 1
    kidLi = popLi[3]
    kidCount = 0
    kidsFromPartner = partnerLi[3]
    lengthKidLi2 = len(kidsFromPartner)
    try:
        for kid in kidsFromPartner:
            if kidCount>=lengthKidLi2:
                print popLi
                break
            kidLi.append(kid)
            kidCount = kidCount+1
    except MemoryError:
        print popLi
    student=[]
    if len(popLi[4])>0 or len(partnerLi[4])>1:
        student = popLi[4]
        for stud in partnerLi[4]:
            student.append(stud)
    income = popLi[5]+int(partnerLi[5])
    address = 999999999
    area = 0
    if popLi[7]>partnerLi[7]:
        jobCode = popLi[7]
    if popLi[7]<=partnerLi[7]:
        jobCode = partnerLi[7]
    ethnicity=popLi[10]
    if popLi[10]<=partnerLi[10]:
        ethnicity = partnerLi[10]
    newLi = []
    newLi.append(name)
    newLi.append(marriedAge)
    newLi.append(married)
    newLi.append(kidLi)
    newLi.append(student)
    newLi.append(income)
    newLi.append(0)
    newLi.append(jobCode)
    newLi.append(area)
    newLi.append(0)
    newLi.append(ethnicity)
    newLi.append(address)
    return newLi

##############################
## Job calls
##############################

def jobDynamics(popLi,popChangeLi):
    ##PopChangeLi = 0:Birth,1:Death,2:Marriage,3:Immigrate,4:Emigrate,5:MoveOutHome-StayInTown
    ##                6:GradCol-StayInTown,7:GradCol-Emigrate,8:divorce,9:MoveOutHome-Emigrate
    ##              10: Retired,11:JobsLost,12:JobsFound,13:newCollegeStudents,14:totalPay,15:totalRaises
    if popLi[1]>65:##If older than 65, forced retirement
        popLi[7]=2
        popChangeLi[10]=popChangeLi[10]+1
    if popLi[7]==2:##If retired, breaks from this module
        return popLi,popChangeLi,False
    if popLi[7]==1:
        keepJobRand = random()
        if keepJobRand>.98:
            ##print "we lost our job... bummer",popLi
            popChangeLi[11]=popChangeLi[11]
            popLi[7]=0
            if popLi[2]==1:
                popLi[5]=popLi[5]/2
            if popLi[2]==0:
                popLi[5]=0
        keepJobRand2 = random()
        if keepJobRand2<=.25:##Only top 25% of households get a raise
            ##print "We got a raise!",popLi
            wage = popLi[5]
            raiseWage = int(wage*((random()*25)/100))##Percent wage raise less than 25%
            ##raiseWage = int(raiseWageRand*1000)##Max raise should be 9999 dollars
            popChangeLi[15]=popChangeLi[15]+raiseWage
            if popLi[2]==1:
                popLi[5] = popLi[5]+raiseWage
    leaveAreaTest = False
    if popLi[7]==0:
        findJobRand = random()
        if findJobRand>.04:
            ##print "we found a job!! yay."
            popChangeLi[12]=popChangeLi[12]+1
            popLi[7]=1
            wageRand = random()
            wage = int(wageRand*100000)
            if popLi[2]==1:
                popLi[5]=popLi[5]+wage
            if popLi[2]==0:
                popLi[5]=wage
        if findJobRand<=.04:
            moveRand = random()
            if moveRand < .91: ##Employment rate US
                leaveAreaTest = True
    popChangeLi[14]=popChangeLi[14]+popLi[5]
    return popLi,popChangeLi,leaveAreaTest

##################################
## Miscellaneous Choices (haveKid,moveAt18,survival)
##################################

def haveKid2(popLi):
    popLi[3].append(0)
    return popLi
        
def moveAt18(popLi,kid,countKids,popChangeLi):
        ##Outgoing: Name, Age, Married(0=No,1=Yes,2=Widowed), kidAgeList, StudentD,
        ##      Income, housetype(0:homeless,1:apt,2:th,3:house),
        ##      jobVariable (0:Unemployed,1=Employed,2=Retired),area,nRooms
        
    intownTest = stayInTown(popLi,kid)
    toCollege = 0
    collegeRand = random()
    if collegeRand>=.5:
        toCollege = 1
    popChangeLi[9]=popChangeLi[9]+1
    if intownTest==True:
        popChangeLi[9]=popChangeLi[9]-1
        popChangeLi[5]=popChangeLi[5]+1
        popLi2 = [str(popLi[0])+"_kid_"+str(len(popLi[3])),kid,0,[],[],5000,0,0,0,0,popLi[10],999999999]##Needs to be adjusted for new population data
        ##print "Kid stayed in town",popLi2
        
        if toCollege==1:##Made up probability of going to college
            popLi2[4]=[1]
            popChangeLi[13]=popChangeLi[13]+1
            ##print "kid is going to college!"
    del popLi[3][countKids]
    try:
        popLi2
    except UnboundLocalError:
        popLi2=[]
    return popLi,popLi2,popChangeLi,toCollege

def survival(age,deathDic):
    ##NEED TO USE THIS: http://gravityandlevity.wordpress.com/2009/07/08/your-body-wasnt-built-to-last-a-lesson-from-human-mortality-rates/
    ##Also this: http://www.cdc.gov/nchs/data/nvsr/nvsr54/nvsr54_14.pdf
    surviveRand = random()
    deathRate = deathDic[str(age)]
    agePrDist = 1.0 ## If age is not found, then pr(death) = 100%
    try:
        agePrDist = 1-deathRate## Pr of surviving
        ##print agePrDist
    except ValueError:
        print "Error",age
    survivalQ = True
    if surviveRand>agePrDist:##If your draw is greater than the pr of surviving, you die
        survivalQ = False
        ##print "Died",age
    return survivalQ


###########################
## Location choices
###########################
def stayInTown(popLi,age):
    corvRand = random()
    intownTest = False
    if corvRand >= .4: ##Made up probability of continuing to live in Corvallis
        intownTest = True
    return intownTest

def whatToMoveInto(popLi, houseDic):
    maxRent = popLi[5]/12
    prefLi = newPop.findPreferences (popLi)
    buy = False
    if random()>.5:
        buy=True##50% chance of looking to buy
    saveLi = utilityMaximize(houseDic,prefLi,buy,maxRent)
    if len(saveLi)==0:
        pass
        ##print "Not found!!"
    if len(saveLi)!=1:
        address = saveLi[0]
        del houseDic[address]
        popLi.append(address)
    ##House or apartment
    return popLi, houseDic

def whereToMove(popLi):##Takes data from developDic, which has already been pulled out
    return popLi

def findProbRooming(popLi):
    prob = 1.0
    married = popLi[2]
    if int(married) == 2:
        prob = prob - 0.5
    nKids = len(popLi[3])
    if nKids > 0:
        prob = prob-.25
    return prob

def findRoomie(popLi,unmatchedPplLi,popDic):
    roomiePopLi = []
    roommateName = ""
    searcherProb = findProbRooming(popLi)
    counthh = 0
    for hh in unmatchedPplLi:
        try:
            tempPopLi = popDic[hh]
            foundProb = findProbRooming(tempPopLi)
            totalProb = (float(foundProb)+float(searcherProb))/2
            ##searcherRand = random()
            foundRand = random()
            ##if searcherRand<=searcherProb:
                ##print "searcherFind"
            if foundRand<=totalProb:
                roommateName = tempPopLi[0]
                name = str(popLi[0])+"_R_"+str(tempPopLi[0])
                roomiePopLi = combineHH(popLi,tempPopLi,name)
                del unmatchedPplLi[counthh]
                ##print "Match"##Follows same rules as marriage, with a different name
                break
        except KeyError:
            pass
        counthh +=1
    ##print roomiePopLi
    return roomiePopLi, roommateName

def moveOrNo(popLi,availableUnitsDic,houseDic,newTakenUnitsLi,unmatchedPplLi,popDic):
    roommateNameDel = ""
    ##print "numberAvailableUnits = ",len(availableUnitsDic)
    if int(houseDic[str(popLi[11])][3])==0: ## Not Renters
           return False, popLi, availableUnitsDic,newTakenUnitsLi,unmatchedPplLi,roommateNameDel
    maxRent = float(popLi[5]/12)## Income divided by 12
    moveOrNo = False
    currentHouseAddy = str(popLi[11])
    currentHousePrice = float(houseDic[currentHouseAddy][7])
    prefLi = newPop.findPreferences(popLi)
    if currentHousePrice>(maxRent) or str(popLi[11])=="999999999":
        ##If monthly rent is greater than monthly rent of income, have to move
        ##print "Need to move"
        ##print popLi
        ##print houseDic[currentHouseAddy]
        previousAddy = str(popLi[11])
        houseDic[previousAddy][6]=1
        availableUnitsDic[previousAddy]=houseDic[previousAddy]
        saveLi = newPop.utilityMaximize(availableUnitsDic,prefLi,False,maxRent,popLi)
        ##print saveLi
        if len(saveLi)!=0:
            ##print "Found new home"
            popLi[11]=saveLi[0]
            houseDic[previousAddy][6] = 1
            houseDic[str(popLi[11])][6] = 0
            availableUnitsDic[previousAddy]=houseDic[previousAddy]
            newTakenUnitsLi.append(str(saveLi[0]))
            del availableUnitsDic[str(saveLi[0])]
        if len(saveLi)==0:
            ##print "Did not find new home - searching for roomie"
            popLi[11]=999999999
            trys = 0
            roomiePopLi = []
            while trys<3:
                roomiePopLi, roommateName = findRoomie(popLi,unmatchedPplLi,popDic)
                if len(roomiePopLi)!=0:
                    ##print "Found ROOMIE!!"
                    newMaxRent = float(roomiePopLi[5]/12)## Income divided by 12
                    newPrefLi = newPop.findPreferences(roomiePopLi)
                    saveLi = newPop.utilityMaximize(availableUnitsDic,newPrefLi,False,newMaxRent,roomiePopLi)
                    if len(saveLi)!=0:
                        ##print "Found house with ROOMIE!!"
                        trys = 10
                        roomiePopLi[11]=saveLi[0]
                        houseDic[previousAddy][6] = 1
                        houseDic[str(roomiePopLi[11])][6] = 0
                        availableUnitsDic[previousAddy]=houseDic[previousAddy]
                        newTakenUnitsLi.append(str(saveLi[0]))
                        del popLi
                        popLi = roomiePopLi
                        roommateNameDel = roommateName
                        del availableUnitsDic[str(saveLi[0])]
                    if len(saveLi)==0:
                        ##print "Roomie and I did not find place - no longer roomies :("
                        unmatchedPplLi.append(roomiePopLi[0])
                        roomiePopLi = []
                        
                trys+=1
            if len(roomiePopLi)==0:
                ##unmatchedPplLi.append(popLi[0])
                moveRand = random()
                if moveRand<.99:
                    moveOrNo=True
                if moveRand>=.99:
                    unmatchedPplLi.append(popLi[0])
    ##print moveOrNo, "|",popLi,"|", len(availableUnitsDic)
    ##returnLi = [moveOrNo,popLi,availableUnitsDic]
    return moveOrNo, popLi, availableUnitsDic, newTakenUnitsLi, unmatchedPplLi, roommateNameDel

##############################
##Global stats
##############################
def findPrices(availableUnitsDic):
    countUnits = 0
    rentStatDic = {"1BRH":0,"2BRH":0,"3BRH":0,"4BRH":0,"5BRH":0,"6BRH":0,
               "1BRA":0,"2BRA":0,"3BRA":0,"4BRA":0,"5BRA":0,
               "1BRTH":0,"2BRTH":0,"3BRTH":0,"4BRTH":0,"5BRTH":0,"6BRTH":0}
    rentPriceDic = {"1BRH":0,"2BRH":0,"3BRH":0,"4BRH":0,"5BRH":0,"6BRH":0,
               "1BRA":0,"2BRA":0,"3BRA":0,"4BRA":0,"5BRA":0,
               "1BRTH":0,"2BRTH":0,"3BRTH":0,"4BRTH":0,"5BRTH":0,"6BRTH":0}
    saleStatDic = {"1BRH":0,"2BRH":0,"3BRH":0,"4BRH":0,"5BRH":0,"6BRH":0,
               "1BRA":0,"2BRA":0,"3BRA":0,"4BRA":0,"5BRA":0,
               "1BRTH":0,"2BRTH":0,"3BRTH":0,"4BRTH":0,"5BRTH":0,"6BRTH":0}
    salePriceDic = {"1BRH":0,"2BRH":0,"3BRH":0,"4BRH":0,"5BRH":0,"6BRH":0,
               "1BRA":0,"2BRA":0,"3BRA":0,"4BRA":0,"5BRA":0,
               "1BRTH":0,"2BRTH":0,"3BRTH":0,"4BRTH":0,"5BRTH":0,"6BRTH":0}
    rentAvgPriceDic = {"1BRH":0,"2BRH":0,"3BRH":0,"4BRH":0,"5BRH":0,"6BRH":0,
               "1BRA":0,"2BRA":0,"3BRA":0,"4BRA":0,"5BRA":0,
               "1BRTH":0,"2BRTH":0,"3BRTH":0,"4BRTH":0,"5BRTH":0,"6BRTH":0}
    saleAvgPriceDic = {"1BRH":0,"2BRH":0,"3BRH":0,"4BRH":0,"5BRH":0,"6BRH":0,
               "1BRA":0,"2BRA":0,"3BRA":0,"4BRA":0,"5BRA":0,
               "1BRTH":0,"2BRTH":0,"3BRTH":0,"4BRTH":0,"5BRTH":0,"6BRTH":0}
    rentSumSqE = {"1BRH":0,"2BRH":0,"3BRH":0,"4BRH":0,"5BRH":0,"6BRH":0,
               "1BRA":0,"2BRA":0,"3BRA":0,"4BRA":0,"5BRA":0,
               "1BRTH":0,"2BRTH":0,"3BRTH":0,"4BRTH":0,"5BRTH":0,"6BRTH":0}
    saleSumSqE = {"1BRH":0,"2BRH":0,"3BRH":0,"4BRH":0,"5BRH":0,"6BRH":0,
               "1BRA":0,"2BRA":0,"3BRA":0,"4BRA":0,"5BRA":0,
               "1BRTH":0,"2BRTH":0,"3BRTH":0,"4BRTH":0,"5BRTH":0,"6BRTH":0}
    rentStDev = {"1BRH":0,"2BRH":0,"3BRH":0,"4BRH":0,"5BRH":0,"6BRH":0,
               "1BRA":0,"2BRA":0,"3BRA":0,"4BRA":0,"5BRA":0,
               "1BRTH":0,"2BRTH":0,"3BRTH":0,"4BRTH":0,"5BRTH":0,"6BRTH":0}
    saleStDev = {"1BRH":0,"2BRH":0,"3BRH":0,"4BRH":0,"5BRH":0,"6BRH":0,
               "1BRA":0,"2BRA":0,"3BRA":0,"4BRA":0,"5BRA":0,
               "1BRTH":0,"2BRTH":0,"3BRTH":0,"4BRTH":0,"5BRTH":0,"6BRTH":0}
    keyDicHT = {"1":"A","2":"TH","3":"H"}
    globalStatDic = {"rentStatDic":rentStatDic,"rentPriceDic":rentPriceDic,
                     "saleStatDic":saleStatDic,"salePriceDic":salePriceDic,
                     "rentAvgPriceDic":rentAvgPriceDic, "saleAvgPriceDic":saleAvgPriceDic,
                     "rentSumSqE":rentSumSqE, "saleSumSqE":saleSumSqE,
                     "rentStDev":rentStDev, "saleStDev":saleStDev}
    
    for unit in availableUnitsDic:
        unitLi = availableUnitsDic[unit]
        ##print unitLi
        if str(unitLi[3])=="0":
            keyStats = "sale"
            refPrice = 8
        if str(unitLi[3])=="1":
            keyStats = "rent"
            refPrice = 7
        ##print unitLi
        BR = unitLi[4]
        HT = unitLi[2]
        key = str(BR)+"BR"+str(keyDicHT[str(HT)])
        ##print key
        try:
            key2 = keyStats+"StatDic"
            value = int(globalStatDic[key2][key])
            value = value+1
            globalStatDic[key2][key] = int(value)
        except KeyError:
            print "Key not found: ",key
        try:
            key2 = keyStats+"PriceDic"
            value2 = int(globalStatDic[key2][key])
            ##print value2
            ##if refPrice == 7:
                ##print unitLi[refPrice]
            value_2 = value2+float(unitLi[refPrice])
            globalStatDic[key2][key]=float(value_2)
        except KeyError:
            print "Key not found: ",key
        countUnits = countUnits+1
    ##print globalStatDic["rentPriceDic"]
    print "CountAvailableUnits ",countUnits
    globalStatDic = getAvgs(globalStatDic)
    globalStatDic = getSqError(globalStatDic,availableUnitsDic,keyDicHT)
    globalStatDic = getStDev(globalStatDic)
    return globalStatDic

def getStDev(globalStatDic):
    for el in ["rent","sale"]:
        for key in globalStatDic[el+"SumSqE"]:
            numerator = globalStatDic[el+"SumSqE"][key]
            n = globalStatDic[el+"StatDic"][key]
            denominator = n-1
            try:
                stDevSquared = numerator/denominator
            except ZeroDivisionError:
                stDevSquared = 0.0
            stDev = stDevSquared**0.5
            globalStatDic[el+"StDev"][key]=stDev
            ##print el+"StDev"
            ##print stDev
    return globalStatDic

def getSqError(globalStatDic,availableUnitsDic,keyDicHT):
    for unit in availableUnitsDic:
        unitLi = availableUnitsDic[unit]
        key = str(unitLi[4])+"BR"+str(keyDicHT[str(unitLi[2])])
        if str(unitLi[3])=="0":
            keyStats = "sale"
            refPrice=8
        if str(unitLi[3])=="1":
            keyStats = "rent"
            refPrice=7
        x = float(unitLi[refPrice])
        x_bar = float(globalStatDic[keyStats+"AvgPriceDic"][key])
        try:
            sqError = (x-x_bar)**2
            ##print "(",x,"-",x_bar,")^2=",sqError
        except OverflowError:
            print x,"-",x_bar," ",key,"\n",globalStatDic[keyStats+"AvgPriceDic"]
        globalStatDic[keyStats+"SumSqE"][key]+=sqError
    return globalStatDic

def getAvgs(globalStatDic):
    for rentable in ["sale","rent"]:
        ##print rentable
        dicPriceKey = rentable+"PriceDic"
        dicStatKey = rentable+"StatDic"
        dicAvgKey = rentable+"AvgPriceDic"
        for hType in globalStatDic[dicPriceKey]:
            priceSum = globalStatDic[dicPriceKey][str(hType)]
            nUnits = globalStatDic[dicStatKey][str(hType)]
            try:
                avgRental = float(priceSum)/float(nUnits)
            except ZeroDivisionError:
                avgRental = 0.0
            globalStatDic[dicAvgKey][str(hType)]=avgRental
            ##print hType,":",avgRental
    return globalStatDic

def printPopData(popChangeLi,popChangeLi2,fout,runCount,year,date):
    fout.write(str(runCount)+"\t"+str(year)+"\t"+str(date)+"\t")
    for el in popChangeLi:
        fout.write(str(el)+"\t")
    for el in popChangeLi2:
        fout.write(str(el)+"\t")
    fout.write("\n")

def printChoiceData(choiceYrLiLi,fout):
    count = 0
##    while count<1:
##        year = choiceYrLiLi[count]
    for year in choiceYrLiLi:
        for hh in year:
            for hh2 in hh:
                fout.write(str(hh2)+"\t")
            fout.write("\n")
        count = count+1

def printHousePrices(globalStatList,fout,runCount,year,date):
    writeLi = []
    if year == 0:
        fout.write("Run\tYear\tMeasurement\t")
    for el in globalStatList["rentStatDic"]:##Headers
        writeLi.append(str(el))
        if year == 0:
            fout.write(str(el)+"\t")
    if year==0:
        fout.write("\n")
    count = 0
    for dic in globalStatList:
        fout.write(str(runCount)+"\t"+str(year)+"\t")
        fout.write(str(dic)+"\t")
        ##print globalStatList[dic]
        for topic in writeLi:
            fout.write(str(globalStatList[str(dic)][str(topic)])+"\t")
        fout.write("\n")

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

def countPopulation(newPopLi):
    fullPop = 0
    minorPop = 0
    studentCount = 0
    for house in newPopLi:## Original households
        nAdults = countHHAdults(house)
        nKids = len(house[3])
        fullPop += nAdults+nKids
        minorPop = minorPop+nKids
        studentCount += len(house[4])
##    for house in masterLi:## New households
##        if house[2]==0:
##            fullPop = fullPop+1
##        if house[2]==1:
##            fullPop = fullPop+2
##        if len(house[4])>0:
##            studentCount = studentCount+len(house[4])
##        nKids = len(house[3])
##        fullPop = fullPop+nKids
##        minorPop = minorPop+nKids
    return minorPop,fullPop, studentCount

def rewritePopData (popDic, newPopLi, newFamLi, deadPopLi):
    for people in newPopLi:## Households still in town
        ##print "NewPopLi",people
        try:
            popDic[people[0]]
        except KeyError:
            popDic[people[0]]=people

    for newFam in newFamLi:## New households created by scenario
        try:
            popDic[newFam[0]]
            print "Duplicate in new families list!!"
        except KeyError:
            popDic[newFam[0]]=newFam

##    for entry in masterLi:## New households created by simulator
##        try:
##            ##print "masterLi",entry
##            continueQ = False
##            while continueQ == False:##If the name is a duplicate (e.g. 2 kids leave home same year), then a random number is drawn for the second kid and added to new name (with 4 digits)... Repeats until there are no duplicates, just in case
##                try:
##                    popDic[entry[0]]
##                    ##print "DUPLICATE!!!!!",entry
##                    entry[0]=str(entry[0])+str(int(random()*100))
##                    ##print "NewName",entry[0]
##                except KeyError:
##                    continueQ = True
##                    popDic[entry[0]]
##        except KeyError:
##            ##print "Saved name",entry[0]
##            popDic[entry[0]]=entry
            
    for people in deadPopLi:## Delete from popDic those households that disappeared
        try:
            ##print "\tShould delete:",popDic[people[0]]
            del popDic[people[0]]
            ##print "\tSuccessfully deleted"
        except KeyError:## If not found, then we're fine
            ##print "Not found...",people,year
            pass
    return popDic

def printHousingStock(houseDic,fout,year,run):
    for house in houseDic:
        fout.write(str(run)+"\t"+str(year)+"\t")
        houseLi = houseDic[house]
        for el in houseLi:
            fout.write(str(el)+"\t")
        fout.write("\n")

##########################################################################
##########################################################################
## Program starts here
##########################################################################
##########################################################################
        
def fullModel(allSubAreaStatsDic,subAreaLi):
    plannedRuns = 1## Number of runs (should be at least 100 during analysis)
    plannedYears = 10## Number of years to run forecast
    
    timeS = time.clock()
    date = time.asctime()
    dateSave = date.replace(" ","-")
    dateSave = dateSave.replace(".","")
    dateSave = dateSave.replace(":","")
    print dateSave
    outputPath = ".\\Outputs"
    popPath = ".\\Population"
    populationDataName = popPath+"\\test_Wed-Jul-25-171432-2012.txt"
    scenPath = ".\\Scenarios"
    developPath = ".\\Development"
    foutPop = open(outputPath+"\\YrlyPopStats_"+dateSave+".txt","w")
    foutChoice = open(outputPath+"\\Choices_"+dateSave+".txt","w")
    foutPrices = open(outputPath+"\\Prices_"+dateSave+".txt","w")
    foutStock = open(outputPath+"\\Stock_"+dateSave+".txt","w")
    foutPop.write("Run\tYear\tDateOfRun\tBirths\tDeaths\tMarriages\tMarriage_Immigrate\tEmigration\tMoveOutHome-StayInTown\tGradCol-StayIntown\tGradCol-Emigrate\tDivorces\tMoveOutHome-Emigrate\tRetirements\tJobsLost\tJobsFound\tNewCollegeStudents\tTotalWages\tTotalRaises\tStartingHHCount\tEndingHHCount\tStartingPop\tStartingPopMinor\tEndingPop\tEndingPopMinor\tScenarioNewFam\tScenarioNewStud\tTotalNStudents\n")
    foutChoice.write("Name\tYear\tRun\tDate\tAge\tMarried\tnKids\tAgeKids\tnStudents\tincome\thouseType\tjobVariable\tarea\tnRooms\tadultDies\tkidsDie\tkidsMoveOut\tkidsToCollege\tprobGettingMarried\tgotMarried\tgotMarried_Immigrated\tmarriedName\tmarriage_kidsAddedTofam\tprobdivorce\tgotDivorced\tparty1Name\tparty2Name\tkidsWentTo\tnChildrenBorn\tgraduatedCollege\tgraduateMoveOut\tjobChange\tamtRaise\tNewSalary\tRentPrice\tSaleprice\tUnitRentable\tAddress\tstudentYrsLi\tnAdults\n")
    foutStock.write("Run\tYear\tAddress\tLocation\tHouseType\tRentable\tnBR\tforSale\tforRent\trentPrice\tsalePrice\t\n")
    foutPrices.write("")

    foutRunTicket = open(outputPath+"\\_RunTicket_"+str(dateSave)+".txt","w")
    foutRunTicket.write("_RunTicket_"+str(dateSave)+".txt\n\n")
    foutRunTicket.write("NRuns : "+str(plannedRuns))
    foutRunTicket.write("\nNYears : "+str(plannedYears))
    foutRunTicket.write("\nPopDataFiName : "+"YrlyPopStats_"+str(dateSave))
    foutRunTicket.write("\nChoiceDataFiName : "+"Choices_"+str(dateSave))
    foutRunTicket.write("\nPopulationDataName : "+populationDataName)
    foutRunTicket.write("\n\n***POPULATION STATISTICS***\n")
    for x in allSubAreaStatsDic:
        foutRunTicket.write("SubArea : "+str(x)+"\n")
        tempDic = allSubAreaStatsDic[x]
        for y in tempDic:
            foutRunTicket.write(str(y)+" : "+str(tempDic[y])+"\n")
    foutRunTicket.close()
    
    runCount = 0
    while runCount<plannedRuns:
        print "Starting statistical run number ", runCount
        primDic = {}
        popDic = {}
        choiceDic = {}
        #####################################
        ####TestPop Population
        #####################################
        ##popDic = {'Jimmy':["Jimmy",26,1,[6,8],0,65000,1,0],
        ##          'Jo-anne':['Jo-anne',23,0,[],0,12000,1,0],
        ##          'Lamp':['Lamp',19,0,[1,2,3],1,3000,1,0]}
        #####################################
        
        ###################################
        ##LIST OF POPLI VARIABLES (HOUSEHOLD CHARACTERISTICS)
        ##(0)Name, (1)Age, (2)Married(0=No,1=Yes,2=Widowed), (3)kidAgeList,
        ##(4)StudentYrs, (5)Income, (6)housetype(0:homeless,1:apt,2:th,3:house),
        ##(7)jobVariable (0:Unemployed,1=Employed,2=Retired),(8)area,(9)nRooms,
        ##(10)Ethnicity (11) Address
        ####################################
        
        scenarioDic = openScenario(scenPath,"_baseline")##Open scenario
        foutRunTicket = open(outputPath+"\\_RunTicket_"+str(dateSave)+".txt","a")
        foutRunTicket.write("\n\n***SCENARIO***\n")
        for el in scenarioDic:
            foutRunTicket.write(str(el)+": "+str(scenarioDic[el])+"\n")
        foutRunTicket.close()
        houseLi, houseDic = initializeHouseLi(developPath+"\\TEST2_StartHouses.txt")
        houseDic["999999999"]=[999999999,1,0,0,0,0,0,0,0]##Homeless
        houseDic["999999998"]=[999999998,1,0,0,0,0,0,1000,0]##Dorms
        developDic = {'jim':1}##Developer dictionary
        popDic,unmatchedPplLi = initializePop(popDic,populationDataName)##Read in population
        print "N Unmatched People = ",len(unmatchedPplLi)
        deathDic = initializeDeathRate(popPath)##Read in probability of death|age
        developDic = initializeDevelop(developDic,developPath)##Add in more developers
        year = 0
        choiceYrLiLi = []
        print "Run inititialization complete"
        while year<=plannedYears:
            print "N Unmatched People = ",len(unmatchedPplLi)
            print "Year = ",year
            availableUnitsDic = {}
            for unit in houseDic:
                unitLi = houseDic[unit]
                if int(unitLi[3])==1 and int(unitLi[6])==1:
                    availableUnitsDic[str(unitLi[0])]=unitLi
            ###################################
            ## All development for the year
            ###################################
            if year>0:
                unmatchedPplLi = findUnmatchedPpl(popDic)
                for developer in developDic:
                    developLi = developDic[developer]
                    developLi = developOrNot(developLi)
                    developLi = whatToMake(developLi)
                    developLi = developSuccess(developLi)
                    newHouseLi = scenarioDev(scenarioDic,year,globalStatDic)
                    for house in newHouseLi:
                        houseDic[house[0]]=house
                        availableUnitsDic[str(house[0])] = house

            ###################################
            ## All consumer action for the year
            ###################################
            startingPop = len(popDic)## Number of households to analyze this year
            ##masterLi = []## For all new households (to be added to popDic)
            newPopLi = []## All original households (to be included in popDic)
            deadPopLi = []## All dead households (to be deleted from popDic)
            marriageLi = checkMarriages(popDic)## Get list of elgible bachelors
            newTakenUnitsLi = []
            ###################################
            ##Prepare stats on population change ('popChangeLi)
            ##0:Birth,1:Death,2:Marriage,3:MarriageImmigrate,4:Emigrate,
            ##5:MoveOutHome-StayInTown,6:GradCol-StayInTown,7:GradCol-Emigrate,
            ##8:divorce,9:MoveOutHome-Emigrate,10:Retired,11:JobsLost,
            ##12:JobsFound,13:NewCollegeStudents,14:TotalWages,15:TotalRaises
            ###################################
            popChangeLi = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            choiceLiLi = []
##            totalStartPop = 0
##            totalStartPop_minor = 0

            tempLi = []
            for hhold in popDic:
                tempLi.append(popDic[hhold])
            totalStartPop_minor, totalStartPop, startStudents = countPopulation(tempLi)
            del tempLi
            
            try:
                for person in popDic:##Each household
                    popLi = popDic[person]##Establish popLi (household characteristics)
                    nAdults = countHHAdults(popLi)
                    ##totalStartPop += nAdults
                    ##totalStartPop = totalStartPop+len(popLi[3])##Count children per household
                    ##totalStartPop_minor = totalStartPop_minor+len(popLi[3])##Count only children
                    try:
                        choiceLi = [popLi[0],year,runCount,date,popLi[1],popLi[2],len(popLi[3]),str(popLi[3]),
                                    len(popLi[4]),popLi[5],houseDic[str(popLi[11])][2],popLi[7],houseDic[str(popLi[11])][1],
                                    houseDic[str(popLi[11])][4],0,0,0,0,0,0,
                                    0,0,0,0,0,
                                    0,0,0,0,0,
                                    0,0,0,0,
                                    houseDic[str(popLi[11])][7],houseDic[str(popLi[11])][8],
                                    houseDic[str(popLi[11])][3],houseDic[str(popLi[11])][0],
                                    str(popLi[4]),nAdults]
                            
                        ## (0)Name,(1)Year,(2)Run,(3)Date,(4)Age,(5)Married,(6)nKids,(7)AgeKids,
                        ## (8)nStudents,(9)income,(10)houseType,(11)jobVariable,(12)area,
                        ## (13)nRooms,(14)adultDies,(15)kidsDie,(16)kidsMoveOut,(17)kidsToCollege,(18)probGettingMarried,(19)gotMarried,
                        ## (20)gotMarried_Immigrated,(21)marriedName,(22)marriage_kidsAddedTofam,(23)probdivorce,(24)gotDivorced,
                        ## (25)party1Name,(26)party2Name,(27)kidsWentTo,(28)nChildrenBorn,(29)graduatedCollege,(30)graduateMoveOut,
                        ## (31)jobChange,(32)amtRaise,(33)NewSalary,
                        ## (34)RentPrice,(35)Saleprice,
                        ## (36)UnitRentable,(37)Address,
                        ## (38)studentYrs,(39)nAdults
                    except IndexError:
                        print popLi
                        print houseDic[str(popLi[11])]
                     
                    ##Basic life changes (aging, marriage, divorce, dying, college,findingJob)
                    popLi,masterLi,hhSurvival,partner,marriageLi,popChangeLi,choiceLi = lifeChanges(popLi,popDic,marriageLi,popChangeLi,deathDic,choiceLi,houseDic)
                    for el in masterLi:##All new households from the lifeChanges method (e.g. divorce, kid moves out)
                        newPopLi.append(el)
                    if hhSurvival==True:## If household did not die 
                        moveAwayTest, popLi, availableUnitsDic, newTakenUnitsLi, unmatchedPplLi, roommateNameDel = moveOrNo(popLi,availableUnitsDic,houseDic,newTakenUnitsLi,unmatchedPplLi,popDic)##Something is happening that is corrupting returnLi[2]
                        if roommateNameDel != "":
                            deadPopLi.append(popDic[roommateNameDel])
                            if int(popDic[roommateNameDel][11])!=999999999 and int(popDic[roommateNameDel][11])!=999999998:
                                houseDic[str(popDic[roommateNameDel][11])][6]=1
                                availableUnitsDic[str(popDic[roommateNameDel][11])] = houseDic[popDic[roommateNameDel][11]]
                        if moveAwayTest==False:
                            newPopLi.append(popLi)##Tracks all the people who were in the popDic for addition later
                        if moveAwayTest==True:
                            hhSurvival==False
                            popChangeLi[4]=popChangeLi[4]+1##Emigration count
                    if hhSurvival==False:## If household died, add to deadPopLi
                        if int(popLi[11]) != 999999999 and int(popLi[11])!=999999998:
                            houseDic[str(popLi[11])][6]=1
                            availableUnitsDic[str(popLi[11])]=houseDic[str(popLi[11])]
                        deadPopLi.append(popLi)
                        ##print "\nActually died:", popLi
                    if partner!="New" and partner!="None":
                        deadPopLi.append(popDic[partner])## If marriage combined households, add absorbed marriage to deadPopLi
                        if int(popDic[partner][11])==999999999 and int(popDic[partner][11])!=999999998:
                            houseDic[str(popDic[partner][11])][6]=1
                            availableUnitsDic[popDic[partner][11]]=houseDic[popDic[partner][11]]
                        ##print "Added to deadPopLi", popDic[partner]
                    choiceLiLi.append(choiceLi)
            except RuntimeError:
                print "RuntimeError: ",popDic[people]
            globalStatDic = findPrices(availableUnitsDic)## Find end prices for year
            houseDic = adjustPrices(houseDic,globalStatDic,availableUnitsDic)
            
            ###########################
            ## Counts population data
            ###########################
            minorPop,fullPop,studentCount = countPopulation(newPopLi)
            graduating = popChangeLi[6]+popChangeLi[7]
            graduatingEmmigrate = popChangeLi[7]
            ##ExistingGrowth = Births + Marriage_Immigrate - GraduatingEmmigrate - MoveOutHome_Emigrate
            existingPopGrowth = popChangeLi[0]+popChangeLi[3]-graduatingEmmigrate-popChangeLi[7]

            #############################
            ## Add new population to meet scenario expectations
            #############################
            totalExpectStudGrowth = int((float(scenarioDic["OSUGrowth"])/100)*studentCount)+graduating
            ##print "Total expected Stud Growth:",totalExpectStudGrowth
            ##print "Growth level: ",(float(scenarioDic["popGrowth"])/100.0)*totalStartPop
            totalExpectGrowth = int((float(scenarioDic["popGrowth"])/100.0)*totalStartPop)+existingPopGrowth
            ##print "Number of new units to add:",totalExpectGrowth
            newPeopleCount = popChangeLi[0]-popChangeLi[1]+popChangeLi[3]
            expectedMinusActual = totalExpectGrowth-totalExpectStudGrowth
            ##print "Number of new units minust students:",expectedMinusActual
            ##newFamLi = []
            newFamLi,newPop,availableUnitsDic,newTakenUnitsLi,newFamily,newKids = yearlyNewFamilies(expectedMinusActual,allSubAreaStatsDic,subAreaLi,year,availableUnitsDic,newTakenUnitsLi,houseDic,scenarioDic)
            newAdults = newFamily-newKids
            minorPop += newKids
            newFamLi,newPop,availableUnitsDic,newTakenUnitsLi,newStud = yearlyNewStudents(totalExpectStudGrowth,allSubAreaStatsDic,subAreaLi,year,availableUnitsDic,newTakenUnitsLi,houseDic,scenarioDic,newFamLi)
            fullPop = fullPop + newFamily + newStud
            totalNStudents = studentCount+newStud
            
##            print "TotalStartPop",totalStartPop
##            print "TotalStartPop_Minors",totalStartPop_minor
##            print "Births",popChangeLi[0]
##            print "Deaths",popChangeLi[1]
##            print "Marriages",popChangeLi[2]
##            print "Marriage-Immigrate",popChangeLi[3]
##            print "ExpectedGrowth",totalExpectGrowth
##            print "newPeople", newPeopleCount
##            print "numberNewPeopleNeeded",expectedMinusActual
##            print "Number of new people received:",newPop
##            print "\n"

            ##################################
            ## Re-write population dictionary with new data
            ##################################
            del popDic
            popDic = {}
            popDic = rewritePopData(popDic, newPopLi, newFamLi, deadPopLi)
            tempLi = []
            for hhold in popDic:
                tempLi.append(popDic[hhold])
            minorPop, fullPop, totalNStudents = countPopulation(tempLi)
            newAdults = newFamily-newKids
            del tempLi

            #####################################################
            ## Write outputs for model
            #####################################################
            popChangeLi2 = [startingPop,len(popDic),totalStartPop,totalStartPop_minor,fullPop,minorPop,newFamily,newStud,totalNStudents]
            printPopData(popChangeLi,popChangeLi2,foutPop,runCount,year,date)## General population demographics
            printHousePrices(globalStatDic,foutPrices,runCount,year,date)
            printHousingStock(houseDic,foutStock,year,runCount)
            
            #####################################################
            ## Prepare for next iteration
            #####################################################
            choiceYrLiLi.append(choiceLiLi)
            year = year+1
        #################################################
        ##Write choice data - for every run
        #################################################
        printChoiceData(choiceYrLiLi,foutChoice)
        runCount = runCount+1

    foutPop.close()
    foutChoice.close()
    timeE = time.clock()
    tempYear = year-1
    return timeS,timeE,runCount,tempYear,startingPop

################################################################################
################################################################################
## Actual initialization... set up demographic data (areas) and performance testing
################################################################################
################################################################################

## SubArea stats by subarea
allSubAreaStatsDic = {1:{"population":52000,
                         "PerWhite":0.827,
                         "AvgAge":[.29,.18,.12,.12,.11,.09,.09],
                         "households":20918,
                         "avgIncome":{0:[.24,.23,.18,.14,.21],1:[.72,.16,.06,.05,.01]},
                         "perBeds":{0:[0,0,0,0,0],1:[.23,.65,.06,.06,0],2:[0,.15,.7,.15,0],3:[.01,.2,.43,.21,.15]},
                         "houseTypes":[0.25,.06,.69],
                         "perMarried":0.30,
                         "perStudents":[0.76,.17,.04,.02,.01],
                         "avgFamSize":3,
                         "areaUnemployment":0.08,
                         "vacancyRate":0.027}}
subAreaLi = [1]
#################################################
###### If a new population is necessary:
####fout2 = open("CheckPreferences.txt","w")
####fout2.write("Name\tPreferenceLi\tLastWeightedHT\tLastWeightedBR\tlastWeigthedTotal\tprice2\tNHousesLeft\tFound\n")
####fout2.close()
##householdLi, houseDic = initializeHouseLi(".\\Development\\TEST2_StartHouses.txt")
##availableDic = {}
##countSales = 0
##countRents = 0
##for house in houseDic:
##    houseLi = houseDic[house]
##    ##print houseLi
##    if houseLi[3] == "0": ## For Sale
##        ##print "Occupied House!"
##        availableDic[house]=houseLi
##        countSales = countSales+1
##    if houseLi[3] == "1": ## For Rent
##        availableDic[house]=houseLi
##        countRents = countRents+1
##print "Total number of units (including unavailable for initial filling: ",len(houseDic)
##print "Number of units (rent and sell) available: ",len(availableDic)
##print "Number of sale units available: ",countSales
##print "Number of rental units available: ",countRents
##createNewHouseholds(".\\Population",allSubAreaStatsDic,subAreaLi,availableDic)
###############################################

counting = 0
##Performance checking
foutPerformance = open("PerformanceCheck.txt","w")
foutPerformance.write("NTest\ttimeS\ttimeE\trunTime\trunCount\tyear\tstartingP\n")
while counting<1:## If not running performance checks... set to 1
    print "Starting performance run number ",counting
    ## Actually runs simulator
    timeS,timeE,runCount,year,startingP = fullModel(allSubAreaStatsDic,subAreaLi)
    ## Check simulation time
    runTime = timeE-timeS
    ## Write to file performance data
    foutPerformance.write(str(counting)+"\t"+str(timeS)+"\t"+str(timeE)+"\t"+str(runTime)+"\t"+str(runCount)+"\t"+str(year)+"\t"+str(startingP)+"\n")
    counting = counting+1
foutPerformance.close()    
