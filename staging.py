#importing the libraries
import os
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

#global definitions
firstcolumn=[]
secondcolumn=[]
tempsecond=[]
dictdataframe=[]
metadatalist = []
metadatadict = {}
filenm=[]
flag=True
flagseven=True

#define the path containing th datasets
path = "C:/Users/karth/Downloads/project/SMD2022_Project/code/Dataset1_VM_BlindedAndReduced/VMData_Blinded"
path2 = "C:/Users/karth/Downloads/project/SMD2022_Project/code/Dataset2_PreAutism_BlindedAndReduced/PreAutismData_Blinded"

#function for parsing VM dataset's Data part to dictionary
def vmmeta(filename):
    csvread = pd.read_csv(filename)
    metadatalist.append(csvread)
    for md in metadatalist:
        for i in range(17):
            firstcolumn=md.iloc[0:17,0].tolist()
            secondcolumn=md.iloc[0:17,1].tolist()
            metadatadict[firstcolumn[i]] = secondcolumn[i]
            metadatadict[firstcolumn[11]] = md.iloc[11,1:3].tolist()
            metadatadict[firstcolumn[15]] = md.iloc[15,0:20].tolist()
            #metadatadict[firstcolumn[2]] =  secondcolumn[2][:-1]
    print("\n The parsed VM metadata dictionary is:\n",metadatadict)
    tempsecond.append(secondcolumn)
    filenm.append(filename)
    return metadatadict    

#function for parsing Pre-autism dataset files (.evt,.dat,.wl1,.wl2)
def parser(filename,flagseven):
    parsedlist=[]
    datalist=[]
    with open(filename, 'r') as file:
        tempfile = file.read()
        parselist = tempfile.split(",")
        parselist = [p.replace('\n', ',').replace('\t', ',') for p in parselist]
        if (filename.endswith('dat') == True) or (filename.endswith('wl1') == True) or (filename.endswith('wl2') == True) :
            datalist=(parselist[0].split(" "))
            datalist[-1] = datalist[-1][:-1]
            for data in datalist:
                try:
                    parsedlist.append(float(float(data)))
                except:
                    pass
            if flagseven:
                sixthquery(parsedlist)
            #print("\n The list parsed from the file is:\n",parsedlist)
        if filename.endswith('evt') == True:
            evtlist=(parselist[0].split(",")[:-1])
            for evt in evtlist:
                    parsedlist.append(int(int(evt)))
            print("\n The list parsed from the file is:\n",parsedlist)
        return parsedlist

#function for plotting first query
#Query1: Individual plotting of the time course of light raw intensity at some wavelength, HbO2 or HbR forsome channel.
def firstqueryplot(ch7,time):
    plt.tick_params(left = False, right = False , labelleft = False ,
            labelbottom = False, bottom = False)
    plt.scatter(time,ch7)
    plt.ylabel("CHANNEL 7")
    plt.xlabel("Time")
    plt.show()

#function for creating required lists for third query
#Query3: A listing of experiments in the database accompanied by the list of factors and treatments given.
def thirdquery(csvlist):
    explist=[]
    facttreatlist=[]    
    for fcsv in csvlist:
        explist.append(fcsv.split("\\")[-1][12:22])
        if(fcsv.endswith("Deoxy.csv")):
            facttreatlist.append(fcsv.split("\\")[-1][23:28] + fcsv.split("\\")[-1][6:11])
        if(fcsv.endswith("Oxy.csv")):
            facttreatlist.append(fcsv.split("\\")[-1][23:26] + fcsv.split("\\")[-1][6:11])
    explist = list(set(explist))  
    facttreatlist = list(set(facttreatlist))      
    print("\n Query3a: The list of names of experiments in the treatments in the database is:\n",explist)
    print("\n Query3b: The list of names of factors and treatments in the database is:\n",facttreatlist)
        
#function for plotting box plot for sixth query
# Query6: A boxplot comparing the distribution of either HbO2 or HbR concentrations for two intervals of time for a subject.
def sixthquery(parsedlist):
    plt.boxplot(parsedlist)
    plt.show()
    
