from random import random
import os
import math
import time

##CURRENT CHALLENGES:
####Household ID disappears (very rarely now, as long as it's only aging that's on), due (somehow) to the aging function (most likely associated with death)
####Accordingly, I can't turn on the other life events, because the errors quickly compound

class fullModel:
    def __init__(self,parent):
        ##############################
        self.plannedRuns = 10
        self.plannedYears = 10
        ##############################
        tempFout = open("_ErrorLog.txt","w")
        tempFout.close()
        self.year = "PRE"
        self.developDir = "Development\\"
        self.popDir = "Population\\"
        self.scenarioDir = "Scenarios\\"
        self.outputsDir = "Outputs\\"
        self.versionHouses = "TEST2_StartHouses.txt"
        self.versionPop = "test2_Mon-Oct-08-171808-2012.txt"
        self.versionHH = "HHTest_Mon-Oct-08-171808-2012.txt"
        self.versionScenario = "_baseline.txt"
        self.date, self.dateSave = self.getTime()
        self.foutMain = open(self.outputsDir+"_MainOut_"+str(self.dateSave)+".txt","w")
        self.foutMain.write("Year\tRun\tName\tAge\tSex\tRace\tStudentD\tJobType\tIncome\tSpouseName\tkidNameLi\tpreviousMarriage\tHHID\tstudentYrs\tstatus\tHHID\tHHType\tHHFormedDate\tadultNames\tchildNames\taddress\tAddress\tLocation\tHousetype\tRentable\tnBR\tforSale\tforRent\trentPrice\tsalePrice\n")
        ##Writes popDic,hhType,houseData
        self.developerDic = {'jim':1}##Developer Dictionary

        self.allSubAreaStatsDic = {1:{"population":5000,
                         "PerWhite":0.827,
                         "AvgAge":[.29,.18,.12,.12,.11,.09,.09],
                         "households":2819,
                         "avgIncome":{0:[.24,.23,.18,.14,.21],1:[.72,.16,.06,.05,.01]},
                         "perBeds":{0:[0,0,0,0,0],1:[.23,.65,.06,.06,0],2:[0,.15,.7,.15,0],3:[.01,.2,.43,.21,.15]},
                         "houseTypes":[0.25,.06,.69],
                         "perMarried":0.30,
                         "perStudents":[0.76,.17,.04,.02,.01],
                         "avgFamSize":3,
                         "areaUnemployment":0.08,
                         "vacancyRate":0.027}}
        #########################
        ##To create a new population, uncomment
        ##
        ##self.createNewPop()
        ##
        #########################
        
        self.runModel()
        self.foutMain.close()

    def runModel(self):
        ##NEED TO WRITE OUTPUTS
        self.runCount = 0
        while self.runCount<self.plannedRuns:
            self.fullPopDic = {}
            self.hhDic = {}
            self.houseDic = {}
            self.scenarioDic = {}
            self.deathDic = {}
            self.availableUnitsDic = {}
            self.studentDic = {}
            self.readInData()
            self.getStudentData()
            
            print "Starting statistical run number ", self.runCount
            self.houseDic["999999999"]=["999999999",1,0,1,0,0,0,0,0]##Homeless
            self.houseDic["999999998"]=["999999998",1,0,1,0,0,0,0,0]##Dorms
            self.hhDic["999999999"]=["999999999",0,"999999999",[],[],"999999999"]
            self.year = 0
            
            while self.year<=self.plannedYears:
                self.delHH = []
                print "Year:",self.year
                moveOutLi = []
                self.unmatchedLi,self.unmatchedDic = self.generateHHUnmatchLi()
                
                
                print "N Unmatched households = ",len(self.unmatchedLi)
                ################################################
                ## All Development for the year
                ################################################
                if self.year == 0:
                    self.searchStats = [0,0]
                    self.startAvail = len(self.availableUnitsDic)
                self.globalStatDic = self.findPrices(self.availableUnitsDic)
                self.allHouseStatDic = self.findPrices(self.houseDic)
                unmatchedPplLi = self.generateHHUnmatchLi()
##                for developer in self.developerDic:
##                    newHouseLi = self.scenarioDev(self.globalStatDic,self.allHouseStatDic,self.searchStats)
##                    for house in newHouseLi:
##                        nameExists = True
##                        nNames = 0
##                        nameHouse = str(self.year)+"-"+house[0]
##                        while nameExists==True:
##                            try:
##                                dump = self.houseDic[nameHouse]
##                                nameHouse = str(nameHouse)+"."+str(nNames)
##                            except KeyError:
##                                nameExists = False
##                        house[0]=nameHouse
##                        self.houseDic[nameHouse]=house
##                        self.availableUnitsDic[nameHouse] = house
                print "Total housing units:",len(self.houseDic)
                print "Total available housing units:",len(self.availableUnitsDic)
                print "Total households:",len(self.hhDic)
                print "Total people:",len(self.fullPopDic)
                studentCount = 0
                for per in self.fullPopDic:
                    tempPop = self.fullPopDic[per]
                    if int(tempPop[4])==1 and int(tempPop[12])==0:
                        studentCount+=1
                print "Total students:",studentCount
                self.searchStats = [0,0]
                self.startAvail = len(self.availableUnitsDic)
                
                ############################################
                ## All consumer action for the year
                ############################################
                startingHHPop = len(self.hhDic)
                startingTownPop = len(self.fullPopDic)
                startingHousePop = len(self.houseDic)
                ##peopleLi,HHLi = self.getPopAndHHLi()
                peopleLi = self.fullPopDic.keys()
                deadLi = []
                
                for person in peopleLi:
                    try:
                        popLi = self.fullPopDic[str(person)]
                        try:
                            if popLi[12]==0:
                                popLi,deadLi = self.lifeChanges(popLi,peopleLi,deadLi)
                        except IndexError:
                            print "Index out of range\n",popLi
                            break
                    except KeyError:
                        pass
                print "Length hhDic before", len(self.hhDic)
                tempDic_1 = self.cleanHH()##Relies on dead people being in popDic
                self.hhDic = {}
                for e in tempDic_1:
                    data = tempDic_1[e]
                    self.hhDic[e]=data
                print "Length hhDic after", len(self.hhDic)
                undeadDic = self.deleteDead(deadLi)##Removes dead people from popDic
                self.fullPopDic = {}
                for f in undeadDic:
                    data_2 = undeadDic[f]
                    self.fullPopDic[f]=data_2

                ##print "\n\n\n"
                ##self.checkData()
                ##self.checkData2()
                self.globalStatDic = {}
                self.allHouseStatDic = {}
                self.globalStatDic = self.findPrices(self.availableUnitsDic)
                self.allHouseStatDic = self.findPrices(self.houseDic)
                self.adjustPrices()
                self.writeDataOut()
                self.writeToData("houses")
                self.pplForScenario(startingTownPop,studentCount)
                ##self.hhDic = self.cleanHH()

                print "\n\n\n"
                ##self.checkData()
                ##self.checkData2()
                self.year+=1
            self.runCount+=1
            errors = open("_ErrorLog.txt")
            eLi = errors.read().split("\n")
            print "Number of errors in '_ErrorLog.txt'",len(eLi)
            errors.close()

