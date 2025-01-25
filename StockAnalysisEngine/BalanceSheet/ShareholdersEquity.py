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

class ShareholdersEquity:
	def __init__(self,ticker):
	
		self.ticker = ticker
		self.SharHolEq_key = None
		self.SharHolEq_df = None
		self.SharHolEq_arr = None
		self.SharHolEq_dict = dict()

		self.TreasuryStock_key = None
		self.TreasuryStock_df = None
		self.TreasuryStock_arr = None
					
		
		self.SharHolEq_unit = None
		self.TreasuryStock_unit = None
	
		self.forked = False
	
	def get_ShareholdersEquity_values(self,company_facts,forking=False,start_fork=False):
		
		KEYS = ['Stockholders Equity']
		
		if start_fork == True:
			self.forked = True
			self.SharHolEq_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.SharHolEq_arr
		
		possible_SharHolEq_keys = [
		'StockholdersEquity',
		'Equity',
		'StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest',
		'StockholdersEquityBeforeTreasuryStock'
		]
	
		accounting_key = kh.get_accounting_key(company_facts,possible_SharHolEq_keys)
		self.SharHolEq_key = list(filter(lambda key: key.strip() in company_facts['facts'][accounting_key[0]].keys(),possible_SharHolEq_keys   ))
			
		if not self.SharHolEq_key:
			self.forked = True
			self.SharHolEq_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.SharHolEq_arr
				
		if len(self.SharHolEq_key) > 1: 
			self.SharHolEq_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.SharHolEq_key) 

		self.SharHolEq_unit = kh.set_unit_key(company_facts,accounting_key,self.SharHolEq_key)
		self.SharHolEq_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.SharHolEq_key[0]]['units'][self.SharHolEq_unit[0]] ).drop_duplicates(subset='end')
		self.SharHolEq_arr = get_arr.get_arr_without_start_date(self.SharHolEq_df)
		
		if not self.SharHolEq_arr:
			self.forked = True
			self.SharHolEq_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.SharHolEq_arr
		
		return self.SharHolEq_arr 
		
		


