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


class receivables:
	def __init__(self,ticker):
		self.ticker = ticker
		self.receivables_key = None
		self.receivables_df = None
		self.receivables_arr = None
		self.unit = None
		self.forked = False
		
		self.possible_receivables_keys = None #<--- special case
	
	def get_receivables_values(self,company_facts,start_fork=False):
		
		KEYS = ['Receivables']
		
		if start_fork == True:
			self.forked = True
			self.receivables_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)			
			return self.receivables_arr


		self.possible_receivables_keys = [
		'AccountsReceivableNetCurrent',#
		'AccountsReceivableNet',#
		'AccountsNotesAndLoansReceivableNetCurrent', #
		'AccountsReceivableGrossCurrent', #
		'CurrentTradeReceivables',#
		'ReceivablesNetCurrent',
		'TradeAndOtherCurrentReceivables',#
		'TradeAndOtherCurrentReceivables',#
		'PremiumsReceivableAtCarryingValue', #
		
		]
		
		accounting_key = kh.get_accounting_key(company_facts,self.possible_receivables_keys)
		
		self.receivables_key = list(filter(lambda key: key.strip() in company_facts['facts'][accounting_key[0]].keys(), self.possible_receivables_keys))
		
		if not self.receivables_key:
			self.forked = True
			self.receivables_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.receivables_arr
		
		if len(self.receivables_key) > 1:
			self.receivables_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.receivables_key)
			
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.receivables_key)
		
		self.receivables_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.receivables_key[0]]['units'][self.unit[0]]  )
		
		try:
			self.receivables_arr = get_arr.get_arr(self.receivables_df)

		except AttributeError:
			self.receivables_arr = get_arr.get_arr_without_start_date(self.receivables_df)		

		if not self.receivables_arr:
			self.forked = True
			self.receivables_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)
			return self.receivables_arr
			
			
		return self.receivables_arr





