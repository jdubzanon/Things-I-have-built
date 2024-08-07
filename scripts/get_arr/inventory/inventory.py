import sys
##for gedit 
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/webpage/bin')
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/scripts')
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/webpage/lib/python3.10/site-packages')
sys.path.append('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts')
sys.path.append('/home/jdubzanon/hdd/envornments/webpage/lib/python3.10/site-packages')


import pandas as pd
import json
import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr

import requests
import time


class inventory:
	def __init__(self,ticker):
		self.ticker = ticker
		self.inventory_key = None
		self.inventory_df = None
		self.inventory_arr = None
		self.unit = None
		self.forked = False
		
	def get_inventory_values(self,company_facts,start_fork=False):
		
		#need to create a fork using yfinance
		
		#NEED TO CHECK WHAT INDUSTRY THE STOCK IS IN USING yfinance or someother api
		#if reit
		
		  # ----> try using theses reit RealEstatePropertyNet RealEstatePropertyAtCarryingValues pld,amt,eqix
		possible_inventory_keys = ['InventoryNet','Inventories','InventoryFinishedGoods','InventoryGross']

		accounting_key = kh.get_accounting_key(company_facts,possible_inventory_keys)

		self.inventory_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_inventory_keys  ))			
		
		if any([start_fork == True, not self.inventory_key]):
			#any then create fork
			self.forked = True
			self.inventory_arr =  {'from_inventory_module': 'need to create fork'}
			return self.inventory_arr
			
		if len(self.inventory_key) > 1:
		
			self.inventory_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.inventory_key)			
			
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.inventory_key)
		
		self.inventory_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.inventory_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')

		try:
			self.inventory_arr = get_arr.get_arr(self.inventory_df)
		except AttributeError:
			self.inventory_arr = get_arr.get_arr_without_start_date(self.inventory_df)
		
		if all([start_fork is False, not self.inventory_key]):
			self.forked = True
			self.inventory_arr = {'from inventory mod': 'need to create arr fork'}
			

		return self.inventory_arr

		

#from pathlib import Path as path
#from pathlib import PurePath as ppath
#import os
#import json
		

#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#single_file = 'HON.json'
#final_path = dir_path / single_file
#ticker = single_file[0:-5]
#with open(final_path,'r') as fr:
#	local_file = fr.read()
#	local_json = json.loads(local_file)
#	rev = NetProfit(ticker)
#	rev_v = rev.get_NetProfit_values(local_json)
#	print(rev_v)			


#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	with open(file_path,'r') as fr:
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		ticker = file_name[0:-5]
#		print(ticker)
#		rev = inventory(ticker)
#		rev_v = rev.get_inventory_values(local_json)
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

#inv = inventory(sample_ticker)
#test = inv.get_inventory_values(response.json())
#print(test)




	
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
#	inv = inventory(sample_ticker)
#	test = inv.get_inventory_values(response.json())

#	print(test)
	
	
	
	
	
	
	
	
	
	

