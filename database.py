import psycopg2

class Database:
    'Save the results from the API to the database'
    
    __conn = None
    
    def __init__(self, dbname, dbuser, dbpass, dbhost):
        try:
            self.conn = psycopg2.connect(database=dbname, user=dbuser, password=dbpass, host=dbhost)
        except psycopg2.DatabaseError as e:
                raise Exception('Error {}'.format(e))
                
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpass = dbpass
        self.dbhost = dbhost
        
        
    def check_connection(self):
        """ Makes sure the database connection is still open before interacting with the database """
        
        if self.conn == None:
            try:
                self.conn = psycopg2.connect(database=self.dbname, user=self.dbuser, password=self.dbpass, host=self.dbhost)
            except psycopg2.DatabaseError as e:
                raise Exception('Error {}'.format(e))
        
        
    def create_fact_table(self):
        self.check_connection()
        
        try:
            cur = self.conn.cursor()
            
            # Build the query to create the fact_data table
            create_table_info = 'CREATE TABLE fact_data ('
            create_table_info += 'Id SERIAL PRIMARY KEY,'
            create_table_info += 'Domain VARCHAR(256),'
            create_table_info += 'Commodity VARCHAR(80),'
            create_table_info += 'Category VARCHAR(80),'
            create_table_info += 'Geographic_level VARCHAR(40),'
            create_table_info += 'Country VARCHAR(30),'
            create_table_info += 'State VARCHAR(80),'
            create_table_info += 'County VARCHAR(80),'
            create_table_info += 'Unit_description VARCHAR(60),'
            create_table_info += 'Value VARCHAR(24),'
            create_table_info += 'Year VARCHAR(4)'
            create_table_info += ')'
            
            # Execute SQL query
            cur.execute("DROP TABLE IF EXISTS fact_data")
            cur.execute(create_table_info)
            
            self.conn.commit()
            
        except psycopg2.DatabaseError as e:
            if self.conn:
                self.conn.rollback()
            raise Exception('Error {}'.format(e))
            
        # finally:
        #     if self.conn:
        #         Database.conn.close()
        
    
    def save_results(self, data):
        """ Saves the results obtained from the API in the fact_data table of the database """
        
        # A list of the data
        facts = []
        for row in data:
            domain = row['domain_desc']
            commodity = row['commodity_desc']
            category = row['statisticcat_desc']
            geography = row['agg_level_desc']
            country = row['country_name']
            state = row['state_name']
            county = row['county_name']
            description = row['unit_desc']
            value = row['Value']
            year = row['year']
            facts.append([domain, commodity, category, geography, country, state, county, description, value, year])
        
        # Convert the list to a tuple
        facts = tuple(facts)
        
        self.check_connection()
        
        # Perform the actual data saving
        try:
            cur = self.conn.cursor()
            query = "INSERT INTO fact_data (Domain, Commodity, Category, Geographic_level, Country, State, County, Unit_description, Value, Year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur.executemany(query, facts)
            
            self.conn.commit()
        except psycopg2.DatabaseError as e:
            if self.conn:
                self.conn.rollback()
            raise Exception("Error: {}".format(3))
            
            
        