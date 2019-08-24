from .DBWrapper import DBWrapper

class Comment(DBWrapper):
    TABLE_NAME = "COMMENT"

    def __init__(self, username, content, post_id):
        super().__init__()
        self.username = username
        self.content = content
        self.post_id = post_id

    def upload(self):
        DBWrapper.cursor.execute('''
            insert into comment(username, content, post_id)
            values(%s, %s, %s);
        ''', (self.username, self.content, self.post_id))

    @staticmethod
    def create_table():
        DBWrapper.exec_query('''
            create table COMMENT(
                username varchar(15),
                content text not null,
                post_id serial,
                add_time timestamp,
                
                constraint fk_comment_username foreign key(username)
                    references USERS(username)
                    on delete cascade,
                
                constraint fk_comment_post foreign key(post_id)
                    references POST(post_id)
                    on delete cascade
            );
            
            create function add_timestamp()
            returns trigger as $$
                BEGIN
                    NEW.add_time = current_timestamp;
                    return NEW;
                END 
            $$ language plpgsql;
            
            create trigger trig_timestamp 
                before insert on COMMENT
                for each row execute procedure add_timestamp();
        ''')

    @staticmethod
    def drop_table():
        DBWrapper.exec_query('''
            DROP TABLE COMMENT;
        ''')

    @staticmethod
    def fetch_for_post(post_id):
        DBWrapper.cursor.execute('''
            select username, content, post_id from COMMENT
            where post_id=(%s)
            order by add_time;
        ''', (post_id,))

        comments = DBWrapper.cursor.fetchall()
        return comments

    @staticmethod
    def fetch_all():
        DBWrapper.cursor.execute('''
            select username, content, post_id from COMMENT
            order by add_time;
        ''')
        return DBWrapper.cursor.fetchall()