##        ##############################
##        ## Where to Live
##        ##############################
##        ##Data handling problem in this section
##        collegeDorm = False
##        if int(popLi[4])==1 and str(popLi[11])=="0":##First year students have to live in dorm
##            collegeDorm = True
##        if int(popLi[4])==1 and str(popLi[11])=="1":
##            collegeDorm = True
##        if hhSurvival==True and collegeDorm == False:
##            popLi = self.fullPopDic[str(popLi[0])]
##            hhLi = self.hhDic[str(popLi[10])]
####            if int(popLi[4])==1:
####                print hhDic
##            moveOrNo = self.moveOrNo(popLi)
##            if moveOrNo==False:
##                ##print "Didn't move out!"
##                popLi = self.fullPopDic[str(popLi[0])]
##            if moveOrNo==True:
##                ##print "Moving out!"
##                pplLi = hhLi[3]+hhLi[4]
##                for per in pplLi:##Handles people
##                    self.fullPopDic[str(popLi[0])][1]="DEAD!"
##                    self.fullPopDic[str(popLi[0])][12]=2##Moving out
##                ##self.deleteHH(str(popLi[10]))
##                if hhLi[0]!="999999999":##If not homeless
##                    ##del self.hhDic[str(popLi[10])]
##                    ##print "Deleted in 'where to live':",popLi[10]
##                    self.delHH.append(str(popLi[10]))
##                    self.hhDic[str(popLi[10])][2]="DEAD!"##HH is dead
##                    self.makeRentalAvailable(str(self.hhDic[str(popLi[10])][5]))
##                ##del self.fullPopDic[str(popLi[0])]
##                hhSurvival=False

    def pplForScenario(self,startingTownPop,startStudentCount):
        nStudent = 0
        for per in self.fullPopDic:
            popLi = self.fullPopDic[per]
            if int(popLi[4])==1:
                nStudent+=1
        print "nStudentNow:",nStudent
        nStudGrowthTarget = self.scenarioDic["OSUGrowth"]
        print "Student Growth Target:",nStudGrowthTarget
        nStudTarget = startStudentCount+(startStudentCount*(nStudGrowthTarget/100.0))
        print "nStudTarget:",nStudTarget
        nStudToAdd = int(nStudTarget-nStudent)
        print "nStudentsToAdd:",nStudToAdd
        countNewStud=0
        print "lengthPopDic Before:",len(self.fullPopDic)
        while countNewStud<nStudToAdd:
            ##print "new student"
            nameExists = True
            nNames = 0
            newName = str(self.year)+"-"+str(len(self.fullPopDic)+1)
            if int(popLi[2])==1:
                sex = 0
            if int(popLi[2])==0:
                sex = 1
            while nameExists == True:
                try:
                    dump = self.fullPopDic[str(newName)]
                    newName = newName+"."+str(nNames)
                except KeyError:
                    nameExists = False
                nNames+=1
            personLi = []
            personLi.append(newName)##ID
            personLi.append(18)
            personLi.append(sex)
            personLi.append(self.findRace())
            personLi.append(1)
            personLi.append(self.jobType(personLi[1]))
            personLi.append(self.income(personLi[1]))
            personLi.append("888888888")
            personLi.append(["777777777"])
            personLi.append("888888888")
            personLi.append(str(newName)+"_dorms")
            personLi.append(0)
            personLi.append(0)
            self.fullPopDic[str(newName)]=personLi
            methodName = self.createHH(newName,False)
            self.hhDic[methodName][5]="999999998"
            self.fullPopDic[str(newName)][10]=str(methodName)
            ##print personLi
            countNewStud+=1
        nPpl = len(self.fullPopDic)
        print "NPpl:",nPpl
        nPplGrowthTarget = self.scenarioDic["popGrowth"]
        print "GrowthTarget:",nPplGrowthTarget
        nPplTarget = startingTownPop+(startingTownPop*(nPplGrowthTarget/100.0))
        print "nPplTarget:",nPplTarget
        nPplToAdd = int(nPplTarget-nPpl)
        print "nPplToAdd (nPplTarget-nPpl):",nPplToAdd
        countNewPop = 0
        self.marriedDic = {}
        while countNewPop<nPplToAdd:
            newIndLi = self.createIndividual([])##Returns list of people created and now stored in fullPopDic
            self.createHH_Original(newIndLi)##Marries people that were just created, all others in single hh
            countNewPop+=1
        ##self.assignSingleHH()##Assigns unmarried people to own household
        ##NOTE: new household starts out homeless
        for ind in self.fullPopDic:
            if len(self.fullPopDic[ind])<13:
                self.fullPopDic[ind][4]=0
                self.fullPopDic[ind].append("999999999")##Student years
                self.fullPopDic[ind].append(0)##Status

    #######################
    ## Marriage (if household is unmarried)
    #######################

    ##If someone marries outside of corvallis... can they move out of corvallis (yes... fix it)
    def marriage():
        if hhSurvival==True and str(popLi[7])=="888888888" and int(popLi[1])>=18:##All unmaarried people qualify, over age 18
            peopleLi_2,HHLi_2 = self.getPopAndHHLi()
            bachelorLi = {}
            bacheloretteLi = {}
            allUnmarriedLi = {}
            marriageRand = random()
            ageMarriageProb = self.findMarriageProb(popLi)##Uses equation to find probability of marriage given age
            if marriageRand<=ageMarriageProb:##Made prob up... ***NEEDS CONFIRMING
                popLi,bachelorLi,bacheloretteLi = self.marriage(popLi,bachelorLi,bacheloretteLi)

    def writeKeyForStatDic(self,ht,nBR):
        htLi = ["homeless","A","TH","H"]
        key = str(nBR)+"BR"+str(htLi[int(ht)])
        return key

    def adjustPrices (self):
        for house in self.houseDic:
            houseLi = self.houseDic[house]
            if houseLi[3]==1 and str(house)!="999999999" and str(house)!="999999998":
                key = self.writeKeyForStatDic(houseLi[2],houseLi[4])
                stDevAll = self.allHouseStatDic["rentStDev"][key]
                tempPrice = self.findRent(self.globalStatDic,houseLi[2],houseLi[4],self.allHouseStatDic,self.searchStats)
                try:
                    valLi = self.availableUnitsDic[str(house)]
                    currentPrice = float(houseLi[7])
                    newPrice = tempPrice
                    ##print "Available unit start price:",currentPrice
                    ##print "Available unit new price:",newPrice
                except KeyError:
                    currentPrice = float(houseLi[7])
                    newPrice = tempPrice
                    prDif = float(newPrice)-float(currentPrice)
                    try:
                        probPriceChange = float(prDif)/float(stDevAll)
                    except ZeroDivisionError:
                        probPriceChange = 0
                    ##print "Prob Price Change:",probPriceChange
                    rand3 = random()
                    if rand3<=probPriceChange:
                        newPrice = newPrice
                        ##print "Change price!"
                    if rand3>probPriceChange:
                        newPrice = currentPrice
                        ##print "Don't change price!"
                    ##print "Occupied unit start price:",currentPrice
                    ##print "Occupied unit end price:",newPrice
                houseLi[7] = str(newPrice)
                self.houseDic[house]=houseLi

    def writeDataOut(self):
        for person in self.fullPopDic:
            countFail = 0
            el = ""
            el_2 = ""
            el_3 = ""
            hhDic = {}
            writeStr = str(self.year)+"\t"+str(self.runCount)+"\t"
            popLi = self.fullPopDic[str(person)]
            count_1 = 0
            ##print popLi[11]
            if len(popLi)>13:
                print popLi
            for el in popLi:
                writeStr += str(el)
                if count_1<len(popLi):
                    writeStr = writeStr+"\t"
                count_1+=1
            count_2 = 0
            try:
                hhDic = self.hhDic[str(popLi[10])]
                for el_2 in self.hhDic[str(popLi[10])]:
                    writeStr += str(el_2)
                    if count_2<len(self.hhDic[str(popLi[10])]):
                        writeStr = writeStr+"\t"
                    count_2+=1
            except KeyError:
                ##print "Printing problem - missing hh in hhDic\n", person, popLi
                fout_2 = open("_ErrorLog.txt","a")
                fout_2.write(str(person)+"\t"+str(popLi)+"\n")
                fout_2.close()
                countFail+=1
                ##writeStr+="\n"
                pass
            try:
                count_3 = 0
                for el_3 in self.houseDic[str(hhDic[5])]:
                    if str(el_3)!="":
                        writeStr+=str(el_3)
                    if str(el_3)=="":
                        count_3+=1
                    if count_3<len(self.houseDic[str(hhDic[5])]):
                        writeStr+="\t"
                    count_3+=1
                writeStr+="\n"
            except KeyError:
                ##print "Printing problem - missing address (and) hh\n", person, popLi
                ##writeStr+="\n"
                countFail+=1
                  
            if countFail>0:
                writeStr+="\n"
            self.foutMain.write(writeStr)
    
    def getStudentData(self):
        studentStats = {}
        for person in self.fullPopDic:
            personLi = self.fullPopDic[person]
            ##print len(self.fullPopDic[person])
            if len(personLi)>13:
                print personLi, "List is too long!"
            if len(personLi)<=13:
                if int(personLi[4])==1:
                    studentYr = int(random()*4)
                    personLi[11]=studentYr
                    try:
                        val = studentStats[studentYr]
                        val+=1
                        studentStats[studentYr]=val
                    except KeyError:
                        studentStats[studentYr]=1
            self.fullPopDic[person]=personLi
        for entry in studentStats:
            print entry,studentStats[entry]

    def deleteDead(self,deadLi):
        print "Number people before",len(self.fullPopDic)
        delHHDic = {}
        saveHHDic = {}
        delPplDic = {}
        savePplDic = {}
        deadLi = []
        delStudDic = {}
        saveStudDic = {}
        
        iterLi = self.fullPopDic.keys()
        for per in iterLi:
            popLi = self.fullPopDic[str(per)]
            try:
                if int(popLi[12])==0:
                    savePplDic[str(per)]=popLi
            except IndexError:
                print "IndexError: List index out of range\n",popLi

        ##self.fullPopDic = {}
        ##self.fullPopDic = savePplDic
        print "Number people after",len(self.fullPopDic)
        return savePplDic

    def cleanHH(self):
        newHHDic = {}
        newHHDic["999999999"]=["999999999",0,"999999999",[],[],"999999999"]
        
        for hh in self.hhDic:
            if str(hh[2])=="DEAD!":
                print "\t####DEAD HOUSEHOLD\n",hh
            if str(hh[2])!="DEAD!":
                ##print "Surviving Household"
                newHH = []
                hhLi = self.hhDic[hh]
                ##print hhLi
                newHH.append(hhLi[0])
                newHH.append(hhLi[1])
                newHH.append(hhLi[2])
                newAdultLi = []
                ##Check adults
                for adult in hhLi[3]:
                    if str(adult)!="":
                        try:
                            data = self.fullPopDic[str(adult)]
                            ##print "Adult"
                            if int(data[12])==0:
                                ##print "Living adult"
                                self.fullPopDic[str(adult)][10]=newHH[0]
                                newAdultLi.append(adult)
                        except KeyError:
                            pass
                            ##print "Dead man:",adult
                newHH.append(newAdultLi)
                newKidLi = []
                for kid in hhLi[4]:
                    if str(kid)!="":
                        try:
                            data = self.fullPopDic[str(kid)]
                            if int(data[12])==0:
                                self.fullPopDic[str(adult)][10]=newHH[0]
                                newKidLi.append(kid)
                        except KeyError:
                            pass
                            ##print "Dead kid:",kid
                newHH.append(newKidLi)
                newHH.append(hhLi[5])
                ##print "\t",newHH
                if len(hhLi[3])==0 and len(hhLi[4])==0:
                    ##Remove hh from list, by ignoring
                    for entry in self.fullPopDic:
                        popLi = self.fullPopDic[entry]
                        if str(popLi[10])==hh[0]:
                            print "\t\t***MISDIRECTED DATA**\n",hh,"\n",popLi
                if len(hhLi[3])==0 and len(hhLi[4])!=0:
                    ##Orphan kids
                    for kid in newHH[4]:
                        self.fullPopDic[str(kid)][10]="999999999"
                if len(hhLi[3])>0:
                    newHHDic[str(newHH[0])]=newHH
        return newHHDic
                    

    def killSomeone(self,popLi):
        hhid = popLi[10]
        ##Try to remove from adult list
        try:
            nameIndex = self.hhDic[popLi[0]][3]
            self.hhDic[popLi[0]][3].remove(nameIndex)
        except ValueError:
            ##Then try to remove from kid list
            try:
                nameIndex = self.hhDic[popLi[0]][4]
                self.hhDic[popLi[0]][4].remove(nameIndex)
            except ValueError:
                print "Person is not in a household\n\n"
        if len(self.hhDic[popLi[0]][3])==0:
            print "Household has passed"
            self.hhDic[popLi[0]][2]="DEAD!"
            if len(self.hhDic[popLi[0]][4])>0:##If kids have no adults, become orphans
                for kid in self.hhDic[popLi[0]][4]:
                   self.fullPopDic[kid][10]="999999999"
            self.hhDic[popLi[0]][4]=[]
        ##Try to remove from kid list
        partnerName = str(popLi[7])
        popLi[1]="DEAD!"
        popLi[12]=1
        self.fullPopDic[str(partnerName)][7]="888888888"
        self.fullPopDic[str(partnerName)][9]=popLi[0]
        ##self.removeFromHH(popLi[10],popLi[0])

    def lifeChanges(self,popLi,peopleLi,deadLi):##Takes data from popLi, which has already been pulled out
        ##list: Name, Age, MarriedDummy, NKids, StudentD, Income
        ##PopChangeLi = 0:Birth,1:Death,2:Marriage,3:Immigrate,4:Emigrate,5:MoveOutHome-StayInTown
        ##                6:GradCol-StayInTown,7:GradCol-Emigrate,8:divorce,9:MoveOutHome-Emigrate
        hhSurvival = True##Represents the person now
        if int(popLi[12])!=0:
            hhSurvival = False
        partner = "None"
        ##################
        ## Age adults
        #################
        if hhSurvival==True:
            survive = self.survival(int(popLi[1]))
            if survive==True:## Lived: Age 1 year
#########################################################
                ##For some reason, this is causing errors (7 out of >50000 runs)
                popLi[1]=int(popLi[1])+1
                pass
