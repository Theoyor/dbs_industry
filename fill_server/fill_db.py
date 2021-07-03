import psycopg2
import decimal
import math
from config import config
from read_csv import *

def if_exists(d,key1,key2, frac = False):

    if key1 in d:
        if key2 in d[key1]:
            return d[key1][key2]

    return None



def create_tables():
    
    commands = []
    commands.append(
        """  
        CREATE TABLE IF NOT EXISTS country (
            country_id VARCHAR(255),
            name VARCHAR(255) NOT NULL,
            income_group VARCHAR(255),
            region VARCHAR(255),
            percentage_agriculture NUMERIC,
            percentage_industry NUMERIC,
            percentage_service NUMERIC,
            PRIMARY KEY(country_id)
        );
        """
    )

    commands.append(
        """
        CREATE TABLE IF NOT EXISTS year (
            year_id INTEGER,
            is_snapshot BOOLEAN,
            PRIMARY KEY(year_id)
        );
        """
    )
    
    commands.append(
        """
        CREATE TABLE IF NOT EXISTS country_in_year (
            country_id VARCHAR(255),
            year_id INTEGER,
            industry_share NUMERIC,
            gdp NUMERIC,
            population INTEGER,
            emission NUMERIC,
            PRIMARY KEY (country_id, year_id),
            FOREIGN KEY (country_id)
                    REFERENCES country (country_id)
                    ON DELETE CASCADE,
            FOREIGN KEY (year_id)
                    REFERENCES year (year_id)
                    ON DELETE CASCADE
        );
        """
    )

    return commands
    
def insert(cur):
    countries = read_countries()
    country_keys = countries.keys()
    years = [x for x in range(1960, 2021)]
    emissions = read_emission(countries)
    country_data = read_country_data(countries)
    gdp = read_gdp(countries)
    industry = read_industry(countries)
    sectors = read_sectors(countries)
    population = read_population_total(countries)
    
    for key in country_keys:
        cur.execute(
            """
            INSERT INTO country (country_id, name, income_group, region, percentage_agriculture, percentage_industry, percentage_service)
            VALUES(%s,%s,%s,%s,%s,%s,%s);
            """,
            (
                key, countries[key], if_exists(country_data, key, "inc"),if_exists(country_data, key, "reg"),
                if_exists(sectors, key, "agr", True), if_exists(sectors, key, "ind", True), if_exists(sectors, key, "ser", True) 
            )
        )
    
    for year in years:
        cur.execute(
             """
            INSERT INTO year (year_id, is_snapshot)
            VALUES(%s,%s);
            """,
            (year, year == 2017)
        )
    
    for key in country_keys:
        for year in years:
            cur.execute(
                """
                INSERT INTO country_in_year (country_id, year_id, industry_share, gdp, population, emission)
                VALUES(%s,%s,%s,%s,%s,%s);
                """,
                (
                    key, year, if_exists(industry, key, year, True), if_exists(gdp, key, year, True),
                    if_exists(population, key, year), if_exists(emissions, key, year, True)
                )
            )

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:

        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()

        # creating tables
        print("Creating tables")
        
        tables = create_tables()

        for table in tables:
            cur.execute(table)
   
        # insert values
        insert(cur)
	    # close the communication with the PostgreSQL
        cur.close()

        # commit changes
        conn.commit()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')




if __name__ == '__main__':
    connect()