#function for parsing VM dataset's metadata into dictonary
def funcdictvm(filename,current,flag):
        vmread = pd.read_csv(filename,header=None)
        vmheader = vmread.iloc[current-1,0]
        vmdata=[vmheader,"CH1","CH2","CH3","CH4","CH5","CH6","CH7","CH8","CH9","CH10","CH11","CH12","CH13","CH14","CH15","CH16","CH17","CH18","CH19","CH20","CH21","CH22","CH23","CH24","Mark","Time","BodyMovement","RemovalMark","PreScan"]
        dictvm = vmread.iloc[current:,0:30]
        dictvm.columns = vmdata
        ch7 = dictvm["CH7"].to_numpy()
        time = dictvm["Time"].to_numpy()    
        if(flag):
            firstqueryplot(ch7,time)
            flag=False
        #print("\n The parsed VM data is:\n",dictvm)
        return dictvm

#find the postion of the current file being parsed
def currentfile(filename):
    with open(filename) as csvfile:
        csvlines = csvfile.readlines()
        for line in csvlines:
            if "Data" in line:
                current = csvlines.index(line)+2
                return current

#changing path to VM Dataset's location
os.chdir(path)
#Running through all the files in the directory and looking for csv files
for subdirectory, directory, files in os.walk(path):
    csvlist = []
    l=[]
    for f in files:
        if f.endswith('.csv'):
            csvlist.append(os.path.join(subdirectory,f))

    for fcsv in csvlist:
        current = currentfile(fcsv)
        vmmetadata=vmmeta(fcsv)
        fdict = funcdictvm(fcsv,current,flag)
        flag = False
        
    thirdquery(csvlist)    

#changing path to Pre-autism Dataset's location
os.chdir(path2)
#Running through all the files in the directory
for subdirectory, directory, files in os.walk(path2):
    for f in files:
        path2 = os.path.join(subdirectory, f)
        parser(path2,flagseven)
        if (path2.endswith('dat') == True):
            flagseven=False

#establishing connection between python and postgresql
dbconnect = psycopg2.connect(
    database="smdvault",
    user='smd',
    password='smd2022',
    host='localhost',
    port='5432'
)

#autocommit for committing all the changes automatically
dbconnect.autocommit = True
#setting up cursor for connecting python and psql
cursor = dbconnect.cursor()

#inserting data from the parsed files into the appropriate tables
for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d]])
    sql2='''insert into smdvaultschema.HubExperiment(sequence , timestamp ,
          source) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to HubExperiment table successfully...")
    except:
    
        pass


for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d],'title'])
    sql2='''insert into smdvaultschema.SatExperimentTitle(sequence , timestamp ,
          source, title) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to SatExperimentTitle table successfully...")
    except:
        
        pass

for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d],'acronym'])
    sql2='''insert into smdvaultschema.SatExperimentAcronym(sequence , timestamp ,
          source, acronym) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to SatExperimentAcronym table successfully...")
    except:
        
        pass
#not working
for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d]])
    sql2='''insert into smdvaultschema.HubExperimentalUnit(sequence , timestamp ,
          source) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to HubExperimentalUnit table successfully...")
    except:
        
        pass
    
for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d], tempsecond[d][0], tempsecond[d][0]])
    sql2='''insert into smdvaultschema.ParticipatesIn(sequence , timestamp ,
          source, experimentalUnit, experiment) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to ParticipatesIn table successfully...")
    except:
        
        pass

for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d], 'ID'])
    sql2='''insert into smdvaultschema.SatExperimentlUnitIdentifier(sequence , timestamp ,
          source, ID) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to SatExperimentlUnitIdentifier table successfully...")
    except:
        
        pass

for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d], tempsecond[d][0], 'isCofactor'])
    sql2='''insert into smdvaultschema.HubFactor(sequence , timestamp ,
          source, experiment, isCofactor) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to HubFactor table successfully...")
    except:
        
        pass

for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d], 'name'])
    sql2='''insert into smdvaultschema.SatFactorName(sequence , timestamp ,
          source, name) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to SatFactorName table successfully...")
    except:
        
        pass

