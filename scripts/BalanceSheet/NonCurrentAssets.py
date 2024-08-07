import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent) )  

import pandas as pd
import json
import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
import yfinance as yf

import requests
import time


class NonCurrentAssets:
	def __init__(self,ticker):
		self.ticker = ticker
		self.NonCurrentAssets_key = None
		self.NonCurrentAssets_df = None
		self.NonCurrentAssets_arr = None
		self.unit = None
		self.forked = False
		
	def get_NonCurrentAsset_values(self,company_facts,start_fork=True):
	
		if start_fork == True:
			self.forked = True
			ticker = yf.Ticker(self.ticker)			
			balance_sheet = ticker.balance_sheet
			try:
				nca = balance_sheet.loc['Total Non Current Assets']
				self.NonCurrentAssets_arr = list(map(lambda values: int(values), nca[pd.notna(nca)].values ))     
				if not self.NonCurrentAssets_arr:
					self.NonCurrentAssets_arr = {'from non current assets':"cant make calculation"}
			except:
				self.NonCurrentAssets_arr = {'from non current assets':'cant make calculation'}	
				
			return self.NonCurrentAssets_arr							

		possible_NCA_keys = ['NoncurrentAssets','AssetsNoncurrent']
		accounting_key = kh.get_accounting_key(company_facts,possible_NCA_keys)
		self.NonCurrentAssets_key = list(filter(lambda key: key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_NCA_keys  ))
		
		if not self.NonCurrentAssets_key:
			self.forked = True
			ticker = yf.Ticker(self.ticker)			
			balance_sheet = ticker.balance_sheet
			try:
				nca = balance_sheet.loc['Total Non Current Assets']
				self.NonCurrentAssets_arr = list(map(lambda values: int(values), nca[pd.notna(nca)].values ))     
				if not self.NonCurrentAssets_arr:
					self.NonCurrentAssets_arr = {'from non current':'cant make calculation'}
			except:
				self.NonCurrentAssets_arr = {'from non current assets':'cant make calculation'}	
				
			return self.NonCurrentAssets_arr				
						
		if len(self.NonCurrentAssets_key) > 1:
			self.NonCurrentAssets_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.NonCurrentAssets_key)
		
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.NonCurrentAssets_key)

		self.NonCurrentAssets_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.NonCurrentAssets_key[0]]['units'][self.unit[0]] ).drop_duplicates(subset='end')	
		
		try:
			self.NonCurrentAssets_arr = get_arr.get_arr(self.NonCurrentAssets_df)	
		
		except AttributeError:
			self.NonCurrentAssets_arr = get_arr.get_arr_without_start_date(self.NonCurrentAssets_df)
			

		return self.NonCurrentAssets_arr

#from pathlib import Path as path
#from pathlib import PurePath as ppath
#import os
#import json
		

####dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
####single_file = 'NEE.json'
####final_path = dir_path / single_file
####ticker = single_file[0:-5]
####with open(final_path,'r') as fr:
####	local_file = fr.read()
####	local_json = json.loads(local_file)
####	rev = InterestExpense(local_json)
####	rev_v = rev.get_InterestExpense_values(local_json)
####	print(rev_v)			


#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	with open(file_path,'r') as fr:
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		ticker = file_name[0:-5]
#		print(ticker)
#		rev = NonCurrentAssets(ticker)
#		rev_v = rev.get_NonCurrentAsset_values(local_json,start_fork=True)
#		print(rev_v)			









#headers = {'User-Agent': 'thorntonbill343@gmail.com'}
#url = 'https://www.sec.gov/files/company_tickers.json'
#response = requests.get(url,headers=headers)
#json = response.json()
#df = pd.DataFrame(json).T	



###########################################
#df.index = df.ticker
#sample = df.loc['AAPL']
#sample_cik = str(sample.cik_str).zfill(10)
#sample_ticker = sample.ticker
#url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'


#response = requests.get(url,headers=headers)

#nca = NonCurrentAssets(sample_ticker)
#test = nca.get_NonCurrentAsset_values(response.json())
#print(test)

#try:
#	for key in response.json()['facts']['us-gaap'].keys():
#		if 'Asset' in key:
#			print(key)
#except KeyError:
#	for key in response.json()['facts']['ifrs-full'].keys():
#		if 'Asset' in key:
#			print(key)

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
#	nca = NonCurrentAssets(sample_ticker)
#	test = nca.get_NonCurrentAsset_values(response.json())

#	print(test)

