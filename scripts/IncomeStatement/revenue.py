import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent) )  
#########
import pandas as pd
import json
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
import forks.forks as fork

import requests
import time
class Revenue:
	def __init__(self,ticker):
		self.ticker = ticker
#		self.company_facts = company_facts_response
		self.revenue_list = None
		self.service_revenue_arr = None
		self.SaleOfGoods_arr = None
		
		self.revenue_df = None
		self.service_revenue_df = None
		self.SaleOfGoods_df = None
		
		self.revenue_key = None
		self.service_revenue_key = None		
		self.SaleOfGoods_key = None
		
		self.unit = None
		self.service_revenue_unit =None
		self.SaleOfGoods_unit = None
		
		self.forked = False
	
	def get_revenue_values(self,company_facts,start_fork=False):
		KEYS = ['Total Revenue']
		
		if start_fork == True:
			self.forked = True
			self.revenue_list = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.revenue_list
					
		possible_revenue_keys = ['Revenue','Revenues'] #check this first
		accounting_key = kh.get_accounting_key(company_facts,possible_revenue_keys)
		self.revenue_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_revenue_keys))						

		if not self.revenue_key: #check this second
			possible_revenue_keys = ['RevenueAndOperatingIncome']
			accounting_key = kh.get_accounting_key(company_facts,possible_revenue_keys)
			self.revenue_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_revenue_keys))	
		
		if not self.revenue_key: #check this third
			possible_sale_service_keys = ['SalesRevenueGoodsNet',
									'RevenueFromSaleOfGoods',
									'SalesRevenueServicesNet']
			accounting_key = kh.get_accounting_key(company_facts,possible_sale_service_keys)
			self.revenue_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_sale_service_keys))								
		
		
		if any([not self.revenue_key,len(self.revenue_key) == 1]): #if still no key fork it or if only one key because SalesRevenueServicesNet may be only half of the equation
			self.forked = True
			self.revenue_list = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.revenue_list
		
		elif self.revenue_key[0] in possible_revenue_keys: #if there is a key from the first two checks do this
			
			self.unit = kh.set_unit_key(company_facts,accounting_key,self.revenue_key)				
			
			self.revenue_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.revenue_key[0]]['units'][self.unit[0]]  ).drop_duplicates('end')
			
			self.revenue_list = get_arr.get_arr(self.revenue_df)
			
			if any([not self.revenue_list, isinstance(self.revenue_list,dict)]): #if no info in json file do this;  note: the dictionary is being returned from get_arr 
				self.forked = True
				self.revenue_list = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
				return self.revenue_list
		
			return self.revenue_list
		
			
		
		else: #if theres keys from the third check do this
			
			#if there is a service and goods key do this
			if all(['SalesRevenueServicesNet' in self.revenue_key, any([ 'SalesRevenueGoodsNet' in self.revenue_key, 'RevenueFromSaleOfGoods' in self.revenue_key ])  ]):  
				self.service_revenue_key = ['SalesRevenueServicesNet']
				self.SaleOfGoods_key = [key for key in self.revenue_key if 'Sale' in key]
				
				if len(self.SaleOfGoods_key) > 1:
					self.SaleOfGoods_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.SaleOfGoods_key)
				
				self.service_revenue_unit = kh.set_unit_key(company_facts,accounting_key,self.service_revenue_key)
				self.SaleOfGoods_unit = kh.set_unit_key(company_facts,accounting_key,self.SaleOfGoods_key)
				
				self.service_revenue_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.service_revenue_key[0]]['units'][self.service_revenue_unit[0]]  ).drop_duplicates(subset='end')
				self.SaleOfGoods_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.SaleOfGoods_key[0]]['units'][self.SaleOfGoods_unit[0]]  ).drop_duplicates(subset='end')
				
				self.service_revenue_arr = get_arr.get_arr(self.service_revenue_df)
				self.SaleOfGoods_arr = get_arr.get_arr(self.SaleOfGoods_df)
				
				if any([isinstance(self.service_revenue_arr,dict),isinstance(self.SaleOfGoods_arr,dict)]): #if a service or goods key comes back a dict because of no info in json file
					self.forked = True
					self.revenue_list = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
					return self.revenue_list
			
				else: #if both comeback with info 
					
					return list(map(lambda sales,service: sales+service, self.service_revenue_arr,self.SaleOfGoods_arr))			
			
			
			elif all(['SalesRevenueServicesNet' not in self.revenue_key, any(['SalesRevenueGoodsNet' in self.revenue_key,'RevenueFromSaleOfGoods' in self.revenue_key ])]):
			#if Sale of goods keys no service key
			
				if len(self.revenue_key) > 1: 
					self.revenue_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.revenue_key)
				
				self.unit = kh.set_unit_key(company_facts,accounting_key,self.revenue_key)
				self.revenue_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.revenue_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')
				self.revenue_list = get_arr.get_arr(self.revenue_df)

				if isinstance(self.revenue_list,dict): #if returns a revenue list is a dict; note: dict returning from get arr
					self.forked = True
					self.revenue_list = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
					return self.revenue_list
				
				else: #if revenue list has info and no dict is returned
					return self.revenue_list
				
				
				
			

				



#from pathlib import Path as path
#from pathlib import PurePath as ppath
#import os
#import json
		

#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#single_file = 'LOW.json'
#final_path = dir_path / single_file
#ticker = single_file[0:-5]
#with open(final_path,'r') as fr:
#	local_file = fr.read()
#	local_json = json.loads(local_file)
#	rev = Revenue(ticker)
#	rev_v = rev.get_revenue_values(local_json)
#	print(rev_v)



#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
##dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	ticker = file_name[0:-5]
#	with open(file_path,'r') as fr:
#		print(ticker)
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		rev = Revenue(ticker)
#		rev_v = rev.get_revenue_values(local_json,start_fork=True)
#		print(rev_v)
#				









#headers = {'User-Agent': 'thorntonbill343@gmail.com'}
#url = 'https://www.sec.gov/files/company_tickers.json'
#response = requests.get(url,headers=headers)
#json = response.json()
#df = pd.DataFrame(json).T	
#######print(df)	



############################################
#df.index = df.ticker
#sample = df.loc['SHOP']
#sample_cik = str(sample.cik_str).zfill(10)
#sample_ticker = sample.ticker
#url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'


#response = requests.get(url,headers=headers)

#b = time.time()
#rev = Revenue(sample_ticker)
##print(rev.revenue_key)
##print(rev.SaleOfGoods_key)
#test = rev.get_revenue_values(response.json())
#e = time.time()
#print(e-b)
#print(test)





#	
#for num in range(100,120):
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
#	rev = Revenue(sample_ticker)
#	test = rev.get_revenue_values(response.json())
#	
#	print(test)
#	
	
	
	
	
	
	
	
	
	
	
	
