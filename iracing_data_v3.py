#!/user/bin/python3

import os
from bs4 import BeautifulSoup
import re
import json
import pymongo

#modifies database
def modifyDB(value1, value2, value3):
    #mongodb setup
    dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = dbclient["iracing_data"]
    carc = db["iracing_cars"]
    trackc = db["racing_tracks"]
    #car: value1==car value2==numCars value3=="car"
    if value3 is "car":
        #single car getting passed in
        if int(value2) == 1:
            mydict = {value1: {"name": value1,"count": 0,"license": {"rookie": 0,"D license": 0,"C license": 0,"B license": 0,"a license": 0},"tracks": {"trackName": 0}}}
            if carc.find_one({value1:{"$exists":"true"}}) is not None:
                print("y is not none")
            elif carc.find_one({value1:{"$exists":"true"}}) is None:
                x = carc.insert_one(mydict)
        #multiple cars getting passed in
        elif int(value2) > 1:
            carlist = value1.split(", ")
            for car in carlist:
                print(car)
                mydict = {car: {"name": car,"count": 0,"license": {"rookie": 0,"D license": 0,"C license": 0,"B license": 0,"a license": 0},"tracks": {"trackName": 0}}}
                if carc.find_one({car:{"$exists":"true"}}) is not None:
                    print("y is not none")
                elif carc.find_one({car:{"$exists":"true"}}) is None:
                    x = carc.insert_one(mydict)
    #track: value1==track layout value2==track name value3=="track"
    elif value3 is "track":
        mydict = {value2: {"name": value1,"count": 0,"license": {"rookie": 0,"D license": 0,"C license": 0,"B license": 0,"a license": 0},"tracks": {"trackName": 0}}}
        if trackc.find_one({value2:{"$exists":"true"}}) is not None:
            print("y is not none")
        elif trackc.find_one({value2:{"$exists":"true"}}) is None:
            x = trackc.insert_one(mydict)
        
#gathers info of cars
def getCars(file):
    print("getting car data:", file)
    fileString = "C:\\scripting\\iracing_data_v2\\web_data\\"+file
    with open(fileString, encoding=('utf-8')) as fs:
        soup = BeautifulSoup(fs, 'html.parser')
    myParse = soup.findAll(re.compile("tr|td"))
    #print(myParse)
    for i in myParse:
        #1: confirm it's car 2: list of cars 3: total cars
        m1 = re.search(r'<td><i class="(icon-car)"></i></td>\s.*<td class="\w.*\s*data-original-title="(\w.*)"\s.*data-toggle="tooltip">',str(i))
        m2 = re.search(r'<td><i class="(icon-cars)"></i></td>\s.*<td class="\w.*\s*data-original-title="(\w.*)"\s.*data-toggle="tooltip">(\d*)',str(i))
        try:
            #if multiple cars
            if m1:
                modifyDB(m1.group(2),1,"car")
            elif m2:
                #print(m1.group(3),m1.group(2),"track")
                modifyDB(m2.group(2),m2.group(3),"car")
        except:
            print("could not find, ", i)
            continue

#gathers info of tracks
def getTracks(file):
    print("##########getting track data: ", file)
    fileString = "C:\\scripting\\iracing_data_v2\\web_data\\"+file
    with open(fileString, encoding=('utf-8')) as fs:
        soup = BeautifulSoup(fs, 'html.parser')
    myParse = soup.findAll(re.compile("tr|td"))
    #print(myParse)
    for i in myParse:
        #1: confirm it's track 2: track layout 3: track name
        m1 = re.search(r'<td class=""><i class="(icon-track)"><\W.*\s.*\s.*data-original-title="(\w.*)"\s.*data-toggle="tooltip">(\w.*\n\s*\w.*)</span></td>',str(i))
        m2 = re.search(r'<td class=""><i class="(icon-track)"><\W.*\s.*\s.*data-original-title="(\w.*)"\s.*data-toggle="tooltip">(\w.*)</span>',str(i))
        try:
            if m1:
                string1 = ' '.join(str(m1.group(2)).replace('\n', ' ').split())
                string2 = ' '.join(str(m1.group(3)).replace('\n', ' ').split())
                #print(' '.join(string1.replace('\n', ' ').split()),' '.join(string2.replace('\n', ' ').split()))
                modifyDB(string1,string2,"track")
            elif m2:
                string1 = ' '.join(str(m2.group(2)).replace('\n', ' ').split())
                string2 = ' '.join(str(m2.group(3)).replace('\n', ' ').split())
                #print(' '.join(string1.replace('\n', ' ').split()),' '.join(string2.replace('\n', ' ').split()))
                modifyDB(string1,string2,"track")
        except:
            print("could not find, ", i)
            continue

#gets data
def getData(webdata, year, season, week):
    print("gathering data: ")
    #stores all the file names to be sent to other functions
    webset = set()
    #searches for files based on year, season and week input
    #all files
    if year == -1 and season == -1 and week == -1:
        print("working on all files: ")
        for files in os.listdir(webdata):
            if files.endswith('.html'):
                webset.add(files)
    #specific year
    elif year != -1 and season == -1 and week == -1:
        print("working on year: ")
        for files in os.listdir(webdata):
            if files.endswith('.html') and files.startswith(f"{year}"):
                webset.add(files)
    #specific season
    elif year != -1 and season != -1 and week == -1:
        print("working on specific season: ")
        for files in os.listdir(webdata):
            if files.endswith('.html') and files.startswith(f"{year}_s{season}"):
                webset.add(files)
    #specific week
    elif year != -1 and season != -1 and week != 1:
        print("working on specific week: ")
        for files in os.listdir(webdata):
            if files.endswith('.html') and files.startswith(f"{year}_s{season}_w{week}"):
                webset.add(files)
    else:
        print("something went wrong")
    print("########## Files found: ", webset)
    #sends each file in webset to either getCars() and getTracks()
    for file in webset:
        getCars(file)
        getTracks(file)

#cleans up database
def cleanDB():
    dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = dbclient["iracing_data"]
    carc = db["iracing_cars"]
    trackc = db["racing_tracks"]
    carc.drop()
    trackc.drop()

#main function
def main():
    print("#################")
    print("#### WELCOME ####")
    print("#################")
    print("Choose Selection: ")
    print("1 - run all")
    print("2 - run specific year")
    print("3 - run specific season")
    print("4 - run specific week")
    print("5 - clean up database CAUTION: DELETES DATABASE ENTRIES")
    print("99 - for testing purposes (year 2024, season 3, week 5)")
    choice = int(input("Enter Choice: "))

    webdata = 'C:\\scripting\\iracing_data_v2\\web_data\\'
    year = -1
    season = -1
    week = -1

    if choice == 1:
        cleanDB()
        getData(webdata, year, season, week)
    elif choice == 2:
        year = int(input("Enter Year: "))
        cleanDB()
        getData(webdata, year, season, week)
    elif choice == 3:
        cleanDB()
        year = int(input("Enter Year: "))
        season = int(input("Enter Season: "))
        getData(webdata, year, season, week)
    elif choice == 4:
        cleanDB()
        year = int(input("Enter Year: "))
        season = int(input("Enter Season: "))
        week = int(input("Enter week: "))
        getData(webdata, year, season, week)
    elif choice == 5:
        cleanDB()
    elif choice == 99:
        getData(webdata,2024,3,5)
    else:
        print("invalid choice")

main()
