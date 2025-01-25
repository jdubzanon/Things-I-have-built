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



