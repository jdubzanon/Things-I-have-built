import csv
from collections import ChainMap
import parser.final_parser as fp 
import numpy as arr
import pathlib


class ListCreator(fp.Parser3):
		def __init__(self, entry_var, file_path, *args):
			super().__init__(entry_var, *args)
			#master_file
			self.file_path = file_path
			self.range1 = None
			self.range2 = None
			self.range3 = None	
			self.data = list()		
		
		def creatin_da_list(self):
			with self.file_path.open() as fi:
				csv_file = csv.DictReader(fi)
				if len(self.split_input) == 2:
					if self.split_input[-1] == 'cats':
						for names in csv_file.fieldnames:
							self.data.append(names)
						return self.data
					
					elif self.split_input[-1] == 'catx':
						count = 0
						for row in csv_file:
							count += 1
							if count == 2:
								for values in csv_file.fieldnames:
									self.data.append(f"{values} :  {row[values]}")			
								break
						return self.data
				
				
				if len(self.split_input) > 2:		
					self.parse()
					if len(self.rangedict) + len(self.list_of_dicts) == 3:
						
						
						
						if len(self.rangedict) == 3:
								
							key_map = list(ChainMap(self.print_cat_dict, self.rangedict[2], self.rangedict[1], self.rangedict[0]))
							
							self.range1 = arr.arange(float(self.rangedict[0][key_map[0]][0]) ,
							float(self.rangedict[0][key_map[0]][1]) + 1,0.1).astype('f')
							
							self.range2 = arr.arange(float(self.rangedict[1][key_map[1]][0]), 
							float(self.rangedict[1][key_map[1]][1]) + 1, 0.1).astype('f')
							
							self.range3 = arr.arange(float(self.rangedict[2][key_map[2]][0]), 
							float(self.rangedict[2][key_map[2]][1]) + 1, 0.1).astype('f')


							filter1 = filter(lambda row: 
														all([float(row[key_map[0]]) in self.range1,
														float(row[key_map[1]]) in self.range2,
														float(row[key_map[2]]) in self.range3   ]), csv_file)
							
							
							for row in filter1:
								if len(self.print_cat_dict[key_map[3]]) > 4:
									self.data.append('Max 4 Categories')
								
								if len(self.print_cat_dict[key_map[3]]) == 4:
									self.data.append((f'{self.print_cat_dict[key_map[3]][0]}: {row[self.print_cat_dict[key_map[3]][0]]} {self.print_cat_dict[key_map[3]][1]}: {row[self.print_cat_dict[key_map[3]][1]]} {self.print_cat_dict[key_map[3]][2]}: {row[self.print_cat_dict[key_map[3]][2]]} {self.print_cat_dict[key_map[3]][3]}: {row[self.print_cat_dict[key_map[3]][3]]}'))
							
								elif len(self.print_cat_dict[key_map[3]]) == 3:
									self.data.append((f'{self.print_cat_dict[key_map[3]][0]}: {row[self.print_cat_dict[key_map[3]][0]]} {self.print_cat_dict[key_map[3]][1]}: {row[self.print_cat_dict[key_map[3]][1]]} {self.print_cat_dict[key_map[3]][2]}: {row[self.print_cat_dict[key_map[3]][2]]}'))						
							
								elif len(self.print_cat_dict[key_map[3]]) == 2:
									self.data.append((f'{self.print_cat_dict[key_map[3]][0]}: {row[self.print_cat_dict[key_map[3]][0]]} {self.print_cat_dict[key_map[3]][1]}: {row[self.print_cat_dict[key_map[3]][1]]}'))
													
								else:
									self.data.append(f'{self.print_cat_dict[key_map[3]][0]}: {row[self.print_cat_dict[key_map[3]][0]]}')							

							return self.data


						elif all([   (len(self.rangedict) == 2),
									(len(self.list_of_dicts) == 1)    ]):
							
							data = list()
								
							key_map = list(ChainMap(self.print_cat_dict, self.list_of_dicts[0], self.rangedict[1], self.rangedict[0]))

							self.range1 = arr.arange(float(self.rangedict[0][key_map[0]][0]), 
							float(self.rangedict[0][key_map[0]][1]) + 1, 0.1).astype('f')
							
							self.range2 = arr.arange(float(self.rangedict[1][key_map[1]][0]), 
							float(self.rangedict[1][key_map[1]][1]) + 1, 0.1).astype('f')
						    

							filter1 = filter(lambda row: all([float(row[key_map[0]]) in self.range1,
															float(row[key_map[1]]) in self.range2 ]), csv_file)

							for row in filter1:
								for val in self.list_of_dicts[0][key_map[2]]:

									if any([row[key_map[2]].upper() == val.upper(),
									float(row[key_map[2]]) > float(val[1:]) if '>' in val else None,
									float(row[key_map[2]]) < float(val[1:]) if '<' in val else None]):
										data.append(row)
									
							for row in data:
								if len(self.print_cat_dict[key_map[3]]) > 4:
									self.data.append('Max 4 Categories')
								
								if len(self.print_cat_dict[key_map[3]]) == 4:
									self.data.append((f'{self.print_cat_dict[key_map[3]][0]}: {row[self.print_cat_dict[key_map[3]][0]]} {self.print_cat_dict[key_map[3]][1]}: {row[self.print_cat_dict[key_map[3]][1]]} {self.print_cat_dict[key_map[3]][2]}: {row[self.print_cat_dict[key_map[3]][2]]} {self.print_cat_dict[key_map[3]][3]}: {row[self.print_cat_dict[key_map[3]][3]]}'))
							
								elif len(self.print_cat_dict[key_map[3]]) == 3:
									self.data.append((f'{self.print_cat_dict[key_map[3]][0]}: {row[self.print_cat_dict[key_map[3]][0]]} {self.print_cat_dict[key_map[3]][1]}: {row[self.print_cat_dict[key_map[3]][1]]} {self.print_cat_dict[key_map[3]][2]}: {row[self.print_cat_dict[key_map[3]][2]]}'))						
							
								elif len(self.print_cat_dict[key_map[3]]) == 2:
									self.data.append((f'{self.print_cat_dict[key_map[3]][0]}: {row[self.print_cat_dict[key_map[3]][0]]} {self.print_cat_dict[key_map[3]][1]}: {row[self.print_cat_dict[key_map[3]][1]]}'))
													
								else:
									self.data.append(f'{self.print_cat_dict[key_map[3]][0]}: {row[self.print_cat_dict[key_map[3]][0]]}')
							
							data.clear()
							return self.data
							    


						elif all([len(self.rangedict) == 1,
								len(self.list_of_dicts) == 2]):
							
							data = list()
							
							key_map = list(ChainMap(self.print_cat_dict, self.list_of_dicts[1], self.list_of_dicts[0], self.rangedict[0]))
							
							self.range1 = arr.arange(   float(self.rangedict[0][key_map[0]][0]),
														float(self.rangedict[0][key_map[0]][1]) + 1, 0.1     ).astype('f')
							
							filter1 = filter(lambda row: float(row[key_map[0]]) in self.range1, csv_file)
							
							for row in filter1:
								for first_val in self.list_of_dicts[0][key_map[1]]:
									for second_val in self.list_of_dicts[1][key_map[2]]:
										if all([ 
										any([	row[key_map[1]].upper() == first_val.upper(),
												float(row[key_map[1]]) > float(first_val[1:]) if '>' in first_val else None,
												float(row[key_map[1]]) < float(first_val[1:]) if '<' in first_val else None]), 
												
												
												any([ row[key_map[2]].upper() == second_val.upper(),
												float(row[key_map[2]]) > float(second_val[1:]) if '>' in second_val else None,
												float(row[key_map[2]]) < float(second_val[1:]) if '<' in second_val else None    ])        ]):
											data.append(row)

							for row in data:
								if len(self.print_cat_dict[key_map[3]]) > 4:
									self.data.append('Max 4 Categories')
								
								if len(self.print_cat_dict[key_map[3]]) == 4:
									self.data.append((f'{self.print_cat_dict[key_map[3]][0]}: {row[self.print_cat_dict[key_map[3]][0]]} {self.print_cat_dict[key_map[3]][1]}: {row[self.print_cat_dict[key_map[3]][1]]} {self.print_cat_dict[key_map[3]][2]}: {row[self.print_cat_dict[key_map[3]][2]]} {self.print_cat_dict[key_map[3]][3]}: {row[self.print_cat_dict[key_map[3]][3]]}'))
							
								elif len(self.print_cat_dict[key_map[3]]) == 3:
									self.data.append((f'{self.print_cat_dict[key_map[3]][0]}: {row[self.print_cat_dict[key_map[3]][0]]} {self.print_cat_dict[key_map[3]][1]}: {row[self.print_cat_dict[key_map[3]][1]]} {self.print_cat_dict[key_map[3]][2]}: {row[self.print_cat_dict[key_map[3]][2]]}'))						
							
								elif len(self.print_cat_dict[key_map[3]]) == 2:
									self.data.append((f'{self.print_cat_dict[key_map[3]][0]}: {row[self.print_cat_dict[key_map[3]][0]]} {self.print_cat_dict[key_map[3]][1]}: {row[self.print_cat_dict[key_map[3]][1]]}'))
													
								else:
									self.data.append(f'{self.print_cat_dict[key_map[3]][0]}: {row[self.print_cat_dict[key_map[3]][0]]}')
							
							
							data.clear()
							return self.data
							

						elif len(self.list_of_dicts) == 3:
							
							data = list()
							
							
							key_map = list(ChainMap(self.print_cat_dict, self.list_of_dicts[2], 
							self.list_of_dicts[1], self.list_of_dicts[0]))

							for row in csv_file:						
								for first_val in self.list_of_dicts[0][key_map[0]]:
									for second_val in self.list_of_dicts[1][key_map[1]]:
										for third_val in self.list_of_dicts[2][key_map[2]]:
											if all([
											
											any([row[key_map[0]].upper() == first_val.upper(),
											 float(row[key_map[0]]) > float(first_val[1:]) if '>' in first_val else None,
											float(row[key_map[0]]) < float(first_val[1:]) if '<' in first_val else None]),
											
											
											
											 any([
											row[key_map[1]].upper() == second_val.upper(), 
											float(row[key_map[1]]) > float(second_val[1:]) if '>' in second_val else None,
											float(row[key_map[1]]) < float(second_val[1:]) if '<' in second_val else None
											]),
											
											
											
											any([ 
											row[key_map[2]].upper() == third_val.upper(), 
											float(row[key_map[2]]) > float(third_val[1:]) if '>' in third_val else None,
											float(row[key_map[2]]) < float(third_val[1:]) if '<' in third_val else None
											
											])
											    ]):
												data.append(row)
											
														
							for row in data:
								if len(self.print_cat_dict[key_map[3]]) > 4:
									self.data.append('Max 4 Categories')
								
								if len(self.print_cat_dict[key_map[3]]) == 4:
									self.data.append((f'{self.print_cat_dict[key_map[3]][0]}: {row[self.print_cat_dict[key_map[3]][0]]} {self.print_cat_dict[key_map[3]][1]}: {row[self.print_cat_dict[key_map[3]][1]]} {self.print_cat_dict[key_map[3]][2]}: {row[self.print_cat_dict[key_map[3]][2]]} {self.print_cat_dict[key_map[3]][3]}: {row[self.print_cat_dict[key_map[3]][3]]}'))
							
								elif len(self.print_cat_dict[key_map[3]]) == 3:
									self.data.append((f'{self.print_cat_dict[key_map[3]][0]}: {row[self.print_cat_dict[key_map[3]][0]]} {self.print_cat_dict[key_map[3]][1]}: {row[self.print_cat_dict[key_map[3]][1]]} {self.print_cat_dict[key_map[3]][2]}: {row[self.print_cat_dict[key_map[3]][2]]}'))						
							
								elif len(self.print_cat_dict[key_map[3]]) == 2:
									self.data.append((f'{self.print_cat_dict[key_map[3]][0]}: {row[self.print_cat_dict[key_map[3]][0]]} {self.print_cat_dict[key_map[3]][1]}: {row[self.print_cat_dict[key_map[3]][1]]}'))
													
								else:
									self.data.append(f'{self.print_cat_dict[key_map[3]][0]}: {row[self.print_cat_dict[key_map[3]][0]]}')
							
							
							data.clear()
							return self.data


					elif len(self.rangedict) + len(self.list_of_dicts) == 2:
						if len(self.rangedict) == 2:
							
							
							key_map = list(ChainMap(self.print_cat_dict, self.rangedict[1], self.rangedict[0]))	
							
							self.range1 = arr.arange( float(self.rangedict[0][key_map[0]][0]),
							float(self.rangedict[0][key_map[0]][1]) + 1, 0.1 ).astype('f')
							
							self.range2 = arr.arange( float(self.rangedict[1][key_map[1]][0]),
							float(self.rangedict[1][key_map[1]][1]) + 1, 0.1 ).astype('f')
							
							filter1 = filter(lambda row: all([ float(row[key_map[0]]) in self.range1,
														       float(row[key_map[1]]) in self.range2     ]), csv_file)
							
							
							for row in filter1:
								if len(self.print_cat_dict[key_map[2]]) > 4:
									self.data.append('Max 4 Categories')
								
								if len(self.print_cat_dict[key_map[2]]) == 4:
									self.data.append((f'{self.print_cat_dict[key_map[2]][0]}: {row[self.print_cat_dict[key_map[2]][0]]} {self.print_cat_dict[key_map[2]][1]}: {row[self.print_cat_dict[key_map[2]][1]]} {self.print_cat_dict[key_map[2]][2]}: {row[self.print_cat_dict[key_map[2]][2]]} {self.print_cat_dict[key_map[2]][3]}: {row[self.print_cat_dict[key_map[2]][3]]}'))
							
								elif len(self.print_cat_dict[key_map[2]]) == 3:
									self.data.append((f'{self.print_cat_dict[key_map[2]][0]}: {row[self.print_cat_dict[key_map[2]][0]]} {self.print_cat_dict[key_map[2]][1]}: {row[self.print_cat_dict[key_map[2]][1]]} {self.print_cat_dict[key_map[2]][2]}: {row[self.print_cat_dict[key_map[2]][2]]}'))						
							
								elif len(self.print_cat_dict[key_map[2]]) == 2:
									self.data.append((f'{self.print_cat_dict[key_map[2]][0]}: {row[self.print_cat_dict[key_map[2]][0]]} {self.print_cat_dict[key_map[2]][1]}: {row[self.print_cat_dict[key_map[2]][1]]}'))
													
								else:
									self.data.append(f'{self.print_cat_dict[key_map[2]][0]}: {row[self.print_cat_dict[key_map[2]][0]]}')
							
							
							return self.data


						elif all([len(self.rangedict) == 1,
							len(self.list_of_dicts) == 1]):

							data = list()

							key_map = list(ChainMap(self.print_cat_dict, self.list_of_dicts[0], self.rangedict[0]))														
	
							self.range1 = arr.arange( float(self.rangedict[0][key_map[0]][0]),
							float(self.rangedict[0][key_map[0]][1]) + 1, 0.1).astype('f')
							
							filter1 = filter(lambda row: float(row[key_map[0]]) in self.range1, csv_file)
												
							for row in filter1:
								for first_val in self.list_of_dicts[0][key_map[1]]:
									if any([row[key_map[1]].upper() == first_val.upper(),
									float(row[key_map[1]]) > float(first_val[1:]) if '>' in first_val else None,
									float(row[key_map[1]]) < float(first_val[1:]) if '<' in first_val else None]):
										data.append(row)
								
							
							for row in data:
								if len(self.print_cat_dict[key_map[2]]) > 4:
									self.data.append('Max 4 Categories')
								
								if len(self.print_cat_dict[key_map[2]]) == 4:
									self.data.append((f'{self.print_cat_dict[key_map[2]][0]}: {row[self.print_cat_dict[key_map[2]][0]]} {self.print_cat_dict[key_map[2]][1]}: {row[self.print_cat_dict[key_map[2]][1]]} {self.print_cat_dict[key_map[2]][2]}: {row[self.print_cat_dict[key_map[2]][2]]} {self.print_cat_dict[key_map[2]][3]}: {row[self.print_cat_dict[key_map[2]][3]]}'))
							
								elif len(self.print_cat_dict[key_map[2]]) == 3:
									self.data.append((f'{self.print_cat_dict[key_map[2]][0]}: {row[self.print_cat_dict[key_map[2]][0]]} {self.print_cat_dict[key_map[2]][1]}: {row[self.print_cat_dict[key_map[2]][1]]} {self.print_cat_dict[key_map[2]][2]}: {row[self.print_cat_dict[key_map[2]][2]]}'))						
							
								elif len(self.print_cat_dict[key_map[2]]) == 2:
									self.data.append((f'{self.print_cat_dict[key_map[2]][0]}: {row[self.print_cat_dict[key_map[2]][0]]} {self.print_cat_dict[key_map[2]][1]}: {row[self.print_cat_dict[key_map[2]][1]]}'))
													
								else:
									self.data.append(f'{self.print_cat_dict[key_map[2]][0]}: {row[self.print_cat_dict[key_map[2]][0]]}')							
							
							data.clear()
							return self.data							
														

						elif len(self.list_of_dicts) == 2:
							
							data = list()
							
							key_map = list(ChainMap(self.print_cat_dict, self.list_of_dicts[1], self.list_of_dicts[0]))
							for row in csv_file:						
								for first_val in self.list_of_dicts[0][key_map[0]]:
									for second_val in self.list_of_dicts[1][key_map[1]]:
										
										if all([ 
																
																
																
												any([row[key_map[0]].upper() == first_val.upper(),  
												float(row[key_map[0]]) > float(first_val[1:]) if '>' in first_val else None,
												float(row[key_map[0]]) < float(first_val[1:]) if '<' in first_val else None     

												]),
												
												any([ row[key_map[1]].upper() == second_val.upper(),
												
												float(row[key_map[1]]) > float(second_val[1:]) if '>' in second_val else None,
												
												float(row[key_map[1]]) > float(second_val[1:]) if '>' in second_val else None
												
												
												])
																
												
														]):
												
											data.append(row)						

							for row in data:
								if len(self.print_cat_dict[key_map[2]]) > 4:
									self.data.append('Max 4 Categories')
								
								if len(self.print_cat_dict[key_map[2]]) == 4:
									self.data.append(
													(f'{self.print_cat_dict[key_map[2]][0]}: {row[self.print_cat_dict[key_map[2]][0]]} {self.print_cat_dict[key_map[2]][1]}: {row[self.print_cat_dict[key_map[2]][1]]} {self.print_cat_dict[key_map[2]][2]}: {row[self.print_cat_dict[key_map[2]][2]]} {self.print_cat_dict[key_map[2]][3]}: {row[self.print_cat_dict[key_map[2]][3]]}'))
							
								elif len(self.print_cat_dict[key_map[2]]) == 3:
									self.data.append((f'{self.print_cat_dict[key_map[2]][0]}: {row[self.print_cat_dict[key_map[2]][0]]} {self.print_cat_dict[key_map[2]][1]}: {row[self.print_cat_dict[key_map[2]][1]]} {self.print_cat_dict[key_map[2]][2]}: {row[self.print_cat_dict[key_map[2]][2]]}'))						
							
								elif len(self.print_cat_dict[key_map[2]]) == 2:
									self.data.append((f'{self.print_cat_dict[key_map[2]][0]}: {row[self.print_cat_dict[key_map[2]][0]]} {self.print_cat_dict[key_map[2]][1]}: {row[self.print_cat_dict[key_map[2]][1]]}'))
													
								else:
									self.data.append(f'{self.print_cat_dict[key_map[2]][0]}: {row[self.print_cat_dict[key_map[2]][0]]}')
						
						data.clear()
						return self.data		

					elif len(self.rangedict) + len(self.list_of_dicts) == 1:
						if self.rangedict:
							
							key_map = list(ChainMap(self.print_cat_dict, self.rangedict[0]))														
							
							self.range1 = arr.arange( float(self.rangedict[0][key_map[0]][0]),
							float(self.rangedict[0][key_map[0]][1]) + 1, 0.1 ).astype('f')

							filter1 = filter(lambda row: float(row[key_map[0]]) in self.range1, csv_file)
							
							for row in filter1:
								if len(self.print_cat_dict[key_map[1]]) > 4:
									self.data.append('Max 4 Categories')
								
								if len(self.print_cat_dict[key_map[1]]) == 4:
									self.data.append(
													(f'{self.print_cat_dict[key_map[1]][0]}: {row[self.print_cat_dict[key_map[1]][0]]} {self.print_cat_dict[key_map[1]][1]}: {row[self.print_cat_dict[key_map[1]][1]]} {self.print_cat_dict[key_map[1]][2]}: {row[self.print_cat_dict[key_map[1]][2]]} {self.print_cat_dict[key_map[1]][3]}: {row[self.print_cat_dict[key_map[1]][3]]}'))
							
								elif len(self.print_cat_dict[key_map[1]]) == 3:
									self.data.append((f'{self.print_cat_dict[key_map[1]][0]}: {row[self.print_cat_dict[key_map[1]][0]]} {self.print_cat_dict[key_map[1]][1]}: {row[self.print_cat_dict[key_map[1]][1]]} {self.print_cat_dict[key_map[1]][2]}: {row[self.print_cat_dict[key_map[1]][2]]}'))						
							
								elif len(self.print_cat_dict[key_map[1]]) == 2:
									self.data.append((f'{self.print_cat_dict[key_map[1]][0]}: {row[self.print_cat_dict[key_map[1]][0]]} {self.print_cat_dict[key_map[1]][1]}: {row[self.print_cat_dict[key_map[1]][1]]}'))
													
								else:
									self.data.append(f'{self.print_cat_dict[key_map[1]][0]}: {row[self.print_cat_dict[key_map[1]][0]]}')							
							
							return self.data 
							
						elif self.list_of_dicts:
															
							data = list()
							
							key_map = list(ChainMap(self.print_cat_dict, self.list_of_dicts[0]))

							for row in csv_file:
								for first_val in self.list_of_dicts[0][key_map[0]]:
								
								
									if any( [row[key_map[0]].upper() == first_val.upper(),
									float(row[key_map[0]]) > float(first_val[1:]) if '>' in first_val else None,
									float(row[key_map[0]]) < float(first_val[1:]) if '<' in first_val else None ]):
										data.append(row)
							
							for row in data:
								if len(self.print_cat_dict[key_map[1]]) > 4:
									self.data.append('Max 4 Categories')
								
								if len(self.print_cat_dict[key_map[1]]) == 4:
									self.data.append((f'{self.print_cat_dict[key_map[1]][0]}: {row[self.print_cat_dict[key_map[1]][0]]} {self.print_cat_dict[key_map[1]][1]}: {row[self.print_cat_dict[key_map[1]][1]]} {self.print_cat_dict[key_map[1]][2]}: {row[self.print_cat_dict[key_map[1]][2]]} {self.print_cat_dict[key_map[1]][3]}: {row[self.print_cat_dict[key_map[1]][3]]}'))
							
								elif len(self.print_cat_dict[key_map[1]]) == 3:
									self.data.append((f'{self.print_cat_dict[key_map[1]][0]}: {row[self.print_cat_dict[key_map[1]][0]]} {self.print_cat_dict[key_map[1]][1]}: {row[self.print_cat_dict[key_map[1]][1]]} {self.print_cat_dict[key_map[1]][2]}: {row[self.print_cat_dict[key_map[1]][2]]}'))						
							
								elif len(self.print_cat_dict[key_map[1]]) == 2:
									self.data.append((f'{self.print_cat_dict[key_map[1]][0]}: {row[self.print_cat_dict[key_map[1]][0]]} {self.print_cat_dict[key_map[1]][1]}: {row[self.print_cat_dict[key_map[1]][1]]}'))
													
								else:
									self.data.append(f'{self.print_cat_dict[key_map[1]][0]}: {row[self.print_cat_dict[key_map[1]][0]]}')
							
							data.clear()
							return self.data
						
					elif all([not self.rangedict, not self.list_of_dicts, self.print_cat_dict]):
						
						
						key_map = list(ChainMap(self.print_cat_dict))
													
						for row in csv_file:
							if len(self.print_cat_dict[key_map[0]]) > 4:
								self.data.append('Max 4 Categories')
							
							if len(self.print_cat_dict[key_map[0]]) == 4:
								self.data.append(
												(f'{self.print_cat_dict[key_map[0]][0]}: {row[self.print_cat_dict[key_map[0]][0]]} {self.print_cat_dict[key_map[0]][1]}: {row[self.print_cat_dict[key_map[0]][1]]} {self.print_cat_dict[key_map[0]][2]}: {row[self.print_cat_dict[key_map[0]][2]]} {self.print_cat_dict[key_map[0]][3]}: {row[self.print_cat_dict[key_map[0]][3]]}'))
						
							elif len(self.print_cat_dict[key_map[0]]) == 3:
								self.data.append((f'{self.print_cat_dict[key_map[0]][0]}: {row[self.print_cat_dict[key_map[0]][0]]} {self.print_cat_dict[key_map[0]][1]}: {row[self.print_cat_dict[key_map[0]][1]]} {self.print_cat_dict[key_map[0]][2]}: {row[self.print_cat_dict[key_map[0]][2]]}'))						
						
							elif len(self.print_cat_dict[key_map[0]]) == 2:
								self.data.append((f'{self.print_cat_dict[key_map[0]][0]}: {row[self.print_cat_dict[key_map[0]][0]]} {self.print_cat_dict[key_map[0]][1]}: {row[self.print_cat_dict[key_map[0]][1]]}'))
												
							else:
								self.data.append(f'{self.print_cat_dict[key_map[0]][0]}: {row[self.print_cat_dict[key_map[0]][0]]}')
							
						
						return self.data
						
						
							
							
