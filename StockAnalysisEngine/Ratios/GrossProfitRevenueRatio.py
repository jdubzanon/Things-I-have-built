
import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
from collections import namedtuple


def GetRatio(rev_class,cogs_class,company_facts):
	FAILED_TO_GET_DATA = {'from gp to rev':'cant make calculation'}
	
	if any([isinstance(rev_class.revenue_list,dict),
			isinstance(rev_class.SaleOfGoods_arr,dict),
			isinstance(rev_class.service_revenue_arr,dict),
			isinstance(cogs_class.cogs_arr,dict),
			rev_class.forked == True,
			cogs_class.forked == True   ]):

		from IncomeStatement.revenue import Revenue
		from IncomeStatement.cogs import Cogs
		
		rev = Revenue(rev_class.ticker)
		rev_values = rev.get_revenue_values(company_facts,start_fork=True)
		
		cog = Cogs(cogs_class.ticker)
		cog_vals = cog.get_cog_values(company_facts,start_fork=True)
		
		if any([isinstance(rev_values,dict),isinstance(cog_vals,dict) ]):
			return FAILED_TO_GET_DATA
			
		try:
			return list(map(lambda gross_profit,revenue: round((gross_profit / revenue)*100,ndigits=2), map(lambda revenue,cogs: revenue-cogs, rev_values,cog_vals),rev_values    ))
		except ZeroDivisionError:
			rev_values = filter(lambda values: values != 0,rev_values)

			return list(map(lambda gross_profit,revenue: round((gross_profit / revenue)*100,ndigits=2), map(lambda revenue,cogs: revenue-cogs, rev_values,cog_vals),rev_values    ))
		
	if not rev_class.revenue_list:
		
		longest_list_length = max([len(rev_class.SaleOfGoods_arr) ,len(rev_class.service_revenue_arr),  len(cogs_class.cogs_arr)     ])
		
		if len(rev_class.SaleOfGoods_arr) >= longest_list_length:
			master_df = rev_class.SaleOfGoods_df
			slave_df = rev_class.service_revenue_df
			slave2_df = cogs_class.cogs_df
		elif len(rev_class.service_revenue_arr) >= longest_list_length:
			master_df = rev_class.service_revenue_df
			slave_df = rev_class.SaleOfGoods_df
			slave2_df = cogs_class.cogs_df
		else:
			master_df = cogs_class.cogs_df
			slave_df = rev_class.SaleOfGoods_df
			slave2_df = rev_class.service_revenue_df
			
		sales = namedtuple('sales','values')
		service = namedtuple('service','values')
		cogs = namedtuple('cogs','values')
		
		sales.values = rev_class.SaleOfGoods_arr
		service.values = rev_class.service_revenue_arr
		cogs.values = cogs_class.cogs_arr
		
		returned_list = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,df_slave2=slave2_df,isolate=True,returning_lists=True)
		#stop and check
		if any([not returned_list[0],not returned_list[1],not returned_list[2] ]):
			from IncomeStatement.revenue import Revenue
			from IncomeStatement.cogs import Cogs
			
			rev = Revenue(rev_class.ticker)
			rev_values = rev.get_revenue_values(company_facts,start_fork=True)
			
			cog = Cogs(cogs_class.ticker)
			cog_vals = cog.get_cog_values(company_facts,start_fork=True)
			
			if any([isinstance(rev_values,dict),isinstance(cog_vals,dict) ]):
				return FAILED_TO_GET_DATA
				
			try:
				return list(map(lambda gross_profit,revenue: round((gross_profit / revenue)*100,ndigits=2), map(lambda revenue,cogs: revenue-cogs, rev_values,cog_vals),rev_values    ))
			except ZeroDivisionError:
				rev_values = filter(lambda values: values != 0,rev_values)

				return list(map(lambda gross_profit,revenue: round((gross_profit / revenue)*100,ndigits=2), map(lambda revenue,cogs: revenue-cogs, rev_values,cog_vals),rev_values    ))
		
		#continue after check
		for lists in returned_list:
			if set(lists).intersection(sales.values):
				sales.values = lists
			elif set(lists).intersection(set(service.values)):
				service.values = lists
			else:
				cogs.values = lists
				
		total_rev_arr = list(map(lambda sales_values,service_values: sales_values + service_values,sales.values,service.values ))
		gross_profit = list(map( lambda rev_values,cogs_values : rev_values - cogs_values, total_rev_arr,cogs.values   ))
		gp_to_rev_ratio = list(map(lambda gp_values,revenue_vals : round((gp_values / revenue_vals)*100,ndigits=2) , gross_profit,total_rev_arr  ))
		
		return np.flip(gp_to_rev_ratio)

	else:
		longest_list_length = max([len(rev_class.revenue_list) , len(cogs_class.cogs_arr) ])
		
		if len(rev_class.revenue_list) >= longest_list_length:
			master_df = rev_class.revenue_df
			slave_df = cogs_class.cogs_df
		else:
			master_df = cogs_class.cogs_df
			slave_df = rev_class.revenue_df

		revenue = namedtuple('revenue','values')
		cogs = namedtuple('cogs','values')
		
		revenue.values = rev_class.revenue_list
		cogs.values = cogs_class.cogs_arr
		
		returned_list = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,isolate=True,returning_lists=True)

		#stop and check
		if any([not returned_list[0],not returned_list[1] ]):
			from IncomeStatement.revenue import Revenue
			from IncomeStatement.cogs import Cogs
			
			rev = Revenue(rev_class.ticker)
			rev_values = rev.get_revenue_values(company_facts,start_fork=True)
			
			cog = Cogs(cogs_class.ticker)
			cog_vals = cog.get_cog_values(company_facts,start_fork=True)
			
			if any([isinstance(rev_values,dict),isinstance(cog_vals,dict) ]):
				return FAILED_TO_GET_DATA
				
			try:
				return list(map(lambda gross_profit,revenue: round((gross_profit / revenue)*100,ndigits=2), map(lambda revenue,cogs: revenue-cogs, rev_values,cog_vals),rev_values    ))
			except ZeroDivisionError:
				rev_values = filter(lambda values: values != 0,rev_values)

				return list(map(lambda gross_profit,revenue: round((gross_profit / revenue)*100,ndigits=2), map(lambda revenue,cogs: revenue-cogs, rev_values,cog_vals),rev_values    ))
		
		#continue after check
		for lists in returned_list:
			if set(lists).intersection(set(revenue.values)):
				revenue.values = lists
			else:
				cogs.values = lists
				
		gross_profit = list(map(lambda rev,cog: rev-cog, revenue.values,cogs.values    ))
		gp_to_rev_ratio = list(map(lambda gp,rev: round((gp / rev)*100,ndigits=2),gross_profit,revenue.values  ))
		
		return np.flip(gp_to_rev_ratio)




