# SI507 Final Project: National Park & Biodiversity

This program is a SI 507 final project designed to facilitate trip to national sites. After implementing the interactive command line tool, the users can enter a state of interest and obtain useful information about the national sites in that state, including site name, site category (national site, national historical site etc.), phone, email, to name a few. Users can also obtain some charts showing the biodiversity information of that national site. 

## Data sources

The program relied on:

* [National Park Service Data API](https://www.nps.gov/subjects/digital/nps-data-api.htm)
* [National Park Service Website](https://www.nps.gov/index.htm)
* [Biodiversity in National Parks csv files](https://www.kaggle.com/nationalparkservice/park-biodiversity)  
for data gathering

## Getting started

These instructions will get you a copy of the project up and running on your local machine for development (or grading :) ) purposes.

### Prerequisites

Python3, Plotly, some knowledge about command line tool (e.g. terminal)

### Installing

In order to configure this project, please follow these steps:

1. Clone the repository onto your local system.
```
$ git clone https://github.com/zhuoqunw/SI507-Final-Project.git
```

2. Obtain (or create) the secret.py file with the necessary API keys. (For the purpose of SI 507, this was turned
in to Canvas with my submission.) For other purpoes, please request a free API key from https://www.nps.gov/subjects/digital/nps-data-api.htm

3. Place secret.py at the root level in the final project directory.

## Running the application

The "FinProj.py" file will initiate the program.
```
$ python3 FinProj.py
```
:bulb: __Note: in your terminal, please change the directory to the final project directory before you run the program__

## Data presentation

1. The program will ask the user to input a state of interest and will return a nicely formatted list displaying all national sites names within that state with indices associated at the beginning of each name
2. The user will then input a number, and the program will display more detailed information of the selected national site, including name, category, address, phone, email, activities, description, website url, map url, the area of the site in acres and if applicable, the number of species in that site  
:bulb: To get access to the website or map, hit cmd+click  
3. If applicable, the user will also be presented with plots showing the biodiversity in the selected national park. More specifically:
    * A __bar chart__ showing the number of species under each category (mammal, bird, fish, Vascular Plant etc.), sorted by the number of species
    * A __bar chart__ showing the number of species under each occurrence category (Present, Not Confirmed, Not Present (Historical Report)), sorted by the number of species
    * A __pie chart__ showing the percentage of species under each nativeness category (native, not native, or unknown)
    * A __bar chart__ showing the number of species under each conservation status (species of concern, endangered etc.), sorted by the number of species  
:warning: Not all national sites have biodiversity data, if there is no plot, it means there is a lack of data

## Built With

* [Python3](https://docs.python.org/3/) - The programming language on the back end  
    Packages:
    * BeautifulSoup - scrape webpage
    * requests - fetch data from API
    * Plotly - visualize data
* [SQLite3](https://www.sqlite.org/docs.html) - The database backing the project

## Authors

* **Lea Wei** - *Initial work* - [zhuoqunw](https://github.com/zhuoqunw)

## Acknowledgments

* Professor Bobby Madamanchi and the instruction team of SI 507 in fall 2020, whose code examples helped form the basis of the this project, especially the web scrping part

## To my special little friend

* Nigel, my roommate's dog, was a great company and comfort for me while I was designing this program :dog: :dog: Isn't he cute?!

![](image/nigel.png)

