import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent) )  

import pandas as pd
import json
import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
import forks.forks as fork




from pathlib import Path as path
from pathlib import PurePath as ppath
import os
import json
import requests
import time


class TotalLiabilities:
	def __init__(self,ticker):
		self.ticker = ticker
		self.TotalLiabilities_key = None
		self.TotalLiabilities_df = None
		self.TotalLiabilities_arr = None
		self.unit = None
		self.forked = False
		
		self.CurrentLiabilities_key = None
		self.CurrentLiabilities_df = None
		self.CurrentLiabilities_arr = None
		self.CurrentLiabilities_unit = None
		
		self.NonCurrentLiabilities_key = None
		self.NonCurrentLiabilities_df = None
		self.NonCurrentLiabilities_arr = None
		self.NonCurrentLiabilities_unit = None
		
	def get_TotalLiabilities_values(self,company_facts,start_fork=False):
		
		KEYS = keys = ['Total Liabilities Net Minority Interest']
		
		if start_fork == True:
			self.forked = True
			self.TotalLiabilities_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.TotalLiabilities_arr
			
		possible_TotalLiabilities_keys = ['Liabilities']
		accounting_key = kh.get_accounting_key(company_facts,possible_TotalLiabilities_keys)
		self.TotalLiabilities_key = list(filter(lambda key : key.strip()  in company_facts['facts'][accounting_key[0]].keys(), possible_TotalLiabilities_keys))	

		if not self.TotalLiabilities_key: #try this
			possible_TotalLiabilities_keys = [
			'LiabilitiesCurrent',
			'CurrentLiabilities',
			'LiabilitiesNoncurrent',
			'NoncurrentLiabilities',]
			
			self.TotalLiabilities_key = list(filter(lambda key: key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_TotalLiabilities_keys  ))

			self.CurrentLiabilities_key = [key for key in self.TotalLiabilities_key if 'Current' in key]
			self.NonCurrentLiabilities_key = [key for key in self.TotalLiabilities_key if 'Noncurrent' in key]
			
			if any([ not self.CurrentLiabilities_key,not self.NonCurrentLiabilities_key]): #if still cant get keys to build a total liabilites then fork it
				self.forked = True
				self.TotalLiabilities_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
				return self.TotalLiabilities_arr
				
			
			try: #try block is because MRK has a key but it has no info so if there is no info fork it
				possible_forms = ['20-F','40-F','10-K','20-F/A']
				
				self.CurrentLiabilities_unit = kh.set_unit_key(company_facts,accounting_key,self.CurrentLiabilities_key)
				self.NonCurrentLiabilities_unit = kh.set_unit_key(company_facts,accounting_key,self.NonCurrentLiabilities_key)
				
				CurrentLiabilities_df_unfiltered = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.CurrentLiabilities_key[0]]['units'][self.CurrentLiabilities_unit[0]]  ).drop_duplicates(subset='end')				
				current_form = np.unique(list(filter(lambda forms: forms in possible_forms, CurrentLiabilities_df_unfiltered.form)))
				self.CurrentLiabilities_df = CurrentLiabilities_df_unfiltered[(CurrentLiabilities_df_unfiltered.form == current_form[0])]
				self.CurrentLiabilities_df.index = range(len(self.CurrentLiabilities_df))
				try:
					self.CurrentLiabilities_arr = get_arr.get_arr(self.CurrentLiabilities_df)				
				except AttributeError:
					self.CurrentLiabilities_arr = get_arr.get_arr_without_start_date(self.CurrentLiabilities_df)
				
				NonCurrentLiabilities_df_unfiltered = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.NonCurrentLiabilities_key[0]]['units'][self.NonCurrentLiabilities_unit[0]] ).drop_duplicates(subset='end')		
				Noncurrent_form = np.unique(list(filter(lambda forms: forms in possible_forms, NonCurrentLiabilities_df_unfiltered.form)))
				self.NonCurrentLiabilities_df = NonCurrentLiabilities_df_unfiltered[(NonCurrentLiabilities_df_unfiltered.form == Noncurrent_form[0])]
				self.NonCurrentLiabilities_df.index = range(len(self.NonCurrentLiabilities_df))				
				
				try:
					self.NonCurrentLiabilities_arr = get_arr.get_arr(self.NonCurrentLiabilities_df)
				except AttributeError:
					self.NonCurrentLiabilities_arr = get_arr.get_arr_without_start_date(self.NonCurrentLiabilities_df)

				self.TotalLiabilities_key = None
				self.TotalLiabilities_df = None
				self.TotalLiabilities_arr = None
				self.unit = None
				
				return list(map(lambda current,noncurrent: current+noncurrent, self.CurrentLiabilities_arr,self.NonCurrentLiabilities_arr ))
				
			except IndexError: #reassign and fork it
				self.CurrentLiabilities_key = None
				self.CurrentLiabilities_df = None
				self.CurrentLiabilities_arr = None
				self.CurrentLiabilities_unit = None
				
				self.NonCurrentLiabilities_key = None
				self.NonCurrentLiabilities_df = None
				self.NonCurrentLiabilities_arr = None
				self.NonCurrentLiabilities_unit = None
				
				self.forked = True
				self.TotalLiabilities_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
				return self.TotalLiabilities_arr

		self.unit = kh.set_unit_key(company_facts,accounting_key,self.TotalLiabilities_key)
		self.TotalLiabilities_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.TotalLiabilities_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')		
		self.TotalLiabilities_arr = get_arr.get_arr_without_start_date(self.TotalLiabilities_df)
		
		return self.TotalLiabilities_arr	
		
		
#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#single_file = 'ACN.json'
#final_path = dir_path / single_file
#ticker = single_file[0:-5]
#with open(final_path,'r') as fr:
#	local_file = fr.read()
#	local_json = json.loads(local_file)
#	to  = TotalLiabilities(ticker)
#	test = to.get_TotalLiabilities_values(local_json)
#	print(test)

#########################################


#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	print(file_name)
#	with open(file_path,'r') as fr:
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		ticker = file_name[0:-5]
#		to  = TotalLiabilities(ticker)
#		test = to.get_TotalLiabilities_values(local_json)
#		print(test)	
				










#		
##		
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

#tl = TotalLiabilities(sample_ticker)
#test = tl.get_TotalLiabilities_values(response.json())
#print(test)
		


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
#	tl = TotalLiabilities(sample_ticker)
#	test = tl.get_TotalLiabilities_values(response.json())
#	print(test)		
#		
		
			
