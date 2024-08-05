## History of project
This project was started for several reasons.
- I wanted to show some of my coding ability on my resume
- I wasn't happy with the current tools out there that grab iRacing data
- I wanted to brush up on my python and learn some new items (such as MongoDB)

Revision 1: the first revision of the project inputted two self managed TSV files. Which the script then converted into JSON files. The "count" for the amount of times a track or car showed up was apart of the JSON. This version was buggy, slow, and required more manual intervention.

Revision 2: similar to the first revision. But without the TSV files. I had the script create the JSON files on the fly with all the data it needed. And the script would just append the JSON file if it found a new car/track. Though similarly to revision 1, revision 2 was buggy and a bit clunky. 

Revision 3: Decided to ditch the JSON files all together and move to a database. Though the only type I was familiar with, SQL, didn't seem like it was up to the challenege for the information I am trying to parse. I needed something a bit more dynamic and a bit more unstructured, as the data could vary depending on the Car/Track. After some research, I decided MongoDB was exactly what I was looking for. Very little code modification was needed to drop it into the script. 

## Plans for Next PR:
**this will be a big change to the code, could take a week to complete** 
- count license class's for each car [DEFERRED for below work]
    - re-design regex to grab all data needed at once [WIP]
        -  license class
        -  car name
        -  track name
        -  track layout
        -  To-Do
            - Combine getCars() and getTracks() into one function [DONE]
            - add license class to the information in the regex
            - create new function to replace modifyDB() to manageDB()
            - delete getCars(), getTracks() and modifyDB()
    - fix modiyDB() for cars
    - fix modiyDB() for track
- Major Fixes:
    - NONE
- minor bug fixes
- architect track DB design [DONE]

## To-do for 1.0:
- Car DB
  - count license class for each car [next PR][WIP][DEFERRED - redesign regex]
    - rookie
    - D
    - C
    - B
    - A
  - count amount of times a track uses it
  - count license for each track
- architect Track DB design [next PR][DONE]
- automate collection of data from iracing website using selenium

## How it works:
- Take snippet from HTML Element for each week of iracings season currently manual
- Cleans up the MongoDB Database by deleting collections in cleandb()
- Figures out which html files the script needs to process based off user choice in getData()
- For each file found, it will parse the file for car and track information in getTracks() and getCars()
- Those functions can both call modifyDB() which modifies the collections for cars and tracks

Database design:
CAR DATABASE:
```
{
    "_id": {
        "$oid": "66b0451f0a80f5e6138a8037"
    },
    "<car_name>": {
        "name": "<car_name>",
        "count": "<int>",
        "license": {
            "rookie": "<int>",
            "D license": "<int>",
            "C license": "<int>",
            "B license": "<int>",
            "a license": "<int>"
        },
        "tracks": {
            "<track_name>": {
                "count": "<int>",
                "rookie": "<int>",
                "D license": "<int>",
                "C license": "<int>",
                "B license": "<int>",
                "A license": "<int>"
            }
        }
    }
}
```
TRACK DATABASE:
```
{
    "_id": {
        "$oid": "66b0451f0a80f5e6138a8037"
    },
    "<track_name>": 
    {
        "name": "<track_name>",
        "count": "<int>",
        "license": 
        {
            "rookie": "<int>",
            "D license": "<int>",
            "C license": "<int>",
            "B license": "<int>",
            "a license": "<int>"
        },
        "tracks_layout": 
        {
            "count": "<int>",
            "rookie": {
                "count":"<int>",
                "<car_name>": "<int>"
            },
            "D license": {
                "count":"<int>",
                "<car_name>": "<int>"
            },
            "C license": {
                "count":"<int>",
                "<car_name>": "<int>"
            },
            "B license": {
                "count":"<int>",
                "<car_name>": "<int>"
            },
            "A license": {
                "count":"<int>",
                "<car_name>": "<int>"
            }
        }
    }
}
```
