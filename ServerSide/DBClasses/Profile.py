from .DBWrapper import DBWrapper
import random

class Profile(DBWrapper):
	TABLE_NAME = "PROFILE"

	def __init__(self, username, name, status, age, lives_in, place, friends, image='default.jpg'):
		self.username = username
		self.name = name
		self.status = status
		self.age = age
		self.lives_in = lives_in
		self.place = place 
		self.friends = friends
		self.image = image

	@staticmethod
	def create_table():
		DBWrapper.exec_query('''
			create table PROFILE(
				username varchar(15), 
				name varchar(15), 
				status text, 
				age integer check(age>=18),
				lives_in varchar(20), 
				place varchar(20), 
				friends integer,
				image varchar(30), 
				constraint cpk_1 primary key(username, name),
				constraint fk_2 foreign key(username) references USERS(username) on delete cascade
			);
		''')

	def upload(self):
		self.cursor.execute('''
			INSERT INTO PROFILE(username, name, status, age, lives_in, place, friends, image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);

		''', (self.username, self.name, self.status, self.age, self.lives_in, self.place, self.friends, self.image))

	
	def user_exists(self):
		self.cursor.execute('''
			SELECT * FROM PROFILE WHERE username=(%s);
		''', (self.username,))

		val = DBWrapper.cursor.fetchone()

		if val is None:
			return False
		return True		


	def update_values(self, username):
		self.cursor.execute('''
			UPDATE PROFILE
			SET name=(%s), status=(%s), age=(%s), lives_in=(%s), place=(%s), friends=(%s), image=(%s)
			WHERE username=(%s);
		''', (self.name, self.status, self.age, self.lives_in, self.place, self.friends, self.image, username))


	@staticmethod
	def drop_table():
		DBWrapper.exec_query('''
			DROP TABLE PROFILE;
		''')
