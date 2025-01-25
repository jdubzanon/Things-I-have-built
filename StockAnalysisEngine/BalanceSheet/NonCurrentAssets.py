import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent) )  

import pandas as pd
import json
import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
import yfinance as yf

import requests
import time


class NonCurrentAssets:
	def __init__(self,ticker):
		self.ticker = ticker
		self.NonCurrentAssets_key = None
		self.NonCurrentAssets_df = None
		self.NonCurrentAssets_arr = None
		self.unit = None
		self.forked = False
		
	def get_NonCurrentAsset_values(self,company_facts,start_fork=True):
	
		if start_fork == True:
			self.forked = True
			ticker = yf.Ticker(self.ticker)			
			balance_sheet = ticker.balance_sheet
			try:
				nca = balance_sheet.loc['Total Non Current Assets']
				self.NonCurrentAssets_arr = list(map(lambda values: int(values), nca[pd.notna(nca)].values ))     
				if not self.NonCurrentAssets_arr:
					self.NonCurrentAssets_arr = {'from non current assets':"cant make calculation"}
			except:
				self.NonCurrentAssets_arr = {'from non current assets':'cant make calculation'}	
				
			return self.NonCurrentAssets_arr							

		possible_NCA_keys = ['NoncurrentAssets','AssetsNoncurrent']
		accounting_key = kh.get_accounting_key(company_facts,possible_NCA_keys)
		self.NonCurrentAssets_key = list(filter(lambda key: key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_NCA_keys  ))
		
		if not self.NonCurrentAssets_key:
			self.forked = True
			ticker = yf.Ticker(self.ticker)			
			balance_sheet = ticker.balance_sheet
			try:
				nca = balance_sheet.loc['Total Non Current Assets']
				self.NonCurrentAssets_arr = list(map(lambda values: int(values), nca[pd.notna(nca)].values ))     
				if not self.NonCurrentAssets_arr:
					self.NonCurrentAssets_arr = {'from non current':'cant make calculation'}
			except:
				self.NonCurrentAssets_arr = {'from non current assets':'cant make calculation'}	
				
			return self.NonCurrentAssets_arr				
						
		if len(self.NonCurrentAssets_key) > 1:
			self.NonCurrentAssets_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.NonCurrentAssets_key)
		
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.NonCurrentAssets_key)

		self.NonCurrentAssets_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.NonCurrentAssets_key[0]]['units'][self.unit[0]] ).drop_duplicates(subset='end')	
		
		try:
			self.NonCurrentAssets_arr = get_arr.get_arr(self.NonCurrentAssets_df)	
		
		except AttributeError:
			self.NonCurrentAssets_arr = get_arr.get_arr_without_start_date(self.NonCurrentAssets_df)
			

		return self.NonCurrentAssets_arr


