
import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
from collections import namedtuple


def GetRatio(LTD_class,NetInc_class,company_facts):
	FAILED_TO_GET_DATA = {'from LTD to NetInc ratio': 'cant make calculations'}
	
	if any([isinstance(LTD_class.LongTermDebt_arr,dict),
			isinstance(NetInc_class.NetProfit_arr,dict),
			LTD_class.forked == True,
			NetInc_class.forked == True]):
			
		from BalanceSheet.LongTermDebt import LongTermDebt
		from IncomeStatement.NetProfit import NetProfit	
			
		ltd = LongTermDebt(LTD_class.ticker)
		ltd_values = ltd.get_LongTermDebt_values(company_facts,start_fork=True)
		
		netInc = NetProfit(NetInc_class.ticker) 
		netInc_values = netInc_values = filter(lambda values: values != 0, netInc.get_NetProfit_values(company_facts,start_fork=True)) #removing zeros from divsior
		
		if any([isinstance(ltd_values,dict), isinstance(netInc_values,dict), not netInc_values, not ltd_values ]):
			return FAILED_TO_GET_DATA
		
		return list(map(lambda ltd_vals,NetInc_vals: round(ltd_vals/NetInc_vals,ndigits=2), ltd_values,netInc_values   ))

	
	longest_list_length = max([len(LTD_class.LongTermDebt_arr),len(NetInc_class.NetProfit_arr) ])
	
	if len(LTD_class.LongTermDebt_arr) >= longest_list_length:
		master_df = LTD_class.LongTermDebt_df
		slave_df = NetInc_class.NetProft_df
	else:
		master_df = NetInc_class.NetProft_df
		slave_df = LTD_class.LongTermDebt_df
	
	LTD = namedtuple('long_term_debt','values')
	NetProfit_tuple = namedtuple('NetProfit','values')
	
	LTD.values = LTD_class.LongTermDebt_arr
	NetProfit_tuple.values = NetInc_class.NetProfit_arr
	
	returned_list = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,returning_lists=True,isolate=True)
	#stop and check
	
	if any([ not returned_list[0], not returned_list[1] ]):
		from BalanceSheet.LongTermDebt import LongTermDebt
		from IncomeStatement.NetProfit import NetProfit	
			
		ltd = LongTermDebt(LTD_class.ticker)
		ltd_values = ltd.get_LongTermDebt_values(company_facts,start_fork=True)
		
		netInc = NetProfit(NetInc_class.ticker) 
		netInc_values = netInc_values = filter(lambda values: values != 0, netInc.get_NetProfit_values(company_facts,start_fork=True)) #removing zeros from divsior
		
		if any([isinstance(ltd_values,dict), isinstance(netInc_values,dict), not netInc_values, not ltd_values ]):
			return FAILED_TO_GET_DATA
		
		return list(map(lambda ltd_vals,NetInc_vals: round(ltd_vals/NetInc_vals,ndigits=2), ltd_values,netInc_values   ))
	
	#continue after check
	for lists in returned_list:
		if set(lists).intersection(set(LTD.values)):
			LTD.values = lists
		else:
			NetProfit_tuple.values = lists
			
	yrs_till_paidoff = list(map(lambda LngTrmDbt,net_profit: round(net_profit / LngTrmDbt,ndigits=2) , NetProfit_tuple.values,LTD.values))

	return np.flip(yrs_till_paidoff)


