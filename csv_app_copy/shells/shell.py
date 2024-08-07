import tkinter as tk
from tkinter import ttk



class Shell(ttk.Frame):
	def add_frame(self, label, row=None, col=None):
		frame = ttk.LabelFrame(self, text=label)
		frame.grid(row=row, column=col,sticky='nsew')
		return frame

	def __init__(self, *args, **kwargs):
		super().__init__()

        #####entry widget/command execution window####
		entry_frame = self.add_frame('Enter Commands Here', row=0)
		entry_frame.columnconfigure(0,weight=1)
		self.entry_var = tk.StringVar()
		self.ent_widget = tk.Entry(entry_frame, textvariable=self.entry_var,font='Times 12')
		self.ent_widget.grid(sticky='ew')

        #####command history window#####  row1
		command_history_frame = self.add_frame('Command History', row=1)
		command_history_frame.columnconfigure(0,weight=1)
		self.history_var = tk.StringVar()
		self.command_history_list = []
		self.command_history = ttk.Combobox(command_history_frame, values=self.command_history_list,background='black',foreground='white',
                                        						postcommand=lambda: self.command_history.configure(
                                            					values=self.command_history_list,
                                            					takefocus=1))
		self.command_history.grid(sticky='ew')

    ###textbox widget/output window#####
		textbox_frame = self.add_frame('Output Window', row=2) 
		textbox_frame.columnconfigure(0,weight=1)
		textbox_frame.rowconfigure(0,weight=1)
		self.big_box = tk.Text(textbox_frame,  background='black', foreground='white',
                           takefocus=0, wrap='none')

		self.big_box.grid(sticky='nsew')

		###widget binding###
		self.command_history.bind('<Return>', self.cmd_history_bind_func)
		self.big_box.bind('<FocusIn>', self.handler)


	def handler(self,event):
		self.big_box.bind('<Any-KeyPress>', lambda event: self.big_box.configure(state='disabled'), add='+')
		self.big_box.bind('<Any-KeyRelease>', lambda event: self.big_box.configure(state='normal'), add='+')


	def cmd_history_bind_func(self, event):
		self.command_history.focus_set()
		self.entry_var.set(self.command_history_list[self.command_history.current()])
		self.ent_widget.focus_set()
		self.ent_widget.icursor(tk.END)
		self.command_history.set('')
		
		
		
