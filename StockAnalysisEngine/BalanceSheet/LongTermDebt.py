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



class LongTermDebt:
	def __init__(self,ticker):
		self.ticker = ticker
		self.LongTermDebt_key = None
		self.unit = None
		self.LongTermDebt_df = None
		self.LongTermDebt_arr = None
		self.forked = False
		
	def get_LongTermDebt_values(self,company_facts,start_fork=False):
		
		KEYS = ['Long Term Debt']
		
		if start_fork == True:
			self.forked = True
			self.LongTermDebt_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.LongTermDebt_arr
					
		possible_LongTermDebt_keys = [
		'LongTermDebtAndCapitalLeaseObligations',
		'LongTermDebtNoncurrent',
		'LongTermDebt',
		'LongTermLoansFromBank'
		]
		
		accounting_key = kh.get_accounting_key(company_facts,possible_LongTermDebt_keys)
		self.LongTermDebt_key = list(filter(lambda key : key.strip()  in company_facts['facts'][accounting_key[0]].keys(), possible_LongTermDebt_keys))
		
		if not self.LongTermDebt_key:
			self.forked = True
			self.LongTermDebt_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.LongTermDebt_arr
		
		if len(self.LongTermDebt_key) > 1:
			self.LongTermDebt_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.LongTermDebt_key)
		
		if not self.LongTermDebt_key:
			self.forked = True
			self.LongTermDebt_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.LongTermDebt_arr
		
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.LongTermDebt_key)
		
		self.LongTermDebt_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.LongTermDebt_key[0]]['units'][self.unit[0]]).drop_duplicates(subset='end')

		self.LongTermDebt_arr = get_arr.get_arr_without_start_date(self.LongTermDebt_df)
		
		if not self.LongTermDebt_arr:
			self.forked = True
			self.LongTermDebt_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.LongTermDebt_arr
		
		return self.LongTermDebt_arr		
		





		


