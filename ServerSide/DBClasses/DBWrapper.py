import psycopg2


class DBWrapper:
    db = psycopg2.connect(database="postgres", user="postgres", password="abcd1234", host="127.0.0.1", port=5432)
    db.set_session(autocommit=True)
    cursor = db.cursor()

    def __init__(self):
        if DBWrapper.db.closed:
            DBWrapper.db = psycopg2.connect(database="postgres", user="postgres", password="abcd1234", host="127.0.0.1", port=5432)
            DBWrapper.db.set_session(autocommit=True)

    @staticmethod
    def exec_query(query):
        DBWrapper.cursor.execute(query)