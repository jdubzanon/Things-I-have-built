from collections import ChainMap
import csv
from graph_parser.graph_parser import GraphParser


class GraphOrganizer(GraphParser):
	def __init__(self, ent_var, file_inp, *args):
		super().__init__(ent_var, *args)
		self.file = file_inp
		

		with open(self.file) as file:
			csv_file = csv.DictReader(file)
			try:
				if self.range1[0]:
					filter1 = filter(lambda row: 
											
										all([float(row[self.key_map[1]]) in self.range1,
					  						row[self.key_map[0]].upper() in self.value_dict[self.key_map[0]]]), csv_file) 
				
					for row in filter1:
						
						for key,value in row.items():
							for high_key,high_value in self.full_mapped_dict.items():
								for low_key,low_value in high_value.items():

									if all([row[self.key_map[0]].upper() == high_key.upper() , low_key == key]):
										self.full_mapped_dict[row[self.key_map[0]].upper()][low_key].append(float(row[key]))



			except TypeError:

				filter1 = filter(lambda row: row[self.key_map[0]].upper() in self.value_dict[self.key_map[0]], csv_file)

				for val in self.boundry_dict[self.key_map[1]]:
					filter2 = filter(lambda row: any([float(row[self.key_map[1]]) > float(val[1:]) if '>' in val else None,
												 float(row[self.key_map[1]]) < float(val[1:]) if '<' in val else None,
												 row[self.key_map[1]].upper() == val.upper()]), filter1) 

				for row in filter2:
					for key,value in row.items():
						for high_key,high_value in self.full_mapped_dict.items():
							for low_key,low_value in high_value.items():
								if all([row[self.key_map[0]].upper() == high_key.upper() , low_key == key]):
									self.full_mapped_dict[row[self.key_map[0]].upper()][low_key].append(float(row[key]))


