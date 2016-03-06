#! /usr/local/bin/python3
import argparse
import apiservice
import database

__author__ = 'Ash'

def main():
    print('NOTE: The current API doesn\'t support full date for start and end period, so only the year will be used')
    
    # Add command line arguments
    parser = argparse.ArgumentParser(description="App fetches NASS dataset from USDA and stores in PostGreSQL database")
    parser.add_argument('-s', '--start_date', help='Start date of the data', required=True)
    parser.add_argument('-e', '--end_date', help='End date of the data', required=True)
    parser.add_argument('-db', '--database_name', help='Name of the database to store the data in', required=True)
    parser.add_argument('-ho', '--database_host', help='Host for the database', required=True)
    parser.add_argument('-u', '--database_user', help='Username to use in accessing the database', required=True)
    parser.add_argument('-p', '--database_password', help='Password to use in accessing the database', required=True)
    args = parser.parse_args()
    
    # Get terminal variables
    dbname     = args.database_name
    dbhost     = args.database_host
    dbuser     = args.database_user
    dbpass     = args.database_password
    start_date = args.start_date
    end_date   = args.end_date
    
    # Create connection to database
    db = database.Database(dbname, dbuser, dbpass, dbhost)
    
    # Create Facts Table to store the API results
    db.create_fact_table()
    
    # Get start and end years
    start = get_year(start_date)
    end   = get_year(end_date)
    
    # Build up the year filter for the API query
    year_filter = ''
    for i in range(start, end + 1):
        year_filter += '&year=' + str(i)
    
    # Get count of results the API query will return
    response = apiservice.get_count(year_filter)
    if response.status_code != 200:
        raise Exception('GET /get_counts/ {}'.format(response.status_code))
    
    result = response.json()
    
    # API can only return a maximum of 50000 records. If query will exceed limit, then change the filter
    if int(result['count']) <= apiservice.API_LIMIT:
        # run the call once
        perform_task(year_filter, db)
        
    else:
        # Get states to add to the filter to keep the number of results per API call under 50000
        response = apiservice.get_param_values('state_name')
        if response.status_code != 200:
            raise Exception('GET /get_param_values/ {}'.format(response.status_code))
    
        result = response.json()
        states = result['state_name']
        
        # Add 'STATE' to the filter
        for state in states:
            query = year_filter + '&state_name=' + state
            perform_task(query, db, True)
       
    
    
def perform_task(query, db, check_count=False):
    if check_count:
        # Get the number of results that will be returned for this latest filter and ignore 0 filters
        response = apiservice.get_count(query)
        if response.status_code != 200:
            raise Exception('GET /get_counts/ {}'.format(response.status_code))
        
        count = response.json()
        if int(count['count']) == 0:
            return
            
    response = apiservice.get_results(query)
    if response.status_code != 200:
        raise Exception('GET /api_GET/ {}'.format(response.status_code))
        
    results = response.json()
    
    # Save the results
    db.save_results(results['data'])
    
    
    
def get_year(date):
    """ Get the year from the date """
    
    index = '-' in date
    if index:
        return int(date[0:index])
    else:
        size = len(date)
        if len(date) <= 4:
            return int(date)
        else:
            raise Exception('Incorrect date supplied. Date should be of the format YYYY-MM-DD or just the year')
            
   
if __name__ == '__main__':
    main()
    