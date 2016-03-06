import requests
import config

# The limit of results that the API will return
API_LIMIT = 1000

# Base filters as part of the requirements for the challenge
base_filters   = '&sector_desc=CROPS&commodity_desc=CORN&agg_level_desc=COUNTY&statisticcat_desc=PRODUCTION'

def get_count(years):
    return requests.get(config.base_url + 'get_counts/?key=' + config.API_KEY + base_filters + years)
    
def get_param_values(query):
    url = config.base_url + 'get_param_values/?key=' + config.API_KEY + base_filters + '&param=' + query
    print(url)
    return requests.get(url)
    
def get_results(years):
    url = config.base_url + 'api_GET/?key=' + config.API_KEY + base_filters + years
    print(url)
    return requests.get(url, timeout=None)
