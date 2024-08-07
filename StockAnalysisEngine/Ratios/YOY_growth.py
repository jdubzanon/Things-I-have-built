import numpy as np

#IF ITS NOT FORKED YOU NEED TO FLIP THE LISTS WHEN CALLING FUCNTIONS


def growth_calculate(list_of_values):
	list_of_values = list(filter(lambda values: values != 0.0, list_of_values ))
	if list_of_values:
		percent_growth = list()
		for index,value in enumerate(list_of_values, start=1):
			if index == len(list_of_values):
				break
			if list_of_values[index] > value:
				diff = list_of_values[index] - value		
				divided = diff / list_of_values[index]
				percent_diff = divided * -100
				percent_growth.append(round(percent_diff,ndigits=4))
			else:
				diff = value - list_of_values[index]
				divided = diff/ value
				percent_diff = divided * 100		
				percent_growth.append(round(percent_diff,ndigits=4))		
		return percent_growth		
	else:
		return {'from YOY': 'cant make calculations'}

