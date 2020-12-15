#################################
##### Name: Lea Wei         #####
##### Uniqname: zhuoqunw    #####
##### SI507 Final Project   #####
##### Fall 2020 UM          #####
#################################

from bs4 import BeautifulSoup
import requests
import secrets as secrets
import json
# import webbrowser
import sqlite3
import plotly.graph_objects as go


api_key = secrets.API_KEY
api_url = f"https://developer.nps.gov/api/v1/parks"
nps_base_url = "https://www.nps.gov"


class NationalSite:
    '''a national site

    Instance Attributes
    -------------------
    category: string
        the category of a national site (e.g. 'National Park', '')
        some sites have blank category.
    
    name: string
        the name of a national site (e.g. 'Isle Royale')

    phone: string
        the phone of a national site (e.g. '(616) 319-7906', '307-344-7381')

    description: string
        the description of the national site
    
    email: string
        email address

    activities: string
        activities available at the site (e.g. 'biking', 'camping')
    
    website: string
        website url
    '''
    def __init__(self, ct = "No Category", nm = "No Name", ph = "No Phone",
                    de = "No Description", em = "No Email", ac = "No Activities", ur = "No Website", json = None):
        if json == None:
            self.category = ct
            self.name = nm
            #self.address = ad
            self.phone = ph
            self.description = de
            self.email = em
            self.activities = ac
            self.website = ur
        else:
            self.category = json["designation"]
            self.name = json["fullName"]
            #self.address = json["addresses"][0]["line1"] + ', ' + json["addresses"][0]["city"]+ ', ' + json["addresses"][0]["stateCode"]+ ', ' + json["addresses"][0]["postalCode"]
            self.phone = json["contacts"]["phoneNumbers"][0]["phoneNumber"]
            self.description = json["description"]
            self.email = json["contacts"]["emailAddresses"][0]["emailAddress"]
            
            activities = []
            for act in json["activities"]:
                activities.append(act["name"])
            act_str = ','.join([str(act) for act in activities])
            
            self.activities = act_str
            self.website = json["url"]
            

    def basic_info(self):
        ''' basic site info
        '''
        return f"{self.name}, {self.category}, {self.website}"
    
    def detailed_info(self):
        ''' detailed site info
        '''
        info = print('* Name:',self.name,
        '\n* Category:',self.category,
        '\n* Phone number:',self.phone,
        '\n* Email:',self.email,
        #'\n* Address:',self.address,
        '\n* Activities:',self.activities,
        '\n* Description:',self.description,
        '\n* Website:',self.website)
        
        return info

def build_state_url_dict():
    ''' Make a dictionary that maps state name to state page url from "https://www.nps.gov"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a state name and value is the url
        e.g. {'michigan':'https://www.nps.gov/state/mi/index.htm', ...}
    '''
    # Collect webpage and create soup object
    response = request_with_cache(nps_base_url)
    soup = BeautifulSoup(response, 'html.parser')

    name_link_dict = {}

    # Pull text from the web page: append state:link pairs to a dictionary
    drop_down_menu_list = soup.find(class_="dropdown-menu SearchBar-keywordSearch").find_all('a')
    for item in drop_down_menu_list:
        state_name = item.text.strip()
        state_link = nps_base_url + item.get('href')
        
        name_link_dict[state_name.lower()] = state_link

    return name_link_dict

def get_site_map(site_url):
    '''Scrape the map link from a national site URL.
    
    Parameters
    ----------
    site_url: string
        The URL for a national site page in nps.gov
    
    Returns
    -------
    msp_link: string
        a national site map link string
    '''
    # Collect the site webpage
    response = request_with_cache(site_url)
    soup = BeautifulSoup(response, 'html.parser')

    # Pull map link from the webpage
    icons_list = soup.find(class_="UtilityNav").find_all('a', href=True)
    
    link_list = []
    for link in icons_list:
        link_list.append(link['href'])
    
    for link in link_list:
        if 'map' in link:
            map_link = nps_base_url + link
            return map_link