#########################################################
            if survive==False:## Died
                ##print "Died:",popLi[0]
                self.killSomeone(popLi)##Not causing errors
                ##deadLi.append(str(popLi[0]))
                hhSurvival = False
        ##################
        ## Age kids
        ##################
        countKids = 0
        nDeadKids = 0
        if hhSurvival==True:## If the household died off, do not run through this section
            popLi = self.fullPopDic[str(popLi[0])]
            if int(popLi[1])==18:
                ##print popLi
                ## If over 18, child moves out and makes choice (method "moveAt18")
                popLi,hhSurvival = self.moveAt18(popLi)
            popLi = self.fullPopDic[str(popLi[0])]

 
        #################################
        ## College graduation
        #################################
        ##try:
        if hhSurvival == True:
            popLi = self.fullPopDic[str(popLi[0])]
            if int(popLi[4])==1 and str(popLi[11])!="999999999":##If a student
                ##Student gets through another year
                popLi[11]+=1##Add one year to student years
                ##Student graduates?
                ###############################################################
                ##Errors coming from this area
                if int(popLi[11])>3:##If that year makes a student in senior year
                    ##########################
                    ##Assume no one can stay after graduation
                    ##########################
                    popLi[4]=0##Graduate - no longer in university, nobody in hh gets to stay
                    if str(self.hhDic[str(popLi[10])])!="DEAD!":##If person is alive...(could have been killed by another person graduating
                        try:
                            self.hhDic[str(popLi[10])][2]="DEAD!"
                            adults = self.hhDic[str(popLi[10])][3]
                            kids = self.hhDic[str(popLi[10])][4]
                            ppl = adults+kids
                            try:##If adult or kid is already gone from town, then no need to worry!
                                for per in ppl:
                                    self.fullPopDic[str(per)][1]="DEAD!"
                                    self.fullPopDic[str(per)][12]=3##Graduated college
                            except KeyError:
                                pass##For students in the household
                        except KeyError:
                            print "student household missing"
                            print popLi
                    hhSurvival=False
                    popLi[1] = "DEAD!"
                    popLi[12] = 3##Graduated college
                    self.fullPopDic[str(popLi[0])]=popLi
                    ##self.removeFromHH(str(popLi[10]),str(popLi[0]))



        #############################
        ## Divorce (If household is married)
        #############################
        
        if hhSurvival and str(popLi[7])!="888888888":
            ##print "Entered divorce if"
            probDivorce = .0036##http://www.nber.org/digest/nov07/w12944.html
            divorceRand = random()
            if divorceRand<=probDivorce:
                self.divorce(popLi)

        ##################################
        ## Having kids
        #################################

        if hhSurvival == True:
            popLi = self.fullPopDic[str(popLi[0])]
            popLi = self.haveKidsOrNo(popLi)


        ################################
        ## Employment
        ################################

        if hhSurvival==True:
            popLi = self.fullPopDic[str(popLi[0])]
            ## If decides to stay in town, then finds (or doesn't find) a job/salary
            preJobCode = popLi[5]
            preIncome = popLi[6]
            popLi,leaveAreaTest = self.jobDynamics(popLi)
            if leaveAreaTest == True:
                for adults in self.hhDic[str(popLi[10])]:
                    self.fullPopDic[adults][1]="DEAD!"
                    self.fullPopDic[adults][12]=4
                for kids in self.hhDic[str(popLi[10])]:
                    self.fullPopDic[kids][1]="DEAD!"
                    self.fullPopDic[kids][12]=4
                self.hhDic[popLi[10]][2]="DEAD!"
                hhSurvival = False

        return popLi,deadLi




###############################################################
## Life Events

    def moveOrNo(self,popLi):
        hhID = popLi[10]
        hhLi = self.hhDic[hhID]
        ##print hhLi
        nAdults = self.hhDic[str(hhID)][3]
        if nAdults==0:
            print "Error in moveOrNo",popLi
        if nAdults==1:
            maxRent = float(popLi[6])/24.0##Income divided by 24 (50% income for rent)
        if nAdults>1:
            hhIncome = self.findHHIncome(self.hhDic[hhID])
            maxRent = float(hhIncome)/24.0
        returnQueue = []
        roommateNameDel = ""
        moveOrNo = False
        ##print "numberAvailableUnits = ",len(availableUnitsDic)
        currentHouseAddy = str(hhLi[5])
        currentHousePrice = float(self.houseDic[currentHouseAddy][6])
        ##print currentHousePrice, maxRent
        graduated = False
        if int(popLi[4])==0 and hhLi[5]=="999999998":
            graduated=True
        
        if currentHousePrice>maxRent or str(hhLi[5])=="999999999" or graduated==True:
            ##If monthly rent is greater than monthly rent of income, have to move
            ##print "Need to move"
            self.searchStats[0]+=1##Searching
            previousAddy = currentHouseAddy
            ##print "In moveOrNo"
            prefLi = self.findPreferences(hhLi)
            if str(previousAddy)!="999999999" and str(previousAddy)!="999999998":
                self.makeRentalAvailable(currentHouseAddy)
            saveLi = self.utilityMaximize(prefLi,False,maxRent,hhLi)
            ##print saveLi
            if len(saveLi)!=0:
                ##print "Found new home"
                self.hhDic[str(popLi[10])][5]=str(saveLi[0])
                self.houseDic[str(saveLi[0])][6] = 0
                ##del self.availableUnitsDic[str(saveLi[0])]
            if len(saveLi)==0:
                ##print "Did not find new home - searching for roomie"
                ##popLi[11]="999999999"
                trys = 0
                roomiePopLi = []
                roomieHHLi = self.findRoomie(self.unmatchedLi,popLi)##Looks for roommate and new rental
                popLi = self.fullPopDic[str(popLi[0])]
                hhLi = self.hhDic[str(popLi[10])]
                if str(hhLi[5])!=currentHouseAddy:
                    pass
                    ##Found roomie
                    ##Yay!!
                if str(hhLi[5])==currentHouseAddy:
                    ##Did not find roomie
                    ##Sad
                    ##self.unmatchedPplLi.append(popLi[0])
                    self.searchStats[1]+=1
                    if str(hhLi[5])=="999999998":
                        pass
                        ##print "Dorms!"
                    if str(hhLi[5])!="999999998":##Students prefer not dorms, but will stay if unable to find apt.
                        if int(popLi[4])==0:##Not a student
                            self.hhDic[str(popLi[10])][5]="999999999"
                            moveRand = random()
                            if moveRand<.99:##If homeless, moving out of town, unless becoming actually homeless
                                moveOrNo = True
                                ##unmatchedPplLi.append(popLi[0])##Currently to avoid losing my entire population
                            if moveRand>=.99:
                                self.unmatchedLi.append(popLi[0])
        return moveOrNo

    def jobDynamics(self,popLi):
        ##PopChangeLi = 0:Birth,1:Death,2:Marriage,3:Immigrate,4:Emigrate,5:MoveOutHome-StayInTown
        ##                6:GradCol-StayInTown,7:GradCol-Emigrate,8:divorce,9:MoveOutHome-Emigrate
        ##              10: Retired,11:JobsLost,12:JobsFound,13:newCollegeStudents,14:totalPay,15:totalRaises
        if popLi[1]>65:##If older than 65, forced retirement
            self.fullPopDic[str(popLi[0])][5]=2
        if int(self.fullPopDic[str(popLi[0])][5])==2:##If retired, breaks from this module
            return popLi,False
        if int(self.fullPopDic[str(popLi[0])][5])==1:
            keepJobRand = random()
            if keepJobRand>.98:
                ##print "we lost our job... bummer",popLi
                self.fullPopDic[str(popLi[0])][5]==0
                self.fullPopDic[str(popLi[0])][6]==0
            keepJobRand2 = random()
            if keepJobRand2<=.25 and int(self.fullPopDic[str(popLi[0])][5])==1:##Only top 25% of households get a raise
                ##print "We got a raise!",popLi
                wage = float(self.fullPopDic[str(popLi[0])][6])
                raiseWage = int(wage*((random()*25)/100))##Percent wage raise less than 25%
                self.fullPopDic[str(popLi[0])][6]=wage+raiseWage
        leaveAreaTest = False
        if int(self.fullPopDic[str(popLi[0])][5])==0:
            findJobRand = random()
            if findJobRand>.04:
                ##print "we found a job!! yay."
                self.fullPopDic[str(popLi[0])][5]=1
                wageRand = random()
                wage = int(wageRand*100000)
                self.fullPopDic[str(popLi[0])][6]
            if findJobRand<=.04:
                moveRand = random()
                if moveRand < .91: ##Employment rate US
                    leaveAreaTest = True
                    if str(popLi[7])=="888888888":
                        ##self.removeFromHH(popLi[10],popLi[0])
                        self.fullPopDic[str(popLi[0])][1]="DEAD!"
                        self.fullPopDic[str(popLi[0])][12]=4##Couldn't find job
        return popLi,leaveAreaTest


    def haveKidsOrNo(self,popLi):
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
            ##print "Having kid"
            newKidLi = self.babyMaker_new(popLi)##Not yet written to dic
            newKidLi.append("999999999")##Years in college
            newKidLi.append(0)##Kid is alive
            ##print self.hhDic[newKidLi[10]]
            self.fullPopDic[str(newKidLi[0])]=newKidLi##Save to master dic
            self.fullPopDic[str(popLi[0])][8].append(newKidLi[0])##Change mother's data
            self.fullPopDic[str(popLi[7])][8].append(newKidLi[0])##change father's data
            hhID = popLi[10]##Find HH ID
            self.hhDic[hhID][4].append(newKidLi[0])##Add to houshold kids list
            popLi = self.fullPopDic[str(popLi[0])]##Reset poplist before returning
            ##print self.hhDic[newKidLi[10]]
            tempTestLi = str(self.fullPopDic[newKidLi[0]])
            if str(tempTestLi)!=str(newKidLi):
                print "ERROR, input problem in 'haveKidsOrNo':\n",newKidLi
            ##print "Childbirth is done"
            ##print newKidLi
            ##print popLi
        return popLi

    def divorce(self,popLi):##Divorcer leaves hh, does not take kids
        startHHID = str(popLi[10])##Household pre divorce
        ###################
        ##Remove divorcer from hh
        self.hhDic[startHHID][3].remove(popLi[0])##Removes from household
        self.hhDic[startHHID][1]=4
        ###################
        origHHDic = self.hhDic[popLi[10]]##Pulls up household dictionary
        mainName = str(popLi[0])##Divorcer Name
        partnerName = str(popLi[7])##Divorcee Name

        ####################
        ##Create new hh name for divorcer
        newName_divorced = str(self.year)+"-"+str(mainName)+"_Divorced"
        nameExists = True
        nNames = 0
        while nameExists == True:
            try:
                waste = self.hhDic[str(newName_divorced)]
                name_2 = newName_divorced+"."+str(nNames)
            except KeyError:
                nameExists = False
            nNames+=1

        ##Adjust data in popdic
        self.fullPopDic[mainName][7]="888888888"
        self.fullPopDic[partnerName][7]="888888888"
        self.fullPopDic[mainName][9]=str(partnerName)
        self.fullPopDic[partnerName][9]=str(mainName)
        self.fullPopDic[partnerName][10] = newName_divorced
        self.fullPopDic[mainName][2]=0##Divorcee Not married
        self.fullPopDic[partnerName][2]=0##Divorcer Not married
        
        newHHLi = [str(newName_divorced),4,self.year,[mainName],[],"999999999"]
        self.hhDic[str(newHHLi[0])]=newHHLi##New HH for divorcer
    
    def findMarriageProb(self,popLi):
        age = popLi[1]
        if age<=30:
            prob = .25
        if age>30:
            prob = .25-((int(age)/200.0)**2.0)
        if prob < 0:
            prob = 0
        ##print prob
        return prob

    def marriage (self,popLi,bachelorLi,bacheloretteLi):
        inHouseProb = .5
        ##PopChangeLi = 0:Birth,1:Death,2:Marriage,3:Marriage-Immigrate,4:Emigrate,5:MoveOutHome-StayInTown
        ##            6:GradCol-StayInTown,7:GradCol-Emigrate
        ##print "Marriage!!!!"
        probEa = 0.0
        partner = "None"
        marriageLi = []
        if int(popLi[2])==1:
            marriageLi = bacheloretteLi
        if int(popLi[2])==0:
            marriageLi = bachelorLi
        if len(marriageLi)>0:
            randInOrOut = random()
            if randInOrOut<=inHouseProb:##If less than value, marry in house
                ##print "marrying in house"
                choiceMade = False
                while choiceMade==False:
                    choice = int(len(marriageLi)*random())##Randomly search for wife
                    ##print choice
                    partnerLi = marriageLi[choice]
                    ##print person2
                    choiceMade = True
                    if int(popLi[2])==1:
                        bacheloretteLi = self.makeUnmarriable(bacheloretteLi,partnerLi)
                        bachelorLi = self.makeUnmarriable(bachelorLi,popLi)
                    if int(popLi[2])==0:
                        bachelorLi = self.makeUnmarriable(bachelorLi,partnerLi)
                        bacheloretteLi = self.makeUnmarriable(bacheloretteLi,partnerLi)
                    del marriageLi[choice]
                newName = self.combineHHMarriage(popLi,partnerLi,"marriage")
                self.fullPopDic[str(popLi[0])][7]=str(partnerLi[0])
                self.fullPopDic[str(partnerLi[0])][7]=str(popLi[0])
                name = popLi[0]
                popLi = self.fullPopDic[str(name)]
        if len(marriageLi)==0 or randInOrOut>inHouseProb:
            ##print "Length of marriage list is 0"
            newIndName = self.createAdultToMarry(popLi)
            tempPopLi = self.fullPopDic[str(newIndName)]
