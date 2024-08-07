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


class NonCurrentLiabilities:
	def __init__(self,ticker):
		self.ticker = ticker
		self.NonCurrentLiabilities_key = None
		self.NonCurrentLiabilities_df = None
		self.NonCurrentLiabilities_arr = None
		self.unit = None
		self.forked = False
	
	def get_NonCurrentLiabilities_values(self,company_facts,start_fork=False):
		
		KEYS = ['Total Non Current Liabilities Net Minority Interest']

		if start_fork == True:
			self.forked = True
			self.NonCurrentLiabilities_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.NonCurrentLiabilities_arr			
					
		possible_NonCurrentLiabilities_keys = ['LiabilitiesNoncurrent','NoncurrentLiabilities']
		accounting_key = kh.get_accounting_key(company_facts,possible_NonCurrentLiabilities_keys)
		self.NonCurrentLiabilities_key = list(filter(lambda key : key.strip()  in company_facts['facts'][accounting_key[0]].keys(), possible_NonCurrentLiabilities_keys))	
			
		if not self.NonCurrentLiabilities_key:
			self.forked = True
			self.NonCurrentLiabilities_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.NonCurrentLiabilities_arr			
			
		if len(self.NonCurrentLiabilities_key) > 1:
			self.NonCurrentLiabilities_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.NonCurrentLiabilities_key)
			
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.NonCurrentLiabilities_key)
		
		self.NonCurrentLiabilities_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.NonCurrentLiabilities_key[0]]['units'][self.unit[0]]  )
		
		self.NonCurrentLiabilities_arr = get_arr.get_arr_without_start_date(self.NonCurrentLiabilities_df)
		
		if any([not self.NonCurrentLiabilities_arr,isinstance(self.NonCurrentLiabilities_arr,dict) ]):
			print('forked bottom')
			self.forked = True
			self.NonCurrentLiabilities_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.NonCurrentLiabilities_arr			

		return self.NonCurrentLiabilities_arr
		


		
from pathlib import Path as path
from pathlib import PurePath as ppath
import os
import json
		

#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#single_file = 'GOOGL.json'
#final_path = dir_path / single_file
#ticker = single_file[0:-5]
#with open(final_path,'r') as fr:
#	local_file = fr.read()
#	local_json = json.loads(local_file)
#	for key in local_json['facts']['us-gaap'].keys():
#		if 'Liabilities' in key:
#			print(key)

#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	with open(file_path,'r') as fr:
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		ticker = file_name[0:-5]
#		print(ticker)
#		rev = NonCurrentLiabilities(ticker)
#		rev_v = rev.get_NonCurrentLiabilities_values(local_json,start_fork=True)
#		print(rev_v)		
		
		
		
		
		
		
		
#headers = {'User-Agent': 'thorntonbill343@gmail.com'}
#url = 'https://www.sec.gov/files/company_tickers.json'
#response = requests.get(url,headers)
#json = response.json()
#df = pd.DataFrame(json).T

#df.index = df.ticker
#sample = df.loc['AMZN']
#sample_cik = str(sample.cik_str).zfill(10)
#sample_ticker = sample.ticker
#url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'

#response = requests.get(url,headers=headers)
#nc = NonCurrentLiabilities(sample_ticker)
#test = nc.get_NonCurrentLiabilities_values(response.json())
#print(nc.NonCurrentLiabilities_df)
#print(test)


#		


#for num in range(0,20):
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
#	tl = TotalLiabilites(sample_ticker)
#	test = tl.get_TotalLiabilites_values(response.json())
#	print(test)		
		
		
			
