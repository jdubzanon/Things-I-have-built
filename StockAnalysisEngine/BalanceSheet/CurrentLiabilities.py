import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent) )  


import pandas as pd
import json
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
import forks.forks as fork


class CurrentLiabilities:
	def __init__(self,ticker):
		self.ticker = ticker
		self.CurrentLiabilities_key = None
		self.CurrentLiabilities_df = None
		self.CurrentLiabilities_arr = None
		self.unit = None
		self.forked = False
	
	def get_CurrentLiabilities_values(self,company_facts,start_fork=False):
		
		KEYS = ['Current Liabilities']
		
		if start_fork == True:
			self.forked = True
			start_fork = True
			self.CurrentLiabilities_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.CurrentLiabilities_arr
		
		possible_CurrentLiabilities_keys = ['LiabilitiesCurrent','CurrentLiabilities']
		accounting_key = kh.get_accounting_key(company_facts,possible_CurrentLiabilities_keys)
		self.CurrentLiabilities_key = list(filter(lambda key : key.strip()  in company_facts['facts'][accounting_key[0]].keys(), possible_CurrentLiabilities_keys))	
		
		
		if not self.CurrentLiabilities_key:
			self.forked = True
			self.CurrentLiabilities_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.CurrentLiabilities_arr
			
		if len(self.CurrentLiabilities_key) > 1:
		
			self.CurrentLiabilities_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.CurrentLiabilities_key)
			
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.CurrentLiabilities_key)
		
		self.CurrentLiabilities_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.CurrentLiabilities_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')
		
		self.CurrentLiabilities_arr = get_arr.get_arr_without_start_date(self.CurrentLiabilities_df)
		
		if not self.CurrentLiabilities_arr:
			self.forked = True
			self.CurrentLiabilities_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.CurrentLiabilities_arr
			
		return self.CurrentLiabilities_arr
		

		
			