##            print tempPopLi
##            print self.hhDic[tempPopLi[10]]
            partnerLi = self.fullPopDic[newIndName]
            ##print partnerLi##Getting this part just fine
            if int(popLi[2])==1:
                bachelorLi = self.makeUnmarriable(bachelorLi,popLi)
            if int(popLi[2])==0:
                bacheloretteLi = self.makeUnmarriable(bacheloretteLi,popLi)
            newName = self.combineHHMarriage(popLi,partnerLi,"marriage")
            self.fullPopDic[str(popLi[0])][7]=partnerLi[0]
            self.fullPopDic[str(partnerLi[0])][7]=popLi[0]
            ##print self.fullPopDic[str(popLi[0])],self.fullPopDic[str(partnerLi[0])]
            popLi = self.fullPopDic[str(popLi[0])]
        return popLi,bachelorLi,bacheloretteLi

    def makeUnmarriable(self,li,partnerLi):
        count = 0
        for unit in li:
            if str(unit)==str(partnerLi[0]):
                del li[count]
                break
            count+=1
        return li

    def stayInTown(self,popLi,age,indic):
        corvRand = random()
        intownTest = False
        if corvRand >= .4 and indic==False: ##Made up probability of continuing to live in Corvallis, if not student
            intownTest = True
        if corvRand >= 0.0 and indic==True:
            intownTest = True##Students more likely to stay
        return intownTest
    
    def moveAt18(self,popLi):
            ##Outgoing: Name, Age, Married(0=No,1=Yes,2=Widowed), kidAgeList, StudentD,
            ##      Income, housetype(0:homeless,1:apt,2:th,3:house),
            ##      jobVariable (0:Unemployed,1=Employed,2=Retired),area,nRooms
        hhSurvives=True
        hh = popLi[10]
        name = popLi[0]
        countKids = 0
        famDic = self.hhDic[str(hh)]
        newFamLi = []
        for entry in famDic[4]:##Need to set up so it re-writes data in hhDic
            if str(entry)!=str(popLi[0]):
                newFamLi.append(entry)
            countKids+=1
        self.hhDic[str(hh)][4]=newFamLi
        intownTest = self.stayInTown(popLi,popLi[2],False)##False = whether a student or not
        ##print intownTest
        toCollege = 0
        collegeRand = random()
        if intownTest==True:
            ###############***********************############################
            ##Add ability for person to get a job when they finish HS
            ##self.hhDic[popLi[0]][5]=##
            ##self.hhDic[popLi[0][6]=##
            #############******************************#####################
            nameExists = True
            newName = str(self.year)+"-"+str(len(self.hhDic)+1)+"_singleHH"
            nNames = 0
            while nameExists == True:
                try:
                    dump = self.hhDic[str(newName)]
                    newName = newName+"."+str(nNames)
                except KeyError:
                    nameExists = False

            hhLi = [newName,4,self.year,[popLi[0]],[],"999999998"]
            self.hhDic[str(newName)]=hhLi
            ##print self.fullPopDic[str(name)]
            self.fullPopDic[str(name)][10]=str(hhLi[0])
            ##print self.fullPopDic[str(name)]
            ########################
            ##Assume everyone who stays goes to college
            self.fullPopDic[name][4]=1
            self.fullPopDic[name][11] = 0
            #########################
            hhSurvives = True
        if intownTest==False:
            hhSurvives = False
        popLi = self.fullPopDic[str(popLi[0])]
        return popLi,hhSurvives
    
    def survival(self,age):
        ##NEED TO USE THIS: http://gravityandlevity.wordpress.com/2009/07/08/your-body-wasnt-built-to-last-a-lesson-from-human-mortality-rates/
        ##Also this: http://www.cdc.gov/nchs/data/nvsr/nvsr54/nvsr54_14.pdf
        deathDic = self.deathDic
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
        if age>=100:
            survivalQ = False
        return survivalQ



###################################################################
## Data Management Tasks

    def deleteHH(self,hhName,kidLi):
        ##print kidLi
        for child in kidLi:
            ##print child
            self.fullPopDic[str(child)][10]="999999999"
            methodName = self.createHH(child,False)
        ##print "Deleting HH"
        ##del self.hhDic[str(hhName)]
        ##print "Deleted in deleteHH:",str(hhName)
        self.delHH.append(hhName)
        self.hhDic[str(hhName)][2]="DEAD!"
        self.makeRentalAvailable(str(self.hhDic[str(hhName)][5]))
        forceDone = []
        ##print "Done Deleting HH"

    def removeFromHH(self,hhName,indName):
        ##print "Removing"
        popLi = self.fullPopDic[str(indName)]
        hhli = self.hhDic[str(hhName)]
        hhid = hhName
        ##Original data
        address = hhli[5]
        adultNames = hhli[3]
        countAdults = 0
        countNameEl = 0
        newAdultLi = []
        for adult in adultNames:##Remove adult from list
            if str(adult)!=str(indName):
                newAdultLi.append(str(adult))
            self.fullPopDic[str(adult)][10]=hhid
            countAdults+=1
        childNames = hhli[4]
        newKidLi = []
        countKid = 0
        for kid in childNames:
            originalKid = str(kid)
            if str(originalKid)!=str(indName):
                newKidLi.append(str(kid))
            self.fullPopDic[str(kid)][10]=hhid
            countKid+=1
##        if str(popLi[7])!="888888888":
##            self.fullPopDic[str(popLi[7])][7]="888888888"
        if len(adultNames)!=0:
            self.hhDic[str(hhid)]=[str(hhid),3,self.year,newAdultLi,newKidLi,address]##Save as new HH
        ##if len(adultNames)==0:
            ##self.deleteHH(hhName,childNames)
        forceRun = []
        
    def combineHH(self,popLi,tempPopLi,name,ty):##Note: Takes HHDic, not popLi
        hhid = name
        hhtype = 3
        HHFormedDate = str(self.year)
        groupA_1 = popLi[3]
        groupA_2 = tempPopLi[3]
        adults = groupA_1+groupA_2
        child_1 = popLi[4]
        child_2 = tempPopLi[4]
        children = child_1+child_2
        address = "999999999"
        roomieHHLi = [hhid,hhtype,HHFormedDate,adults,children,address]
        return roomieHHLi

    def combineHHMarriage(self,popLi,tempPopLi,ty):##Note: Takes popLi, not HHDic
        ##print 'Marriage1:',popLi
        ##print 'Marriage2:',tempPopLi
        HHID_1 = popLi[10]
        HHID_2 = tempPopLi[10]
        name = str(self.year)+"-"+str(HHID_1)+"_M_"+str(HHID_2)
        hhType = 2
        HHFormedDate = self.year
        adults_1 = self.hhDic[str(HHID_1)][3]
        adults_2 = self.hhDic[str(HHID_2)][3]
        kids_1 = self.hhDic[str(HHID_1)][4]
        kids_2 = self.hhDic[str(HHID_2)][4]
        ##print self.hhDic[HHID_1]
        addy_1 = self.hhDic[str(HHID_1)][5]
        addy_2 = self.hhDic[str(HHID_2)][5]
        address = "999999999"##Placeholder, until decision made
        adults = adults_1+adults_2
        children = kids_1+kids_2
            
        if str(addy_1)!="999999999" and str(addy_2)!="999999999":
            if int(self.houseDic[str(addy_1)][2])>int(self.houseDic[str(addy_2)][2]):
                address = str(addy_1)
                self.makeRentalAvailable(addy_1)
            if int(self.houseDic[str(addy_1)][2])<=int(self.houseDic[str(addy_2)][2]):
                address = str(addy_2)
                self.makeRentalAvailable(addy_2)

        if str(addy_1)=="999999999" and str(addy_2)=="999999999":
            address = "999999999"
        hhLi = [name,hhType,HHFormedDate,adults,children,address]
        nameExists = True
        countNames = 0
        while nameExists==True:
            try:
                oldLi = self.hhDic[str(name)]
                name = name+"."+str(countNames)
            except KeyError:
                nameExists = False
            countNames+=1
        self.hhDic[str(name)]=hhLi
        for adult in adults:
            self.fullPopDic[str(adult)][10]=str(hhLi[0])
        for kid in children:
            self.fullPopDic[str(kid)][10]=str(hhLi[0])
        ##print "Deleted from combineHHMarriage:",HHID_1,HHID_2
        self.delHH.append(str(HHID_1))
        self.delHH.append(str(HHID_2))
        self.hhDic[str(HHID_1)][2]="DEAD!"
        self.makeRentalAvailable(str(self.hhDic[str(HHID_1)][5]))
        self.hhDic[str(HHID_2)][2]="DEAD!"
        self.makeRentalAvailable(str(self.hhDic[str(HHID_2)][5]))
        ##del self.hhDic[str(HHID_2)

        return name
            

    def makeRentalAvailable(self,address):
        keyLi = ["HOMELESS","A","TH","H"]
        if address!="999999999":
            housingLi = self.houseDic[address]
            key = str(housingLi[4])+"BR"+str(keyLi[int(housingLi[2])])
            rentPrice = self.findRent(self.globalStatDic, housingLi[2], housingLi[4], self.allHouseStatDic,self.searchStats)
            housingLi[6]=1
            housingLi[7]=rentPrice
            self.availableUnitsDic[str(address)]=housingLi
            self.houseDic[str(address)]=housingLi
            ##print housingLi


