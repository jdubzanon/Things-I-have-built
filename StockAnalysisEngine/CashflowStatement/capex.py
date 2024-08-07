import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent) )  

import pandas as pd
import json
import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
import yfinance as yf
import forks.forks as fork
import requests
import time


class capex:
	def __init__(self,ticker):
		self.ticker = ticker
		self.capex_key = None
		self.capex_df = None
		self.capex_arr = None
		self.unit = None
		self.forked = False
		
	def get_capex_values(self,company_facts,start_fork=False):
		KEYS = ['Net PPE Purchase And Sale','Capital Expenditure','Capital Expenditure Reported']
		
		if start_fork == True: #cashflow strategy changes based on forking
			self.forked = True
			self.capex_arr = fork.fork(ticker_id=self.ticker,statement='cashflow',keys=KEYS)
			return self.capex_arr
		
		possible_capex_keys = [
		'PurchaseOfPropertyPlantAndEquipmentIntangibleAssetsOtherThanGoodwillInvestmentPropertyAndOtherNoncurrentAssets',
		'PurchaseOfOtherLongtermAssetsClassifiedAsInvestingActivities',
		'PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities',
		'PaymentsToAcquirePropertyPlantAndEquipment',
		'PaymentsToAcquireOtherPropertyPlantAndEquipment'
	
		]
		accounting_key = kh.get_accounting_key(company_facts,possible_capex_keys)

		self.capex_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_capex_keys  ))		
		
		if not self.capex_key:
			possible_capex_keys = ['PropertyPlantAndEquipment','PropertyPlantAndEquipmentNet','PropertyPlantAndEquipmentGross']
			accounting_key = kh.get_accounting_key(company_facts,possible_capex_keys)
			self.capex_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_capex_keys  ))		
			
			
		if not self.capex_key:
			self.forked = True
			self.capex_arr = fork.fork(ticker_id=self.ticker,statement='cashflow',keys=KEYS)
			return self.capex_arr
				
		if len(self.capex_key) > 1:
			self.capex_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.capex_key)

		self.unit = kh.set_unit_key(company_facts,accounting_key,self.capex_key)

		self.capex_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.capex_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')
		
		try:
			self.capex_arr = get_arr.get_arr(self.capex_df)
			
		except AttributeError:
			self.capex_arr = get_arr.get_arr_without_start_date(self.capex_df)
			
		if not self.capex_arr:
			self.forked = True
			self.capex_arr = fork.fork(ticker_id=self.ticker,statement='cashflow',keys=KEYS)
			return self.capex_arr
		
		return self.capex_arr


#Note the capex can be either a number given as a key or it has to be calculated as a change YOY depending on what the key is reported must check what the key is when doing calculation
#if its PaymentsToAcquirePropertyPlantAndEquipment thats the same as PP&E y2 - PP&E y2
#if its PropertyPlantAndEquipmentNet PropertyPlantAndEquipment
	#need to make calculation

#from pathlib import Path as path
#from pathlib import PurePath as ppath
#import os
#import json
#		

#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#single_file = 'JPM.json'
#final_path = dir_path / single_file
#ticker = single_file[0:-5]
#with open(final_path,'r') as fr:
#	local_file = fr.read()
#	local_json = json.loads(local_file)
#	cap = capex(ticker)
#	capv = cap.get_capex_values(local_json,start_fork=True)
#	print(capv)		


#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	with open(file_path,'r') as fr:
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		ticker = file_name[0:-5]
#		print(ticker)
#		cap = capex(ticker)
#		capv = cap.get_capex_values(local_json,start_fork=True)
#		print(capv)





















#headers = {'User-Agent': 'thorntonbill343@gmail.com'}
#url = 'https://www.sec.gov/files/company_tickers.json'
#response = requests.get(url,headers=headers)
#json = response.json()
#df = pd.DataFrame(json).T	



##########################################
#df.index = df.ticker
#sample = df.loc['DIS']
#sample_cik = str(sample.cik_str).zfill(10)
#sample_ticker = sample.ticker
#url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'


#response = requests.get(url,headers=headers)
#capx = capex(sample_ticker)
#test = capx.get_capex_values(response.json())
#print(test)
#try:
#	for key in response.json()['facts']['us-gaap'].keys():
#		if 'PropertyPlant' in key:
#			print(key)
#except KeyError:
#	for key in response.json()['facts']['ifrs-full'].keys():
#		if 'PropertyPlant' in key:
#			print(key)
#for key in response.json()['facts']['ifrs-full'].keys():
#		if 'PropertyPlant' in key:
#			print(key)

##	
#for num in range(10,50):
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
#	capx = capex(sample_ticker)
#	test = capx.get_capex_values(response.json())
##	print(test)
#	time.sleep(1)











