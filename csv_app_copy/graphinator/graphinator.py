import tkinter as tk
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from graph_organizer.graph_organizer import GraphOrganizer


class Graphinator(GraphOrganizer):
	def __init__(self, ent_var, file_inp,root=None):
		super().__init__(ent_var,file_inp)
		
		self.root = Toplevel(root)
		self.root.columnconfigure(0,weight=1)
		self.root.rowconfigure(0,weight=1)
		
		
		
		self.check_var = tk.StringVar()
		
		# frame for title row 0
		self.title_frame = tk.Frame(self.root,borderwidth=5)
		self.title_frame.grid(row=0,column=0,sticky='ew')
		self.title_frame.columnconfigure(0,weight=1)	
		
		# label holding title
		self.title_label = tk.Label(self.title_frame,text='Choose Your Graph Type!',height=3,relief='groove',bg='red')
		self.title_label.grid(sticky='ew')
		
								
		#frame for row 1
		self.text_box_frame_pie = tk.Frame(self.root,borderwidth=5,relief='groove')
		self.text_box_frame_pie.grid(row=1,column=0)
		
		#image holder
		self.pie_bbox = tk.Text(self.text_box_frame_pie,height=10,width=35)
		self.pie_bbox.grid(row=0,column=1)
		
		#photo
		pie_image = tk.PhotoImage(master=self.root,file='/media/jdubzanon/SS/csv_app/graph_photo/pie.png')
		self.pie_bbox.image_create('1.0', image=pie_image)
		
		self.radio_btn1 = tk.Radiobutton(self.text_box_frame_pie, text='Pie\n\tGraph\t', variable=self.check_var,value='Pie')
		self.radio_btn1.grid(row=0, column=0)
		
		###############################################################
		
		self.tex_box_frame_bar = tk.Frame(self.root,borderwidth=5,relief='groove')
		self.tex_box_frame_bar.grid(row=2,column=0)

		self.bar_image_bbox = tk.Text(self.tex_box_frame_bar, height=10,width=35)
		self.bar_image_bbox.grid(row=0,column=1)
		
		bar_image = tk.PhotoImage(master=self.root,file='/media/jdubzanon/SS/csv_app/graph_photo/bar.png')
		
		self.bar_image_bbox.image_create('1.0', image=bar_image)
		
		self.radio_btn2 = tk.Radiobutton(self.tex_box_frame_bar, text='Bar\n\tGraph\t', variable=self.check_var,value='bar')
		self.radio_btn2.grid(row=0, column=0)
		
		##############################################################################
		
		self.text_box_frame_line = tk.Frame(self.root,borderwidth=5,relief='groove')
		self.text_box_frame_line.grid(row=3,column=0)

		self.line_image_bbox = tk.Text(self.text_box_frame_line, height=10,width=35)
		self.line_image_bbox.grid(row=0,column=1)
		
		line_image = tk.PhotoImage(master=self.root,file='/media/jdubzanon/SS/csv_app/graph_photo/line.png')

		self.line_image_bbox.image_create('1.0', image=line_image)
		
		self.radio_btn3 = tk.Radiobutton(self.text_box_frame_line, text='Line\n\tGraph\t', variable=self.check_var,value='line')
		self.radio_btn3.grid(row=0,column=0)

###########################################################################################################		
		self.error_var = tk.StringVar()
		self.error_label = tk.Label(self.root, textvariable=self.error_var)
		self.error_label.grid()

#############################################################################################################		
		self.button = tk.Button(self.root,text='Press to Graph!', command=self.getter,fg='white',bg='black')
		self.button.grid()
		
		
		self.root.geometry('700x700')
		self.root.mainloop()		
	
	def getter(self):
		try:	
			if self.check_var.get() == 'Pie': 
				data = list()
				distance = 0.2
				sep = list()
				for i in range(len(self.map_set)):
					sep.append(distance)
						
				for high_key,high_value in self.full_mapped_dict.items():
					for low_key in high_value:
						data.append(max(self.full_mapped_dict[high_key][low_key]))
				
				self.root.destroy()
				plt.pie(x=data,labels=self.map_set,autopct=f'%.2f',shadow=True,explode=sep)					
				plt.show()
		
		
			elif self.check_var.get() == 'bar':
				data = list()
					
				for high_key,high_value in self.full_mapped_dict.items():
					for low_key in high_value:
						data.append(max(self.full_mapped_dict[high_key][low_key]))
					
				self.root.destroy()
				map_colors = list(mcolors.CSS4_COLORS)
					
				colors_for_graph = list()
							
				for i in range(len(self.map_set)):
					colors_for_graph.append(map_colors[i*3])		
							
					
				plt.barh(y=self.map_set,height=0.8,align='center',width=data,color=colors_for_graph,label=self.map_set)


				plt.legend(loc='best',fontsize='x-small')
				plt.show()
			
			
			elif self.check_var.get() == 'line':
	
				for high_key,high_value in self.full_mapped_dict.items():
						for low_key in high_value:
							plt.plot(self.full_mapped_dict[high_key][low_key], label=(f'{high_key}-{low_key}'))				
				
				self.root.destroy()
				
				plt.legend(loc='best', fontsize='x-small')
				
				plt.show()

			else:
				self.error_var.set('Need to choose a graph style')
				self.error_label.config(bg='red')
							
		except ValueError:
			self.error_var.set('Bad Syntax close window and check your categories')
			self.error_label.config(bg='red', font='Times 15')








