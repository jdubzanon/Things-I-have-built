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


#from IncomeStatement.InterestExpense import InterestExpense
#from IncomeStatement.OperatingIncome import OpIncome

def GetRatio(IntExp_class,OpInc_class,company_facts):
	FAILED_TO_GET_DATA = {'from ratio func intexp2opic':'cant make calculations'}
	
	if any([isinstance(IntExp_class.IntExp_arr,dict),
			isinstance(OpInc_class.OpIncome_arr,dict),
			IntExp_class.forked == True,
			OpInc_class.forked == True  ]):
		from IncomeStatement.InterestExpense import InterestExpense
		from IncomeStatement.OperatingIncome import OpIncome
	
		Interest_Exp = InterestExpense(IntExp_class.ticker)
		IntExp_values = Interest_Exp.get_InterestExpense_values(company_facts,start_fork=True)
		
		Operating_Inc = OpIncome(OpInc_class.ticker)
		OpInc_values = Operating_Inc.get_OpIncome_values(OpInc_class.ticker,start_fork=True)
		
		if any([isinstance(IntExp_values,dict),isinstance(OpInc_values,dict)  ]):
			return FAILED_TO_GET_DATA
		
		try:
			return list(map(lambda IntExp,Opinc: round((IntExp / Opinc)*100,ndigits=2), IntExp_values,OpInc_values  ))
		except ZeroDivisionError:
			OpInc_values = filter(lambda values: values != 0, OpInc_values) 
			
			if not OpInc_values:
				return FAILED_TO_GET_DATA
			
			return list(map(lambda IntExp,Opinc: round((IntExp / Opinc)*100,ndigits=2), IntExp_values,OpInc_values  ))

	
	longest_list_length = max([len(IntExp_class.IntExp_arr),len(OpInc_class.OpIncome_arr)  ])	
	
	if len(OpInc_class.OpIncome_arr) >= len(IntExp_class.IntExp_arr):
		master_df = OpInc_class.OpIncome_df
		slave_df = IntExp_class.IntExp_df
	else:
		master_df = IntExp_class.IntExp_df
		slave_df = IntExp_class.IntExp_df
	
	OpInc = namedtuple('OpInc','values')
	IntExp = namedtuple('IntExp','values')
	
	OpInc.values = OpInc_class.OpIncome_arr
	IntExp.values = IntExp_class.IntExp_arr
	
	
	returned_list = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,isolate=True,returning_lists=True)
	
	#stop and check
	if any([not returned_list[0], not returned_list[1] ]):
		from IncomeStatement.InterestExpense import InterestExpense
		from IncomeStatement.OperatingIncome import OpIncome
	
		Interest_Exp = InterestExpense(IntExp_class.ticker)
		IntExp_values = Interest_Exp.get_InterestExpense_values(company_facts,start_fork=True)
		
		Operating_Inc = OpIncome(OpInc_class.ticker)
		OpInc_values = Operating_Inc.get_OpIncome_values(OpInc_class.ticker,start_fork=True)
		
		if any([isinstance(IntExp_values,dict),isinstance(OpInc_values,dict)  ]):
			return FAILED_TO_GET_DATA
		
		try:
			return list(map(lambda IntExp,Opinc: round((IntExp / Opinc)*100,ndigits=2) , IntExp_values,OpInc_values  ))
		except ZeroDivisionError:
			OpInc_values = filter(lambda values: values != 0, OpInc_values) 
			
			if not OpInc_values:
				return FAILED_TO_GET_DATA
			
			return list(map(lambda IntExp,Opinc: round((IntExp / Opinc)*100,ndigits=2), IntExp_values,OpInc_values  ))
	
	#continue after check	
	for lists in returned_list:
		if set(lists).intersection(set(OpInc.values)):
			OpInc.values = lists
		else:
			IntExp.values = lists
			
	if any([OpInc_class.OpIncome_key[0] ==  OpInc_class.possible_OpIncome_keys[0], OpInc_class.OpIncome_key[0] == OpInc_class.possible_OpIncome_keys[1]]):
		#the keys im chekcing here hold values representing income before tax so i have to add in income expense to get a operating income value
		
		OpInc_added_interest = list(map(lambda opInc,intExp: opInc + intExp, OpInc.values,IntExp.values    ))
		
		intexp_to_opinc = list(map(lambda intEx,opInc: round((intEx / opInc) * 100,ndigits=2), IntExp.values,OpInc_added_interest  ))
		
		return np.flip(intexp_to_opinc)
	else:
		IntExp_to_OpInc = list(map(lambda intEx,opInc: round((intEx / opInc) * 100,ndigits=2), IntExp.values,OpInc.values  ))

		return np.flip(IntExp_to_OpInc)











#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#single_file = 'HON.json'
#final_path = dir_path / single_file
#ticker = single_file[0:-5]
#with open(final_path,'r') as fr:
#	local_file = fr.read()
#	local_json = json.loads(local_file)
#	op = OpIncome(ticker)
#	op_v = op.get_OpIncome_values(local_json)
#	rev = Revenue(ticker)
#	rev_v = rev.get_revenue_values(local_json)

#	test = opInc_to_revenue_ratio(op,rev)		
#	print(test)




#########################################


#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
##print(sorted(os.listdir(dir_path)))
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	print(file_name)
#	ticker = file_name[0:-5]
#	with open(file_path,'r') as fr:
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		op = OpIncome(ticker)
#		op_v = op.get_OpIncome_values(local_json)
#		
#		intx = InterestExpense(ticker)
#		intx_v = intx.get_InterestExpense_values(local_json)
#		
#		test = IntExp_to_OpInc_ratio(intx,op,local_json)		
#		print(test)
#		
		
		
		
		
		