def get_sites_link_for_state(state_url):
    '''Make a list of national site links from a state URL.
    
    Parameters
    ----------
    state_url: string
        The URL for a state page in nps.gov
    
    Returns
    -------
    list
        a list of national site links
    '''
    # collect the state webpage
    response = request_with_cache(state_url)
    soup = BeautifulSoup(response, 'html.parser')

    # pull all the site urls
    site_list = soup.find('div',id="parkListResultsArea").find_all('h3')
    
    site_link_list = []
    for item in site_list:
        site_link = nps_base_url + item.find('a').get('href') + "index.htm"
        site_link_list.append(site_link)
    
    return site_link_list

def get_api_data(site_link):
    '''Obtain API data from NPS API.
    
    Parameters
    ----------
    site_object: object
        an instance of a national site
    
    Returns
    -------
    dict
        a converted API return from NPS API
    '''
    # call API
    cache_dict = open_cache()

    park_code = site_link.split('/')[3] # get park_code from site link
    api_key = secrets.API_KEY
    params = {
        'api_key': api_key, 'parkCode': park_code
    }
    if park_code in cache_dict:
        # print("Using Cache")
        response = cache_dict[park_code]
    else:
        # print("Fetching")
        response = requests.get(api_url, params).text
        cache_dict[park_code] = response
        save_cache(cache_dict)
    response = json.loads(response)
    response = response["data"][0]

    return response

# Cache functions. Called wherever needed.
CACHE_FILENAME = 'Finalproj_cache.json'

def open_cache():
    ''' Open the cache file or create a new cache dictionary

    Parameters
    ----------
    None
    
    Returns
    -------
    dict
        a cache dictionary
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_content = cache_file.read()
        cache_dict = json.loads(cache_content)
        cache_file.close()
    except:
        cache_dict = {}
    
    return cache_dict

def save_cache(cache_dict):
    ''' Save cache dictionary to the cache file

    Parameters
    ----------
    cache_dict: dictionary
        the cache dictionary
    
    Returns
    -------
    None
    '''
    dump_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME, 'w')
    fw.write(dump_json_cache)
    fw.close()

def request_with_cache(url):
    ''' If URL in cache, retrieve the corresponding values from cache. Otherwise, connect to API again and retrieve from API.
    
    Parameters
    ----------
    url: string
        a URL
    
    Returns
    -------
    a string containing values of the URL from cache or from API
    '''
    cache_dict = open_cache()
    if url in cache_dict.keys():
        print("Using Cache")
        response = cache_dict[url]
    else:
        print("Fetching")
        response = requests.get(url).text # need to append .text, otherwise, can't save a Response object to dict
        cache_dict[url] = response # save all the text on the webpage as strings to cache_dict
        save_cache(cache_dict)
    return response


# SQL queries & plotly:
def get_category_species_info(park_name):
    ''' Constructs and executes SQL query to retrieve category and species from the species table. 
    Prepare for a bar chart showing the number of species under each category. 
    
    Parameters
    ----------
    park_name: string.
        The name of the park.
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = sqlite3.connect("biodiversity/Biodiversity.sqlite")
    cursor = connection.cursor()
    park_name = "'" + park_name + "'"
    query = "SELECT Category, COUNT([Species ID]) AS cnt FROM species WHERE [Park Name] = {} GROUP BY Category ORDER BY cnt DESC".format(park_name) # use square bracket to escape the space in column name
    result = cursor.execute(query).fetchall()
    connection.close()
    return result

#print(get_category_species_info("Acadia National Park"))

