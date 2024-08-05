Plans for Next PR:
- count license class's for each car
- Major Fixes:
    - NONE
- minor bug fixes
- architect track DB design

Needed for 1.0:
- Car DB
  - count license class for each car [next PR]
    - rookie
    - D
    - C
    - B
    - A
  - count amount of times a track uses it
  - count license for each track
- architect Track DB design [next PR]
-----------------------
How it works:
- Take snippet from HTML Element for each week of iracings season currently manual
- Cleans up the MongoDB Database by deleting collections in cleandb()
- Figures out which html files the script needs to process based off user choice in getData()
- For each file found, it will parse the file for car and track information in getTracks() and getCars()
- Those functions can both call modifyDB() which modifies the collections for cars and tracks

Database design:
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
                "a license": "<int>"
            }
        }
    }
}
```
