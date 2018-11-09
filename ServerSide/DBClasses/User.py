from .DBWrapper import DBWrapper


class User(DBWrapper):
    TABLE_NAME = "USERS"

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password


    # Push current object onto DB
    def upload(self):
        self.cursor.execute('''
            INSERT INTO USERS(Username, Password) VALUES (%s, %s);
        ''', (self.username, self.password))


    # Fetch an entry from DB, and return it as a python object of this class
    @staticmethod
    def fetch(username):
        DBWrapper.cursor.execute('''
            SELECT * FROM USERS WHERE Username=%s;
        ''', (username,))

        rec = DBWrapper.cursor.fetchone()
        if rec is None:
            return None

        return User(rec[0], rec[1])


    # Fetch an entry into current object
    def fetch_into(self, username):
        self.cursor.execute('''
            SELECT * FROM USERS WHERE Username=(%s);
        ''', username)

        rec = self.cursor.fetchone()
        if rec is None:
            return self
        self.username = rec[0]
        self.password = rec[1]

        return self

    @staticmethod
    def create_table():
        DBWrapper.exec_query('''
            create table USERS(
                
            )
        ''')
