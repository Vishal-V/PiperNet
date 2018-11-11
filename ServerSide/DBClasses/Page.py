from .DBWrapper import DBWrapper
from flask_login import UserMixin

class Profile(DBWrapper):
	TABLE_NAME = "PAGE"

	def __init__(self, create_by, create_for, followers, content, place, image='default.jpg', misc='default.jpg'):
		self.create_by = create_by
		self.create_for = create_for
		self.followers = followers
		self.content = content
		self.place = place
		self.image = image 
		self.misc = misc

	@staticmethod
	def create_table():
		DBWrapper.exec_query('''
			create table PROFILE(
				id serial,
				create_by varchar(15), 
				create_for varchar(15), 
				followers integer,
				content text, 
				place varchar(20), 	
				image varchar(150), 
				misc varchar(30),
				constraint cpk_2 primary key(id, create_for)
			);
		''')

	def upload(self):
		self.cursor.execute('''
			INSERT INTO PROFILE(create_by, create_for, followers, content, place, image, misc) VALUES (%s,%s,%s,%s,%s,%s,%s);

		''', (self.create_by, self.create_for, self.followers, self.content, self.place, self.image, self.misc))

	@staticmethod
    def drop_table():
        DBWrapper.exec_query('''
            DROP TABLE PAGE;
        ''')