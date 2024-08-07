import sqlite3
import pathlib

class DbHandler:
	def __init__(self,entry_var):
		self.entry_var = entry_var.split()
		self.file_name = None
		self.master_path = pathlib.Path('/media') 
		self.resolved_path = None
		
		self.con = sqlite3.connect('website.db')
		self.cur = self.con.cursor()
		

	def get_web_site(self):
		data = list(self.cur.execute('SELECT * FROM web_mapper'))

		return data if data else None




	def add_record(self):
		self.file_name = self.entry_var[1]

		#verifying that the file being added is an actual file on /media

		self.resolved_path = list(self.master_path.glob(f'**/{self.file_name}'))
		
		if len(self.entry_var) == 3:
			if self.resolved_path:
				adding = (self.entry_var[1], self.entry_var[2])
				if list(self.cur.execute('SELECT * FROM web_mapper Where file_name LIKE "{}"'.format(adding[0]) )):
					raise AttributeError
				else: 
					self.cur.execute('INSERT INTO web_mapper VALUES (?,?)', adding)	
		
					self.con.commit()
					self.con.close
					
			else:
				raise TypeError 
	
	
	def del_record(self):
		self.file_name = self.entry_var[1]
		self.resolved_path = list(self.master_path.glob(f'**/{self.file_name}'))
		
		# IF ITS NOT IN THE DB THE RAISE AN ERROR
		if self.resolved_path:
			if not list(self.cur.execute('SELECT * FROM web_mapper WHERE file_name LIKE "{}"'.format(self.file_name))):
				raise AttributeError
			# IF IT IS IN THE DB THE DELETE IT
			else:
				self.cur.execute('DELETE FROM web_mapper WHERE file_name LIKE "{}"'.format(self.file_name ))		
		else:
			raise FileNotFoundError
		
		self.con.commit()
		self.con.close()		
			
	

	def see_db(self):
		data = list(self.cur.execute('SELECT * FROM web_mapper'))
		
		self.con.close()
		
		return data if data else None
			

























