#!/user/bin/python3
import os
from bs4 import BeautifulSoup
import re
import pymongo

def carDB(carString1,carString2,trackString1,trackString2,mylicense):
    #mongodb setup
    dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = dbclient["iracing_data"]
    carc = db["iracing_cars"]
    trackc = db["racing_tracks"]
    #single car getting passed in
    if int(carString2) == 1:
        carlist = carString1.replace('.','')
        #if not already in database
        if carc.find_one({'_id':carlist}) is None:
            carc.insert_one({"_id":carlist,carlist:{"count":0,"license":{"Rookie":0,"Class D":0,"Class C":0,"Class B":0,"Class A":0},"tracks":{trackString2:{"count":0,"license":{"Rookie":0,"Class D":0,"Class C":0,"Class B":0,"Class A":0}}}}})
            carc.find_one_and_update({carlist:{"$exists":"true"}},{"$inc":{carlist+".count":1,carlist+".license."+mylicense:1,carlist+".tracks."+trackString2+".count":1,carlist+".tracks."+trackString2+".license."+mylicense:1}})
        #if already in database
        elif carc.find_one({'_id':carlist}) is not None:
            #if track doesn't exist 
            if carc.find_one({carlist+'.tracks.'+trackString2:{"$exists":"true"}}) is None:
                carc.find_one_and_update({carlist:{"$exists":"true"}},{"$set":{carlist+".tracks."+trackString2:{"count":0,"license":{"Rookie":0,"Class D":0,"Class C":0,"Class B":0,"Class A":0}}}})
                carc.find_one_and_update({carlist:{"$exists":"true"}},{"$inc":{carlist+".count":1,carlist+".license."+mylicense:1,carlist+".tracks."+trackString2+".count":1,carlist+".tracks."+trackString2+".license."+mylicense:1}})
            #if track already exists
            else:
                carc.find_one_and_update({carlist:{"$exists":"true"}},{"$inc":{carlist+".count":1,carlist+".license."+mylicense:1,carlist+".tracks."+trackString2+".count":1,carlist+".tracks."+trackString2+".license."+mylicense:1}})
        else:
            print("could not add:",carString1,trackString1)
    #multiple cars getting passed in
    elif int(carString2) > 1:
        carlist = carString1.replace('.','').split(", ")
        #goes through every car
        for car in carlist:
            #if not already in database
            if carc.find_one({'_id':car}) is None:
                carc.insert_one({"_id":car,car:{"count":0,"license":{"Rookie":0,"Class D":0,"Class C":0,"Class B":0,"Class A":0},"tracks":{trackString2:{"count":0,"license":{"Rookie":0,"Class D":0,"Class C":0,"Class B":0,"Class A":0}}}}})
                carc.find_one_and_update({car:{"$exists":"true"}},{"$inc":{car+".count":1,car+".license."+mylicense:1,car+".tracks."+trackString2+".count":1,car+".tracks."+trackString2+".license."+mylicense:1}})
            #if already in database
            elif carc.find_one({'_id':car}) is not None:
                #if track doesn't exist
                if carc.find_one({car+'.tracks.'+trackString2:{"$exists":"true"}}) is None:
                    carc.find_one_and_update({car:{"$exists":"true"}},{"$set":{car+".tracks."+trackString2:{"count":0,"license":{"Rookie":0,"Class D":0,"Class C":0,"Class B":0,"Class A":0}}}})
                    carc.find_one_and_update({car:{"$exists":"true"}},{"$inc":{car+".count":1,car+".license."+mylicense:1,car+".tracks."+trackString2+".count":1,car+".tracks."+trackString2+".license."+mylicense:1}})
                #if track already exists
                else:
                    carc.find_one_and_update({car:{"$exists":"true"}},{"$inc":{car+".count":1,car+".license."+mylicense:1,car+".tracks."+trackString2+".count":1,car+".tracks."+trackString2+".license."+mylicense:1}})
            else:
                print("could not add:",car,trackString2)

