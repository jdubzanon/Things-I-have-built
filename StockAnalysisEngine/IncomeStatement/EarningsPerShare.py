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

class EarningsPerShare:
	def __init__(self,ticker):
		self.ticker = ticker
		self.eps_key = None
		self.eps_df = None
		self.eps_arr = None
		self.unit = None
		self.forked = False
	
	def get_eps_values(self,company_facts,start_fork=False):
	
		if start_fork == True:
			self.forked = True
			self.eps_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=['Diluted EPS'],keep_float=True)
			return self.eps_arr
			
		possible_eps_keys = ['BasicEarningsLossPerShare','DilutedEarningsLossPerShare','EarningsPerShareDiluted','EarningsPerShareBasic']
		accounting_key = kh.get_accounting_key(company_facts,possible_eps_keys)
		self.eps_key = list(filter(lambda key: key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_eps_keys  ))
		
		if not self.eps_key:
			self.forked = True
			self.eps_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=['Diluted EPS'],keep_float=True)
			return self.eps_arr
			
		if len(self.eps_key) > 1:
			self.eps_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.eps_key)
			
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.eps_key)
		
		self.eps_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.eps_key[0]]['units'][self.unit[0]] ).drop_duplicates(subset='end')
		
		try:
			self.eps_arr = get_arr.get_arr(self.eps_df)
		except AttributeError:
			self.eps_arr = get_arr.get_arr_without_start_date(self.eps_df)
		
		if not self.eps_arr:
			self.forked = True
			self.eps_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=['Diluted EPS'],keep_float=True)
			
		return self.eps_arr


from pathlib import Path as path
from pathlib import PurePath as ppath
import os
import json
#		

#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#single_file = 'BRK-B.json'
#final_path = dir_path / single_file
#ticker = single_file[0:-5]
#with open(final_path,'r') as fr:
#	local_file = fr.read()
#	local_json = json.loads(local_file)
#	eps = EarningsPerShare(ticker)
#	epsv = eps.get_eps_values(local_json)
#	print(epsv)

#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	with open(file_path,'r') as fr:
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		ticker = file_name[0:-5]
#		print(ticker)
#		eps = EarningsPerShare(ticker)
#		epsv = eps.get_eps_values(local_json)
#		print(epsv)








#headers = {'User-Agent': 'thorntonbill343@gmail.com'}
#url = 'https://www.sec.gov/files/company_tickers.json'
#response = requests.get(url,headers=headers)
#json = response.json()
#df = pd.DataFrame(json).T	



###########################################
#df.index = df.ticker
#sample = df.loc['BRK-B']
#sample_cik = str(sample.cik_str).zfill(10)
#sample_ticker = sample.ticker
#url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'


#response = requests.get(url,headers=headers)
#eps = EarningsPerShare(sample_ticker)
#test = eps.get_eps_values(response.json())
#print(test)

#try:
#	for key in response.json()['facts']['us-gaap'].keys():
#		if 'PerShare' in key:
#			print(key)
#except KeyError:
#	for key in response.json()['facts']['ifrs-full'].keys():
#		if 'PerShare' in key:
#			print(key)
#for key in response.json()['facts']['ifrs-full'].keys():
#		if 'PropertyPlant' in key:
#			print(key)

#	
#for num in range(50,100):
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
#	eps = EarningsPerShare(sample_ticker)
#	test = eps.get_eps_values(response.json())

#	print(test)
#	time.sleep(1)








