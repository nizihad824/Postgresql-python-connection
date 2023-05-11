import psycopg2

# establish a connection to the database
conn = psycopg2.connect(
    dbname="OnlineLearner",
    user="postgres",
    password="root",
    host="localhost"
)

# create a new cursor
cur = conn.cursor()

# list of tables to fetch data from
tables = ['users', 'course', 'tasks']

# execute each SQL command to fetch data from the tables
for table in tables:
    try: 
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        
        print(f"\n--- Data from {table} ---")
        for row in rows:
            print(row)
        
    except Exception as e:
        print(f"An error occurred: {e}")

# close the cursor and the connection
cur.close()
conn.close()