def category_species_bar_chart(sql_result, park_name):
    '''Plot bar chart showing the number of species under each category with the SQL result

    Parameters
    ----------
    sql_result: list
        A list of tuples with the information for plot
    park_name: string
        a string of park name

    Returns
    -------
        A bar plot made with plotly
    '''
    xvals = []
    yvals = []

    for tuple in sql_result:
        xvals.append(tuple[0])
        yvals.append(tuple[1])

    bar_data = go.Bar(x = xvals, y = yvals)
    basic_layout = go.Layout(title = "Number of Species per Category at {}".format(park_name))
    fig = go.Figure(data = bar_data, layout = basic_layout)

    return fig.show()

# category_species_bar_chart(get_category_species_info("Acadia National Park"), "Acadia National Park")

def get_occurrence_info(park_name):
    ''' Constructs and executes SQL query to retrieve occurence info from the species table. 
    Prepare for a bar chart showing the number of species under each occurrence category.
    
    Parameters
    ----------
    park_name: string.
        The name of the park.
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = sqlite3.connect("biodiversity/Biodiversity.sqlite")
    cursor = connection.cursor()
    park_name = "'" + park_name + "'"
    query = "SELECT Occurrence, count(*) AS cnt\
                          FROM species WHERE [Park Name] = {}\
                          GROUP BY Occurrence ORDER BY cnt DESC".format(park_name) # use square bracket to escape the space in column name
    result = cursor.execute(query).fetchall()
    connection.close()
    return result

def occurrence_species_bar_chart(sql_result, park_name):
    '''Plot bar chart showing the number of species under each occurrence status with the SQL result

    Parameters
    ----------
    sql_result: list
        A list of tuples with the information for plot
    park_name: string
        a string of park name

    Returns
    -------
        A bar plot made with plotly
    '''
    xvals = []
    yvals = []

    for tuple in sql_result:
        xvals.append(tuple[0])
        yvals.append(tuple[1])

    bar_data = go.Bar(x = xvals, y = yvals)
    basic_layout = go.Layout(title = "Number of Species per Occurrence status at {}".format(park_name))
    fig = go.Figure(data = bar_data, layout = basic_layout)

    return fig.show()

# print(occurrence_species_bar_chart(get_occurrence_info("Acadia National Park"), "Acadia National Park"))

def get_nativeness_info(park_name):
    ''' Constructs and executes SQL query to retrieve nativeness info from the species table.
    Prepare for a pie chart showing the percentages of species under each nativeness category.
    
    Parameters
    ----------
    park_name: string.
        The name of the park.
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = sqlite3.connect("biodiversity/Biodiversity.sqlite")
    cursor = connection.cursor()
    park_name = "'" + park_name + "'"
    query = "SELECT Nativeness, (count(*) * 100\
                          / sum(count(*)) OVER ()) AS percent\
                          FROM species WHERE [Park Name] = {}\
                          GROUP BY Nativeness ORDER BY percent".format(park_name) # use square bracket to escape the space in column name
    result = cursor.execute(query).fetchall()
    connection.close()
    return result

def nativeness_species_pie_chart(sql_result, park_name):
    '''Plot pie chart showing the percentage of each nativeness status with the SQL result

    Parameters
    ----------
    sql_result: list
        A list of tuples with the information for plot
    park_name: string
        a string of park name

    Returns
    -------
        A bar plot made with plotly
    '''
    labels = []
    values = []

    for tuple in sql_result:
        labels.append(tuple[0])
        values.append(tuple[1])

    pie_data = go.Pie(labels = labels, values = values)
    basic_layout = go.Layout(title = "Percentage of Species per Nativeness status at {}".format(park_name))
    fig = go.Figure(data = pie_data, layout = basic_layout)

    return fig.show()

# print(nativeness_species_pie_chart(get_nativeness_info("Acadia National Park"), "Acadia National Park"))

