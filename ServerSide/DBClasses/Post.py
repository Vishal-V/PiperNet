from .DBWrapper import DBWrapper
from datetime import datetime


class Post(DBWrapper):
    TABLE_NAME = "POST"

    def __init__(self, username):
        super().__init__()
        self.username = username

    @staticmethod
    def create_table():
        DBWrapper.exec_query('''
           create table POST(
                username varchar(15),
                post_id serial primary key,
                title varchar(20) not null,
                date varchar(20),
                content text,
                picture text,
                constraint fk_post foreign key(username)
                    references USERS(username)
                    on delete cascade
            );
        ''')

    @staticmethod
    def drop_table():
        DBWrapper.exec_query('''
            DROP TABLE POST;
        ''')