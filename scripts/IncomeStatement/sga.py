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


#sga --> Selling General And Administrative  

class sga:
	def __init__(self,ticker):
		self.ticker = ticker
		self.sga_key = None
		self.marketing_key = None
		self.admin_key = None
		
		self.sga_df = None
		self.marketing_df = None
		self.admin_df = None
		
		self.sga_arr = None
		self.marketing_arr = None
		self.admin_arr = None
		
		self.unit = None
		self.marketing_unit = None
		self.admin_unit = None
		
		self.mark_admin_arr = None
		
		self.forked = False
		
	def get_sga_values(self,company_facts,start_fork=False):
		KEYS = ['Selling General And Administration']
		
		if start_fork == True:
			self.forked = True
			self.sga_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.sga_arr
		
		possible_sga_keys = [
		'SellingGeneralAndAdministrative',
		'SellingGeneralAndAdministrativeExpense',
		'SellingAndMarketingExpense',
		'GeneralAndAdministrativeExpense',
		'MarketingAndAdvertisingExpense',
		'AdministrativeExpense'
		]

		accounting_key = kh.get_accounting_key(company_facts,possible_sga_keys)
		self.sga_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(),possible_sga_keys))
		
		if not self.sga_key:
			self.forked = True
			self.sga_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.sga_arr
				
		if len(self.sga_key) > 1:
#block1			
			if all(['SellingGeneralAndAdministrativeExpense' in self.sga_key, len(self.sga_key) < 3  ]):
				#if SellingGeneralAndAdministrativeExpense some other expense that only reports part of the expense EX: AdministrativeExpense which doesnt report market and general as well
#				print('block1')
				self.sga_key = ['SellingGeneralAndAdministrativeExpense']
				self.unit = kh.set_unit_key(company_facts,accounting_key,self.sga_key)
				self.sga_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.sga_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')
				try:
					self.sga_arr = get_arr.get_arr(self.sga_df)
				except AttributeError:
					self.sga_arr = get_arr.get_arr_without_start_date(self.sga_df)
				return self.sga_arr
#block2 		
			if all(['SellingGeneralAndAdministrativeExpense' in self.sga_key, len(self.sga_key) > 2   ]): #<--- need to fix this block admin is using marketing keys
				# seperate SellingGeneralAndAdministrativeExpense and other keys; add other keys together and measure against SellingGeneralAndAdministrativeExpense give back the arr with most info
				
#				print('block2')
				sga_key = ['SellingGeneralAndAdministrativeExpense']
				sga_unit = kh.set_unit_key(company_facts,accounting_key,sga_key)
				sga_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][sga_key[0]]['units'][sga_unit[0]]  )					
				try:
					sga_arr = get_arr.get_arr(sga_df)
				except AttributeError:
					sga_arr = get_arr.get_arr_without_start_date(sga_df) 

				self.marketing_key = [key for key in self.sga_key if 'Marketing' in key]
				self.admin_key = [key for key in self.sga_key if 'Administrative' in key]

				if len(self.marketing_key) > 1:
					print(accounting_key,self.marketing_key)
					self.marketing_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.marketing_key)
				if len(self.admin_key) > 1:
					self.admin_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.admin_key)

				self.marketing_unit = kh.set_unit_key(company_facts,accounting_key,self.marketing_key)
				self.marketing_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.marketing_key[0]]['units'][self.marketing_unit[0]]  ).drop_duplicates(subset='end')

				self.admin_unit = kh.set_unit_key(company_facts,accounting_key,self.admin_key)	
				self.admin_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.admin_key[0]]['units'][self.admin_unit[0]]  ).drop_duplicates(subset='end')
				try:
					self.marketing_arr = get_arr.get_arr(self.marketing_df)
					self.admin_arr = get_arr.get_arr(self.admin_df)
				except AttributeError:
					self.marketing_arr = get_arr.get_arr_without_start_date(self.marketing_df)
					self.admin_arr = get_arr.get_arr_without_start_date(self.admin_df)
				
				mark_admin_arr = get_arr.add_multiple_to_get_values(self.marketing_arr,self.admin_arr)

				if len(mark_admin_arr) < len(sga_arr): #if sga arr has more info
					self.sga_key = sga_key					
					self.sga_df = sga_df
					self.unit = sga_unit
					self.sga_arr = sga_arr
					
					self.marketing_key = None
					self.marketing_unit = None
					self.marketing_df = None
					self.marketing_arr = None
					
					self.admin_key = None
					self.admin_unit = None
					self.admin_df = None
					self.admin_arr = None
					
				else: #if sga has less info
					self.sga_key = None
					self.unit = None
					self.sga_df = None
					self.sga_arr = None
					
				return mark_admin_arr if len(mark_admin_arr) > len(sga_arr) else sga_arr

			if all(['SellingGeneralAndAdministrativeExpense' not in self.sga_key ]):
