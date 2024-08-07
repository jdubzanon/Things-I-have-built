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



class OpIncome:
	def __init__(self,ticker):
		self.ticker = ticker
		self.OpIncome_key = None
		self.OpIncome_df = None
		self.OpIncome_arr = None
		self.unit = None
		self.forked = False
		self.possible_OpIncome_keys = None #special case attribute so i use indexing to check key in intexp_to_opinc ratio function
		
	def get_OpIncome_values(self,company_facts,start_fork=False):
		
		KEYS = ['Operating Income','Operating Revenue']
		
		if start_fork == True:
			self.forked = True
			self.OpIncome_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.OpIncome_arr
		
		
		self.possible_OpIncome_keys = [
		'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest',
		'ProfitLossFromOperatingActivites',
		'RevenueAndOperatingIncome',
		'OperatingIncomeLoss',
		'ProfitLossFromOperatingActivities'
		]
		
		accounting_key = kh.get_accounting_key(company_facts,self.possible_OpIncome_keys)
		self.OpIncome_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(),self. possible_OpIncome_keys))
			
		if not self.OpIncome_key:
			self.forked = True
			self.OpIncome_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.OpIncome_arr
						
		if len(self.OpIncome_key) > 1:
			self.OpIncome_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.OpIncome_key)
		
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.OpIncome_key)
		self.OpIncome_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.OpIncome_key[0]]['units'][self.unit[0]]).drop_duplicates(subset='end')
		self.OpIncome_arr = get_arr.get_arr(self.OpIncome_df)
			
		if not self.OpIncome_arr:
			self.forked = True
			self.OpIncome_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.OpIncome_arr

		return self.OpIncome_arr	
		
		

#from pathlib import Path as path
#from pathlib import PurePath as ppath
#import os
#import json



#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#single_file = 'TM.json'
#final_path = dir_path / single_file
#ticker = single_file[0:-5]
#with open(final_path,'r') as fr:
#	local_file = fr.read()
#	local_json = json.loads(local_file)
#	op = OpIncome(ticker)
#	test = op.get_OpIncome_values(local_json)		
#	print(test)


#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	with open(file_path,'r') as fr:
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		ticker = file_name[0:-5]
#		print(ticker)
#		rev = OpIncome(ticker)
#		rev_v = rev.get_OpIncome_values(local_json,start_fork=True)
#		print(rev_v)







##		
#headers = {'User-Agent': 'thorntonbill343@gmail.com'}
#url = 'https://www.sec.gov/files/company_tickers.json'
#response = requests.get(url,headers)
#json = response.json()
#df = pd.DataFrame(json).T	
###print(df)	



#########################################
#df.index = df.ticker
#sample = df.loc['TM']
#sample_cik = str(sample.cik_str).zfill(10)
#sample_ticker = sample.ticker
#url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'

##print(url)

#response = requests.get(url,headers=headers)

#OpInc = OpIncome(sample_ticker)
#test = OpInc.get_OpIncome_values(response.json())


#print(test)





#	
#for num in range(0,20):
#	
#	sample = df.iloc[num]
#	sample_cik = str(sample.cik_str).zfill(10)
#	sample_ticker = sample.ticker
#	url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'
#	print(sample_ticker)
#	response = requests.get(url,headers=headers)

#	try:
#		data = response.json()
#	except:
#		continue
#	OpInc = OpIncome(sample_ticker)
#	test = OpInc.get_OpIncome_values(response.json())
#	print(test)
#	time.sleep(1)	
###	
#			
		
		
		
		
		
		
		
		
		
		
		
		
		
		
