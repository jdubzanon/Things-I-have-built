from collections import ChainMap
import numpy as arr



class GraphParser:
	def __init__(self, ent_var, *args):
		self.inp = ent_var.split()
		self.cat_dict = dict()
		self.value_dict = dict()
		self.boundry_dict = dict()
		self.key_map = None
		self.range1 = None
		self.full_mapped_dict = dict()
		
		self.map_set = list()
		
		for i in range(len(self.inp)):
			if i%2 != 0:
				if self.inp[i] == 'category':
					self.cat_dict[self.inp[i].replace('-', ' ')] = [val.replace('-', ' ') for val in self.inp[i+1].split('&')]
				elif not self.value_dict.keys():
					self.value_dict[self.inp[i].replace('-', ' ')] = [val.replace('-', ' ') for val in self.inp[i+1].upper().split('&')]
				elif all([self.value_dict.keys(), not self.boundry_dict.keys()]):
					self.boundry_dict[self.inp[i].replace('-',' ')] = [val.replace('-', ' ') for val in self.inp[i+1].split('&')]
		# check for ranges
		
		for key, value in self.boundry_dict.items():
			for item in value:
				if item[0].isdigit():
					self.boundry_dict[key] = item.split()
					
		self.key_map = list(ChainMap(self.cat_dict, self.boundry_dict, self.value_dict))	
		
		if len(self.boundry_dict[self.key_map[1]]) > 1:
			self.range1 = arr.arange(float(self.boundry_dict[self.key_map[1]][0]), 
			float(self.boundry_dict[self.key_map[1]][1]) + 1, 0.1   ).astype('f')

		# creating nested dictionary
		for val in self.value_dict[self.key_map[0]]:
			self.full_mapped_dict[val] = {cat:list() for cat in self.cat_dict[self.key_map[2]]}
			
		
		#creating the keys for the map
		for high_key, high_value in self.full_mapped_dict.items():
			for low_key in high_value.keys():
				self.map_set.append((f'{high_key}\n{low_key}'))

		
			
									
