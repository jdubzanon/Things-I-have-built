import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent) )  

import pandas as pd
import json
import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
import forks.forks as fork
from Ratios import SpecialGrowthCalculation, GetAverages, YOY_growth
import requests
import time

class RetainedEarnings:
	def __init__(self,ticker):
		self.ticker = ticker
		self.RetainedEarnings_key = None
		self.RetainedEarnings_df = None
		self.RetainedEarnings_arr = None
		self.unit = None
		self.forked = False
		
	def get_RetainedEarnings_values(self,company_facts,start_fork=False):
		KEYS = ['Retained Earnings']		
		
		if start_fork == True:
			self.forked = True
			self.RetainedEarnings_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)	
			if isinstance(self.RetainedEarnings_arr,dict):
				return self.RetainedEarnings_arr
			return GetAverages.GetAllAvg(SpecialGrowthCalculation.GrowthCalculate(self.RetainedEarnings_arr))
			
		possible_RetainedEarnings_keys = ['RetainedEarnings','RetainedEarningsAccumulatedDeficit','RetainedEarningsUnappropriated']
		accounting_key = kh.get_accounting_key(company_facts,possible_RetainedEarnings_keys)
		self.RetainedEarnings_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_RetainedEarnings_keys))
		
		if not self.RetainedEarnings_key:
			self.forked = True
			self.RetainedEarnings_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)	
			if isinstance(self.RetainedEarnings_arr,dict):
				return self.RetainedEarnings_arr
			return GetAverages.GetAllAvg(SpecialGrowthCalculation.GrowthCalculate(self.RetainedEarnings_arr))
			
		if len(self.RetainedEarnings_key) > 1:
			self.RetainedEarnings_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.RetainedEarnings_key)
#		print(self.RetainedEarnings_key)#########<--------------
		
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.RetainedEarnings_key)
		self.RetainedEarnings_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.RetainedEarnings_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')
		
		try:
			self.RetainedEarnings_arr = get_arr.get_arr(self.RetainedEarnings_df)
		except AttributeError:
			self.RetainedEarnings_arr = get_arr.get_arr_without_start_date(self.RetainedEarnings_df)
		
		if not self.RetainedEarnings_arr:
			self.forked = True
			self.RetainedEarnings_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=KEYS)	
			if isinstance(self.RetainedEarnings_arr,dict):
				return self.RetainedEarnings_arr
			return GetAverages.GetAllAvg(SpecialGrowthCalculation.GrowthCalculate(self.RetainedEarnings_arr))

		if isinstance(self.RetainedEarnings_arr,dict):
			return self.RetainedEarnings_arr
		if	self.RetainedEarnings_key[0] == possible_RetainedEarnings_keys[1]:
			return GetAverages.GetAllAvg(SpecialGrowthCalculation.GrowthCalculate(self.RetainedEarnings_arr))
		return GetAverages.GetAllAvg(YOY_growth.growth_calculate(self.RetainedEarnings_arr))

		