for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d], 'levelValue'])
    sql2='''insert into smdvaultschema.SatFactorLevel(sequence , timestamp ,
          source, levelValue) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to SatFactorLevel table successfully...")
    except:
        
        pass

for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d], tempsecond[d][0], tempsecond[d][0]])
    sql2='''insert into smdvaultschema.HubTreatment(sequence , timestamp ,
          source, experiment) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to HubTreatment table successfully...")
    except:
        
        pass
    
for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d], tempsecond[d][0]])
    sql2='''insert into smdvaultschema.SatTreatmentFactorLevel(sequence , timestamp ,
          source, factorLevel) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to SatTreatmentFactorLevel table successfully...")
    except:
        
        pass
    
for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d], tempsecond[d][0]])
    sql2='''insert into smdvaultschema.HubGroup(sequence , timestamp ,
          source, treatment) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to HubGroup table successfully...")
    except:
        
        pass

for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d], 'name'])
    sql2='''insert into smdvaultschema.SatGroupName(sequence , timestamp ,
          source, name) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to SatGroupName table successfully...")
    except:
        
        pass

for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d], tempsecond[d][0], tempsecond[d][0]])
    sql2='''insert into smdvaultschema.AssignedTo(sequence , timestamp ,
          source, experimentalUnit, groupp) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to AssignedTo table successfully...")
    except:
        
        pass
    
for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d]])
    sql2='''insert into smdvaultschema.HubSession(sequence , timestamp ,
          source) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to HubSession table successfully...")
    except:
        
        pass

for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d], 'name'])
    sql2='''insert into smdvaultschema.SatSessionName(sequence , timestamp ,
          source, name) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to SatSessionName table successfully...")
    except:
        
        pass
    
for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d], tempsecond[d][0], tempsecond[d][0], tempsecond[d][0]])
    sql2='''insert into smdvaultschema.AttendsSession(sequence , timestamp ,
          source, experimentalUnit, groupp, session) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to AttendsSession table successfully...")
    except:
        
        pass

for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d], tempsecond[d][0]])
    sql2='''insert into smdvaultschema.HubObservation(sequence , timestamp ,
          source, collectedAtsession) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to HubObservation table successfully...")
    except:
        
        pass

for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d], 'name'])
    sql2='''insert into smdvaultschema.SatObservationName(sequence , timestamp ,
          source, name) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to SatObservationName table successfully...")
    except:
        
        pass
    
for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d], [4,2,3,8], tempsecond[d][9]])
    sql2='''insert into smdvaultschema.SatObservationValue(sequence , timestamp ,
          source, value, timestamps) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to SatObservationValue table successfully...")
    except:
        
        pass

for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d]])
    sql2='''insert into smdvaultschema.HubMetaData(sequence , timestamp ,
          source) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to HubMetaData table successfully...")
    except:
        
        pass
    
for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d],tempsecond[d][0],'value'])
    sql2='''insert into smdvaultschema.SatMetaDataKeyValuePair(sequence , timestamp ,
          source, key, value) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to SatMetaDataKeyValuePair table successfully...")
    except:
        
        pass

for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d],tempsecond[d][0], tempsecond[d][0]])
    sql2='''insert into smdvaultschema.SessionMetaData(sequence , timestamp ,
          source, session, metadata) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to SessionMetaData table successfully...")
    except:
        
        pass
    
for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d],tempsecond[d][0], tempsecond[d][0]])
    sql2='''insert into smdvaultschema.ObservationMetaData(sequence , timestamp ,
          source, observation, metadata) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to ObservationMetaData table successfully...")
    except:
        
        pass

for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d],'name'])
    sql2='''insert into smdvaultschema.HubSubject(sequence , timestamp ,
          source, name) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to HubSubject table successfully...")
    except:
        
        pass

for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d],20])
    sql2='''insert into smdvaultschema.SatSubjectAge(sequence , timestamp ,
          source, age) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to SatSubjectAge table successfully...")
    except:
        
        pass

for d in range(len(tempsecond)):
    i = tuple([tempsecond[d][0],tempsecond[d][9],filenm[d],'name'])
    sql2='''insert into smdvaultschema.SatSubjectName(sequence , timestamp ,
          source, name) VALUES{};'''.format(i)
    try:
        cursor.execute(sql2)
        print("List has been inserted to SatSubjectName table successfully...")
    except:
        
        pass

#close connection with database after the operations
dbconnect.close() 