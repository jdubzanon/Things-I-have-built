
import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
from collections import namedtuple






def GetRatio(TL_class,SharHolEq_class,company_facts):
	FAILED_TO_GET_DATA = {'from debt_to_equity_ratio': 'cant make calculations'}

	if any([isinstance(TL_class.TotalLiabilities_arr,dict),
			isinstance(TL_class.CurrentLiabilities_arr,dict),
			isinstance(TL_class.NonCurrentLiabilities_arr,dict),
			isinstance(SharHolEq_class.SharHolEq_arr,dict),
			TL_class.forked == True,
			SharHolEq_class.forked == True]):
		
		from BalanceSheet.TotalLiabilities import TotalLiabilities
		from BalanceSheet.ShareholdersEquity import ShareholdersEquity
	
		total_liabilities = TotalLiabilities(TL_class.ticker)	
		total_liabilities_values = total_liabilities.get_TotalLiabilities_values(company_facts,start_fork=True)
		
		shareholder_eq = ShareholdersEquity(SharHolEq_class.ticker)
		shareholder_eq_values = shareholder_eq.get_ShareholdersEquity_values(company_facts,start_fork=True)
		
		if any([isinstance(total_liabilities_values,dict), isinstance(shareholder_eq_values,dict)]):
			return FAILED_TO_GET_DATA
		
		try:
		 	return list(map(lambda tot_lia,sharhldeq: round((tot_lia/sharhldeq),ndigits=2),total_liabilities_values,shareholder_eq_values ))
		except ZeroDivisionError:
			
			total_liabilities_values = list(filter(lambda value: value != 0,total_liabilities_values )) 
			shareholder_eq_values = list(filter(lambda value: value != 0, shareholder_eq_values))			
			
			if any([not total_liabilities_values,not shareholder_eq_values ]):
				return FAILED_TO_GET_DATA

			return list(map(lambda tot_lia,sharhldeq: round((tot_lia/sharhldeq),ndigits=2),total_liabilities_values,shareholder_eq_values ))			
	
	if not TL_class.TotalLiabilities_arr:
		#your current and noncurrent to add up; then divide by SharHolEq
		longest_list_length = max([len(TL_class.CurrentLiabilities_arr),len(TL_class.NonCurrentLiabilities_arr),len(SharHolEq_class.SharHolEq_arr)   ])
		
		if len(TL_class.CurrentLiabilities_arr) >= longest_list_length:
			master_df = TL_class.CurrentLiabilities_df
			slave_df = TL_class.NonCurrentLiabilities_df
			slave2_df = SharHolEq_class.SharHolEq_df
		elif len(TL_class.NonCurrentLiabilities_arr):
			master_df = TL_class.NonCurrentLiabilities_df
			slave_df = TL_class.CurrentLiabilities_df
			slave2_df = SharHolEq_class.SharHolEq_df
		else:
			master_df = SharHolEq_class.SharHolEq_df
			slave_df = TL_class.CurrentLiabilities_df
			slave2_df = TL_class.NonCurrentLiabilities_df
		
		returned_list = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,df_slave2=slave2_df,isolate=True,returning_lists=True)
		#stop here do a check
		if any([not returned_list[0],not returned_list[1],not returned_list[2]]):
			from BalanceSheet.TotalLiabilities import TotalLiabilities
			from BalanceSheet.ShareholdersEquity import ShareholdersEquity
		
			total_liabilities = TotalLiabilities(TL_class.ticker)	
			total_liabilities_values = total_liabilities.get_TotalLiabilities_values(company_facts,start_fork=True)
			
			shareholder_eq = ShareholdersEquity(SharHolEq_class.ticker)
			shareholder_eq_values = shareholder_eq.get_ShareholdersEquity_values(company_facts,start_fork=True)
			
			if any([isinstance(total_liabilities_values,dict), isinstance(shareholder_eq_values,dict)]):
				return FAILED_TO_GET_DATA
			
			try:
		 		return list(map(lambda tot_lia,sharhldeq: round((tot_lia/sharhldeq),ndigits=2),total_liabilities_values,shareholder_eq_values ))
			except ZeroDivisionError:
			
				total_liabilities_values = list(filter(lambda value: value != 0,total_liabilities_values )) 
				shareholder_eq_values = list(filter(lambda value: value != 0, shareholder_eq_values))			
				
				if any([not total_liabilities_values,not shareholder_eq_values ]):
					return FAILED_TO_GET_DATA

				return list(map(lambda tot_lia,sharhldeq: round((tot_lia/sharhldeq),ndigits=2),total_liabilities_values,shareholder_eq_values ))		
		
		#continue after check
		NonCurrent = namedtuple('NonCurrent','values')
		Current = namedtuple('current','values')
		Shareholder = namedtuple('Shareholder','values')
		
		NonCurrent.values = TL_class.NonCurrentLiabilities_arr
		Current.values = TL_class.CurrentLiabilities_arr
		Shareholder.values = SharHolEq_class.SharHolEq_arr
		
		for lists in returned_list:
			if set(lists).intersection(set(NonCurrent.values)):
				NonCurrent.values = lists
			elif set(lists).intersection(set(Current.values)):
				Current.values =lists
			else:
				Shareholder.values = lists
		add_current_and_Noncurrent = list(map( lambda current,noncurrent: current+noncurrent,NonCurrent.values,Current.values ))
		
		debtToEquityRatio = list(map(lambda liabilites,shareq: round((liabilites / shareq),ndigits=2), add_current_and_Noncurrent, Shareholder.values  ))
		
		return np.flip(debtToEquityRatio)
				
	else:
		longest_list_length = max([len(TL_class.TotalLiabilities_arr),len(SharHolEq_class.SharHolEq_arr)   ])
		
		if len(SharHolEq_class.SharHolEq_arr) >= longest_list_length:
			master_df = SharHolEq_class.SharHolEq_df
			slave_df = TL_class.TotalLiabilities_df
			
		else:
			master_df = TL_class.TotalLiabilities_df
			slave_df = SharHolEq_class.SharHolEq_df
			
		Total = namedtuple('total_liabilities','values')
		Shareholder = namedtuple('shareholder','values')
		
		Total.values = TL_class.TotalLiabilities_arr
		Shareholder.values = SharHolEq_class.SharHolEq_arr
		
		returned_list = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,isolate=True,returning_lists=True)
		
		#stop here do a check
		if any([not returned_list[0],not returned_list[1] ]):
			from BalanceSheet.TotalLiabilities import TotalLiabilities
			from BalanceSheet.ShareholdersEquity import ShareholdersEquity
		
			total_liabilities = TotalLiabilities(TL_class.ticker)	
			total_liabilities_values = total_liabilities.get_TotalLiabilities_values(company_facts,start_fork=True)
			
			shareholder_eq = ShareholdersEquity(SharHolEq_class.ticker)
			shareholder_eq_values = shareholder_eq.get_ShareholdersEquity_values(company_facts,start_fork=True)
			
			if any([isinstance(total_liabilities_values,dict), isinstance(shareholder_eq_values,dict)]):
				return FAILED_TO_GET_DATA

			try:
		 		return list(map(lambda tot_lia,sharhldeq: round((tot_lia/sharhldeq),ndigits=2),total_liabilities_values,shareholder_eq_values ))
			except ZeroDivisionError:
			
				total_liabilities_values = list(filter(lambda value: value != 0,total_liabilities_values )) 
				shareholder_eq_values = list(filter(lambda value: value != 0, shareholder_eq_values))			
				
				if any([not total_liabilities_values,not shareholder_eq_values ]):
					return FAILED_TO_GET_DATA

				return list(map(lambda tot_lia,sharhldeq: round((tot_lia/sharhldeq),ndigits=2),total_liabilities_values,shareholder_eq_values ))		

		#continue after check
		for lists in returned_list:
			if set(lists).intersection(set(Total.values)):
				Total.values = lists
			else:
				Shareholder.values = lists
		
		debtToEquityRatio = list(map(lambda liabilites,shareq : round((liabilites / shareq),ndigits=2) , Total.values,Shareholder.values   ))
		
		return np.flip(debtToEquityRatio)
			
		
		

