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



#if dividend is forked i need to add to net profit because it returns a negative as in being subtracted from cashflow /if its not forked then subtract from net_income because its the number payed

def GetRatio(lsbe_class,dividend_class,net_profit_class,company_facts):
	FAILED_TO_GET_DATA = {'from return_on_capital':'cant make calculations'}
	
	
	if any([isinstance(lsbe_class.LiabilitiesAndStockholdersEquity_arr,dict),
			isinstance(net_profit_class.NetProfit_arr,dict),
			isinstance(dividend_class.dividends_arr,dict),
			lsbe_class.forked == True,
			net_profit_class.forked == True,
			dividend_class.forked == True]):
		
			
			from BalanceSheet.LiabilitiesAndStockholdersEquity import LiabilitiesAndStockholdersEquity
			from IncomeStatement.NetProfit import NetProfit
			from CashflowStatement.Dividends import Dividends
			
			
			lsbe = LiabilitiesAndStockholdersEquity(lsbe_class.ticker)
			lsbe_values = lsbe.get_LiabilitiesAndStockholdersEquity_values(company_facts,start_fork=True)
			
			net_income = NetProfit(net_profit_class.ticker)
			np_values = net_income.get_NetProfit_values(company_facts,start_fork=True)
			
			dividend = Dividends(dividend_class.ticker)
			dividend_values = dividend.get_dividend_values(company_facts,start_fork=True)
			
			if any([isinstance(lsbe_values,dict),isinstance(np_values,dict)]):
				return FAILED_TO_GET_DATA
			
			first_equation = map(lambda np,div: np + div, np_values,dividend_values)
			
			return_on_capital_vals = map(lambda first_eq,lsbe_vals: round(first_eq / lsbe_vals,ndigits=2), first_equation,filter(lambda values: values != 0, lsbe_values) )
			
			return list(return_on_capital_vals)			
					
	
	longest_lists_length = max([len(lsbe_class.LiabilitiesAndStockholdersEquity_arr), len(dividend_class.dividends_arr), len(net_profit_class.NetProfit_arr)    ])
	
	if len(lsbe_class.LiabilitiesAndStockholdersEquity_arr) >= longest_lists_length:	
		master_df = lsbe_class.LiabilitiesAndStockholdersEquity_df
		slave_df = dividend_class.dividends_df
		slave2_df = net_profit_class.NetProft_df
	
	elif len(net_profit_class.NetProfit_arr) >= longest_lists_length:
		master_df = net_profit_class.NetProft_df
		slave_df = dividend_class.dividends_df
		slave2_df = lsbe_class.LiabilitiesAndStockholdersEquity_df
	
	else:
		master_df = dividend_class.dividends_df
		slave_df = net_profit_class.NetProft_df
		slave2_df = lsbe_class.LiabilitiesAndStockholdersEquity_df
		
	net_income = namedtuple('net_income','values')
	lsbe = namedtuple('lsbe','values')
	dividend = namedtuple('dividend','values')
	
	net_income.values = net_profit_class.NetProfit_arr
	lsbe.values = lsbe_class.LiabilitiesAndStockholdersEquity_arr
	dividend.values = dividend_class.dividends_arr
	
	returned_lists = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,df_slave2=slave2_df,isolate=True,returning_lists=True)
	
	#stop and check
	if any([not returned_lists[0],not returned_lists[1],not returned_lists[2]]):
		from BalanceSheet.LiabilitiesAndStockholdersEquity import LiabilitiesAndStockholdersEquity
		from IncomeStatement.NetProfit import NetProfit
		from CashflowStatement.Dividends import Dividends
		
		
		lsbe = LiabilitiesAndStockholdersEquity(lsbe_class.ticker)
		lsbe_values = lsbe.get_LiabilitiesAndStockholdersEquity_values(company_facts,start_fork=True)
		
		net_income = NetProfit(net_profit_class.ticker)
		np_values = net_income.get_NetProfit_values(company_facts,start_fork=True)
		
		dividend = Dividends(dividend_class.ticker)
		dividend_values = dividend.get_dividend_values(company_facts,start_fork=True)
		
		if any([isinstance(lsbe_values,dict),isinstance(np_values,dict),isinstance(dividend_values,dict)]):
			return FAILED_TO_GET_DATA
		
		first_equation = map(lambda np,div: np + div, np_values,dividend_values)
		
		return_on_capital_vals = map(lambda first_eq,lsbe_vals: round(first_eq / lsbe_vals,ndigits=2), first_equation,filter(lambda values: values != 0, lsbe_values) )
		
		return list(return_on_capital_vals)			
	
	#continue after check
	for lists in returned_lists:
		if set(lists).intersection(set(net_income.values)):
			net_income.values = np.flip(lists)
		
		elif set(lists).intersection(set(lsbe.values)):
			lsbe.values = np.flip(lists)
		
		else:
			dividend.values = np.flip(lists)
			
	first_calculation = list(map(lambda net_income,dividends: net_income-dividends, net_income.values,dividend.values   ))
	
	return_on_capital_values = list(map(lambda first_calc,lia_and_stk_hld_eq:round(first_calc / lia_and_stk_hld_eq,ndigits=3) , first_calculation,lsbe.values ))
	
	return return_on_capital_values
		
		



#from pathlib import Path as path
#from pathlib import PurePath as ppath
#import os
#import json
#		

#from CashflowStatement.Dividends import Dividends
#from IncomeStatement.NetProfit import NetProfit
#from BalanceSheet.LiabilitiesAndStockholdersEquity import LiabilitiesAndStockholdersEquity

#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#single_file = 'AMD.json'
#final_path = dir_path / single_file
#ticker = single_file[0:-5]
#with open(final_path,'r') as fr:
#	local_file = fr.read()	
#	local_json = json.loads(local_file)
#	ticker = single_file[0:-5]
#	print(ticker)

#	np = NetProfit(ticker)
#	npv = np.get_NetProfit_values(local_json)

#	div = Dividends(ticker)
#	div_v = div.get_dividend_values(local_json)

#	lia = LiabilitiesAndStockholdersEquity(ticker)
#	lia_v = lia.get_LiabilitiesAndStockholdersEquity_values(local_json,start_fork=True)
#	test = return_on_capital(lia,div,np,local_json)
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

#		np = NetProfit(ticker)
#		npv = np.get_NetProfit_values(local_json)

#		div = Dividends(ticker)
#		div_v = div.get_dividend_values(local_json)

#		lia = LiabilitiesAndStockholdersEquity(ticker)
#		lia_v = lia.get_LiabilitiesAndStockholdersEquity_values(local_json)
#		test = return_on_capital(lia,div,np,local_json)
#		
#		print(test)	
#		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
