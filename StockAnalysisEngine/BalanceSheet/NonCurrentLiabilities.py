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


class NonCurrentLiabilities:
	def __init__(self,ticker):
		self.ticker = ticker
		self.NonCurrentLiabilities_key = None
		self.NonCurrentLiabilities_df = None
		self.NonCurrentLiabilities_arr = None
		self.unit = None
		self.forked = False
	
	def get_NonCurrentLiabilities_values(self,company_facts,start_fork=False):
		
		KEYS = ['Total Non Current Liabilities Net Minority Interest']

		if start_fork == True:
			self.forked = True
			self.NonCurrentLiabilities_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.NonCurrentLiabilities_arr			
					
		possible_NonCurrentLiabilities_keys = ['LiabilitiesNoncurrent','NoncurrentLiabilities']
		accounting_key = kh.get_accounting_key(company_facts,possible_NonCurrentLiabilities_keys)
		self.NonCurrentLiabilities_key = list(filter(lambda key : key.strip()  in company_facts['facts'][accounting_key[0]].keys(), possible_NonCurrentLiabilities_keys))	
			
		if not self.NonCurrentLiabilities_key:
			self.forked = True
			self.NonCurrentLiabilities_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.NonCurrentLiabilities_arr			
			
		if len(self.NonCurrentLiabilities_key) > 1:
			self.NonCurrentLiabilities_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.NonCurrentLiabilities_key)
			
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.NonCurrentLiabilities_key)
		
		self.NonCurrentLiabilities_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.NonCurrentLiabilities_key[0]]['units'][self.unit[0]]  )
		
		self.NonCurrentLiabilities_arr = get_arr.get_arr_without_start_date(self.NonCurrentLiabilities_df)
		
		if any([not self.NonCurrentLiabilities_arr,isinstance(self.NonCurrentLiabilities_arr,dict) ]):
			print('forked bottom')
			self.forked = True
			self.NonCurrentLiabilities_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.NonCurrentLiabilities_arr			

		return self.NonCurrentLiabilities_arr
		



		


