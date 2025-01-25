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

class EarningsPerShare:
	def __init__(self,ticker):
		self.ticker = ticker
		self.eps_key = None
		self.eps_df = None
		self.eps_arr = None
		self.unit = None
		self.forked = False
	
	def get_eps_values(self,company_facts,start_fork=False):
	
		if start_fork == True:
			self.forked = True
			self.eps_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=['Diluted EPS'],keep_float=True)
			return self.eps_arr
			
		possible_eps_keys = ['BasicEarningsLossPerShare','DilutedEarningsLossPerShare','EarningsPerShareDiluted','EarningsPerShareBasic']
		accounting_key = kh.get_accounting_key(company_facts,possible_eps_keys)
		self.eps_key = list(filter(lambda key: key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_eps_keys  ))
		
		if not self.eps_key:
			self.forked = True
			self.eps_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=['Diluted EPS'],keep_float=True)
			return self.eps_arr
			
		if len(self.eps_key) > 1:
			self.eps_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.eps_key)
			
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.eps_key)
		
		self.eps_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.eps_key[0]]['units'][self.unit[0]] ).drop_duplicates(subset='end')
		
		try:
			self.eps_arr = get_arr.get_arr(self.eps_df)
		except AttributeError:
			self.eps_arr = get_arr.get_arr_without_start_date(self.eps_df)
		
		if not self.eps_arr:
			self.forked = True
			self.eps_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=['Diluted EPS'],keep_float=True)
			
		return self.eps_arr



