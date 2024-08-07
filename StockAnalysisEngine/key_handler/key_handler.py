import pandas as pd
from operator import itemgetter
import numpy as np
import get_arr.get_arr as get_arr 


def get_accounting_key(company_facts,possible_keys):
	columns = ['start','end','val','form']
	accounting_type = list(company_facts['facts'].keys())
	possible_accounting_keys = [ 'ifrs-full', 'us-gaap']
	accounting_keys = list(filter(lambda accounting_key: accounting_key in possible_accounting_keys, accounting_type))
#	print(accounting_keys)
	if len(accounting_keys) > 1:
		search_dict_key_one = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_keys[0]].keys(), possible_keys))		
		search_dict_key_two = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_keys[1]].keys(), possible_keys))	
				
		if search_dict_key_one:
			accounting_keys = [accounting_keys[0]]
		else:
			accounting_keys = [accounting_keys[1]]
			
	return accounting_keys






#def get_ReportingKey_with_two_accounting_keys(company_facts,accounting_keys,possible_keys):
#	''' this function handles situations when there are two accounting keys reported. Im looking through both sections of json to find my reporting key'''
#	
#	search_dict_key_one = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_keys[0]].keys(), possible_keys))		
#	search_dict_key_two = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_keys[1]].keys(), possible_keys))
#	print(search_dict_key_one)
#	print(search_dict_key_two)
#	
#	if search_dict_key_one:
#		reporting_key = search_dict_key_one
#	else:
#		reporting_key = search_dict_key_two
#	
#	return reporting_key
#	
	






def set_unit_key(company_facts,accounting_key,reporting_key): 
	
	if isinstance(reporting_key,str):
		unit_key = list(company_facts['facts'][accounting_key[0]][reporting_key]['units'].keys())
	else:
		unit_key = list(company_facts['facts'][accounting_key[0]][reporting_key[0]]['units'].keys())
	
	if len(unit_key) > 1:
		tracker = list()
		for unit in unit_key:
			if isinstance(reporting_key,str):
				generic_dataframe = pd.DataFrame(company_facts['facts'][accounting_key[0]][reporting_key]['units'][unit]  )			

			else:
				generic_dataframe = pd.DataFrame(company_facts['facts'][accounting_key[0]][reporting_key[0]]['units'][unit]  )

			if all(['start' in generic_dataframe.columns, 'end' in generic_dataframe.columns   ]):
				try:
					get_arr_info = get_arr.get_arr(generic_dataframe)
					tracker.append((unit,len(get_arr_info)))			
				except:
					continue
			else:
				try:
					get_arr_info = get_arr.get_arr_without_start_date(generic_dataframe)
					tracker.append((unit,len(get_arr_info)))	
				except:
					continue
####			 if there are mulitple keys i want the one with the most information available
#		print(looking_for_best_key)
		looking_for_best_key = sorted(tracker,key=itemgetter(1),reverse=True)
		best_reporting_key = looking_for_best_key[0][0]
		return [best_reporting_key]
	return unit_key





def sort_out_multiple_reporting_keys(company_facts,accounting_key,reporting_key): 
	tracker = list()
	
	for key in reporting_key:
		unit = set_unit_key(company_facts,accounting_key,key)	
		generic_dataframe = pd.DataFrame(company_facts['facts'][accounting_key[0]][key]['units'][unit[0]])			
		
		if all(['start' in generic_dataframe.index, 'end' in generic_dataframe.index  ]):
			try:
				get_arr_info = get_arr.get_arr(generic_dataframe)
				tracker.append((key,len(get_arr_info)))				
			except: 
				continue
		else:
			
			try:
				get_arr_info = get_arr.get_arr_without_start_date(generic_dataframe)		
				tracker.append((key,len(get_arr_info)))		
			except:
				continue
	looking_for_best_key = sorted(tracker,key=itemgetter(1),reverse=True)
	try:	
		best_reporting_key = looking_for_best_key[0][0]
		return [best_reporting_key]
	except IndexError:
		
		return {'mean_all' : 'unable to make calculation',
			'maean_last_five' : 'unable to make calculation'}














				
