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


class OpExpense:
	def __init__(self,ticker):
		self.ticker = ticker
		self.OpExpense_key = None
		self.unit = None
		self.OpExpense_df = None
		self.OpExpense_arr = None
		self.forked = False
		
		
	def get_OpExpense_values(self,company_facts,start_fork=False):
		KEYS = ['Operating Expense']
		
		if start_fork == True:
			self.forked = True
			self.OpExpense_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.OpExpense_arr
			
		possible_OpExpense_keys = ['OperatingExpenses','CostsAndExpenses','NoninterestExpense','OperatingExpenseExcludingCostOfSales']
		accounting_key = kh.get_accounting_key(company_facts,possible_OpExpense_keys)
		self.OpExpense_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_OpExpense_keys))
		
		if not self.OpExpense_key:
			self.forked = True
			self.OpExpense_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.OpExpense_arr
			
		if len(self.OpExpense_key) > 1:
			if all([ 'OperatingExpenses' in self.OpExpense_key, 'CostsAndExpenses' in self.OpExpense_key ]):
				self.OpExpense_key = ['CostsAndExpenses']
			
			else:
				other_keys = [key for key in self.OpExpense_key if all([ key != 'OperatingExpenses', key != 'CostsAndExpenses'   ])]	
				self.OpExpense_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,other_keys)
						
		
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.OpExpense_key)
		
		self.OpExpense_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.OpExpense_key[0]]['units'][self.unit[0]]).drop_duplicates(subset='end')
		
		self.OpExpense_arr = get_arr.get_arr(self.OpExpense_df)
			
		if not self.OpExpense_arr:
			self.forked = True
			self.OpExpense_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.OpExpense_arr		

		return self.OpExpense_arr	
			
			
			

