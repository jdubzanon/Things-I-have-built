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
			
			






