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

# list of SQL commands to create the tables
tables = [
    """
    CREATE TABLE users (
        email TEXT NOT NULL,
        name TEXT NOT NULL,
        password TEXT NOT NULL,
        number SERIAL PRIMARY KEY
    )
    """,
    """
    CREATE TABLE course (
        ID SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        enrollmentkey VARCHAR(10),
        free_places INT NOT NULL CHECK (free_places BETWEEN 0 AND 100),
        creator INT NOT NULL,
        FOREIGN KEY (creator) REFERENCES users(number)
    )
    """,
    """
    CREATE TABLE enroll (
        user_id INT NOT NULL,
        course INT NOT NULL,
        date_of_entry TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY (user_id, course),
        FOREIGN KEY (user_id) REFERENCES users(number),
        FOREIGN KEY (course) REFERENCES course(ID) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE submission (
        id SERIAL PRIMARY KEY,
        submission_text TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE tasks (
        number SERIAL,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        nr INT NOT NULL,
        PRIMARY KEY(number, nr),
        FOREIGN KEY(nr) REFERENCES course (ID) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE submit (
        sid INT NOT NULL,
        cid INT NOT NULL,
        tid INT NOT NULL,
        user_id INT NOT NULL,
        PRIMARY KEY (sid, cid, tid , user_id),
        FOREIGN KEY (sid) REFERENCES submission(id) ON DELETE CASCADE,
        FOREIGN KEY(cid, tid) REFERENCES tasks (nr, number) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(number)
    )
    """,
    """
    CREATE TABLE canRate (
        grade INT CHECK(grade BETWEEN 1 AND 5),
        comment TEXT,
        submission INT NOT NULL,
        user_id INT NOT NULL,
        PRIMARY KEY(submission, user_id),
        FOREIGN KEY(submission) REFERENCES submission(id),
        FOREIGN KEY(user_id) REFERENCES users(number)
    )
    """
]

data_inserts = [
    """
    INSERT INTO users (email, name, password) VALUES
        ('dummy@dummy.com', 'DummyUser', 'dummy'),
        ('alan@turing.com', 'Alan Turing', 'alan'),
        ('donald@eKnuth.com', 'DonaldEKnuth', 'donald'),
        ('tim@bernersLee.com', 'Tim Berners Lee', 'tim'),
        ('fuhr@fuhr.com', 'Nobert Fuhr', 'fuhr'),
        ('aker@aker.com', 'Ahmet Aker', 'aker')
    """,
    """
    INSERT INTO course (name, description, enrollmentkey, free_places, creator)  VALUES
        ('Datenbanken', 'Einfuehrung in relationale Datenbanken', 'db2', 50, 5),
        ('Information Mining', 'Data Mining Basics', 'im', 30, 6),
        ('Information Retrieval', 'IR Basics', 'ir', 20, 5),
        ('Information Engineering', 'Daten vs Information vs Wissen', NULL, 60, 4),
        ('Deep Learning 101', 'Learn the new AI technologies', NULL, 80, 3),
        ('Arts', 'History about Arts', 'arts', 10, 2),
        ('Social Sciences', 'Social Sciences for Beginners', NULL, 2, 1)
    """,
    """
    INSERT INTO tasks (name, description, nr)  VALUES
        ('ER-Modellierung', 'Was ist Unterschied zwischen Entität und Relation?', 1),
        ('Relationale Algebra', 'Was ist Unterschied zwischen Projetion und Selektion?', 1),
        ('SQL', 'Wofür steht SQL?', 1),
        ('ACID', 'Was bedeut Atomicity?', 1),
        ('Naive Bayes', 'Was ist naive Annahme in Naive Bayes?', 2),
        ('SVM', 'Ist SVM ein linearer Klassifikator?', 2),
        ('TF-IDF', 'Was macht IDF?', 3),
        ('K-Means', 'Wie wählt man K aus?', 3)
    """
]

# execute each SQL command to insert the data
for data_insert in data_inserts:
    try: 
        cur.execute(data_insert)
        conn.commit()  # commit after each data insertion
        print("Data inserted successfully")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()  # rollback the current transaction if there's an error

# execute each SQL command to create the tables
for table in tables:
    try: 
        cur.execute(table)
        conn.commit()  # commit after each table creation
        print("Table created successfully")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()  # rollback the current transaction if there's an error

# close the cursor and the connection
cur.close()
conn.close()
