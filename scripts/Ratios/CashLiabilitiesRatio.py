import sys
##for gedit 
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/webpage/bin')
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/scripts')
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/webpage/lib/python3.10/site-packages')
sys.path.append('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts')
sys.path.append('/home/jdubzanon/hdd/envornments/webpage/lib/python3.10/site-packages')

import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
from collections import namedtuple



#from pathlib import Path as path
#from pathlib import PurePath as ppath
#import os
#import json
#import requests
#import time

def GetRatio(cash_class,liabilites_class,company_facts): #pass cash and current liabilties
	FAILED_TO_GET_DATA = {'from cash to liabilites':'cant make calculation'}
	
	if any([isinstance(cash_class.cash_arr,dict),
			isinstance(liabilites_class.CurrentLiabilities_arr,dict),
			cash_class.forked == True,
			liabilites_class.forked == True  ]):

		
		from BalanceSheet.cash import cash
		from BalanceSheet.CurrentLiabilities import CurrentLiabilities
		
		cl = CurrentLiabilities(cash_class.ticker)
		cl_vals = cl.get_CurrentLiabilities_values(company_facts,start_fork=True) 		
		
		cash_ = cash(liabilites_class.ticker)
		cash_vals = cash_.get_cash_values(company_facts,start_fork=True)
		
		if any([isinstance(cl_vals,dict),isinstance(cash_vals,dict) ]):
			return FAILED_TO_GET_DATA

		try:
			return list(map(lambda cash,current_liabilties: round((cash/current_liabilties),ndigits=2),cash_vals,cl_vals    ))				
		
		except ZeroDivisionError:
			cash_vals = list(filter(lambda values: values != 0, cash_vals))
			cl_vals = list(filter(lambda values: values != 0, cl_vals))
			
			if any([not cash_vals,not cl_vals]):
				return FAILED_TO_GET_DATA

			return list(map(lambda cash,current_liabilties: round((cash/current_liabilties),ndigits=2),cash_vals,cl_vals    ))				
			
			
			
	#continue here if niether were forked
	longest_list_length = max([len(cash_class.cash_arr), len(liabilites_class.CurrentLiabilities_arr)   ])
	
	if len(cash_class.cash_arr) >= longest_list_length:
		master_df = cash_class.cash_df
		slave_df = liabilites_class.CurrentLiabilities_df
	else:
		master_df = liabilites_class.CurrentLiabilities_df
		slave_df = cash_class.cash_df
		
	cash = namedtuple('cash','values')
	current = namedtuple('current','values')
	
	cash.values = cash_class.cash_arr
	current.values = liabilites_class.CurrentLiabilities_arr
	
	returned_lists = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,isolate=True,returning_lists=True)
	# stop and check here
	if any([not returned_lists[0],not returned_lists[1]]): #if no dates line up in the above function then fork it and work with those values

		from BalanceSheet.cash import cash
		from BalanceSheet.CurrentLiabilities import CurrentLiabilities
		
		cl = CurrentLiabilities(cash_class.ticker)
		cl_vals = cl.get_CurrentLiabilities_values(company_facts,start_fork=True) 		
		
		cash_ = cash(liabilites_class.ticker)
		cash_vals = cash_.get_cash_values(company_facts,start_fork=True)
		
		if any([isinstance(cl_vals,dict),isinstance(cash_vals,dict) ]):
			return FAILED_TO_GET_DATA

		try:
			return list(map(lambda cash,current_liabilties: round((cash/current_liabilties),ndigits=2),cash_vals,cl_vals    ))				

		except ZeroDivisionError:
			cash_vals = list(filter(lambda values: values != 0, cash_vals))
			cl_vals = list(filter(lambda values: values != 0, cl_vals))
			
			if any([not cash_vals,not cl_vals]):
				return FAILED_TO_GET_DATA

			return list(map(lambda cash,current_liabilties: round((cash/current_liabilties),ndigits=2),cash_vals,cl_vals    ))		

	#continue here
	for lists in returned_lists:
		if set(lists).intersection(set(cash.values)):
			cash.values = lists
		else:
			current.values = lists
			
	cash_to_current = list(map(lambda cash,current_vals: round(cash / current_vals,ndigits=2), cash.values,current.values))

	return np.flip(cash_to_current)




#from pathlib import Path as path
#from pathlib import PurePath as ppath
#import os
#import json
#		

#from BalanceSheet.cash import cash
#from BalanceSheet.CurrentLiabilities import CurrentLiabilities



#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#single_file = 'GE.json'
#final_path = dir_path / single_file
#ticker = single_file[0:-5]
#with open(final_path,'r') as fr:
#	local_file = fr.read()
#	local_json = json.loads(local_file)
#	c_lia = CurrentLiabilities(ticker)
#	c_lia_v = c_lia.get_CurrentLiabilities_values(local_json)
#	
#	cash_ = cash(ticker)
#	cash_v = cash_.get_cash_values(local_json)
#	
#	test = cash_to_current_liabilities(cash_,c_lia,local_json)
#	
#	print(test)


#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	with open(file_path,'r') as fr:
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		ticker = file_name[0:-5]
#		print(ticker)
#		c_lia = CurrentLiabilities(ticker)
#		c_lia_v = c_lia.get_CurrentLiabilities_values(local_json)
#		
#		cash_ = cash(ticker)
#		cash_v = cash_.get_cash_values(local_json)
#		
#		test = cash_to_current_liabilities(cash_,c_lia,local_json)
#		
#		print(test)
##		
#		
		
		
		
		
		
		
			
