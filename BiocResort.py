#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import ConfigParser
import collections
import sys
import os
import getopt

def main(myCSVfile):
    #myCSVfile="FIA_FIA_SS_template_test_AB SCIEX_KIT3-0-5604_1015709577-1_1_2017-03-06.csv"
    #myCSVfile="FIA_CHRIS5000_2017-01-31_AB SCIEX_KIT3-0-560401_1015699014-1_1_2017-01-31.csv"
    #myCSVfile="LCMS_CHRIS5000_2017-01-31_AB SCIEX_KIT2-0-5614_1015698998-1_1_2017-01-31.csv"
    #format of injection file:
    #colnum    content
    #   0       sampleNane: plateBarcode_X_Y_ZZ_sampleID, Y=injection number
    #   1       sampleID
    #   7       vialpos
    #   9 or 11       sampletype
    #   12 or 14     setname
    #   13  or 15    outputfile
    myOutfile = myCSVfile[:-4]+"resorted.csv"

    

    # try:
    #     opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    # except getopt.GetoptError:
    #     print "Didn't understand your input. The format should be:"
    #     print 'BiocResort.exe -i <inputfile>'
    #     sys.exit(2)

    # for opt, arg in opts:
    #     if opt in ("-i", "--ifile"):
    #         myCSVfile = arg
    #         myOutfile = myCSVfile[:-4]+"resorted.csv"
    def fixSampletype(myColList):
        sampleID=myColList[1]
        print len(myColList)
        if len(myColList)>22:
            idx=11
        else:
            idx=9
        sampleType=myColList[idx]
        if sampleID=='10000001':
            sampleType='Double Blank'
        elif sampleID=='11000002':
            sampleType='Blank'
        elif sampleID in ('721029','721046','721050'):
            sampleType='QC'
        myColList[idx]=sampleType
        return myColList



    def getEssentials(myColList):
        #print(myColDict)
        #print(len(myColDict))
        outputfile=myColList[13]
        setName=myColList[12]
        vialPos=myColList[7]
        sampleID=myColList[1]
        nameSplit=myColList[0].split("_")
        plateBarcode=nameSplit[0]
        injecionNumber=nameSplit[2]
        return {"outputfile":outputfile, "setName":setName, "sampleID":sampleID, 
            "plateBarcode":plateBarcode, "injectionNumber":injecionNumber, 
            "vialPos":vialPos}

    def getQCseq(workingdict,myperiod,perioddict,usednums):
        retlist=list()
        for onePer in perioddict:
            perioditem=perioddict[onePer]
            if perioditem[0]==myperiod:
                periodIDs=perioditem[2:]
                for oneID in periodIDs:
                    sampl=workingdict[oneID]
                    for vialPos in sampl:
                        foundOne=False
                        for injNum in sampl[vialPos]:
                            for setName in sampl[vialPos][injNum]:
                                oldOrder=sampl[vialPos][injNum][setName]
                                if oldOrder not in usedNums:
                                    #print "QC",oldOrder, oneID, vialPos, injNum, setName
                                    retlist.append(oldOrder)
                                    foundOne=True
                            if foundOne:
                                break
                        if perioditem[1]=="one":
                            break
                        elif perioditem[1]=="each":
                            continue
        return retlist

    #print os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),myOutfile)
    with open(myCSVfile, "rb") as f:
        reader = csv.reader(f, delimiter='\t')
        rownum = 0
        header=""
        rowdict=collections.OrderedDict()
        workingdict=collections.OrderedDict()
        for row in reader:
            if rownum==0:
                header=row
            else:
                colnum=0
                coldict=dict()
                collist=list()
                for col in row:
                    coldict[colnum]=col
                    collist.append(col)
                    colnum+=1
                essent=getEssentials(coldict)
                #coldict.update(essent)
                collist=fixSampletype(collist)
                rowdict[rownum]={'raw':collist,'essent':essent}
                if essent["sampleID"] not in workingdict:
                    workingdict[essent["sampleID"]]=collections.OrderedDict()
                if essent["vialPos"] not in workingdict[essent["sampleID"]]:
                    workingdict[essent["sampleID"]][essent["vialPos"]]=collections.OrderedDict()
                if essent["injectionNumber"] not in workingdict[essent["sampleID"]][essent["vialPos"]]:
                    workingdict[essent["sampleID"]][essent["vialPos"]][essent["injectionNumber"]]=collections.OrderedDict()
                workingdict[essent["sampleID"]][essent["vialPos"]][essent["injectionNumber"]][essent["setName"]]=rownum
                    
            rownum+=1
        f.close()
        maxSet=0
        for sampleID in workingdict:
            sampl=workingdict[sampleID]
            for vialPos in sampl:
                vial=sampl[vialPos]
                #if len(vial)>1:
                    #print sampleID, vialPos, len(vial)
                for injNum in vial:
                    samplCnt=len(vial[injNum])
                    if samplCnt>maxSet:
                        maxSet=samplCnt


        Config = ConfigParser.ConfigParser()
        configFile=os.path.join(os.path.dirname(os.path.abspath(__file__)),"resort.ini")
        if os.path.isfile(configFile):
            print configFile
            Config.read(configFile)
        else:
            configFile=os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),"resort.ini")
            print configFile
            Config.read(configFile)

        
        #print 
        
        newOrder=1
        usedNums=list()

        with open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),myOutfile), "wb") as oF:
            writer = csv.writer(oF, delimiter='\t')
            writer.writerow(header)
            if '20000004' in workingdict:
                #special case of system suitability for FIA
                ss_items=('10000001','20000004')
                totCnt=0
                sampl=workingdict['20000004']
                for vialPos in sampl:
                    totCnt+=len(sampl[vialPos])
                #print totCnt
                for i in range(0,totCnt):
                    for sampleID in ss_items:
                        sampl=workingdict[sampleID]
                        foundOne=False
                        for vialPos in sampl:
                            for injNum in sampl[vialPos]:
                                for setName in sampl[vialPos][injNum]:
                                    oldOrder=sampl[vialPos][injNum][setName]
                                    if oldOrder not in usedNums:
                                        print newOrder, oldOrder, sampleID, vialPos, injNum, setName
                                        writer.writerow(rowdict[oldOrder]['raw'])
                                        usedNums.append(oldOrder)
                                        newOrder+=1
                                        foundOne=True
                                if foundOne:
                                    break
                            if foundOne:
                                break
            else:
                #all other sorting done here
                begin_items = Config.items( "Begin" )
                for sampleID, howMany in begin_items:
                    if sampleID in workingdict:
                        sampl=workingdict[sampleID]
                        if howMany=="all":
                            for vialPos in sampl:
                                for injNum in sampl[vialPos]:
                                    for setName in sampl[vialPos][injNum]:
                                        oldOrder=sampl[vialPos][injNum][setName]
                                        print newOrder, oldOrder, sampleID, vialPos, injNum, setName
                                        writer.writerow(rowdict[oldOrder]['raw'])
                                        usedNums.append(oldOrder)
                                        newOrder+=1
                        elif howMany=="one":
                            for vialPos in sampl:
                                for injNum in sampl[vialPos]:
                                    foundOne=False
                                    for setName in sampl[vialPos][injNum]:
                                        oldOrder=sampl[vialPos][injNum][setName]
                                        if oldOrder not in usedNums:
                                            foundOne=True
                                            print newOrder, oldOrder, sampleID, vialPos, injNum, setName
                                            writer.writerow(rowdict[oldOrder]['raw'])
                                            usedNums.append(oldOrder)
                                            newOrder+=1
                                    if foundOne:
                                        break

                period_items=Config.items( "Periods" )
                periodDict=collections.OrderedDict()
                periodsList=list()
                periodsIDs=list()
                period_cnt=0
                for dum, period in period_items:
                    mySplit=period.split(",")
                    mySplit[0]=str(int(mySplit[0])*maxSet)
                    if mySplit[0] not in periodsList:
                        periodsList.append(mySplit[0])
                    periodDict[period_cnt]=mySplit
                    for oneID in mySplit[2:]:
                        if oneID not in periodsIDs:
                            periodsIDs.append(oneID)
                    period_cnt +=1

                periodsCounter=dict()
                for onePer in periodsList:
                    periodsCounter[onePer]=1

                for sampleID in workingdict:
                    if sampleID not in periodsIDs:
                        sampl=workingdict[sampleID]
                        for vialPos in sampl:
                            vial=sampl[vialPos]
                            for InjectionNum in vial:
                                inj=vial[InjectionNum]
                                for setName in inj:
                                    oldOrder=inj[setName]
                                    if oldOrder not in usedNums:
                                        #put in the sample in the new dict
                                        print newOrder, oldOrder, sampleID, vialPos, injNum, setName
                                        writer.writerow(rowdict[oldOrder]['raw'])
                                        usedNums.append(oldOrder)
                                        newOrder+=1
                                        for onePer in periodsList:
                                            cnt=periodsCounter[onePer]
                                            #print cnt,onePer,cnt==int(onePer)
                                            if cnt % int(onePer) ==0:
                                                #trigger a QC
                                                #print "QC", onePer, cnt
                                                oldorderlist=getQCseq(workingdict,onePer,periodDict,usedNums)
                                                for oneOld in oldorderlist:
                                                    QC=rowdict[oneOld]['essent']
                                                    print newOrder, oneOld, QC["sampleID"], QC["vialPos"], QC["injectionNumber"], QC["setName"]
                                                    writer.writerow(rowdict[oneOld]['raw'])
                                                    usedNums.append(oneOld)
                                                    newOrder+=1

                                            periodsCounter[onePer]+=1

        oF.close()

if __name__ == "__main__":
    argv=sys.argv[1:]
    for myCSVfile in argv:
        main(myCSVfile)                        
                            