###################################################################
## General

    def getPopAndHHLi(self):
        popLi = []
        HHLi = []
        for pop in self.fullPopDic:
            popLi.append(str(pop))
        for hh in self.hhDic:
            HHLi.append(str(hh))
        return popLi,HHLi

    def availableUnitsCount(self):
        tempDic = {}
        for unit in self.houseDic:
            unitLi = self.houseDic[unit]
            if int(unitLi[3])==1 and int(unitLi[6])==1:
                self.availableUnitsDic[str(unitLi[0])]=unitLi
        print "Available Units (Start):",len(self.availableUnitsDic)
        
    def findHHIncome(self,popLi):
        totIncome = 0
        try:
            len(popLi[3])
        except TypeError:
            print "findHHIncome error", popLi
        for adults in popLi[3]:
            ##print self.fullPopDic[adults]
            totIncome+=float(self.fullPopDic[str(adults)][6])
            ##print totIncome
        return totIncome    

    def generateHHUnmatchLi(self):
        unmatchedLi = []
        unmatchedDic = {}
        for entry in self.fullPopDic:
            popLi = self.fullPopDic[entry]
            try:
                hhLi = self.hhDic[str(popLi[10])]
            except KeyError:##For some reason, some households are not showing up... but they show up later
                pass
                ##if str(popLi[10])!="999999999":
                    ##print "Key ERROR in 'generateHHUnmatchLi':\n",popLi
            if str(hhLi[5])=="999999999":
                try:
                    value = unmatchedDic[str(hhLi[0])]
                except KeyError:
                    unmatchedLi.append(str(hhLi[0]))
                    unmatchedDic[str(hhLi[0])]=hhLi
##        for entry in self.hhDic:
##            if str(self.hhDic[entry][5])=="999999999":
##                unmatchedLi.append(entry)
##                unmatchedDic[entry]=self.hhDic[str(entry)]
        return unmatchedLi,unmatchedDic

    def getTime(self):
        date = time.asctime()
        dateSave = date.replace(" ","-")
        dateSave = dateSave.replace(":","")
        dateSave = dateSave.replace(".","")
        return date,dateSave

    def writeToData(self,ty):
        if ty == "population":
            fout = open(self.popDir+"test2_"+str(self.dateSave)+".txt","w")
            fout.write("Name\tAge\tSex\tRace\tStudentD\tJobType\tIncome\tSpouseName\tkidNameLi\tpreviousMarriage\tHHID\t\n")
            for entry in self.fullPopDic:
                data = self.fullPopDic[str(entry)]
                for row in data:
                    fout.write(str(row)+"\t")
                fout.write("\n")

        if ty == "hh":
            fout = open(self.popDir+"HHTest_"+str(self.dateSave)+".txt","w")
            fout.write("HHID\tHHType\tHHFormedDate\tadultNames\tchildNames\taddress\t\n")
            for entry in self.hhDic:
                data = self.hhDic[str(entry)]
                for row in data:
                    fout.write(str(row)+"\t")
                fout.write("\n")
        if ty =="houses":
            if int(self.year)==0:
                fout = open(self.outputsDir+"Stock_"+str(self.dateSave)+".txt","w")
                fout.write("Year\tRun\tAddress\tLocation\tHousetype\tRentable\tnBR\tforSale\tforRent\trentPrice\tsalePrice\n")
            if int(self.year)>0:
                fout = open(self.outputsDir+"Stock_"+str(self.dateSave)+".txt","a")            
            for entry in self.houseDic:
                fout.write(str(self.year)+"\t"+str(self.runCount)+"\t")
                data = self.houseDic[str(entry)]
                for row in data:
                    fout.write(str(row)+"\t")
                fout.write("\n")

####################################################################
## Consumer Housing Decisions

    def findProbRooming(self,popLi):
        prob = .75
        married = 0
        if int(popLi[1])==2:
            prob = prob - 0.5
        try:
            nKids = len(popLi[4])
        except TypeError:
            print "findProbRooming Problem:",popLi
        if nKids > 0:
            prob = prob-.25
        return prob

    def findRoomie(self,unmatchedPplLi,popLi):##Finds a roommate from the list of unmatched, searches for house, if found, adjusts records
        roomiePopLi = []
        roommateName = ""
        try:
            searcherProb = self.findProbRooming(self.hhDic[str(popLi[10])])
        except:
            print "findRoomie:",popLi
        currentIncome = self.findHHIncome(self.hhDic[str(popLi[10])])
        counthh = 0
        for person in unmatchedPplLi:
            try:
                tempPopLi = self.fullPopDic[str(person)]
                tempIncome = self.findHHIncome(self.hhDic[str(tempPopLi[0])])
                if (currentIncome+tempIncome)>currentIncome:
                    foundProb = self.findProbRooming(self.hhDic[str(tempPopLi[10])])
                    totalProb = float(foundProb)*float(foundProb)
                    ##searcherRand = random()
                    foundRand = random()
                    ##if searcherRand<=searcherProb:
                        ##print "searcherFind"
                    if foundRand<=totalProb:
                        ##Found roommate
                        roommateName = tempPopLi[0]
                        name = str(popLi[0])+"_R_"+str(tempPopLi[0])##HH Name
                        roomieHHLi = self.combineHH(popLi,tempPopLi,name,"roomie")##Combines
                        tempDic_1 = {}
                        tempDic_1[roomieHHLi[0]]=roomieHHLi
                        success,hhLi = self.matchHHWithHouse(tempDic_1)##Look for house, return indicator, hhli
                        if success==True:
                            ##If house was found
                            for adult in roomieHHLi[3]:
                                self.fullPopDic[str(adult)][10]=hhLi[0]
                            for child in roomieHHLi[4]:
                                self.fullPopDic[str(child)][10]=hhLi[0]
                            self.hhDic[str(hhLi[0])]=hhLi##Adds roomie household to list
                            ##del self.hhDic[str(popLi[10])]##Erase old hhdic
                            self.delHH.append(str(popLi[10]))
                            self.delHH.append(str(tempPopLi[10]))
                            self.hhDic[str(popLi[10])][2]="DEAD!"
                            self.makeRentalAvailable(str(self.hhDic[str(popLi[10])][5]))
                            self.hhDic[str(tempPopLi[10])][2]="DEAD!"
                            self.makeRentalAvailable(str(self.hhDic[str(tempPopLi[10])][5]))
                            ##print "Deleted in findRoomie",popLi[10],tempPopLi[10]
                            ##del self.hhDic[str(tempPopLi[10])]
                            del self.unmatchedLi[counthh]
                            ##print "Match"##Follows same rules as marriage, with a different name
                            break
                        if success==False:
                            ##If house was not found
                            del tempDic_1
        
            except KeyError:
                pass
            counthh +=1

    def matchHHWithHouse(self,tempHHDic):
        success = True
        hhLi = []
        for hh in tempHHDic:
            hhLi = self.hhDic[str(hh)]
            address = self.findHousing(hhLi)
            hhLi[5]=address
            if str(address)=="999999999":
                success = False
            if str(address)!="999999999":
                pass
##                hhLi.append(hh)
        return success,hhLi

    def findHousing(self,popLi):
        houseDic = self.houseDic
        ##print "In findHousing"
        prefLi = self.findPreferences (popLi)
        income = self.findHHIncome(popLi)
        maxRent = float(income)/24.0
        buy = False
        if random()<=.5:
            buy=True##50% chance of looking to buy
        saveLi = self.utilityMaximize(prefLi,buy,maxRent,popLi)
        if len(saveLi)!=0:
            address = str(saveLi[0])
            if buy==False:
                self.houseDic[str(address)][6]=0
                self.houseDic[str(address)][5]=2
            if buy==True:
                self.houseDic[str(address)][5]=0
                self.houseDic[str(address)][6]=2
            ##print address
        if len(saveLi)==0:
            address = str(999999999)
            ##print "Not found!!"
        return address
    
    def findPreferences (self,popLi):
        student = 0
        totAge = 0
        ethnicity = 0
        removeAdults = 0
        for adult in popLi[3]:
            indLi = self.fullPopDic[str(adult)]
            try:
                totAge+=int(indLi[1])
            except ValueError:
                removeAdults+=1
            if indLi[4]==1:
                student = 1
            if indLi[3]==1:
                ethnicity=1
        try:
            age = float(totAge)/len(popLi[3])
            adult = len(popLi[3])-removeAdults
            minors = len(popLi[4])
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
        except ZeroDivisionError:
            ##print "PrefLi Empty",popLi
            ##self.deleteHH(str(popLi[0]),popLi[4])
            prefLi = [0.0,0.0,0.0,0.0]

        ##print prefLi
        return prefLi

    def findWeights (self,prefLi,houseLi,refPrice):
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
            print "findWeightsError",prefLi
            print "findwWeightError",houseLi
            print "findWeightError",refPrice
        return priceWeighted

    def utilityMaximize (self,prefLi,buy,maxRent,popLi):
        ##Weight by price by preference, so if I have an 8 percent chance of picking an apt,
        ##  then the price of the house will be discounted by 8%, so that it's more expensive than
        ##  the house option (discounted by 92%)
        ##print "Into UtilityMaximize"
        price2 = 1000000000000000000000000.0
        saveLi = []
        refPrice = 7
        refAvail = 6
        searchPattern = 1##For rent
        found = False
        if buy == True:
            refPrice = 8
            refAvail = 5
            searchPattern = 0
        while found==False and searchPattern<2:
            if searchPattern == 1:
                refPrice = 7## If couldn't find house to buy, look again for house to rent
            for house in self.houseDic:
                ##print "Into houseDic Loop"
                houseLi = self.houseDic[house]
                if float(houseLi[refPrice])>0 and int(houseLi[refAvail])==1:
                    ##print houseLi[refPrice]
                    if refPrice == 7 and float(houseLi[refPrice])>float(maxRent):
                        priceWeighted = 100000000000000000000000000000000.0##Don't even try
                    if refPrice == 8:
                        priceWeighted = self.findWeights(prefLi,houseLi,refPrice)
                    if refPrice == 7 and float(houseLi[refPrice])<=float(maxRent):
                        priceWeighted = self.findWeights(prefLi,houseLi,refPrice)
                        ##print priceWeighted
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
        ##fout2.write(str([0])+"\t"+str(prefLi)+"\t"+str(HTWeight)+"\t"+str(BRWeight)+"\t"+str(priceWeighted)+"\t"+str(price2)+"\t"+str(len(houseDic))+"\t"+str(found)+"\t"+str(saveLi[refPrice])+"\t"+str(buy)+"\n")
        ##fout2.close()
        return saveLi               



