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




from pathlib import Path as path
from pathlib import PurePath as ppath
import os
import json



class TaxesPaid:
	def __init__(self,ticker):
		self.ticker = ticker
		self.TaxesPaid_key = None
		self.TaxesPaid_df = None
		self.TaxesPaid_arr = None
		self.unit = None
		self.forked = False
		
	def get_TaxesPaid_values(self,company_facts,start_fork=False):
		KEYS = ['Tax Provision']		
		
		if start_fork == True:
			self.forked = True
			self.TaxesPaid_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)	
			return self.TaxesPaid_arr
		
		possible_TaxesPaid_keys = [
		'IncomeTaxesPaid',
		'IncomeTaxesPaidNet',
		'IncomeTaxExpenseContinuingOperations',
		'ResultsOfOperationsIncomeTaxExpense'
		]
		
		accounting_key = kh.get_accounting_key(company_facts,possible_TaxesPaid_keys)
		self.TaxesPaid_key = list(filter(lambda key: key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_TaxesPaid_keys ))
		
		if not self.TaxesPaid_key:
			self.forked = True
			self.TaxesPaid_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)	
			return self.TaxesPaid_arr
			
		if len(self.TaxesPaid_key) > 1:
			self.TaxesPaid_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.TaxesPaid_key)
			
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.TaxesPaid_key)
		self.TaxesPaid_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.TaxesPaid_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')
		
		try:
			self.TaxesPaid_arr = get_arr.get_arr(self.TaxesPaid_df)
		
		except AttributeError:
			self.TaxesPaid_arr = get_arr.get_arr_without_start_date(self.TaxesPaid_df)
			
		if not self.TaxesPaid_arr:
			self.forked = True
			self.TaxesPaid_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)	
			return self.TaxesPaid_arr

		
		return self.TaxesPaid_arr



