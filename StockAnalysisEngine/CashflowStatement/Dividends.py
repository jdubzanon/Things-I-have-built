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


class Dividends:
	def __init__(self,ticker):
		self.ticker = ticker
		self.dividends_key = None
		self.dividends_df = None
		self.dividends_arr = None
		self.unit = None
		self.forked = False
	
	def get_dividend_values(self,company_facts,start_fork=False):
		
		if start_fork == True:
			self.forked = True
			self.dividends_arr = fork.fork(ticker_id=self.ticker,statement='cashflow',keys=['Cash Dividends Paid'])
			if isinstance(self.dividends_arr,dict):
				self.dividends_arr = [0,0,0,0]
			return self.dividends_arr	
				
		
		possible_dividends_keys = [
		'PaymentsOfDividends',
		'PaymentsOfDividendsCommonStock',
		'PaymentsOfOrdinaryDividends',
		'DividendsPaidOrdinaryShares',
		'DividendsPaid']
		
		accounting_key = kh.get_accounting_key(company_facts,possible_dividends_keys)

		if len(accounting_key) > 1:
			self.dividends_key = kh.get_ReportingKey_with_two_accounting_keys(company_facts,accounting_key,possible_dividends_keys)

		else:
			self.dividends_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_dividends_keys  ))			
			
#		return self.dividends_key
		
		if not self.dividends_key:
			self.forked = True
			self.dividends_arr = fork.fork(ticker_id=self.ticker,statement='cashflow',keys=['Cash Dividends Paid'])
			if isinstance(self.dividends_arr,dict):
				self.dividends_arr = [0,0,0,0]
			return self.dividends_arr	
				
		if len(self.dividends_key) > 1:
			self.dividends_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.dividends_key)
			
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.dividends_key)
		
		self.dividends_df = pd.DataFrame( company_facts['facts'][accounting_key[0]][self.dividends_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')
		try:
			self.dividends_arr = get_arr.get_arr(self.dividends_df)
			
		except AttributeError:
			self.dividends_arr = get_arr.get_arr_without_start_date(self.dividends_df)
		
		if not self.dividends_arr:
			self.forked = True
			self.dividends_arr = fork.fork(ticker_id=self.ticker,statement='cashflow',keys=['Cash Dividends Paid'])
			if isinstance(self.dividends_arr,dict):
				self.dividends_arr = [0,0,0,0]
			return self.dividends_arr	
		return self.dividends_arr	
	#not all companies pay dividends need to figure this out
	#dividends can also be calculated net income - net change in retained earnings
	#this module is to calculate return on capital if there is no dividends you can omit it because its just part of an equation that may or may not be subtracted 
	#in calculation if self.dividends_arr is None then omit the dividends in calculation
	#usin module for return on capital (net income - dividend)/(debt+equity)



