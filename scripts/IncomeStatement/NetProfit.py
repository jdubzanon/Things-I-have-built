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

class NetProfit:
	def __init__(self,ticker):
		self.ticker = ticker
		self.NetProfit_key = None
		self.NetProft_df = None
		self.NetProfit_arr = None
		self.unit = None
		self.forked = False
		
		
	def get_NetProfit_values(self,company_facts,start_fork=False):
		KEYS = ['Net Income']
		
		if start_fork == True:
			self.forked = True
			self.NetProfit_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)		
			return self.NetProfit_arr
			
		possible_NetProfit_keys = ['ProfitLoss','NetIncomeLoss']
		accounting_key = kh.get_accounting_key(company_facts,possible_NetProfit_keys)
		self.NetProfit_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_NetProfit_keys))
			
		if not self.NetProfit_key:
			self.forked = True
			self.NetProfit_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)		
			return self.NetProfit_arr
						
		if len(self.NetProfit_key) > 1:
			self.NetProfit_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.NetProfit_key)

		self.unit = kh.set_unit_key(company_facts,accounting_key,self.NetProfit_key)
		self.NetProft_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.NetProfit_key[0]]['units'][self.unit[0]]).drop_duplicates(subset='end')
		
		try:
			self.NetProfit_arr = get_arr.get_arr(self.NetProft_df)
		except:
			self.NetProfit_arr = {'from net profit mod' : 'No Information Available'}
		
		if not self.NetProfit_arr:
			self.forked = True
			self.NetProfit_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)		
			return self.NetProfit_arr
		
		return self.NetProfit_arr


from pathlib import Path as path
from pathlib import PurePath as ppath
import os
import json
		

#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#single_file = 'BP.json'
#final_path = dir_path / single_file
#ticker = single_file[0:-5]
#with open(final_path,'r') as fr:
#	local_file = fr.read()
#	local_json = json.loads(local_file)
#	rev = NetProfit(ticker)
#	rev_v = rev.get_NetProfit_values(local_json)
#	print(rev_v)			


#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	with open(file_path,'r') as fr:
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		ticker = file_name[0:-5]
#		print(ticker)
#		rev = NetProfit(ticker)
#		rev_v = rev.get_NetProfit_values(local_json,start_fork=True)
#		print(rev_v)	










		
#headers = {'User-Agent': 'thorntonbill343@gmail.com'}
#url = 'https://www.sec.gov/files/company_tickers.json'
#response = requests.get(url,headers)
#json = response.json()
#df = pd.DataFrame(json).T	
######print(df)	



###########################################
#df.index = df.ticker
#sample = df.loc['CNI']
#sample_cik = str(sample.cik_str).zfill(10)
#sample_ticker = sample.ticker
#url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'

##print(url)

#response = requests.get(url,headers=headers)

#net = NetProfit('CNI')
#test = net.get_NetProfit_values(response.json())
#print(isinstance(test,dict))
#print(test)





	
#for num in range(50,200):
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
#	net = NetProfit(sample_ticker)
#	test = net.get_NetProfit_values(data)
#	try:
#		print(test[0])
#	except:
#		print(test)
#	time.sleep(1)	
###	
##			
			
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
