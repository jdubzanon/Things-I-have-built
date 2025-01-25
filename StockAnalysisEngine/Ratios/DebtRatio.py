

import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
from collections import namedtuple





def GetRatio(total_liabilities_class,total_assets_class,company_facts):
	FAILED_TO_GET_DATA = {'from tot_lia to tot_asset ratio':'cant make calculations'}

	if any([isinstance(total_liabilities_class.TotalLiabilities_arr,dict),
			isinstance(total_liabilities_class.CurrentLiabilities_arr,dict),   
			isinstance(total_liabilities_class.NonCurrentLiabilities_arr,dict), 
			isinstance(total_assets_class.TotalAssets_arr,dict),
			total_liabilities_class.forked == True,
			total_assets_class.forked == True]):
		
		from BalanceSheet.TotalAssets import TotalAssets
		from BalanceSheet.TotalLiabilities import TotalLiabilities
		
		ta = TotalAssets(total_assets_class.ticker)
		ta_values = ta.get_TotalAsset_values(company_facts,start_fork=True)
		
		tl = TotalLiabilities(total_liabilities_class.ticker)
		tl_values = tl.get_TotalLiabilities_values(company_facts,start_fork=True)
		
		if any([isinstance(ta_values,dict),isinstance(tl_values,dict)]):
			return FAILED_TO_GET_DATA
		
		debt_to_asset_ratio = list(map(lambda liabilities,assets: round((liabilities/assets),ndigits=2),tl_values,filter(lambda values:values != 0,ta_values ) ))
		
		return debt_to_asset_ratio
		
	if not total_liabilities_class.TotalLiabilities_key:
		
		longest_list_length = max([len(total_liabilities_class.CurrentLiabilities_arr),len(total_liabilities_class.NonCurrentLiabilities_arr),len(total_assets_class.TotalAssets_arr)   ])
		
		if len(total_liabilities_class.CurrentLiabilities_arr) >= longest_list_length:
			master_df = total_liabilities_class.CurrentLiabilities_df
			slave_df = total_liabilities_class.NonCurrentLiabilities_df
			slave2_df = total_assets_class.TotalAssets_df
			
		elif len(total_liabilities_class.NonCurrentLiabilities_arr) >= longest_list_length:
			master_df = total_liabilities_class.NonCurrentLiabilities_df
			slave_df = total_liabilities_class.CurrentLiabilities_df
			slave2_df = total_assets_class.TotalAssets_df
			
		else:
			master_df =  total_assets_class.TotalAssets_df
			slave_df = total_liabilities_class.CurrentLiabilities_df
			slave2_df = total_liabilities_class.NonCurrentLiabilities_df
			
		returned_list = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,df_slave2=slave2_df,isolate=True,returning_lists=True)
		
		#stop and check
		if any([not returned_list[0], not returned_list[1], not returned_list[2] ]):
			from BalanceSheet.TotalAssets import TotalAssets
			from BalanceSheet.TotalLiabilities import TotalLiabilities
			
			ta = TotalAssets(total_assets_class.ticker)
			ta_values = ta.get_TotalAsset_values(company_facts,start_fork=True)
			
			tl = TotalLiabilities(total_liabilities_class.ticker)
			tl_values = tl.get_TotalLiabilities_values(company_facts,start_fork=True)
			
			if any([isinstance(ta_values,dict),isinstance(tl_values,dict)]):
				return FAILED_TO_GET_DATA
			
			debt_to_asset_ratio = map(lambda liabilities,assets: round((liabilities/assets),ndigits=2),tl_values,filter(lambda values:values != 0,ta_values ) )
			
			return list(debt_to_asset_ratio)
		
		
		#continue after check		
		current = namedtuple('current_liabilities','values')
		NonCurrent = namedtuple('current_liabilities','values')
		assets = namedtuple('assets','values')
		
		current.values = total_liabilities_class.CurrentLiabilities_arr
		NonCurrent.values = total_liabilities_class.NonCurrentLiabilities_arr
		assets.values = total_assets_class.TotalAssets_arr
		
		for lists in returned_list:
			if set(lists).intersection(set(current.values)):
				current.values = lists
			elif set(lists).intersection(set(NonCurrent.values)):
				NonCurrent.values = lists
			else:
				assets.values = lists
		
		total_liabilities = map(lambda current,Noncurrent: current+Noncurrent,NonCurrent.values,current.values   )
		
		assets_to_liabilities_ratio = list(map(lambda liabilites,assets: round( (liabilites / assets)  ,ndigits=2), total_liabilities,assets.values  ))
		
	else:
		longest_list_length = max([len(total_liabilities_class.TotalLiabilities_arr),  len(total_assets_class.TotalAssets_arr)    ])
		
		if len(total_assets_class.TotalAssets_arr) >= longest_list_length:
			master_df = total_assets_class.TotalAssets_df
			slave_df = total_liabilities_class.TotalLiabilities_df
		else:
			master_df = total_liabilities_class.TotalLiabilities_df
			slave_df = total_assets_class.TotalAssets_df
			
		total_liabilities = namedtuple('total_liabilities','values')
		total_assets = namedtuple('total_assets','values')
		
		total_liabilities.values = total_liabilities_class.TotalLiabilities_arr
		total_assets.values = total_assets_class.TotalAssets_arr
		
		
		returned_list = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,returning_lists=True,isolate=True)
		
		#stop and check
		if any([ not returned_list[0], not returned_list[1]  ]):
			from BalanceSheet.TotalAssets import TotalAssets
			from BalanceSheet.TotalLiabilities import TotalLiabilities
			
			ta = TotalAssets(total_assets_class.ticker)
			ta_values = ta.get_TotalAsset_values(company_facts,start_fork=True)
			
			tl = TotalLiabilities(total_liabilities_class.ticker)
			tl_values = tl.get_TotalLiabilities_values(company_facts,start_fork=True)
			
			if any([isinstance(ta_values,dict),isinstance(tl_values,dict)]):
				return FAILED_TO_GET_DATA
			
			debt_to_asset_ratio = map(lambda liabilities,assets: round((liabilities/assets),ndigits=2),tl_values,filter(lambda values:values != 0,ta_values ) )
			
			return list(debt_to_asset_ratio)

		#continue after check
		for lists in returned_list:
			if set(lists).intersection(set(total_liabilities.values)):
				total_liabilities.values = lists
			else:
				total_assets.values = lists
				
		assets_to_liabilities_ratio = list(map(lambda liabilites,assets:round((liabilites / assets)  ,ndigits=2) , total_liabilities.values,total_assets.values    ))
			
	return np.flip(assets_to_liabilities_ratio)




