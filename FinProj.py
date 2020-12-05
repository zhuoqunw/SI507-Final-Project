#################################
##### Name: Lea Wei         #####
##### Uniqname: zhuoqunw    #####
##### SI507 Final Project   #####
##### Fall 2020             #####
#################################

from bs4 import BeautifulSoup
import requests
import secrets as secrets
import json
import plotly.graph_objects as go


api_key = secrets.API_KEY
api_url = f"https://developer.nps.gov/api/v1/parks"
nps_base_url = "https://www.nps.gov"

# retrieve the national sites' information from API and save it to a json file
# with open('national_park.json', 'w') as f:
#     json.dump(results_obj, f)

class NationalSite:
    '''a national site

    Instance Attributes
    -------------------
    category: string
        the category of a national site (e.g. 'National Park', '')
        some sites have blank category.
    
    name: string
        the name of a national site (e.g. 'Isle Royale')

    address: string
        the city and state of a national site (e.g. 'Houghton, MI')

    zipcode: string
        the zip-code of a national site (e.g. '49931', '82190-0168')

    phone: string
        the phone of a national site (e.g. '(616) 319-7906', '307-344-7381')
    '''
    def __init__(self, ct, nm, ad, zc, ph):
        self.category = ct
        self.name = nm
        self.address = ad
        self.zipcode = zc
        self.phone = ph
        self.description = de
        pass
    
    def info(self):
        return f"{self.name} ({self.category}): {self.address} {self.zipcode}"

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
    '''Retrieve the map link from a national site URL.
    
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
            return print(map_link)


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

def get_site_info(site_dict):
    '''Parse json dictionary and obtain site information. Return site instance based on the site info.
    
    Parameters
    ----------
    site_dict: dict
        a dictionary containing site info
    
    Returns
    -------
    instance
        a national site instance
    '''
    data = site_dict['data'][0]
    pass


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
        print("Using Cache")
        response = cache_dict[park_code]
    else:
        print("Fetching")
        response = requests.get(api_url, params).text
        cache_dict[park_code] = response
        save_cache(cache_dict)
    response = json.loads(response)
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

if __name__ == "__main__":

    state_url_dict = build_state_url_dict()
    command = input("Enter a state name (e.g. Michigan, michigan) or 'exit':")

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

    for site_link in site_list:
        print(get_api_data(site_link))