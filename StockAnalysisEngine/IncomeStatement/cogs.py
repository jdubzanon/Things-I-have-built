import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent) )  

import time

import pandas as pd
import json
import numpy as np
import requests
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
import forks.forks as fork




class Cogs:
	def __init__(self,ticker,fork=False):
		self.ticker = ticker
		self.cogs_key = None
		self.unit = None
		self.cogs_df = None
		self.cogs_arr = None
		self.forked = False
		
	def get_cog_values(self,company_facts,start_fork=False):
		KEYS = ['Cost Of Revenue']
		
		if start_fork == True:
			self.forked = True
			self.cogs_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.cogs_arr
		
		possible_cogs_keys = [ 
		'CostOfGoodsSoldExcludingDepreciationDepletionAndAmortization',
		'CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization',
		'CostOfGoodsAndServicesSold',
		'CostOfGoodsSold',
		'CostOfRevenue',
		'CostOfSales'  
		]
		accounting_key = kh.get_accounting_key(company_facts,possible_cogs_keys)
		self.cogs_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_cogs_keys))
			
		if not self.cogs_key:
			possible_cogs_keys = ['CostsAndExpenses', 'NoninterestExpense']
			self.cogs_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_cogs_keys))
		
		if not self.cogs_key: 
			self.forked = True
			self.cogs_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.cogs_arr
					
		if len(self.cogs_key) > 1:
			self.cogs_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.cogs_key)
			
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.cogs_key)
		self.cogs_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.cogs_key[0]]['units'][self.unit[0]]).drop_duplicates(subset='end')
		self.cogs_arr = get_arr.get_arr(self.cogs_df)	
		
		if not self.cogs_arr:
			self.forked = True
			self.cogs_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.cogs_arr		
		
		return self.cogs_arr
		
from pathlib import Path as path
from pathlib import PurePath as ppath
import os
import json
		

#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#single_file = 'V.json'
#final_path = dir_path / single_file
#ticker = single_file[0:-5]
#with open(final_path,'r') as fr:
#	local_file = fr.read()
#	local_json = json.loads(local_file)
#	cogs = Cogs(ticker)
#	cogs_v = cogs.get_cog_values(local_json)

#	print(cogs_v)			


#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	with open(file_path,'r') as fr:
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		ticker = file_name[0:-5]
#		print(ticker)
#		rev = Cogs(ticker)
#		rev_v = rev.get_cog_values(local_json,start_fork=True)
#		print(rev_v)			
			
			
			
			
#			
##			
#headers = {'User-Agent': 'thorntonbill343@gmail.com'}
#url = 'https://www.sec.gov/files/company_tickers.json'
#response = requests.get(url,headers=headers)
#json = response.json()
#df = pd.DataFrame(json).T	
##print(df)	





#		
#	
#########################################
#df.index = df.ticker
#sample = df.loc['BRK-B']
#sample_cik = str(sample.cik_str).zfill(10)
#sample_ticker = sample.ticker
#url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'


#response = requests.get(url,headers=headers)
#cog = Cogs(sample_ticker)
#test = cog.get_cog_values(response.json())

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
#	
#	test = Cogs(sample_ticker).get_cog_values(response.json())	
#	print(test)
#	time.sleep(2)	
##	
			
#location = '/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/ticker_file/ticker.txt'

#with open(location,'r') as ticker:
#	data = ticker.readlines()
#	for lines in data[0:20]:
#		s_lines = lines.split()
#		sample_cik = str(s_lines[1]).zfill(10)
#		url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'


