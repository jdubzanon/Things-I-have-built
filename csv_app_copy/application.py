import tkinter as tk
from tkinter import *
import subprocess
import webbrowser as wb
import parser.final_parser as fp
from shells import shell
from file_systemizer import file_systemizer as fsys
from list_creature import create_list
from graphinator.graphinator import Graphinator as gp
from db_handler.db_handler import DbHandler 
from file_saver.file_saver import Save


class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.lc = None
		self.organized_data = list()
		self.function_dict = {
            'showme': self.showme,
            'connect': self.connect,
            'check' : self.check,
            'peek': self.peek,
        	'synop' : self.get_web_page,
            'list': self.create_list,
            'filter': self.organize,
            'graph': self.graph,
        	'add' : self.add_record,
        	'delete' : self.del_record,
        	'db!' : self.see_database,
        	'save' : self.save
        }
		
		self.columnconfigure(0,weight=1)
		self.rowconfigure(0,weight=1)

		self.sh = shell.Shell()
		
		
		self.sh.columnconfigure(0,weight=1)
		self.sh.rowconfigure(0,weight=0)
		self.sh.rowconfigure(1,weight=0)
		self.sh.rowconfigure(2,weight=1)
		self.sh.grid(sticky='nsew',padx=20,pady=20)
		
		self.sh.ent_widget.focus_set()		
		
		self.sh.ent_widget.bind('<Return>', self.bind_ent_widget_func)
		
		
	def bind_ent_widget_func(self, event):
		if self.sh.entry_var.get():
			self.sh.big_box.delete('1.0', tk.END)

		# command history list
		command = self.sh.entry_var.get()
		self.sh.command_history_list.append(command)