#####################################################################
## Initialize data
    def createHHDic(self,houseFi):
        fi = open(houseFi)
        fiObj = fi.read()
        fi.close()
        fiObjLi = fiObj.split("\n")
        ##print "Number of entries in house file: ",len(fiObjLi)
        rowCount = 0
        for row in fiObjLi:
            rowLi = row.split("\t")
            if len(rowLi)>1 and rowCount>0:
                try:
                    self.houseDic[str(rowLi[0])]
                    print "OVERWRITING!!!"
                except KeyError:
                    self.houseDic[str(rowLi[0])]=rowLi
                ##print rowLi[0]
            rowCount = rowCount+1    
        


######################################################################
## Marriage
    def findMarriageBuckets(self,newIndLi):
        bachelorLi = []
        bacheloretteLi = []
        allUnmarriedLi = []
        for personName in newIndLi:
            ##Filters into bachelor or bachelorrette bucket if unmarried
            ## and over 18
            ##print self.fullPopDic[personName]
            person = self.fullPopDic[str(personName)]
            ##print person
            ##if len(person)<2:
                ##print len(person), personName
##            try:
##                int(person[2])
##            except ValueError:
            try:
                if str(person[7])=="888888888" and int(person[2])==1 and int(person[1])>=18:
                    bachelorLi.append(person)
                    allUnmarriedLi.append(person)
                    ##print "New bachelor!"
                if str(person[7])=="888888888" and int(person[2])==0 and int(person[1])>=18:
                    bacheloretteLi.append(person)
                    allUnmarriedLi.append(person)
                    ##print "New bachelorette!"
            except IndexError:
                print "Empty PopLi syndrome",personName
        ##print len(bachelorLi)
        ##print len(bacheloretteLi)
        return bachelorLi,bacheloretteLi,allUnmarriedLi    

