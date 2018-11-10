from .DBWrapper import DBWrapper

class Profile(DBWrapper):
	TABLE_NAME = "PROFILE"

	def __init__(self, username, name, profile_pic='default.jpg', status, dob, lives_in, place, friends):
		self.username = username
		self.name = name
		self.profile_pic = profile_pic
		self.status = status
		self.dob = dob
		self. lives_in = lives_in
		self.place = place 
		self.friends = friends

	@staticmethod
	def create_table():
		DBWrapper.exec_query('''
			create table PROFILE(
				username varchar(15), 
				name varchar(15), 
				image varchar(30), 
				status text, 
				dob date, 
				lives_in varchar(20), 
				place varchar(20), 
				friends integer,
				constraint cpk_1 primary key(username, name),				
			);
		''')