#		 parsing text based commands and calling functions from entrybox widget
		
		self.func_list = list(filter(lambda func: func in self.function_dict, self.sh.entry_var.get().split()))
		if not self.func_list:
			self.sh.big_box.insert('1.0', 'Need to begin your Query with a command!\n ')
		
		elif len(self.func_list) > 1:
			self.sh.big_box.insert('1.0', 'Too Many Functions, Try Again')
		
		else:
			for item in self.func_list:
				if item in self.function_dict:
					self.function_dict[item]()
		self.sh.entry_var.set('')
		
	def showme(self):
		self.fs = fsys.FileSystemizer(self.sh.entry_var.get())
		file = self.fs.showme()
		self.sh.big_box.insert('1.0', file)

	def connect(self):
		self.fs = fsys.FileSystemizer(self.sh.entry_var.get())
		self.fs.connect()
		
		if self.fs.master_file:
			self.sh.big_box.insert('1.0', f'You are connected to {self.fs.master_file.name}')
		else:
			self.sh.big_box.insert('1.0', f'Please enter a valid file name')
		
	def check(self):
		try:
			if self.fs.master_file:
				if 'file' in self.sh.entry_var.get(): 
					self.sh.big_box.insert('1.0', self.fs.master_file.name)
				elif 'dir' in self.sh.entry_var.get():
					self.sh.big_box.insert('1.0', self.fs.master_file.parts[-2])
				else:
					self.sh.big_box.insert('1.0', f'{self.sh.entry_var.get().split()[1:]} is not a file!')
			else:
				self.sh.big_box.insert('1.0', "Need to connect to a file!")
		except AttributeError:
			self.sh.big_box.insert('1.0' , 'Need to connect to a file first')		
	
	def peek(self):
		try:
			subprocess.run(['gedit', '{}'.format(self.fs.master_file)])
		except AttributeError:
			self.sh.big_box.insert('1.0', 'Need to connect to a file first!')
	

	def create_list(self):
		self.organized_data.clear()
		try:	
			try:
				self.lc = create_list.ListCreator(entry_var=self.sh.entry_var.get(),
										 file_path=self.fs.master_file)
				try:
					for data in self.lc.creatin_da_list()[::-1]:
						self.sh.big_box.insert('1.0', (str(data) + '\n'))
					if not self.lc.data:
						self.sh.big_box.insert('1.0', 'No Matches')
				except TypeError:
					self.sh.big_box.insert('1.0', "No Matches")
			except AttributeError:
				self.sh.big_box.insert('1.0', "Need to connect to a file first!")
		except (IndexError, KeyError, ValueError):
		 	self.sh.big_box.insert('1.0', 'Bad Syntax, Try again')
			

	def organize(self):
		self.organized_data.clear()
		try:
			for values in self.lc.data[::-1]:
				if values not in self.organized_data:
					self.organized_data.append(values)
			
			
			for data in self.organized_data:
				self.sh.big_box.insert('1.0', data + '\n')
	
		except AttributeError:
			self.sh.big_box.insert('1.0', 'No data to organize!')
	
	def graph(self):
		try:
			try:
				gp_ = gp(ent_var=self.sh.entry_var.get(),
									file_inp=self.fs.master_file,root=self)					
			except IndexError:
				self.sh.big_box.insert('1.0', 'Bad Syntax, Try Again!')
			except ValueError:
				self.sh.big_box.insert('1.0', 'Are you trying to graph words?')
		
		except AttributeError:
			self.sh.big_box.insert('1.0', 'Need to connect to a file first!')
		
					
	
	def get_web_page(self):
		web_site = None		
		dh = DbHandler(self.sh.entry_var.get())
		data = dh.get_web_site()
		try:
			if data:
				for file_, website in dh.get_web_site():
					if file_ == self.fs.master_file.name:
						web_site = website
			
				try:
					df = wb.get()
					df.open(web_site)	
				except TypeError:
					self.sh.big_box.insert('1.0', 'File is not in database use "db!" to check database\n') 
					dh.con.close()
		
			else:
				self.sh.big_box.insert('1.0', 'DataBase is Empty!')
				dh.con.close()
		except AttributeError:
			self.sh.big_box.insert('1.0', 'Need to connect to a file')


	def add_record(self):
		dh = DbHandler(self.sh.entry_var.get())
	
		try:
			dh.add_record()
		except AttributeError:
			self.sh.big_box.insert('1.0', 'File is already in the DataBase!')
		except TypeError:
			self.sh.big_box.insert('1.0', f' {self.sh.entry_var.get().split()[1:]} is not a file')

	
	
	def del_record(self):
		dh = DbHandler(self.sh.entry_var.get())
		try:
			dh.del_record()
		except FileNotFoundError:
			self.sh.big_box.insert('1.0', f'{self.sh.entry_var.get().split()[1:]} is not a file!')
		except AttributeError:
			self.sh.big_box.insert('1.0', f'{self.sh.entry_var.get().split()[1:]} is not in the DataBase!')
		
		
	def see_database(self):
		dh = DbHandler(self.sh.entry_var.get())
		data = dh.see_db()
		if data:
			for file_ , website in data:
				self.sh.big_box.insert('1.0',f'\n{file_} --> {website}\n')
		else:
			self.sh.big_box.insert('1.0', 'Database is Empty!!')

	def save(self):
		try:
			if not self.lc.data:
				self.sh.big_box.insert('1.0', 'No data to write!')
			
			elif self.organized_data:
				save = Save(ent_var=self.sh.entry_var.get(), data=self.organized_data)
				save.to_file()
				self.organized_data.clear()
				self.sh.big_box.insert('1.0', f'Your data has been saved in {save.path}')

			else:
				save = Save(ent_var=self.sh.entry_var.get(), data=self.lc.data)			
				save.to_file()				
				self.organized_data.clear()
				self.sh.big_box.insert('1.0', f'Your data has been saved in {save.path}')
		except AttributeError:
			self.sh.big_box.insert('1.0', 'No data to write!')
		except IndexError:
			self.sh.big_box.insert('1.0', 'Need a file name!')



if __name__ == '__main__':
	app = App()
	app.title('CSV EATER')
	app.mainloop()
	
	
	
