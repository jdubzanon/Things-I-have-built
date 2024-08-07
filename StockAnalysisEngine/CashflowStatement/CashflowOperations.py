import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent) )  

import pandas as pd
import json
import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
import forks.forks as fork

import requests
import time




from pathlib import Path as path
from pathlib import PurePath as ppath
import os
import json



class cashflow_operations:
	def __init__(self,ticker):
		self.ticker = ticker
		self.cashflow_operations_key = None
		self.cashflow_operations_df = None
		self.cashflow_operations_arr = None
		self.unit = None
		self.forked = False
		
		
	def get_cashflow_operations_values(self,company_facts,start_fork=False):
		
		if start_fork == True:
			self.forked = True
			self.cashflow_operations_arr = fork.fork(ticker_id=self.ticker,statement='cashflow',keys=['Operating Cash Flow'])		
			return self.cashflow_operations_arr
		
		
		possible_cashflow_op_keys = ['CashFlowsFromUsedInOperatingActivities','NetCashProvidedByUsedInOperatingActivities','NetCashProvidedByUsedInOperatingActivitiesContinuingOperations']
		accounting_key = kh.get_accounting_key(company_facts,possible_cashflow_op_keys)
		self.cashflow_operations_key = list(filter(lambda key: key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_cashflow_op_keys  ))

		
		if not self.cashflow_operations_key:
			self.forked = True
			self.cashflow_operations_arr = fork.fork(ticker_id=self.ticker,statement='cashflow',keys=['Operating Cash Flow'])		
			return self.cashflow_operations_arr
		
		if len(self.cashflow_operations_key) > 1:
#			print('activated')
			self.cashflow_operations_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.cashflow_operations_key)		
		
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.cashflow_operations_key)

		self.cashflow_operations_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.cashflow_operations_key[0]]['units'][self.unit[0]]   ).drop_duplicates(subset='end')
#		print(self.cashflow_operations_df[self.cashflow_operations_df.form == "10-K"])		
		try:
			self.cashflow_operations_arr = get_arr.get_arr(self.cashflow_operations_df)
		except AttributeError:
			self.cashflow_operations_arr = get_arr.get_arr_without_start_date(self.cashflow_operations_df)
		
		if not self.cashflow_operations_arr:
			self.forked = True
			self.cashflow_operations_arr = fork.fork(ticker_id=self.ticker,statement='cashflow',keys=['Operating Cash Flow'])		
			return self.cashflow_operations_arr

		return self.cashflow_operations_arr




##dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#single_file = 'DIS.json'
#final_path = dir_path / single_file
#ticker = single_file[0:-5]
#with open(final_path,'r') as fr:
#	local_file = fr.read()
#	local_json = json.loads(local_file)
#	cf = cashflow_operations(ticker)
#	test = cf.get_cashflow_operations_values(local_json)
#	print(test)


#	try:
#		for keys in local_json['facts']['us-gaap'].keys():
#			if 'Tax' in keys:
#				print(keys)

#	except:
#		for keys in local_json['facts']['ifrs-full'].keys():
#			if 'Tax' in keys:
#				print(keys)
		





#########################################

#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	with open(file_path,'r') as fr:
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		ticker = file_name[0:-5]
#		print(ticker)
#		cf = cashflow_operations(ticker)
#		test = cf.get_cashflow_operations_values(local_json)
#		print(test)	
#		
		
		
		
		
		
		
		
		
		
		
