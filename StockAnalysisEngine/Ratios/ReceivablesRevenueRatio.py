import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
from collections import namedtuple


def GetRatio(rev_class,rec_class,company_facts):
	FAILED_TO_GET_DATA = {'receivables_to_revenue':'cant make calculation'}
	
	if any([isinstance(rev_class.revenue_list,dict), 
		isinstance(rev_class.SaleOfGoods_arr,dict),
		isinstance(rev_class.service_revenue_arr,dict),
		isinstance(rec_class.receivables_arr,dict),
		rec_class.forked == True,
		rev_class.forked == True ]):
		
		from BalanceSheet.receivables import receivables
		from IncomeStatement.revenue import Revenue
		
		rec = receivables(rec_class.ticker)
		rec_values = rec.get_receivables_values(company_facts,start_fork=True)

		rev = Revenue(rec_class.ticker)		
		rev_values = list(filter(lambda values: values != 0, rev.get_revenue_values(company_facts,start_fork=True))    )
		
		if any([ isinstance(rec_values,dict), isinstance(rev_values,dict), not rev_values ]):
			return FAILED_TO_GET_DATA
		
		rec_to_rev_ratio = map(lambda receivable_vals,revenue_vals: round((receivable_vals/revenue_vals)*100 ,ndigits=2), rec_values,rev_values)
		
		return list(rec_to_rev_ratio)
		
	if rev_class.revenue_list:
		
		longest_list_length = max([len(rev_class.revenue_list),len(rec_class.receivables_arr)   ])
		
		if len(rev_class.revenue_list) >= longest_list_length:
			master_df = rev_class.revenue_df
			slave_df = rec_class.receivables_df
		else:
			master_df = rec_class.receivables_df
			slave_df = rev_class.revenue_df
		
		revenue = namedtuple('revenue','values')
		receivables = namedtuple('receivables','values')
		
		revenue.values = rev_class.revenue_list
		receivables.values = rec_class.receivables_arr
		
		returned_list = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,returning_lists=True,isolate=True)
		
		#stop and check
		if any([not returned_list[0], not returned_list[1] ]):
			from BalanceSheet.receivables import receivables
			from IncomeStatement.revenue import Revenue
			
			rec = receivables(rec_class.ticker)
			rec_values = rec.get_receivables_values(company_facts,start_fork=True)

			rev = Revenue(rec_class.ticker)		
			rev_values = list(filter(lambda values: values != 0, rev.get_revenue_values(company_facts,start_fork=True))    )
			
			if any([ isinstance(rec_values,dict), isinstance(rev_values,dict), not rev_values ]):
				return FAILED_TO_GET_DATA
			
			rec_to_rev_ratio = map(lambda receivable_vals,revenue_vals: round((receivable_vals/revenue_vals)*100 ,ndigits=2), rec_values,rev_values)
			
			return list(rec_to_rev_ratio)			
		
		#continue after check
		for lists in returned_list:
			if set(lists).intersection(set(revenue.values)):
				revenue.values = np.flip(lists)
			else:
				receivables.values = np.flip(lists)

		receivables_to_revenue = list(map(lambda rec,rev: round((rec / rev)*100, ndigits=2), receivables.values,revenue.values   ))
		
		return 	receivables_to_revenue
		
	else:
		longest_list_length = max([len(rev_class.SaleOfGoods_arr), len(rev_class.service_revenue_arr), len(rec_class.receivables_arr)  ])
		
		#trying to get the dataframe with the most information to use as the main dataframe to pull info from
		if len(rev_class.SaleOfGoods_arr) >= longest_list_length: 
			master_df = rev_class.SaleOfGoods_df
			slave_df = rev_class.service_revenue_df
			slave2_df = rec_class.receivables_df
		
		elif len(rev_class.service_revenue_arr) >= longest_list_length:
			master_df = rev_class.service_revenue_df
			slave_df = rev_class.SaleOfGoods_df
			slave2_df = rec_class.receivables_df
		
		else:
			master_df = rec_class.receivables_df
			slave_df = rev_class.SaleOfGoods_df
			slave2_df = rev_class.service_revenue_df
		
		sales = namedtuple('sales','values')
		service = namedtuple('service','values')
		receivables = namedtuple('receivables','values')
		
		sales.values = rev_class.SaleOfGoods_arr
		service.values = rev_class.service_revenue_arr
		receivables.values = rec_class.receivables_arr		
		
		returned_list = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,df_slave2=slave2_df,isolate=True,returning_lists=True)

#		stop and check		
		if any([not returned_list[0], not returned_list[1],not returned_list[2] ]):
			from BalanceSheet.receivables import receivables
			from IncomeStatement.revenue import Revenue
			
			rec = receivables(rec_class.ticker)
			rec_values = rec.get_receivables_values(company_facts,start_fork=True)

			rev = Revenue(rec_class.ticker)		
			rev_values = list(filter(lambda values: values != 0, rev.get_revenue_values(company_facts,start_fork=True))    )
			
			if any([ isinstance(rec_values,dict), isinstance(rev_values,dict), not rev_values ]):
				return FAILED_TO_GET_DATA
			
			rec_to_rev_ratio = map(lambda receivable_vals,revenue_vals: round((receivable_vals/revenue_vals)*100 ,ndigits=2), rec_values,rev_values)
			
			return list(rec_to_rev_ratio)			
	
#		continue after check		
		for lists in returned_list:
			if set(lists).intersection(set(sales.values)):
				sales.values = np.flip(lists)
			elif set(lists).intersection(set(service.values)):
				service.values = np.flip(lists)
			else:
				receivables.values = np.flip(lists)
		
		receivables_to_revenue = list(map(lambda rec,rev: round((rec / rev)*100,ndigits=2), receivables.values,   map(lambda sales_vals,service_vals: sales_vals + service_vals, sales.values,service.values )))
		
		return receivables_to_revenue




