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



class TotalAssets:
	def __init__(self,ticker):
		self.ticker = ticker
		self.TotalAssets_key = None
		self.TotalAssets_df = None
		self.TotalAssets_arr = None
		self.unit = None
		self.forked = False
		
	
	def get_TotalAsset_values(self,company_facts,start_fork=False) :
		
		KEYS = ['Total Assets']
		
		if start_fork == True:
			self.forked = True
			self.TotalAssets_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.TotalAssets_arr
						
		possible_TA_keys = ['Assets']
		accounting_key = kh.get_accounting_key(company_facts,possible_TA_keys)
		self.TotalAssets_key = list(filter(lambda key: key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_TA_keys  ))			
		
		if not self.TotalAssets_key:
			self.forked = True
			self.TotalAssets_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.TotalAssets_arr
			
		if len(self.TotalAssets_key) > 1:
			self.TotalAssets_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.TotalAssets_key)
			
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.TotalAssets_key)
		
		self.TotalAssets_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.TotalAssets_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')
		
		try:
			self.TotalAssets_arr = get_arr.get_arr(self.TotalAssets_df)
			
		except AttributeError:
			self.TotalAssets_arr = get_arr.get_arr_without_start_date(self.TotalAssets_df)
		
		if not self.TotalAssets_arr:
			self.forked = True
			self.TotalAssets_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.TotalAssets_arr
		
		return self.TotalAssets_arr


