import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent) )   


import pandas as pd
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
import forks.forks as fork



class cash:
	def __init__(self,ticker):
		self.ticker = ticker
		self.cash_key = None
		self.cash_df = None
		self.cash_arr = None
		self.unit = None
		self.forked = False
		
	def get_cash_values(self,company_facts,start_fork=False):
		
		if start_fork == True:
			self.forked = True
			self.cash_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=['Cash And Cash Equivalents'])
			if isinstance(self.cash_arr,dict):
				self.cash_arr = {'from cash':'cant make calculations'}
			return self.cash_arr
		
		possible_cash_key = ['CashAndCashEquivalentsAtCarryingValue','CashAndCashEquivalents']
		accounting_key = kh.get_accounting_key(company_facts,possible_cash_key)
		self.cash_key = list(filter(lambda key: key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_cash_key  ))

		if not self.cash_key:
			self.forked = True
			self.cash_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=['Cash And Cash Equivalents'])
			if isinstance(self.cash_arr,dict):
				self.cash_arr = {'from cash':'cant make calculations'}
			return self.cash_arr
		

		if len(self.cash_key) > 1:
			self.cash_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.cash_key)
			
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.cash_key)
		
		self.cash_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.cash_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')
		
		try:
			self.cash_arr = get_arr.get_arr(self.cash_df)

		except AttributeError:
			self.cash_arr = get_arr.get_arr_without_start_date(self.cash_df)
		
		return self.cash_arr





	













