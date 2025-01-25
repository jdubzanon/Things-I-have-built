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


class SharesOutstanding:
	def __init__(self,ticker):
		self.ticker = ticker
		self.SharesOutstanding_key = None
		self.SharesOutstanding_df = None
		self.SharesOutstanding_arr = None
		self.unit = None
		self.forked = False
		
	def get_SharesOutstanding_values(self,company_facts,start_fork=False):
		KEYS = ['Ordinary Shares Number']
		
		if start_fork == True:
			self.forked = True
			self.SharesOutstanding_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.SharesOutstanding_arr
			
		possible_so_keys = ['WeightedAverageNumberOfDilutedSharesOutstanding',
		'WeightedAverageNumberOfSharesOutstandingBasic',
		'WeightedAverageShares',
		'AdjustedWeightedAverageShares',
		'NumberOfSharesOutstanding',
		'CommonStockSharesOutstanding']
		
		accounting_key = kh.get_accounting_key(company_facts,possible_so_keys)
		self.SharesOutstanding_key = list(filter(lambda key: key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_so_keys))
		
		if not self.SharesOutstanding_key:
			self.forked = True
			self.SharesOutstanding_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.SharesOutstanding_arr
		
		if len(self.SharesOutstanding_key) > 1:
			self.SharesOutstanding_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.SharesOutstanding_key)
		
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.SharesOutstanding_key)
		self.SharesOutstanding_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.SharesOutstanding_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')
		
		try:
			self.SharesOutstanding_arr = get_arr.get_arr(self.SharesOutstanding_df)

		except AttributeError:
			self.SharesOutstanding_arr = get_arr.get_arr_without_start_date(self.SharesOutstanding_df)
			
		if not self.SharesOutstanding_key:
			self.forked = True
			self.SharesOutstanding_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.SharesOutstanding_arr			
		
		return self.SharesOutstanding_arr


