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



class OpIncome:
	def __init__(self,ticker):
		self.ticker = ticker
		self.OpIncome_key = None
		self.OpIncome_df = None
		self.OpIncome_arr = None
		self.unit = None
		self.forked = False
		self.possible_OpIncome_keys = None #special case attribute so i use indexing to check key in intexp_to_opinc ratio function
		
	def get_OpIncome_values(self,company_facts,start_fork=False):
		
		KEYS = ['Operating Income','Operating Revenue']
		
		if start_fork == True:
			self.forked = True
			self.OpIncome_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.OpIncome_arr
		
		
		self.possible_OpIncome_keys = [
		'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest',
		'ProfitLossFromOperatingActivites',
		'RevenueAndOperatingIncome',
		'OperatingIncomeLoss',
		'ProfitLossFromOperatingActivities'
		]
		
		accounting_key = kh.get_accounting_key(company_facts,self.possible_OpIncome_keys)
		self.OpIncome_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(),self. possible_OpIncome_keys))
			
		if not self.OpIncome_key:
			self.forked = True
			self.OpIncome_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.OpIncome_arr
						
		if len(self.OpIncome_key) > 1:
			self.OpIncome_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.OpIncome_key)
		
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.OpIncome_key)
		self.OpIncome_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.OpIncome_key[0]]['units'][self.unit[0]]).drop_duplicates(subset='end')
		self.OpIncome_arr = get_arr.get_arr(self.OpIncome_df)
			
		if not self.OpIncome_arr:
			self.forked = True
			self.OpIncome_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.OpIncome_arr

		return self.OpIncome_arr	
		
		