######################################################################
## Create Person
    ##DO NOT USE
    def matchInitial(self,unmatchedLi,unmatchedDic):##Finds matches for unmatched households, only initially though, not for use laer
        for entry in unmatchedDic:
            hhLi = unmatchedDic[entry]
            if len(hhLi[3])>1:
                print "Homeless married couple:",hhLi
            self.findRoomie(unmatchedLi,self.fullPopDic[str(hhLi[3][0])])##NEEDS TO SEND "FINDROOMIE" popLi, not HHLI
    ##DO NOT USE
            
    def assignSingleHH(self):
        for person in self.fullPopDic:
            personLi = self.fullPopDic[str(person)]
            try:
                personLi[10]
            except IndexError:
                pass
                ##print personLi
            if personLi[10]=="NoHH":
                hhID =str(personLi[10])+"_singleHH"
                HHType = 1
                HHFormedDate = "PRE"
                adultNames = []
                adultNames.append(str(person))
                childNames = []
                address = "999999999"
                tryNew = True
                countNames = 0
                while tryNew == True:
                    try:
                        value = self.hhDic[str(hhID)]
                        print "Duplicate in Single HHID"
                        hhID = str(hhID)+"_"+countNames
                    except KeyError:
                        tryNew = False
                self.hhDic[str(hhID)]=[str(hhID),HHType,HHFormedDate,adultNames,childNames,address]
                    


    def createIndividual(self,newIndLi):
        nameExists = True
        nNames=0
        newName = str(self.year)+"-"+str(len(self.fullPopDic))
        while nameExists==True:
            try:
                dump = self.fullPopDic[str(newName)]
                newName = newName+"."+str(nNames)
            except KeyError:
                nameExists=False
            nNames+=1
        ##print newName
        personLi = [str(newName)]##ID
        personLi.append(self.findAge(False))##Age
        personLi.append(self.findSex())##Sex
        personLi.append(self.findRace())##Race
        personLi.append(self.studentStatus(personLi[1]))##Student Status
        personLi.append(self.jobType(personLi[1]))##Jobtype
        personLi.append(self.income(personLi[1]))##Income
        
        partnerLi,personLi,hhLi = self.marriedOrNo(personLi)##PersonLi comes back with spouse name
        
        self.fullPopDic[str(newName)]=personLi##Saves list
        newIndLi.append(newName)
        
        if len(partnerLi)>0:
            newIndLi.append(partnerLi[0])
            self.fullPopDic[str(partnerLi[0])] = partnerLi
        ##Then we go through and create hh
        return newIndLi

    def marriedOrNo(self,popLi):
        ##Test probability of marriage
        marriage = False
        if random()<self.allSubAreaStatsDic[1]["perMarried"] and int(popLi[1])>=18:##Try to marry or no
            marriage = True
        hhLi = []
        partnerLi = []
        alreadyMarried = False
        try:
            partner = self.marriedDic[popLi[0]]
            alreadyMarried = True
        except KeyError:
            pass
        if marriage == True and alreadyMarried == False:
            partnerLi = self.createAdultToMarry(popLi)
            partnerLi[7]=popLi[0]
            popLi.append(partnerLi[0])
            popLi.append(["777777777"])
            popLi.append("888888888")##Assume no previous marriages
            nameHH = str(popLi[0])+"_M_"+str(partnerLi[0])
            hhLi = [nameHH,2,"PRE",[popLi[0],partnerLi[0]],[],"999999999"]##HH starts homeless
            popLi.append(nameHH)
            partnerLi[10]=nameHH
            self.marriedDic[partnerLi[0]] = popLi[0]
            self.marriedDic[popLi[0]] = partnerLi[0]
        if marriage == False and alreadyMarried == False:
            nameHH = str(popLi[0])+"_singleHH"
            hhLi = [nameHH,1,"PRE",[popLi[0]],[],"999999999"]
            popLi.append("888888888")##Unmarried
            popLi.append(["777777777"])
            popLi.append("888888888")
            popLi.append(nameHH)
        if alreadyMarried == True:
            partnerLi = self.fullPopDic[partner]
            popLi.append(partner)
            popLi.append(["777777777"])
            popLi.append("888888888")##Assume no previous marriages
            hhLi = self.hhDic[partnerLi[10]]
            popLi.append(hhLi[0])
        self.hhDic[hhLi[0]] = hhLi
        return partnerLi,popLi,hhLi

    def createAdultToMarry(self,popLi):
        nameExists = True
        nNames = 0
        newName = str(self.year)+"-"+str(len(self.fullPopDic)+1)
        if int(popLi[2])==1:
            sex = 0
        if int(popLi[2])==0:
            sex = 1
        while nameExists == True:
            try:
                dump = self.fullPopDic[str(newName)]
                newName = newName+"."+str(nNames)
            except KeyError:
                nameExists = False
            nNames+=1
        personLi = []
        personLi.append(newName)##ID
        personLi.append(self.findAge(True))
        personLi.append(sex)
        personLi.append(self.findRace())
        personLi.append(self.studentStatus(personLi[1]))
        personLi.append(self.jobType(personLi[1]))
        personLi.append(self.income(personLi[1]))
        personLi.append("888888888")
        personLi.append(["777777777"])
        personLi.append("888888888")
        personLi.append(str(newName)+"_singleHH")
        return personLi
        

    def createHH(self,name_per,indic):
        nameHH = str(self.year)+"-"+self.fullPopDic[str(name_per)][10]
        ##print nameHH
        HHType = 1
        
        HHFormedDate = "PRE"
        if indic==False:
            HHFormedDate = self.year
        adultNames = []
        adultNames.append(name_per)
        childNames = []
        address = "999999999"
        nameExists = True
        nNames = 0
        while nameExists == True:
            try:
                value = self.hhDic[str(nameHH)]
                nameHH = str(nameHH)+"."+str(nNames)
                ##print "Duplicate in Single HHID"
            except KeyError:
                nameExists = False
            nNames+=1
        self.fullPopDic[str(name_per)][10]=nameHH
        self.hhDic[str(nameHH)]=[str(nameHH),HHType,HHFormedDate,adultNames,childNames,address]
        return nameHH


    def useProbLiLogic(self, li):
        ##print li
        continueQ = True
        while continueQ==True:
            randVal = random()
            bottomProb = 0.0
            count = 1
            for val in li:
                topProb = float(val)+bottomProb
                ##print bottomProb, randVal, topProb
                if randVal>=bottomProb and randVal<=topProb:
                    ##print bottomProb,randVal,topProb
                    continueQ=False
                    return randVal,count
                count+=1
                bottomProb = topProb

    def findAge(self,adult):
        liAges = {1:[18,25],2:[26,35],3:[36,45],4:[46,55],5:[56,65],6:[66,75],7:[75,100]}
        valueLi = self.allSubAreaStatsDic[1]["AvgAge"]
        ##print self.valueLi
        randVal,listLoc = self.useProbLiLogic(valueLi)
        bot = liAges[listLoc][0]
        top = liAges[listLoc][1]
        age = int((random()*(top-bot))+bot)
        return age

    def findSex(self):
        sex = 1##Male
        if random()>.5:
            sex = 0
        return sex

    def findRace(self):
        perWhite = self.allSubAreaStatsDic[1]["PerWhite"]
        race = 0##White
        if random()>perWhite:
            race = 1##Not White
        return race

    def studentStatus(self,age):
        ageLi = [[18,25],[26,35],[36,45],[46,55],[55,100]]
        valueLi = self.allSubAreaStatsDic[1]["perStudents"]
        ##print valueLi
        status = 0
        count = 0
        if age>17:
            for ageSet in ageLi:
                if age>=ageLi[count][0] and age<=ageLi[count][1]:
                    prob = valueLi[count]
                    ##print prob
                    if random()<prob:
                        status = 1
                count+=1
        return status

    def jobType(self,age):
        if age<18:
            return 0
        job = 0
        if random()>self.allSubAreaStatsDic[1]["areaUnemployment"]:
            job = 1
        if age>65:
            job=2
        return job

    def income(self,age):##From census - http://factfinder2.census.gov/faces/tableservices/jsf/pages/productview.xhtml?src=bkmk
        avgIncomeLi = [.161,.056,.151,.113,.119,.141,.1,.101,.029,.03]
        ## NOTE: Does not assume students have a diff income distro
        if age<18:
            return 0
        incomeRand = random()
        if incomeRand<=.161:
            rangeDif = 9.9-0
            incomeRand = random()
            income = int((incomeRand*rangeDif)*1000)
            return income
        if incomeRand<=.217:
            rangeDif = 14.9-10
            incomeRand = random()
            income = int(((incomeRand*rangeDif)+10)*1000)
            return income
        if incomeRand<=.368:
            rangeDif = 24.9-15
            incomeRand = random()
            income = int(((incomeRand*rangeDif)+15)*1000)
            return income
        if incomeRand<=.481:
            rangeDif = 34.9-25
            incomeRand = random()
            income = int(((incomeRand*rangeDif)+25)*1000)
            return income
        if incomeRand<=.6:
            rangeDif = 49.9-35
            incomeRand = random()
            income = int(((incomeRand*rangeDif)+35)*1000)
            return income
        if incomeRand<=.741:
            rangeDif = 74.9-50
            incomeRand = random()
            income = int(((incomeRand*rangeDif)+50)*1000)
            return income
        if incomeRand<=.841:
            rangeDif = 99.9-75
            incomeRand = random()
            income = int(((incomeRand*rangeDif)+75)*1000)
            return income
        if incomeRand<=.942:
            rangeDif = 149.9-100
            incomeRand = random()
            income = int(((incomeRand*rangeDif)+100)*1000)
            return income
        if incomeRand<=.971:
            rangeDif = 199.9-150
            incomeRand = random()
            income = int(((incomeRand*rangeDif)+150)*1000)
            return income
        if incomeRand>.971:
            rangeDif = 300-200
            incomeRand = random()
            income = int(((incomeRand*rangeDif)+200)*1000)
            return income

    def findProbMarriage(self,guy,person):
        try:
            ageDiff = ((guy[4]-person[4])/float(person[4]))/10.0
        except ZeroDivisionError:
            ageDiff = 0
        ##Gives diminising prob of marriage as age dif
        ## increases - percentage difference/10.0
        prPickAge = 1-abs(ageDiff)
        if random()<=prPickAge:
            return True
        return False

    def createMarriages(self,newIndLi):
        tempMarriages = {}
        bachelorLi,bacheloretteLi,allUnmarriedSearchLi = self.findMarriageBuckets(newIndLi)
        print "Length bachelor li",len(bachelorLi)
        print "Length bachelorette li",len(bacheloretteLi)
        allUnmarriedSearchLi = bachelorLi+bacheloretteLi
        print "Total unmarried li",len(allUnmarriedSearchLi)
        sexLi = [bachelorLi,bacheloretteLi]
        countUnmar = 0
        for person in allUnmarriedSearchLi:##Everyone in list
            ##print person[7]
            if str(person[7])=="888888888":##If un-married continue, otherwise pass
                ##print "Unmarried..."
                if random()<self.allSubAreaStatsDic[1]["perMarried"] and int(person[1])>=18:##Try to marry or no
                    ##print "Chosen to marry!"
                    ty = sexLi[person[2]]##Selects list type... bachelor or bachelorette... opposite of marrying sex
                    personHH = person[10]##Household to start
                    personHHLi = self.hhDic[str(personHH)]##Household list to start
                    personHHAdult = personHHLi[3]##Name of adults in hh
                    personHHKid = personHHLi[3]##Name of kids in hh
                    if len(ty)>0:##Continue if the bachelor/bachelorette list is not empty
                        countNoob = 0##People 'courted'
                        ##print "List was sufficiently long to run"
                        for noob in ty:##Person on unmarried list
                            indic = self.findProbMarriage(noob,person)##How compatible are people
                            ##print "Tested compatibility"
                            if indic == True:##If findProbMarriage = True
                                print "WEDDING!!!"
                                try:
                                    noobHHLi = self.hhDic[noob[10]]##Fiance hh list
                                except KeyError:
                                    print noob
                                    print person
                                noobHHAdult = noobHHLi[3]##Fiance hh adults
                                noobHHKid = noobHHLi[4]##Fiance hh kids
                                ALLAdult = personHHAdult+noobHHAdult##All adults
                                ALLKid = personHHKid+noobHHKid##All kids
                                self.fullPopDic[str(noob[0])][7]=person[0]##Change name in "married to" for fiance
                                self.fullPopDic[str(person[0])][7]=noob[0]##Change name in "married to" for courter
                                self.fullPopDic[str(person[0])][4]=1##Change marriage status for courter
                                self.fullPopDic[str(noob[0])][4]=1##Change marriage status for fiance
                                ##Find new houshold name##
                                newName = str(self.year)+"-"+str(person[0])+"_M_"+str(noob[0])
                                nameExists = True
                                nNames = 0
                                while nameExists == True:
                                    try:
                                        waste = self.hhDic[str(newName)]
                                        newName = newName+"."+str(nNames)
                                    except KeyError:
                                        nameExists = False
                                ##########################
                                tempLi = [newName,2,"PRE",ALLAdult,ALLKid,"999999999"]##New hh list
                                tempMarriages[str(tempLi[0])]=tempLi##Save to temp marriages dic, for babymaker function
                                try:
                                    sexLi[int(self.fullPopDic[str(person[0])][2])].remove(noob[0])##Remove from unmarriedLi
                                except ValueError:
                                    print "Not on list of unmarried"
                                try:
                                    sexLi[int(self.fullPopDic[str(noob[0])][2])].remove(person[0])
                                except ValueError:
                                    print "Not on list of unmarried"
                                countNoob-=1
                                self.hhDic[str(noob[10])][2]="DEAD!"
                                self.makeRentalAvailable(str(self.hhDic[str(noob[10])][5]))
                                self.hhDic[str(person[10])][2]="DEAD!"
                                self.makeRentalAvailable(str(self.hhDic[str(person[10])][5]))
                                ##del self.hhDic[str(person[10])]
                                for adult in ALLAdult:
                                    self.fullPopDic[str(adult)][10]=newName
                                for kid in ALLKid:
                                    self.fullPopDic[str(kid)][10]=newName
                                print "Marriage complete!"
                                break
                            countNoob+=1
            countUnmar+=1
        print "Number of marriages = ",len(tempMarriages)
        return tempMarriages

    def babyMaker_new(self,popLi):
        name = str(self.year)+"-"+str(popLi[0])+"_"+str(popLi[7])+"_KID_"+str(self.year)
        age = 0
        sex = 0
        if random()>.5:
            sex = 1
        race = self.findRace()
        studentStatus = 0
        jobType = 0
        income = 0
        spouseName = "888888888"
        kidName = ["777777777"]
        prevMarriage = "888888888"
        momHHID = popLi[10]
        dadHHID = self.fullPopDic[str(popLi[7])][10]
        if str(momHHID)!=str(dadHHID):
            print "ERROR: Parent HH DOES NOT EXIST, error in 'babyMaker_new'"
        hhID = popLi[10]
        hhLi = self.hhDic[hhID]
        if str(hhLi[2])=="DEAD!":
            print "THIS HOUSEHOLD IS ALREADY DEAD!!\n",popLi
        nameExists = True
        while nameExists == True:
            try:
                value = self.fullPopDic[str(name)]
                name = str(name)+"_"+str(self.year)
            except KeyError:
                nameExists = False
        saveLi = [name,age,sex,race,studentStatus,jobType,income,spouseName,kidName,prevMarriage,hhID]
        return saveLi

    def babyMaker(self,hh,tempMarriages):
        kidLi = []
        kidsOrNo = False
        if random()>.8:##Kids make up about 22% of OR population according to 2012 CPS (Census) survey
            kidsOrNo = True
        if kidsOrNo==True:
            nKids = int(random()*5)
            
            countKids = 0
            while countKids<nKids:
                name = str(hh)+"_KID_"+str(countKids)
                age = int(random()*18)
                sex = 0
                if random()>.5:
                    sex=1
                race = self.findRace()
                studentStatus = 0
                jobType = 0
                income = 0
                spouseName = 888888888
                kidName = [777777777]
                address = tempMarriages[hh][5]
                hhID = hh
                nameExists = True
                nNames = 0
                while nameExists==True:
                    try:
                        value = self.fullPopDic[str(name)]
                        name = str(name)+"."+str(nNames)
                    except KeyError:
                        nameExists=False
                    nNames+=1
                self.fullPopDic[str(name)]=[name,age,sex,race,studentStatus,jobType,income,spouseName,kidName,"888888888",hhID]
                kidLi.append(name)
                countKids+=1
        return kidLi


    def createHH_Original(self,newIndLi):
        ##print "Entered into marriage section"
        ##tempMarriages = self.createMarriages(newIndLi)
        tempHH = {}
        for ind in newIndLi:
            tempHH[self.fullPopDic[ind][10]]=self.hhDic[self.fullPopDic[ind][10]]
        for hh in tempHH:
            ##print tempHH[hh]
            babiesLi = self.babyMaker(hh,tempHH)
            ##print len(babiesLi)
            tempHH[hh][4]=babiesLi
            ##print tempHH[hh]
            self.hhDic[hh]=tempHH[hh]
            for per in tempHH[hh][3]:
                self.fullPopDic[str(per)][10]=hh
                self.fullPopDic[str(per)][8]=babiesLi
            for kid in tempHH[hh][4]:
                self.fullPopDic[str(kid)][10]=hh

    def createNewPop(self):
        self.fullPopDic = {}
        self.delHH = []
        self.hhDic = {}
        self.houseDic = {}
        self.scenarioDic = {}
        self.deathDic = {}
        self.availableUnitsDic = {}
        self.studentDic = {}
        self.marriedDic = {}
        countRuns = 0
        ##Creates people, households##
        popC = 0
        while popC<self.allSubAreaStatsDic[1]["population"]:
            newIndLi = self.createIndividual([])##One person at a time, possibly 2 if they get married
            self.createHH_Original(newIndLi)##Up to 5 kids
            kidDic = {}
            for ind in newIndLi:
                for kid in self.fullPopDic[ind][8]:
                    ##print kid
                    if str(kid)!="777777777":
                        ##print kid
                        kidDic[kid]=1
            popC += len(kidDic)+len(newIndLi)
        ###################
        print "Cleaning hh data"
        newHHDic = {}
        for hhID in self.hhDic:
            hh = self.hhDic[hhID]
            if str(hh[2])!="DEAD!":
                newHHLi = []
                newHHLi.append(hh[0])
                newHHLi.append(hh[1])
                newHHLi.append(hh[2])
                newAdultLi = []
                for adult in hh[3]:
                    newAdultLi.append(adult)
                    self.fullPopDic[str(adult)][10]=newHHLi[0]
                newHHLi.append(newAdultLi)
                newKidLi = []
                for kid in hh[4]:
                    newKidLi.append(kid)
                    self.fullPopDic[str(kid)][10]=newHHLi[0]
                newHHLi.append(newKidLi)
                newHHLi.append(hh[5])
            newHHDic[str(newHHLi[0])]=newHHLi
        
        self.hhDic = newHHDic
        print "Checking HH Data"
        self.checkData2()
        self.checkData()
        ##self.assignSingleHH()
        self.createHHDic(self.developDir+self.versionHouses)
        print "Matching houses with households"
        success,hhLi = self.matchHHWithHouse(self.hhDic)
        print "Matching households w/o homes and searching for homes as roomies"
        unmatchedLi,unmatchedDic = self.generateHHUnmatchLi()
        ##print len(unmatchedLi)
        self.matchInitial(unmatchedLi,unmatchedDic)
        ##print len(unmatchedLi)
        print "Writing data out"
        self.writeToData("population")
        self.writeToData("hh")