def get_conservation_info(park_name):
    ''' Constructs and executes SQL query to retrieve conservation info from the species table.
    Prepare for a pie chart showing the percentages of species under each conservation status.
    
    Parameters
    ----------
    park_name: string.
        The name of the park.
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = sqlite3.connect("biodiversity/Biodiversity.sqlite")
    cursor = connection.cursor()
    park_name = "'" + park_name + "'"
    query = "SELECT [Conservation Status], count(*) AS cnt\
                          FROM species WHERE [Park Name] = {}\
                          GROUP BY [Conservation Status] ORDER BY cnt DESC".format(park_name) # use square bracket to escape the space in column name
    result = cursor.execute(query).fetchall()
    connection.close()
    return result


def conservation_species_bar_chart(sql_result, park_name):
    '''Plot bar chart showing the number of species under each conservation status with the SQL result

    Parameters
    ----------
    sql_result: list
        A list of tuples with the information for plot
    park_name: string
        a string of park name

    Returns
    -------
        A bar plot made with plotly
    '''
    xvals = []
    yvals = []

    for tuple in sql_result:
        xvals.append(tuple[0])
        yvals.append(tuple[1])

    bar_data = go.Bar(x = xvals, y = yvals)
    basic_layout = go.Layout(title = "Number of Species per conservation status at {}".format(park_name))
    fig = go.Figure(data = bar_data, layout = basic_layout)

    return fig.show()
#print(conservation_species_bar_chart(get_conservation_info("Acadia National Park"), "Acadia National Park"))

def get_park_acre(park_name):
    ''' Constructs and executes SQL query to retrieve acre info from the park table.
    
    Parameters
    ----------
    park_name: string.
        The name of the park.
    
    Returns
    -------
    list
        a list of tuples that represent the query result
    '''
    connection = sqlite3.connect("biodiversity/Biodiversity.sqlite")
    cursor = connection.cursor()
    park_name = "'" + park_name + "'"
    query = 'SELECT parks."Park Name", parks.Acres, COUNT(species."Species ID")\
            FROM parks JOIN species ON parks."Park Name" = species."Park Name" WHERE parks.[Park Name] = {} GROUP BY parks.[Park Name]'.format(park_name) # use square bracket to escape the space in column name
    result = cursor.execute(query).fetchall()
    connection.close()

    # park_full_name = result[0][0]
    park_acre = result[0][1]
    species_num = result[0][2]

    return print('* Area:',park_acre, 'acres',\
        '\n* Number of Species:', species_num)

# get_park_acre("Canyonlands National Park")


if __name__ == "__main__":

    state_url_dict = build_state_url_dict()
    command = input("Enter a state name (e.g. Michigan, michigan) or 'exit':")

    while True:

        while True:
            state_url = None
            if command == 'exit':
                print('\nBye!')
                exit()
            try:
                state_url = state_url_dict[command.lower()]
                break
            except:
                print('[ERROR] Enter proper state name')
                command = input("\nEnter a state name (e.g. Michigan, michigan) or 'exit':")

        site_list = get_sites_link_for_state(state_url)
        #print(instance_list)

        basic_info_obj = []
        detailed_info_obj = []

        basic_info = []
        detailed_info = []

        map_list = []

        for site_link in site_list:
            basic_info_obj.append(NationalSite(json = get_api_data(site_link)))
            basic_info.append(NationalSite(json = get_api_data(site_link)).basic_info())
            map_list.append(get_site_map(site_link))
            #detailed_info.append(NationalSite(json = get_api_data(site_link)).detailed_info())

        # append number in front of the each site
        for i in range(len(basic_info)):
            basic_info_str = str(i+1) + ' ' + str(basic_info[i])
            print(basic_info_str)

        # choose a site to get more info
        command2 = input("\nChoose the number of a site for more details or 'exit' or 'back':")

        while True:

            if command2 != 'exit' and command2 != 'back':
                try:
                    command2 = int(command2)
                    if command2 > 0 and command2 <= len(basic_info):
                        site_object = basic_info_obj[command2 - 1]
                        print("                ")
                        site_object.detailed_info()
                        print('* Map: ', map_list[command2 - 1])
                        get_park_acre("Canyonlands National Park")
                        # webbrowser.open(map_list[command2 - 1])

                        command3 = input("\nInterested in biodiversity at this national park? Enter 'yes' to receive more information, enter 'back' to go back, and 'exit' to exit the program:")

                        while True:

                            if command3 != 'exit' and command3 != 'back':
                                try:
                                    command3 = command3.lower()
                                    if command3 == 'yes':
                                        #print(command3)

                                        while True:
                                            if command3 != 'back' and command3 != 'exit':
                                                command4 = input("\nPlease select which attribute to display: A. category B. occurrence C.nativeness D.conservation. Please enter the letter associated with each option.\
                                            \n(Note: if there is no chart, it means that there is currently a lack of information about the biodiversity in that site. We are doing our best to add more information, so please stay tuned!)")

                                                while True:
                                                    while True:
                                                        command4 = command4.lower()
                                                        #print(command4)
                                                        if command4 == 'a':
                                                            #print(command4)
                                                            category_species_bar_chart(get_category_species_info(site_object.name), site_object.name)
                                                            break
                                                        elif command4 == 'b':
                                                            occurrence_species_bar_chart(get_occurrence_info(site_object.name), site_object.name)
                                                            break
                                                        elif command4 == 'c':
                                                            nativeness_species_pie_chart(get_nativeness_info(site_object.name), site_object.name)
                                                            break
                                                        elif command4 == 'd':
                                                            conservation_species_bar_chart(get_conservation_info(site_object.name), site_object.name)
                                                            break
                                                        else:
                                                            print('\n[ERROR] Invalid input')
                                                            command4 = input("\nPlease select which attribute to display: A. category B. occurrence C.nativeness D.conservation. Please enter the letter associated with each option:\
                                                                            \n(Note: if there is no chart, it means that there is currently a lack of information about the biodiversity in this site. We are doing our best to add more information, so please stay tuned!)")

                                                    command4 = input("\nChoose another attribute or 'exit' or 'back':")
                                                    command4 = command4.lower()

                                                    if command4 in ['a', 'b', 'c', 'd']:
                                                        continue
                                                    elif command4 == 'back':
                                                        command3 = input("\nInterested in biodiversity at this national park? Enter 'yes' to receive more information, enter 'back' to go back, and 'exit' to exit the program:")
                                                        break
                                                    elif command4 == 'exit':
                                                        command3 = command4
                                                        break
                                                    else:
                                                        print('\n[ERROR] Invalid input')
                                                        command4 = input("\nChoose another attribute or 'exit' or 'back':")
                                            elif command3 == 'back':
                                                break
                                            elif command3 == 'exit':
                                                break
                                    else:
                                        print('\n[ERROR] Invalid input')
                                        command3 = input("\nInterested in biodiversity at this national park? Enter 'yes' to go reveal more information, including some charts, enter 'back' to go back, and 'exit' to exit the program.")
                                except:
                                    print('\n[ERROR] Invalid input')
                                    command3 = input("\nInterested in biodiversity at this national park? Enter 'yes' to go reveal more information, including some charts, enter 'back' to go back, and 'exit' to exit the program.")

                            elif command3 == 'back':
                                command2 = input("\nChoose the number of a site for more details or 'exit' or 'back':")
                                break

                            elif command3 == 'exit':
                                command2 = command3
                                break

                    else:
                        print('\n[ERROR] Invalid input')
                        command2 = input("\nChoose the number of a site for more details or 'exit' or 'back':")

                except:
                    print('\n[ERROR] Invalid input')
                    command2 = input("\nChoose the number of a site for more details or 'exit' or 'back':")

            elif command2 == 'back':
                command = input("\nEnter a state name (e.g. Michigan, michigan) or 'exit':")
                break

            elif command2 == 'exit':
                print('\nBye!')
                exit()
