## History of project
This project was started for several reasons.
- I wanted to show some of my coding ability on my resume
- I wasn't happy with the current tools out there that grab iRacing data
- I wanted to brush up on my python and learn some new items (such as MongoDB)

Revision 1: the first revision of the project inputted two self managed TSV files. Which the script then converted into JSON files. The "count" for the amount of times a track or car showed up was apart of the JSON. This version was buggy, slow, and required manual intervention.

Revision 2: similar to the first revision. But without the TSV files. I had the script create the JSON files on the fly with all the data it needed. the script would just append the JSON file if it found a new car/track. Though similarly to revision 1, revision 2 was buggy and a bit clunky. 

Revision 3: Decided to ditch the JSON files all together and move to a database. Though the only type I was familiar with, SQL, but SQL wouldn't plug very nicely into the code I already had. I needed something a bit more dynamic and a bit more unstructured, as the data could vary depending on the Car/Track. After some research, I decided MongoDB was exactly what I was looking for. Very little code modification was needed to drop it into the script. 

NOTE: I care more about the car-track relationship then I do track-car relationship. Meaning, I car more about what tracks are avaibable for a specific car then what cars are avaibable for a specific track. 

## Plans for future PR's (each will get it's own PR):

P1 = what is currently in progress
P2 = next priority(s)
P3 = least priority, will only get to once all P2 are done

- [P1][WIP] implement Track DB
- [P2] proper logging
- [P2] figure out a way to process the data, either cli or ui
- [P3] automate selenium for data extraction from iRacing website
- [P3] get running in Jenkins
- [P3] code cleanup

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
    "_id": <car_name>,
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
