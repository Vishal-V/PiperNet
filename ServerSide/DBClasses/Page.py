from .DBWrapper import DBWrapper

class Page(DBWrapper):
	TABLE_NAME = "PAGE"

	def __init__(self, create_by, create_for, company, followers, content, place, image='default.jpg', misc='default.jpg'):
		super().__init__()
		self.create_by = create_by
		self.create_for = create_for
		self.company = company
		self.followers = followers
		self.content = content
		self.place = place
		self.image = image 
		self.misc = '/celebrity/' + create_for

	@staticmethod
	def create_table():
		DBWrapper.exec_query('''
			create table PAGE (
				create_by varchar(15), 
				create_for varchar(15),
				company varchar(20) ,
				followers integer,
				content text, 
				place varchar(20), 	
				image varchar(150), 
				misc varchar(150),
				id serial,
				constraint cpk_2 primary key(id, create_for),
				constraint fk_4 foreign key(create_by) references USERS(username) on delete cascade
			);
		''')

	def upload(self):
		self.cursor.execute('''
			INSERT INTO PAGE (create_by, create_for, company, followers, content, place, image, misc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);

		''', (self.create_by, self.create_for, self.company, self.followers, self.content, self.place, self.image, self.misc))

	@staticmethod
	def drop_table():
		DBWrapper.exec_query('''
			DROP TABLE PAGE;
		''')