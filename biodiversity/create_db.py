#################################################
##### Name: Lea Wei                         #####
##### Uniqname: zhuoqunw                    #####
##### SI507 Final Project - build database  #####
##### Fall 2020                             #####
#################################################

import csv, sqlite3

conn = sqlite3.connect('Biodiversity.sqlite')
cur = conn.cursor()

#### create table parks ####
drop_parks = '''
    DROP TABLE IF EXISTS "parks";
'''

create_parks = '''
    CREATE TABLE IF NOT EXISTS "parks" (
        "Park Code" TEXT NOT NULL, 
        "Park Name" TEXT PRIMARY KEY, 
        "State" TEXT NOT NULL, 
        "Acres" INTEGER NOT NULL, 
        "Latitude" INTEGER NOT NULL, 
        "Longitude" INTEGER NOT NULL
        );
'''

cur.execute(drop_parks)
cur.execute(create_parks)

with open('parks.csv','r') as parks: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(parks) # comma is default delimiter
    to_db = [(i['Park Code'], i['Park Name'], i['State'], i['Acres'], i['Latitude'], i['Longitude']) for i in dr]

cur.executemany("INSERT INTO parks VALUES (?, ?, ?, ?, ?, ?);", to_db)

#### create table species ####
drop_species = '''
    DROP TABLE IF EXISTS "species"
'''

create_species = '''
    CREATE TABLE IF NOT EXISTS "species" (
        "Species ID" TEXT PRIMARY KEY UNIQUE,
        "Park Name" TEXT NOT NULL,
        "Category" TEXT NOT NULL,
        "Order" TEXT NOT NULL,
        "Family" TEXT NOT NULL,
        "Scientific Name" TEXT NOT NULL,
        "Common Names" TEXT NOT NULL,
        "Record Status" TEXT NOT NULL,
        "Occurrence" TEXT NOT NULL,
        "Nativeness" TEXT NOT NULL,
        "Abundance" TEXT,
        "Seasonality" TEXT,
        "Conservation Status" TEXT
    );
'''

cur.execute(drop_species)
cur.execute(create_species)

with open('species.csv','r') as species: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr2 = csv.DictReader(species) # comma is default delimiter
    to_db2 = [(i['Species ID'], i['Park Name'], i['Category'], i['Order'], i['Family'], i['Scientific Name'], i['Common Names'], i['Record Status'], i['Occurrence'], i['Nativeness'],i['Abundance'], i['Seasonality'], i['Conservation Status']) for i in dr2]

cur.executemany("INSERT INTO species VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db2)


conn.commit()
conn.close()