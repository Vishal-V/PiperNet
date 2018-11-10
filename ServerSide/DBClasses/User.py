from .DBWrapper import DBWrapper
from flask_login import UserMixin

class User(DBWrapper, UserMixin):
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

        return User(rec[0], rec[2], rec[3])


    @staticmethod
    def fetch_username(username):
        DBWrapper.cursor.execute('''
            SELECT * FROM USERS WHERE username=(%s);
        ''', (username,))

        rec = DBWrapper.cursor.fetchone()
        if rec is None:
            return None

        return User(rec[0], rec[1], rec[2])        

    @staticmethod
    def fetch_userid(user_id):
        DBWrapper.cursor.execute('''
            SELECT * FROM USERS WHERE id=(%s);
        ''', (user_id,))

        rec = DBWrapper.cursor.fetchone()
        if rec is None:
            return None

        return User(rec[0], rec[1], rec[2]) 

    # def is_authenticated(self):
    #     return True

    # def is_active(self):
    #     return True

    # def is_anonymous(self):
    #     return False

    #This method defies logic, but it works. It is an overrride
    def get_id(self):
        DBWrapper.cursor.execute('''
            SELECT * FROM USERS WHERE id=(%s);
        ''', (self.username,))

        rec = DBWrapper.cursor.fetchone()
        if rec is None:
            return None

        user1 = User(rec[0], rec[1], rec[2])  
        return (user1.username)

    # Fetch an entry into current object
    def fetch_into(self, email):
        self.cursor.execute('''
            SELECT * FROM USERS WHERE email=(%s);
        ''', email)

        rec = self.cursor.fetchone()
        if rec is None:
            return self
        self.email = rec[1]
        self.password = rec[2]

        return self

    @staticmethod
    def create_table():
        DBWrapper.exec_query('''
            create table USERS(
                id serial,
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
