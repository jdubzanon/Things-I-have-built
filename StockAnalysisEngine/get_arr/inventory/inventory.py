


import pandas as pd
import json
import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr

import requests
import time


class inventory:
	def __init__(self,ticker):
		self.ticker = ticker
		self.inventory_key = None
		self.inventory_df = None
		self.inventory_arr = None
		self.unit = None
		self.forked = False
		
	def get_inventory_values(self,company_facts,start_fork=False):
		
		#need to create a fork using yfinance
		
		#NEED TO CHECK WHAT INDUSTRY THE STOCK IS IN USING yfinance or someother api
		#if reit
		
		  # ----> try using theses reit RealEstatePropertyNet RealEstatePropertyAtCarryingValues pld,amt,eqix
		possible_inventory_keys = ['InventoryNet','Inventories','InventoryFinishedGoods','InventoryGross']

		accounting_key = kh.get_accounting_key(company_facts,possible_inventory_keys)

		self.inventory_key = list(filter(lambda key : key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_inventory_keys  ))			
		
		if any([start_fork == True, not self.inventory_key]):
			#any then create fork
			self.forked = True
			self.inventory_arr =  {'from_inventory_module': 'need to create fork'}
			return self.inventory_arr
			
		if len(self.inventory_key) > 1:
		
			self.inventory_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.inventory_key)			
			
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.inventory_key)
		
		self.inventory_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.inventory_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')

		try:
			self.inventory_arr = get_arr.get_arr(self.inventory_df)
		except AttributeError:
			self.inventory_arr = get_arr.get_arr_without_start_date(self.inventory_df)
		
		if all([start_fork is False, not self.inventory_key]):
			self.forked = True
			self.inventory_arr = {'from inventory mod': 'need to create arr fork'}
			

		return self.inventory_arr

		





