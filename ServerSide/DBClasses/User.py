from .DBWrapper import DBWrapper


class User(DBWrapper):
    TABLE_NAME = "USERS"

    def __init__(self, username, password, email):
        super().__init__()
        self.username = username
        self.password = password
        self.email = email


    # Push current object onto DB
    def upload(self):
        self.cursor.execute('''
            INSERT INTO USERS(username, password, email) VALUES (%s, %s, %s);
        ''', (self.username, self.password, self.email))


    # Fetch an entry from DB, and return it as a python object of this class
    @staticmethod
    def fetch(email):
        DBWrapper.cursor.execute('''
            SELECT * FROM USERS WHERE email=(%s);
        ''', (email,))

        rec = DBWrapper.cursor.fetchone()
        if rec is None:
            return None

        return User(rec[0], rec[1], rec[2])


    # Fetch an entry into current object
    def fetch_into(self, email):
        self.cursor.execute('''
            SELECT * FROM USERS WHERE email=(%s);
        ''', email)

        rec = self.cursor.fetchone()
        if rec is None:
            return self
        self.email = rec[0]
        self.password = rec[1]

        return self

    @staticmethod
    def create_table():
        DBWrapper.exec_query('''
            create table USERS(
                username varchar(15) primary key,
                password varchar(100) not null,
                email varchar(30) not null unique,
                constraint password_length check(length(password)>=5)
            );

        ''')

    @staticmethod
    def drop_table():
        DBWrapper.exec_query('''
            DROP TABLE USERS;
        ''')
