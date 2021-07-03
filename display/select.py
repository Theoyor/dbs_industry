import psycopg2

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
            call += " "
        call += "FROM "
        for t in table:
            call += t
            call += " "
        
        if where != "":
            call += "WHERE "
            call+= where

        call +=";"


        cur.execute(call)        

        table = cur.fetchall()
        

        print(table) 
	    # close the communication with the PostgreSQL
        cur.close()

        # commit changes
        conn.commit()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
    finally:
        if conn is not None:
            conn.close()


