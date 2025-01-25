import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent) )  

import pandas as pd
import json
import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
import yfinance as yf
import forks.forks as fork
import requests
import time


class capex:
	def __init__(self,ticker):
		self.ticker = ticker
		self.capex_key = None
		self.capex_df = None
		self.capex_arr = None
		self.unit = None
		self.forked = False
		
	def get_capex_values(self,company_facts,start_fork=False):
		KEYS = ['Net PPE Purchase And Sale','Capital Expenditure','Capital Expenditure Reported']
		
		if start_fork == True: #cashflow strategy changes based on forking
			self.forked = True
			self.capex_arr = fork.fork(ticker_id=self.ticker,statement='cashflow',keys=KEYS)
			return self.capex_arr
		
		possible_capex_keys = [
		'PurchaseOfPropertyPlantAndEquipmentIntangibleAssetsOtherThanGoodwillInvestmentPropertyAndOtherNoncurrentAssets',
		'PurchaseOfOtherLongtermAssetsClassifiedAsInvestingActivities',
		'PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities',
		'PaymentsToAcquirePropertyPlantAndEquipment',
		'PaymentsToAcquireOtherPropertyPlantAndEquipment'
	
		]
		accounting_key = kh.get_accounting_key(company_facts,possible_capex_keys)

		self.capex_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_capex_keys  ))		
		
		if not self.capex_key:
			possible_capex_keys = ['PropertyPlantAndEquipment','PropertyPlantAndEquipmentNet','PropertyPlantAndEquipmentGross']
			accounting_key = kh.get_accounting_key(company_facts,possible_capex_keys)
			self.capex_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_capex_keys  ))		
			
			
		if not self.capex_key:
			self.forked = True
			self.capex_arr = fork.fork(ticker_id=self.ticker,statement='cashflow',keys=KEYS)
			return self.capex_arr
				
		if len(self.capex_key) > 1:
			self.capex_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.capex_key)

		self.unit = kh.set_unit_key(company_facts,accounting_key,self.capex_key)

		self.capex_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.capex_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')
		
		try:
			self.capex_arr = get_arr.get_arr(self.capex_df)
			
		except AttributeError:
			self.capex_arr = get_arr.get_arr_without_start_date(self.capex_df)
			
		if not self.capex_arr:
			self.forked = True
			self.capex_arr = fork.fork(ticker_id=self.ticker,statement='cashflow',keys=KEYS)
			return self.capex_arr
		
		return self.capex_arr



