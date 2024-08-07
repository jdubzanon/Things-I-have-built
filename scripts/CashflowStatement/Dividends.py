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


class Dividends:
	def __init__(self,ticker):
		self.ticker = ticker
		self.dividends_key = None
		self.dividends_df = None
		self.dividends_arr = None
		self.unit = None
		self.forked = False
	
	def get_dividend_values(self,company_facts,start_fork=False):
		
		if start_fork == True:
			self.forked = True
			self.dividends_arr = fork.fork(ticker_id=self.ticker,statement='cashflow',keys=['Cash Dividends Paid'])
			if isinstance(self.dividends_arr,dict):
				self.dividends_arr = [0,0,0,0]
			return self.dividends_arr	
				
		
		possible_dividends_keys = [
		'PaymentsOfDividends',
		'PaymentsOfDividendsCommonStock',
		'PaymentsOfOrdinaryDividends',
		'DividendsPaidOrdinaryShares',
		'DividendsPaid']
		
		accounting_key = kh.get_accounting_key(company_facts,possible_dividends_keys)

		if len(accounting_key) > 1:
			self.dividends_key = kh.get_ReportingKey_with_two_accounting_keys(company_facts,accounting_key,possible_dividends_keys)

		else:
			self.dividends_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_dividends_keys  ))			
			
#		return self.dividends_key
		
		if not self.dividends_key:
			self.forked = True
			self.dividends_arr = fork.fork(ticker_id=self.ticker,statement='cashflow',keys=['Cash Dividends Paid'])
			if isinstance(self.dividends_arr,dict):
				self.dividends_arr = [0,0,0,0]
			return self.dividends_arr	
				
		if len(self.dividends_key) > 1:
			self.dividends_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.dividends_key)
			
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.dividends_key)
		
		self.dividends_df = pd.DataFrame( company_facts['facts'][accounting_key[0]][self.dividends_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')
		try:
			self.dividends_arr = get_arr.get_arr(self.dividends_df)
			
		except AttributeError:
			self.dividends_arr = get_arr.get_arr_without_start_date(self.dividends_df)
		
		if not self.dividends_arr:
			self.forked = True
			self.dividends_arr = fork.fork(ticker_id=self.ticker,statement='cashflow',keys=['Cash Dividends Paid'])
			if isinstance(self.dividends_arr,dict):
				self.dividends_arr = [0,0,0,0]
			return self.dividends_arr	
		return self.dividends_arr	
	#not all companies pay dividends need to figure this out
	#dividends can also be calculated net income - net change in retained earnings
	#this module is to calculate return on capital if there is no dividends you can omit it because its just part of an equation that may or may not be subtracted 
	#in calculation if self.dividends_arr is None then omit the dividends in calculation
	#usin module for return on capital (net income - dividend)/(debt+equity)


#from pathlib import Path as path
#from pathlib import PurePath as ppath
#import os
#import json
		

#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#single_file = 'BRK-B.json'
#final_path = dir_path / single_file
#ticker = single_file[0:-5]
#with open(final_path,'r') as fr:
#	local_file = fr.read()
#	local_json = json.loads(local_file)
#	div = Dividends(ticker)
#	divv = div.get_dividend_values(local_json,start_fork=True)
#	print(divv)

#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	with open(file_path,'r') as fr:
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		ticker = file_name[0:-5]
#		print(ticker)
#		div = Dividends(ticker)
#		divv = div.get_dividend_values(local_json)
#		print(divv)









#headers = {'User-Agent': 'thorntonbill343@gmail.com'}
#url = 'https://www.sec.gov/files/company_tickers.json'
#response = requests.get(url,headers=headers)
#json = response.json()
#df = pd.DataFrame(json).T	



###########################################
#df.index = df.ticker
#sample = df.loc['PFE']
#sample_cik = str(sample.cik_str).zfill(10)
#sample_ticker = sample.ticker
#url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'


#response = requests.get(url,headers=headers)

#div = Dividends(sample_ticker)
#test = div.get_dividend_values(response.json())
#print(test)


#try:
#	for key in response.json()['facts']['us-gaap'].keys():
#		if 'Dividend' in key:
#			print(key)
#except KeyError:
#	for key in response.json()['facts']['ifrs-full'].keys():
#		if 'Dividend' in key:
#			print(key)

##	
#for num in range(10,60):
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
#	div = Dividends(sample_ticker)
#	test = div.get_dividend_values(response.json())


#	print(test)
#	time.sleep(1)