#				print('block3')
				self.marketing_key = [key for key in self.sga_key if 'Marketing' in key]
				self.admin_key = [key for key in self.sga_key if 'Administrative' in key]
				
				if len(self.marketing_key) > 1:
					self.marketing_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.marketing_key)
				if len(self.admin_key) > 1:
					self.admin_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.admin_key)
				
				self.marketing_unit = kh.set_unit_key(company_facts,accounting_key,self.marketing_key)
				self.marketing_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.marketing_key[0]]['units'][self.marketing_unit[0]]  ).drop_duplicates(subset='end')
				
				self.admin_unit = kh.set_unit_key(company_facts,accounting_key,self.admin_key)	
				self.admin_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.admin_key[0]]['units'][self.admin_unit[0]]  ).drop_duplicates(subset='end')
				try:
					self.marketing_arr = get_arr.get_arr(self.marketing_df)
					self.admin_arr = get_arr.get_arr(self.admin_df)
				except AttributeError:
					self.marketing_arr = get_arr.get_arr_without_start_date(self.marketing_df)
					self.admin_arr = get_arr.get_arr_without_start_date(self.admin_df)
				
				self.sga_key = None
				self.unit = None
				self.sga_df = None
				self.sga_arr = None
				return get_arr.add_multiple_to_get_values(self.marketing_arr,self.admin_arr)
				
		else: #there is only on sga_key
#			print('block4')
#				print(self.sga_key)
			self.unit = kh.set_unit_key(company_facts,accounting_key,self.sga_key)
			self.sga_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.sga_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')
			try:
				self.sga_arr = get_arr.get_arr(self.sga_df)
			except AttributeError:
				self.sga_arr = get_arr.get_arr_without_start_date(self.sga_df)
			return self.sga_arr	



from pathlib import Path as path
from pathlib import PurePath as ppath
import os
import json




#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#single_file = 'BHP.json'
#final_path = dir_path / single_file
#ticker = single_file[0:-5]
#with open(final_path,'r') as fr:
#	local_file = fr.read()
#	local_json = json.loads(local_file)
#	op = sga(ticker)
#	test = op.get_sga_values(local_json)		
#	print(test)







#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	with open(file_path,'r') as fr:
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		ticker = file_name[0:-5]
#		print(ticker)
#		tr = sga(ticker)
#		test = tr.get_sga_values(local_json)
#		print(test)	
#					
		

###		
#headers = {'User-Agent': 'thorntonbill343@gmail.com'}
#url = 'https://www.sec.gov/files/company_tickers.json'
#response = requests.get(url,headers=headers)
#json = response.json()
#df = pd.DataFrame(json).T	
####print(df)	



###########################################
#df.index = df.ticker
#sample = df.loc['AMZN']
#sample_cik = str(sample.cik_str).zfill(10)
#sample_ticker = sample.ticker
#url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'

#response = requests.get(url,headers=headers)

#sga = sga(sample_ticker)
#test = sga.get_sga_values(response.json())

#print(sga.sga_key)

#print(test)





#	
#for num in range(20,40):
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

#	s = sga(sample_ticker)
#	test = s.get_sga_values(data)
#	
#	print(test)
##	
	
	
	
	
	
	
