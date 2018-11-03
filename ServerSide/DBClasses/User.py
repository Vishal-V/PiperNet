from DBWrapper import DBWrapper
import psycopg2


class User(DBWrapper):
    TABLE_NAME = "USER"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def upload(self):
        DBWrapper.cursor.execute('''
            INSERT INTO USERS(Username, Password) VALUES (%s, %s);
        ''', (self.username, self.password))

    def fetch(self, username):
        DBWrapper.cursor.execute('''
            SELECT * FROM USERS WHERE Username=(%s);
        ''', username)

        return DBWrapper.cursor.fetchone()

