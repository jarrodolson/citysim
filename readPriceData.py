import os

pricesFileName = ".\\Outputs\\Prices_Wed-Jul-25-192908-2012"
fi = open(pricesFileName+".txt")
fiObj = fi.read()
fi.close()

rentPriceDic = {}
rentStatDic = {}
headerLi = []
fiObjLi = fiObj.split("\n")
count = 0
for row in fiObjLi:
    countCol = 0
    rowLi = row.split("\t")
    ##print rowLi
    if count==0:
        for col in rowLi:
            print col
            headerLi.append(col)
    if count!=0 and len(rowLi)>1:
        run = rowLi[0]
        year = rowLi[1]
        name = rowLi[2]
        for col in rowLi:
            colName = headerLi[countCol]
            key = str(colName)+"_"+year
            if str(name)=="rentAvgPriceDic" and countCol>2 and col!="":
                try:
                    value1 = rentPriceDic[key]
                    value2 = value1+float(col)
                    rentPriceDic[key] = value2
                except KeyError:
                    rentPriceDic[key] = float(col)
            countCol += 1
    count += 1

##for column in rentPriceDic:
typeLi = ["A","H","TH"]
fout = open(pricesFileName+"_2.txt","w")
fout.write("Year\tMeasure\t")
year = 0
writeTrue=False
while year<=10:
    if writeTrue == True:
        fout.write(str(year)+"\t"+"RentAvgPrice\t")
    for ty in typeLi:
        roomCount = 1
        while roomCount<=5:
            key = str(roomCount)+"BR"+str(ty)+"_"+str(year)
            try:
                if writeTrue == False:
                    fout.write(str(key)+"\t")
                if writeTrue == True:
                    fout.write(str(rentPriceDic[key]/100)+"\t")
            except KeyError:
                print key,"Not found"
            roomCount+=1
    if writeTrue==True:
        year+=1
        fout.write("\n")
    if writeTrue==False:
        writeTrue=True
        fout.write("\n")
fout.close()

