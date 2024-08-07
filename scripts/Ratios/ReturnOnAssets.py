import sys
##for gedit 
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/webpage/bin')
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/scripts')
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/webpage/lib/python3.10/site-packages')
sys.path.append('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts')
sys.path.append('/home/jdubzanon/hdd/envornments/webpage/lib/python3.10/site-packages')

import numpy 
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
from collections import namedtuple



def GetRatio(NetInc_class,total_assets_class,company_facts):
	#net income / total_assets return on assets
	FAILED_TO_GET_DATA = {'from return_on_assets':'cant make calculations'}
	
	if any([isinstance(NetInc_class.NetProfit_arr,dict ), 
			isinstance(total_assets_class.TotalAssets_arr,dict),	
	    	NetInc_class.forked == True,
	    	total_assets_class.forked == True]):
		from BalanceSheet.TotalAssets import TotalAssets
		from IncomeStatement.NetProfit import NetProfit
		
		ta = TotalAssets(total_assets_class.ticker)
		ta_values = list(filter(lambda values: values != 0, ta.get_TotalAsset_values(company_facts,start_fork=True)))   
		
		np = NetProfit(NetInc_class.ticker)
		np_values = np.get_NetProfit_values(company_facts,start_fork=True)
		
		if any([ isinstance(ta_values,dict),isinstance(np_values,dict),not ta_values ]):
			return FAILED_TO_GET_DATA
		
		return_on_assets = map(lambda net_profit_vals, assets_vals: round((net_profit_vals / assets_vals)*100,ndigits=2), np_values,ta_values)
		
		return list(return_on_assets)
			
	longest_lists_length = max([len(NetInc_class.NetProfit_arr), len(total_assets_class.TotalAssets_arr)  ])	
	
	if len(NetInc_class.NetProfit_arr) >= longest_lists_length:
		master_df = NetInc_class.NetProft_df
		slave_df = total_assets_class.TotalAssets_df
	else:
		master_df = total_assets_class.TotalAssets_df
		slave_df = NetInc_class.NetProft_df
		
	net_income = namedtuple('net_income','values')
	assets = namedtuple('assets','values')
	
	net_income.values = NetInc_class.NetProfit_arr
	assets.values = total_assets_class.TotalAssets_arr
	
	returned_lists = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,isolate=True,returning_lists=True)
	
	#stop and check
	if any([ not returned_lists[0],not returned_lists[1] ]):
		from BalanceSheet.TotalAssets import TotalAssets
		from IncomeStatement.NetProfit import NetProfit
		
		ta = TotalAssets(total_assets_class.ticker)
		ta_values = list(filter(lambda values: values != 0, ta.get_TotalAsset_values(company_facts,start_fork=True)))   
		
		np = NetProfit(NetInc_class.ticker)
		np_values = np.get_NetProfit_values(company_facts,start_fork=True)
		
		if any([ isinstance(ta_values,dict),isinstance(np_values,dict),not ta_values ]):
			return FAILED_TO_GET_DATA
		
		return_on_assets = map(lambda net_profit_vals, assets_vals: round((net_profit_vals / assets_vals)*100,ndigits=2), np_values,ta_values)
		
		return list(return_on_assets)
	#continue after check
	for lists in returned_lists:
		if set(lists).intersection(set(net_income.values)):
			net_income.values = numpy.flip(lists)
		else:
			assets.values = numpy.flip(lists)
			
	return_on_assets_values = list(map(lambda net_income,assets: round((net_income / assets),ndigits=2), net_income.values,assets.values    ))		

	return return_on_assets_values





#from BalanceSheet.TotalAssets import TotalAssets
#from IncomeStatement.NetProfit import NetProfit


#from pathlib import Path as path
#from pathlib import PurePath as ppath
#import os
#import json

#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#single_file = 'HON.json'
#final_path = dir_path / single_file
#ticker = single_file[0:-5]
#with open(final_path,'r') as fr:
#	local_file = fr.read()
#	local_json = json.loads(local_file)
#	rev = NetProfit(ticker)
#	rev_v = rev.get_NetProfit_values(local_json)
#	print(rev_v)			


#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	with open(file_path,'r') as fr:
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		ticker = file_name[0:-5]
#		print(ticker)
#		np = NetProfit(ticker)
#		npv = np.get_NetProfit_values(local_json)
#		asset = TotalAssets(ticker)
#		asset_v = asset.get_TotalAsset_values(local_json,start_fork=True)
#		test = return_on_assets(np,asset,local_json)
#		
#		print(test)	













