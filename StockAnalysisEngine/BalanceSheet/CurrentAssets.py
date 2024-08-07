import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent) )  


import pandas as pd
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
import forks.forks as fork



class CurrentAssets:
	def __init__(self,ticker):
		self.ticker = ticker
		self.CurrentAssets_key = None
		self.CurrentAssets_df = None
		self.CurrentAssets_arr = None
		self.unit = None
		self.forked = False
		
	def get_CurrentAsset_values(self,company_facts,start_fork=False):
		
		KEYS = ['Current Assets']
		
		if start_fork == True:
			self.forked = True
			self.CurrentAssets_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.CurrentAssets_arr

		possible_CA_keys = ['AssetsCurrent','CurrentAssets']
		
		accounting_key = kh.get_accounting_key(company_facts,possible_CA_keys)
		
		self.CurrentAssets_key = list(filter(lambda key: key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_CA_keys  ))		
		
		if not self.CurrentAssets_key:
			self.forked = True
			self.CurrentAssets_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.CurrentAssets_arr
		
		if len(self.CurrentAssets_key) > 1:
			self.CurrentAssets_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.CurrentAssets_key)
			
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.CurrentAssets_key)
		
		self.CurrentAssets_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.CurrentAssets_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')
		
		try:
			self.CurrentAssets_arr = get_arr.get_arr(self.CurrentAssets_df)
		
		except AttributeError:
			self.CurrentAssets_arr = get_arr.get_arr_without_start_date(self.CurrentAssets_df)
		
		if not self.CurrentAssets_arr:
			self.forked = True
			self.CurrentAssets_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.CurrentAssets_arr
			
		return self.CurrentAssets_arr
			
			
#from pathlib import Path as path
#from pathlib import PurePath as ppath
#import os
#import json
		

#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#single_file = 'MS.json'
#final_path = dir_path / single_file
#ticker = single_file[0:-5]
#with open(final_path,'r') as fr:
#	local_file = fr.read()
#	local_json = json.loads(local_file)
#	rev = CurrentAssets(ticker)
#	rev_v = rev.get_CurrentAsset_values(local_json)
#	print(rev_v)						


#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	with open(file_path,'r') as fr:
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		ticker = file_name[0:-5]
#		print(ticker)
#		rev = CurrentAssets(ticker)
#		rev_v = rev.get_CurrentAsset_values(local_json)
#		print(rev_v)						
#			
			
			
			
			


#headers = {'User-Agent': 'thorntonbill343@gmail.com'}
#url = 'https://www.sec.gov/files/company_tickers.json'
#response = requests.get(url,headers=headers)
#json = response.json()
#df = pd.DataFrame(json).T	



###########################################
#df.index = df.ticker
#sample = df.loc['BX']
#sample_cik = str(sample.cik_str).zfill(10)
#sample_ticker = sample.ticker
#url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'


#response = requests.get(url,headers=headers)

#ca = CurrentAssets(sample_ticker)
#test = ca.get_CurrentAsset_values(response.json())
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
#	ca = CurrentAssets(sample_ticker)
#	test = ca.get_CurrentAsset_values(response.json())

#	print(test)