#trackc.insert_one({"_id":trackString2,trackString2:{"count":0,"license":{"Rookie":0,"Class D":0,"Class C":0,"Class B":0,"Class A":0},"layouts":{trackString1:{"count":0,"license":{"Rookie":0,"Class D":0,"Class C":0,"Class B":0,"Class A":0},"cars":{carString1:{"count":0,"license":{"Rookie":0,"Class D":0,"Class C":0,"Class B":0,"Class A":0}}}}}}})
def trackDB(carString1,carString2,trackString1,trackString2,mylicense):
    #mongodb setup
    dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = dbclient["iracing_data"]
    carc = db["iracing_cars"]
    trackc = db["racing_tracks"]
    #if track doesn't exist
    if trackc.find_one({"_id":trackString2}) is None:
        #if single car
        if int(carString2) == 1:
            trackc.insert_one({"_id":trackString2,trackString2:{"count":0,"license":{"Rookie":0,"Class D":0,"Class C":0,"Class B":0,"Class A":0},"layouts":{trackString1:{"count":0,"license":{"Rookie":0,"Class D":0,"Class C":0,"Class B":0,"Class A":0},"cars":{carString1:{"count":0,"license":{"Rookie":0,"Class D":0,"Class C":0,"Class B":0,"Class A":0}}}}}}})
            trackc.find_one_and_update({trackString2:{"$exists":"true"}},{"$inc":{trackString2+".count":1,trackString2+".layouts."+trackString1+".count":1,trackString2+".layouts."+trackString1+".license."+mylicense:1,trackString2+".layouts."+trackString1+".cars."+carString1+".count":1,trackString2+".layouts."+trackString1+".cars."+carString1+".license."+mylicense:1}})
        #if multicar
        elif int(carString2) > 1:
            carlist = carString1.replace('.','').split(", ")
            for car in carlist:
                #if layout does not exist
                if trackc.find_one({trackString2+".layout."+trackString1:{"$exists":"true"}}) is None:
                    trackc.find_one_and_update({trackString2:{"$exists":"true"}},{"$set":{trackString2+".layouts."+trackString1:{"count":0,"license":{"Rookie":0,"Class D":0,"Class C":0,"Class B":0,"Class A":0},"cars":{car:{"count":0,"license":{"Rookie":0,"Class D":0,"Class C":0,"Class B":0,"Class A":0}}}}}})
                elif trackc.find_one({trackString2+".layout."+trackString1:{"$exists":"true"}}) is not None:
                    trackc.find_one_and_update({trackString2:{"$exists":"true"}},{"$inc":{trackString2+".count":1,trackString2+".layouts."+trackString1+".count":1,trackString2+".layouts."+trackString1+".license."+mylicense:1,trackString2+".layouts."+trackString1+".cars."+car+".count":1,trackString2+".layouts."+trackString1+".cars."+car+".license."+mylicense:1}})
    #if track exists
    elif trackc.find_one({"_id":trackString2}) is not None:
        x = -1
        if int(carString2) == 1:
            trackc.find_one_and_update({trackString2:{"$exists":"true"}},{"$inc":{trackString2+".count":1,trackString2+".layouts."+trackString1+".count":1,trackString2+".layouts."+trackString1+".license."+mylicense:1,trackString2+".layouts."+trackString1+".cars."+carString1+".count":1,trackString2+".layouts."+trackString1+".cars."+carString1+".license."+mylicense:1}})
        elif int(carString2) > 1:
            carlist = carString1.replace('.','').split(", ")
            for car in carlist:
                #if layout does not exist
                if trackc.find_one({trackString2+".layout."+trackString1:{"$exists":"true"}}) is None:
                    trackc.find_one_and_update({trackString2:{"$exists":"true"}},{"$set":{trackString2+".layouts."+trackString1:{"count":0,"license":{"Rookie":0,"Class D":0,"Class C":0,"Class B":0,"Class A":0},"cars":{car:{"count":0,"license":{"Rookie":0,"Class D":0,"Class C":0,"Class B":0,"Class A":0}}}}}})
                    trackc.find_one_and_update({trackString2:{"$exists":"true"}},{"$inc":{trackString2+".count":1,trackString2+".layouts."+trackString1+".count":1,trackString2+".layouts."+trackString1+".license."+mylicense:1,trackString2+".layouts."+trackString1+".cars."+car+".count":1,trackString2+".layouts."+trackString1+".cars."+car+".license."+mylicense:1}})
                elif trackc.find_one({trackString2+".layout."+trackString1:{"$exists":"true"}}) is not None:
                    trackc.find_one_and_update({trackString2:{"$exists":"true"}},{"$inc":{trackString2+".count":1,trackString2+".layouts."+trackString1+".count":1,trackString2+".layouts."+trackString1+".license."+mylicense:1,trackString2+".layouts."+trackString1+".cars."+car+".count":1,trackString2+".layouts."+trackString1+".cars."+car+".license."+mylicense:1}})
                
