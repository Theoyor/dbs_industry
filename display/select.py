from pandas.core.frame import DataFrame
import psycopg2
import pandas
import decimal

def select(attributes, table, where = ""):
    conn = None
    try:

        # read connection parameters

        conn = psycopg2.connect(
        host="localhost",
        database="emissions",
        user="postgres",
        password="8DMoAc0dRouZ3CX1ZrFy")
		
        # create a cursor
        cur = conn.cursor()

        call = "SELECT "
        for a in attributes:
            call += a
            call += ", "
        
        call = call.rstrip(", ")
        call+= " "

        call += "FROM "
        for t in table:
            call += t
            call += ", "

        call = call.rstrip(", ")
        call+= " "
        
        if where != "":
            call += "WHERE "
            call+= where

        call +=";"

        cur.execute(call)        

        table = cur.fetchall()

        
        d ={}
        for a in attributes:
            d[a] =[]
        
        for row in table:
            for i in range(len(attributes)):
                if isinstance(row[i], decimal.Decimal):
                    d[attributes[i]].append(float(row[i]))
                else:
                    d[attributes[i]].append(row[i])



        df = DataFrame(data=d)
        #print(table) 
	    # close the communication with the PostgreSQL
        cur.close()

        # commit changes
        conn.commit()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
    finally:
        if conn is not None:
            conn.close()
        return df

print(select(["country_id", "name", "income_group"], ["country"]))