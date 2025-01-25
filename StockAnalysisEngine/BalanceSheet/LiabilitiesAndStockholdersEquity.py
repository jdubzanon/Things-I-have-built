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


class LiabilitiesAndStockholdersEquity:
	def __init__(self,ticker):
		self.ticker = ticker
		self.LiabilitiesAndStockholdersEquity_key = None
		self.LiabilitiesAndStockholdersEquity_df = None
		self.LiabilitiesAndStockholdersEquity_arr = None
		self.unit = None
		self.forked = False
	
	def get_LiabilitiesAndStockholdersEquity_values(self,company_facts,start_fork=False):

		LIABILITIES_KEYS = ['Total Liabilities Net Minority Interest']
		STOCKHOLDERS_KEYS = ['Stockholders Equity']
		
		if start_fork == True:
			self.forked = True
			liabilities_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=LIABILITIES_KEYS)
			stockholders_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=STOCKHOLDERS_KEYS)
			if isinstance(liabilities_arr,dict):
				self.LiabilitiesAndStockholdersEquity_arr = liabilities_arr
			elif isinstance(stockholders_arr,dict):
				self.LiabilitiesAndStockholdersEquity_arr = stockholders_arr
			else:
				self.LiabilitiesAndStockholdersEquity_arr = list(map(lambda liabilities,stockholders: liabilities+stockholders,liabilities_arr,stockholders_arr))
			return self.LiabilitiesAndStockholdersEquity_arr
			
		possible_LiabilitiesAndStockholdersEquity_keys = ['LiabilitiesAndStockholdersEquity']
		accounting_key = kh.get_accounting_key(company_facts,possible_LiabilitiesAndStockholdersEquity_keys)
		self.LiabilitiesAndStockholdersEquity_key = list(filter(lambda key : key.strip()  in company_facts['facts'][accounting_key[0]].keys(), possible_LiabilitiesAndStockholdersEquity_keys))	
			
		if not self.LiabilitiesAndStockholdersEquity_key:
			self.forked = True
			liabilities_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=LIABILITIES_KEYS)
			stockholders_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=STOCKHOLDERS_KEYS)
			if isinstance(liabilities_arr,dict):
				self.LiabilitiesAndStockholdersEquity_arr = liabilities_arr
			elif isinstance(stockholders_arr,dict):
				self.LiabilitiesAndStockholdersEquity_arr = stockholders_arr
			else:
				self.LiabilitiesAndStockholdersEquity_arr = list(map(lambda liabilities,stockholders: liabilities+stockholders,liabilities_arr,stockholders_arr))
			
			return self.LiabilitiesAndStockholdersEquity_arr


		if len(self.LiabilitiesAndStockholdersEquity_key) > 1:
		
			self.LiabilitiesAndStockholdersEquity_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.LiabilitiesAndStockholdersEquity_key)
		
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.LiabilitiesAndStockholdersEquity_key)		
	
		self.LiabilitiesAndStockholdersEquity_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.LiabilitiesAndStockholdersEquity_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')
		
		self.LiabilitiesAndStockholdersEquity_arr = get_arr.get_arr_without_start_date(self.LiabilitiesAndStockholdersEquity_df)
		

		if not self.LiabilitiesAndStockholdersEquity_arr:
			self.forked = True
			liabilities_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=LIABILITIES_KEYS)
			stockholders_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=STOCKHOLDERS_KEYS)
			if isinstance(liabilities_arr,dict):
				self.LiabilitiesAndStockholdersEquity_arr = liabilities_arr
			elif isinstance(stockholders_arr,dict):
				self.LiabilitiesAndStockholdersEquity_arr = stockholders_arr
			else:
				self.LiabilitiesAndStockholdersEquity_arr = list(map(lambda liabilities,stockholders: liabilities+stockholders,liabilities_arr,stockholders_arr))
			
			return self.LiabilitiesAndStockholdersEquity_arr


		return self.LiabilitiesAndStockholdersEquity_arr 
		
		
		