################################################################
## Developer

    def scenarioDev(self,globalStatDic,allHouseStatDic,searchStat):
        newHouseLi = []
        totalStartAmt = 0
        for entry in allHouseStatDic['rentStatDic']:
            data = allHouseStatDic['rentStatDic'][entry]
            totalStartAmt += data
        perGrowTot = float(self.scenarioDic["perGrow"])/100.0
        nNewHouses = self.scenarioDic["nNewHouses"]##First number in li is percent of other housetypes will be houses, remaining are % of each roomcount per type
        nNewApts = self.scenarioDic["nNewApts"]
        nNewTH = self.scenarioDic["nNewTH"]
        probRoomsH = nNewHouses[1:len(nNewHouses)]
        probRoomsA = nNewApts[1:len(nNewApts)]
        probRoomsTH = nNewApts[1:len(nNewTH)]
        htProbRoomLi = [probRoomsA,probRoomsTH,probRoomsH]
        totalNewDev = float(totalStartAmt)*perGrowTot
        "Total new development:", totalNewDev
        
        ##totalNewH = int(float(totalNewDev)*(float(nNewHouses[0])/100.0))
        ##totalNewA = int(float(totalNewDev)*(float(nNewApts[0])/100.0))
        ##totalNewTH = int(float(totalNewDev)*(float(nNewTH[0])/100.0))
        countUnit = 0
        while countUnit <= totalNewDev:
            ht = None
            while ht==None:
                ht = self.chooseHT(float(float(nNewHouses[0])/100.0),float(float(nNewApts[0])/100.0),float(float(nNewTH[0])/100.0))
            nBR = None
            while nBR==None:
                nBR = self.chooseRooms(htProbRoomLi[int(ht)-1])
            addy = str(self.year)+"_"+str(ht)+"_"+str(countUnit)
            location = 1
            rentable = 1
            forSale = 0
            forRent = 1
            rentPrice = self.findRent(globalStatDic,ht,nBR,allHouseStatDic,searchStat)
            salePrice = 0
            newHouseLi.append([addy,location,ht,rentable,nBR,forSale,forRent,rentPrice,salePrice])
            countUnit+=1        
        return newHouseLi

    def chooseHT(self,probH, probA, probTH):
        probLi = [probA,probTH,probH]
        countTries = 0
        htRand = random()
        probSum = 0.0
        while countTries<len(probLi):
            prob = float(probLi[countTries])/100.0
            probBottom = probSum
            probTop = probSum+prob
            if htRand<=probTop and htRand>probBottom:
                return countTries+1
            probSum+=prob
            countTries+=1

    def chooseRooms(self,probLi):
        roomRand = random()
        countTries = 0##Tells us which probability to retrieve, and also the total number of rooms
        probSum = 0.0
        while countTries<len(probLi):
            prob = float(probLi[countTries])/100.0
            probBottom = probSum
            probTop = probSum+prob
            if roomRand<=probTop and roomRand>probBottom:
                return countTries+1
            probSum+=prob
            countTries+=1

    def findRent(self,globalStatDic,ht,nBR,allHouseStatDic,searchStat):
        ##CURRENTLY USED TO SET NEW HOME PRICES
        htLi = ["HOMELESS","A","TH","H"]
        nDemand = searchStat[0]
        nUnmetD = int(searchStat[1])
        nSupplied = self.startAvail
        priceChangeValue = nDemand/nSupplied
        priceChangeValue -= 1.0 ## This makes oversupply values decrease prices and undersupply increase
        ## E.g. if 300 demanded and 100 supplied, priceChangeValue = 2.0... prices increase by 2xSt.Dev
        ##  if 300 demanded and 600 supplied, priceChangeValue = -.5... prices decrease by -.5xSt.Dev
        ##difUnmet = nUnmetD-nSupplied
        ##priceChangeValue = float(difUnmet)/1000.0##1000 arbitrary, should do as percent (100%)
##        if priceChangeValue>1.0:
##            priceChangeValue = 1.0##Stops at 1000% change, so prices can't go up by 10x
##        if priceChangeValue<1.0:
##            priceChangeValue = -1.0
        rentPriceDicRemain = globalStatDic["rentAvgPriceDic"]
        rentStDevDicRemain = globalStatDic["rentStDev"]
        rentCountDicRemain = globalStatDic["rentStatDic"]
        rentPriceDicAll = allHouseStatDic["rentAvgPriceDic"]
        rentStDevDicAll = allHouseStatDic["rentStDev"]
        rentCountDicAll = allHouseStatDic["rentStatDic"]
        rentPrice = 0
        if int(nBR)!=0 and str(ht)!="HOMELESS":
            key = str(int(nBR))+"BR"+str(htLi[int(ht)])
            baselineRent = rentPriceDicAll[key]
            stDev = rentStDevDicAll[key]
            rentPrice = baselineRent+((2*stDev)*priceChangeValue)
        ##print ht,":",nBR
        ##print baselineRent,"+(",StDev,"*",rand,")=",rentPrice
        ##Temporarily set at baselineRent
        return rentPrice


################################################################
## Statistics
    def findPrices(self,tempDic):
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

        for unit in tempDic:
            unitLi = tempDic[str(unit)]
            if str(unitLi[0])!="999999999" and str(unitLi[0])!="999999998":
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
                try:
                    key = str(BR)+"BR"+str(keyDicHT[str(HT)])
                except KeyError:
                    print "Key error:",unitLi
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
        globalStatDic = self.getAvgs(globalStatDic)
        globalStatDic = self.getSqError(globalStatDic,keyDicHT)
        globalStatDic = self.getStDev(globalStatDic)
        print "Number of Units",countUnits
        return globalStatDic


    def getStDev(self,globalStatDic):
        for el in ["rent","sale"]:
            for key in globalStatDic[el+"SumSqE"]:
                numerator = globalStatDic[el+"SumSqE"][key]
                n = globalStatDic[el+"StatDic"][key]
                denominator = n-1
                try:
                    stDevSquared = numerator/denominator
                except ZeroDivisionError:
                    stDevSquared = 0.0
                try:
                    stDev = stDevSquared**0.5
                except ValueError:
                    stDev = 0##For if there are no units (n-1) = -1
                globalStatDic[el+"StDev"][key]=stDev
                ##print el+"StDev"
                ##print stDev
        return globalStatDic

    def getSqError(self,globalStatDic,keyDicHT):
        for unit in self.availableUnitsDic:
            unitLi = self.availableUnitsDic[unit]
            if str(unitLi[0])!="999999999" and str(unitLi[0])!="999999998":
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
                    sqError = (x-x_bar)*(x-x_bar)
                    ##print "(",x,"-",x_bar,")^2=",sqError
                except OverflowError:
                    print "getSqError Error",x,"-",x_bar," ",key,"\n",globalStatDic[keyStats+"AvgPriceDic"]
                globalStatDic[keyStats+"SumSqE"][key]+=sqError
        return globalStatDic

    def getAvgs(self,globalStatDic):
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

#################################################################
## Initialize

    def initializeDeathRate(self):
        deathDic = {}
        data = open(self.popDir+"deathRate.txt")
        dataObj = data.read()
        data.close()
        dataObjLi = dataObj.split("\n")
        for age in dataObjLi:
            ageLi = age.split("\t")
            if len(ageLi)>1:
                deathDic[ageLi[0]]=float(ageLi[1])
        self.deathDic = deathDic

    def readInData(self):
        self.readInPop()
        self.readInHH()

        self.createHHDic(self.developDir+self.versionHouses)
        self.readInScenario()
        self.initializeDeathRate()
        self.availableUnitsCount()
        self.checkData()
        self.checkData2()

    def checkData2(self):
        for per in self.fullPopDic:
            popLi = self.fullPopDic[per]
            if str(popLi[7])!="888888888" and int(popLi[1])<18:
                print "UNDERAGE MARRIAGE"
        
    def checkData(self):
        popDicKeys = self.fullPopDic.keys()
        for per in self.fullPopDic:
            popLi = self.fullPopDic[per]
            try:
                hhLi = self.hhDic[str(popLi[10])]
                if str(popLi[7])!="888888888" and len(hhLi[3])<2:
                    print "Problem with initial read in data - marriage, but no spouse in hh"
                    print popLi
                    print self.fullPopDic[popLi[7]]
                    print hhLi
                    print self.hhDic[self.fullPopDic[popLi[7]][10]]
            except KeyError:
                if str(popLi[10])!="999999999":
                    print "Household has been deleted:\n",popLi


    def readInScenario(self):
        scenarioDic = {}
        data = open(self.scenarioDir+self.versionScenario)
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
        self.scenarioDic = scenarioDic

    def readInPop(self):
        pathPop = self.popDir+self.versionPop
        self.fullPopDic = self.turnToDic(pathPop)
        for entry in self.fullPopDic:
            self.fullPopDic[entry].append("999999999")##Says that everyone is not a student
            self.fullPopDic[entry].append(0)##Says that everyone's status is "alive"

    def readInHH(self):
        pathHH = self.popDir+self.versionHH
        self.hhDic = self.turnToDic(pathHH)

    def turnToDic(self,path):
        tempDic = {}
        fi = open(path)
        fiObj = fi.read()
        fi.close()
        fiObjLi = fiObj.split("\n")
        ##print "Number of entries in house file: ",len(fiObjLi)
        rowCount = 0
        for row in fiObjLi:
            rowLi = row.split("\t")
            if len(rowLi)>1 and rowCount>0:
                try:
                    tempDic[str(rowLi[0])]
                    print "OVERWRITING!!!"
                except KeyError:
                    countRowLi = 0
                    for item in rowLi:
                        if item.startswith("["):
                            item = item.replace("[","")
                            item = item.replace("]","")
                            item = item.replace("'","")
                            item = item.replace('"',"")
                            itemLi = item.split(", ")
                            if len(itemLi)!=0:
                                item = itemLi
                        if item!="":
                            rowLi[countRowLi]=item
                        if item=="":
                            del rowLi[countRowLi]
                        countRowLi+=1
                    tempDic[str(rowLi[0])]=rowLi
                ##print rowLi[0]
            rowCount = rowCount+1
        return tempDic

#######################################################################
root = []
myApp = fullModel(root)
