import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent) )  

import time

import pandas as pd
import json
import numpy as np
import requests
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
import forks.forks as fork




class Cogs:
	def __init__(self,ticker,fork=False):
		self.ticker = ticker
		self.cogs_key = None
		self.unit = None
		self.cogs_df = None
		self.cogs_arr = None
		self.forked = False
		
	def get_cog_values(self,company_facts,start_fork=False):
		KEYS = ['Cost Of Revenue']
		
		if start_fork == True:
			self.forked = True
			self.cogs_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.cogs_arr
		
		possible_cogs_keys = [ 
		'CostOfGoodsSoldExcludingDepreciationDepletionAndAmortization',
		'CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization',
		'CostOfGoodsAndServicesSold',
		'CostOfGoodsSold',
		'CostOfRevenue',
		'CostOfSales'  
		]
		accounting_key = kh.get_accounting_key(company_facts,possible_cogs_keys)
		self.cogs_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_cogs_keys))
			
		if not self.cogs_key:
			possible_cogs_keys = ['CostsAndExpenses', 'NoninterestExpense']
			self.cogs_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_cogs_keys))
		
		if not self.cogs_key: 
			self.forked = True
			self.cogs_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.cogs_arr
					
		if len(self.cogs_key) > 1:
			self.cogs_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.cogs_key)
			
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.cogs_key)
		self.cogs_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.cogs_key[0]]['units'][self.unit[0]]).drop_duplicates(subset='end')
		self.cogs_arr = get_arr.get_arr(self.cogs_df)	
		
		if not self.cogs_arr:
			self.forked = True
			self.cogs_arr = fork.fork(ticker_id=self.ticker,statement='income',keys=KEYS)
			return self.cogs_arr		
		
		return self.cogs_arr
		

