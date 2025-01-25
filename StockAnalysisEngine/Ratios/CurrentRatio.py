


import pandas as pd
import json
import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
from collections import namedtuple



from pathlib import Path as path
from pathlib import PurePath as ppath
import os
import json
import requests
import time



def GetRatio(current_assets_class,current_liabilities_class,company_facts):
	FAILED_TO_GET_DATA = {'from current_assets_current_liabilities_ratio':'cant make calculation'}
	
	if any([isinstance(current_assets_class.CurrentAssets_arr,dict), 
			isinstance(current_liabilities_class.CurrentLiabilities_arr,dict),
			current_assets_class.forked == True,
			current_liabilities_class.forked == True   ]):
		
		from BalanceSheet.CurrentLiabilities import CurrentLiabilities
		from BalanceSheet.CurrentAssets import CurrentAssets

		ca = CurrentAssets(current_assets_class.ticker)
		ca_vals = ca.get_CurrentAsset_values(company_facts,start_fork=True)		
		
		cl = CurrentLiabilities(current_assets_class.ticker) 
		cl_vals = cl.get_CurrentLiabilities_values(company_facts,start_fork=True)				
		
		if any([isinstance(ca_vals,dict),isinstance(cl_vals,dict) ]):
			return FAILED_TO_GET_DATA
		
		try:
			return list(map(lambda current_assets,current_liabilities:  round((current_assets/current_liabilities),ndigits=2), ca_vals,cl_vals  ))
		
		except ZeroDivisionError:
			ca_vals = list(filter(lambda values: values != 0, ca_vals))
			cl_vals = list(filter(lambda values: values != 0, cl_vals))
			
			if any([not ca_vals, not cl_vals]):
				return FAILED_TO_GET_DATA
			
			return list(map(lambda current_assets,current_liabilities:  round((current_assets/current_liabilities),ndigits=2), ca_vals,cl_vals  ))
		
	#if none were forked 
	longest_list_length = max([len(current_assets_class.CurrentAssets_arr), len(current_liabilities_class.CurrentLiabilities_arr)   ])
	
	if len(current_assets_class.CurrentAssets_arr) >= longest_list_length:
		master_df = current_assets_class.CurrentAssets_df
		slave_df = current_liabilities_class.CurrentLiabilities_df
	
	else:	
		master_df = current_liabilities_class.CurrentLiabilities_df
		slave_df = current_assets_class.CurrentAssets_df
		
	assets = namedtuple('assets','values')
	liabilites = namedtuple('liabilites','values')
	
	assets.values = current_assets_class.CurrentAssets_arr
	liabilites.values = current_liabilities_class.CurrentLiabilities_arr
	
	returned_lists = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,isolate=True,returning_lists=True)
	#stop here and check
	if any([not returned_lists[0], not returned_lists[1]]): #if dates dont line up fork both 
		from BalanceSheet.CurrentLiabilities import CurrentLiabilities
		from BalanceSheet.CurrentAssets import CurrentAssets

		ca = CurrentAssets(current_assets_class.ticker)
		ca_vals = ca.get_CurrentAsset_values(company_facts,start_fork=True)		
		
		cl = CurrentLiabilities(current_assets_class.ticker) 
		cl_vals = cl.get_CurrentLiabilities_values(company_facts,start_fork=True)				
		
		if any([isinstance(ca_vals,dict),isinstance(cl_vals,dict) ]):
			return FAILED_TO_GET_DATA
		
		try:
			return list(map(lambda current_assets,current_liabilities:  round((current_assets/current_liabilities),ndigits=2), ca_vals,cl_vals  ))
		
		except ZeroDivisionError:
			ca_vals = list(filter(lambda values: values != 0, ca_vals))
			cl_vals = list(filter(lambda values: values != 0, cl_vals))
			
			if any([not ca_vals, not cl_vals]):
				return FAILED_TO_GET_DATA
			
			return list(map(lambda current_assets,current_liabilities:  round((current_assets/current_liabilities),ndigits=2), ca_vals,cl_vals  ))
	#continue here			
	for lists in returned_lists:
		if set(lists).intersection(set(assets.values)):
			assets.values = lists
		else:
			liabilites.values = lists

	ratio = list(map(lambda asset_vals,liabilite_vals: round(asset_vals/liabilite_vals,ndigits=2), assets.values,liabilites.values  ))
	
	return np.flip(ratio)
	
	
	
	
	