#grabs info to be inputted into DB
def getInfo(file):
    print("getting info: ", file)
    #opening .htnml files
    fileString = "C:\\scripting\\iracing_data_v3\\web_data\\"+file
    with open(fileString, encoding=('utf-8')) as fs:
        soup = BeautifulSoup(fs, 'html.parser')
    myParse = soup.findAll(re.compile("p|tr|td"))
    for i in myParse:
        #get car info
        car1 = re.search(r'<td><i class="(icon-car)"></i></td>\s.*<td class="\w.*\s*data-original-title="(\w.*)"\s.*data-toggle="tooltip">',str(i))
        car2 = re.search(r'<td><i class="(icon-cars)"></i></td>\s.*<td class="\w.*\s*data-original-title="(\w.*)"\s.*data-toggle="tooltip">(\d*)',str(i))
        try:
            #if single car
            if car1:
                carString1 = car1.group(2)
                carString2 = 1
            #if multiple cars
            elif car2:
                carString1 = car2.group(2)
                carString2 = car2.group(3)
        except:
            print("could not find, ", i)
            continue
        #get track info
        track1 = re.search(r'<td class=""><i class="(icon-track)"><\W.*\s.*\s.*data-original-title="(\w.*)"\s.*data-toggle="tooltip">(\w.*\n\s*\w.*)</span></td>',str(i))
        track2 = re.search(r'<td class=""><i class="(icon-track)"><\W.*\s.*\s.*data-original-title="(\w.*)"\s.*data-toggle="tooltip">(\w.*)</span>',str(i))
        try:
            if track1:
                trackString1 = ' '.join(str(track1.group(2)).replace('\n', ' ').split())
                trackString2 = ' '.join(str(track1.group(3)).replace('\n', ' ').split())
            elif track2:
                trackString1 = ' '.join(str(track2.group(2)).replace('\n', ' ').split())
                trackString2 = ' '.join(str(track2.group(3)).replace('\n', ' ').split())
        except:
            print("could not find, ", i)
            continue
        #get license info
        license = re.search(r'\s*<p class="chakra-text css-11y2hb3">(\w.*)</p>',str(i))
        try:
            if license:
                mylicense = str(license.group(1))
        except:
            print("could not find license, ", i)
        #modifyDB
        if car1 or car2:
            carDB(carString1,carString2,trackString1,trackString2,mylicense)
            trackDB(carString1,carString2,trackString1,trackString2,mylicense)
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
        getInfo(file)

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

    webdata = 'C:\\scripting\\iracing_data_v3\\web_data\\'
    year = -1
    season = -1
    week = -1

    #process 'choice'
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
        cleanDB()
        getData(webdata,2024,3,5)
    else:
        print("invalid choice")

main()
