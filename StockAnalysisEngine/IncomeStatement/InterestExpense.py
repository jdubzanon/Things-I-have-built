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



#have to get interest expense and operating income

class InterestExpense:
	def __init__(self,ticker):
		self.ticker = ticker
		self.IntExpKey = None
		self.IntExp_df = None
		self.IntExp_arr = None
		self.unit = None
		self.forked = False
		
		
		
	def get_InterestExpense_values(self,company_facts,start_fork=False):
		
		KEYS = ['Interest Expense','Net Non Operating Interest Income Expense']
		
		if start_fork == True:
			self.forked = True
			self.IntExp_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.IntExp_arr
			
		possible_IntExpKeys = [
		'InterestExpense', 
		'FinanceCosts',
		'InterestExpenseDebt', 
		'InterestAndDebtExpense',
		'InterestPaidNet',
		'FinanceIncomeCost'
		]

		accounting_key = kh.get_accounting_key(company_facts,possible_IntExpKeys)
		self.IntExpKey =  list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_IntExpKeys))

		if not self.IntExpKey:
			self.forked = True
			self.IntExp_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=['Interest Expense','Net Non Operating Interest Income Expense'])
			return self.IntExp_arr

		if len(self.IntExpKey) > 1:
			self.IntExpKey = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.IntExpKey)
				
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.IntExpKey)
		self.IntExp_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.IntExpKey[0]]['units'][self.unit[0]]).drop_duplicates(subset='end')			

		try:
			self.IntExp_arr = get_arr.get_arr(self.IntExp_df)
		
		except:
			self.IntExp_arr = get_arr.get_arr_without_start_date(self.IntExp_df)

		if not self.IntExp_arr:
			self.forked = True
			self.IntExp_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.IntExp_arr
				
		return self.IntExp_arr
		
			
from pathlib import Path as path
from pathlib import PurePath as ppath
import os
import json
#		

#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#single_file = 'CRM.json'
#final_path = dir_path / single_file
#ticker = single_file[0:-5]
#with open(final_path,'r') as fr:
#	local_file = fr.read()
#	local_json = json.loads(local_file)
#	rev = InterestExpense(ticker)
#	rev_v = rev.get_InterestExpense_values(local_json,start_fork=True)
#	print(rev_v)			


#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	with open(file_path,'r') as fr:
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		ticker = file_name[0:-5]
#		print(ticker)
#		rev = InterestExpense(ticker)
#		rev_v = rev.get_InterestExpense_values(local_json,start_fork=True)
#		print(rev_v)			
#			
			
			
#headers = {'User-Agent': 'thorntonbill343@gmail.com'}
#url = 'https://www.sec.gov/files/company_tickers.json'
#response = requests.get(url,headers)
#json = response.json()
#df = pd.DataFrame(json).T	
####print(df)	



##########################################
#df.index = df.ticker
#sample = df.loc['XOM']
#sample_cik = str(sample.cik_str).zfill(10)
#sample_ticker = sample.ticker
#url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'

######print(url)

#response = requests.get(url,headers=headers)

#IntExp = InterestExpense('XOM')
#test = IntExp.get_InterestExpense_values(response.json())
#print(test)


###for key in response.json()['facts']['us-gaap']:
##	print(key)
##	print('')
##	time.sleep(1.25)



##	
#for num in range(150,201):
#	
#	sample = df.iloc[num]
#	sample_cik = str(sample.cik_str).zfill(10)
#	sample_ticker = sample.ticker
#	url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'
#	print(sample_ticker,' ',num)
#	response = requests.get(url,headers=headers)

#	try:
#		data = response.json()
#	except:
#		continue
#	
#	IntExp = InterestExpense('AAPL')
#	test = IntExp.get_InterestExpense_values(response.json())
#	
#	print(test)
#	time.sleep(.25)	
##	
#			
		
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			









		

