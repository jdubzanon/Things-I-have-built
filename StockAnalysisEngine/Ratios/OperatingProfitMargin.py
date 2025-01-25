import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
from collections import namedtuple




####MAY USE THIS OVER GROSS PROFIT / REVENUE

def GetRatio(OpInc_class,rev_class,IntExp_class,company_facts):
	FAILED_TO_GET_DATA = {'from opinc func':'no calculations'} 

#  workflow: first check rev_class and opInc class to see if they are forked or returned a dictionary
	if any([isinstance(OpInc_class.OpIncome_arr,dict),
			isinstance(rev_class.revenue_list,dict),
			isinstance(rev_class.service_revenue_arr,dict),
			isinstance(rev_class.SaleOfGoods_arr,dict),
			OpInc_class.forked == True,
			rev_class.forked == True]):
			
			from IncomeStatement.OperatingIncome import OpIncome
			from IncomeStatement.revenue import Revenue
			
			OpInc = OpIncome(OpInc_class.ticker)	
			OpInc_values = OpInc.get_OpIncome_values(company_facts,start_fork=True)

			rev = Revenue(rev_class.ticker)
			rev_values = list(filter(lambda values: values != 0, rev.get_revenue_values(company_facts,start_fork=True)))  #removing zero from divisor)

			if any([ isinstance(OpInc_values,dict), isinstance(rev_values,dict), not rev_values  ]):
				return FAILED_TO_GET_DATA
																														
			return list(map(lambda opInc_vals,rev_vals: round( (opInc_vals / rev_vals)*100 ,ndigits=2  ),OpInc_values, rev_values ))			
	
	#this block below is if interest is already subtracted out of opincome values i need to add the interest back into the operating income values 
	#workflow: if none are forked then check the op income key 
	if OpInc_class.OpIncome_key[0] == OpInc_class.possible_OpIncome_keys[0]: #first main check continuation is marked 
		
		#first check
		#workflow: if this block is activated im going to need IntExp_class; check if IntExp_class is forked or has returned a dictionary, if yes then activate fork 		
		if any([ isinstance(IntExp_class.IntExp_arr,dict),  IntExp_class.forked == True ]):
			
			from IncomeStatement.OperatingIncome import OpIncome
			from IncomeStatement.revenue import Revenue
			
			OpInc = OpIncome(OpInc_class.ticker)	
			OpInc_values = OpInc.get_OpIncome_values(company_facts,start_fork=True)

			rev = Revenue(rev_class.ticker)
			rev_values = list(filter(lambda values: values != 0, rev.get_revenue_values(company_facts,start_fork=True) ))  #removing zero from divisor
		
			if any([ isinstance(OpInc_values,dict), isinstance(rev_values,dict), not rev_values  ]):
				return FAILED_TO_GET_DATA
																																	
			return list(map(lambda opInc_vals,rev_vals: round( (opInc_vals / rev_vals)*100 ,ndigits=2  ),OpInc_values, rev_values ))			
		
		
		#workflow: continue after check
		if not rev_class.revenue_list:
			longest_list_length = max([ len(rev_class.SaleOfGoods_arr), len(rev_class.service_revenue_arr), len(OpInc_class.OpIncome_arr), len(IntExp_class.IntExp_arr)    ])		
		
			if len(rev_class.SaleOfGoods_arr) >= longest_list_length:
				master_df = rev_class.SaleOfGoods_df
				slave_df = rev_class.service_revenue_df
				slave2_df = OpInc_class.OpIncome_df
				slave3_df = IntExp_class.IntExp_df
			elif len(rev_class.service_revenue_arr) >= longest_list_length:
				master_df = rev_class.service_revenue_df	
				slave_df = rev_class.SaleOfGoods_df
				slave2_df = OpInc_class.OpIncome_df
				slave3_df = IntExp_class.IntExp_df
			elif len(OpInc_class.OpIncome_arr) >= longest_list_length:
				master_df = OpInc_class.OpIncome_df
				slave_df = rev_class.SaleOfGoods_df
				slave2_df = rev_class.service_revenue_df	
				slave3_df = IntExp_class.IntExp_df
			else:
				master_df = IntExp_class.IntExp_df
				slave_df = rev_class.SaleOfGoods_df
				slave2_df = rev_class.service_revenue_df	
				slave3_df = OpInc_class.OpIncome_df
		
			sales = namedtuple('sales','values')
			service = namedtuple('service','values')
			interest = namedtuple('interest','values')
			income = namedtuple('operating_income','values')
			
			sales.values = rev_class.SaleOfGoods_arr
			service.values = rev_class.service_revenue_arr
			interest.values = IntExp_class.IntExp_arr
			income.values = OpInc_class.OpIncome_arr
			
			returned_list = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,df_slave2=slave2_df,df_slave3=slave3_df,returning_lists=True,isolate=True)
			
			#stop and checks
			if any([ not returned_list[0],not returned_list[1],not returned_list[2],not returned_list[3]  ]):
				
				from IncomeStatement.OperatingIncome import OpIncome
				from IncomeStatement.revenue import Revenue
				
				OpInc = OpIncome(OpInc_class.ticker)	
				OpInc_values = OpInc.get_OpIncome_values(company_facts,start_fork=True)

				rev = Revenue(rev_class.ticker)
				rev_values = list(filter(lambda values: values != 0, rev.get_revenue_values(company_facts,start_fork=True) ))   #removing zero from divisor
			
				if any([ isinstance(OpInc_values,dict), isinstance(rev_values,dict), not rev_values  ]):
					return FAILED_TO_GET_DATA
																																			
				return list(map(lambda opInc_vals,rev_vals: round( (opInc_vals / rev_vals)*100 ,ndigits=2  ),OpInc_values, rev_values ))			

			#continue after check
			for lists in returned_list:
				if set(lists).intersection(set(sales.values)):
					sales.values = lists
				elif set(lists).intersection(set(service.values)):
					service.values = lists
				elif set(lists).intersection(set(interest.values)):
					interest.values = lists
				else:
					income.values = lists
	
#	keep two variables they are identifying which is which in the operating_income_margin iterables 			
	#		operating_income = map(lambda interest_vals,income_vals: interest_vals + income_vals, interest.values,income.values )
	#		total_revenue = map(lambda sales_vals,service_vals: sales_vals + service_vals, sales.values,service.values   )
			
			operating_income_margin = list(map(lambda opInc_val,rev_vals:  opInc_val / rev_vals, map(lambda interest_vals,income_vals: interest_vals + income_vals, interest.values,income.values ), 
																								map(lambda sales_vals,service_vals: sales_vals + service_vals, sales.values,service.values   )   ))
			return np.flip(operating_income_margin)
		
		else:
			longest_list_length = max([ len(rev_class.revenue_list), len(OpInc_class.OpIncome_arr), len(IntExp_class.IntExp_arr)  ])
			
			if len(rev_class.revenue_list) >= longest_list_length:
				master_df = rev_class.revenue_df
				slave_df = OpInc_class.OpIncome_df
				slave2_df = IntExp_class.IntExp_df
			
			elif len(OpInc_class.OpIncome_arr) >= longest_list_length:
				master_df = OpInc_class.OpIncome_df
				slave_df = rev_class.revenue_df
				slave2_df = IntExp_class.IntExp_df
			
			else:
				master_df = IntExp_class.IntExp_df
				slave_df = rev_class.revenue_df
				slave2_df = OpInc_class.OpIncome_df
			
			revenue = namedtuple('revenue','values')
			interest = namedtuple('interest','values')
			income = namedtuple('operating_income','values')
			
			revenue.values = rev_class.revenue_list
			interest.values = IntExp_class.IntExp_arr
			income.values = OpInc_class.OpIncome_arr
			
			returned_list = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,df_slave2=slave2_df,returning_lists=True,isolate=True)
			
			#stop and check here
			if any([not returned_list[0], not returned_list[1], not returned_list[2]  ]):
				
				from IncomeStatement.OperatingIncome import OpIncome
				from IncomeStatement.revenue import Revenue

				OpInc = OpIncome(OpInc_class.ticker)	
				OpInc_values = OpInc.get_OpIncome_values(company_facts,start_fork=True)

				rev = Revenue(rev_class.ticker)
				rev_values = list(filter(lambda values: values != 0, rev.get_revenue_values(company_facts,start_fork=True) )) #removing zero from divisor
	
				if any([ isinstance(OpInc_values,dict), isinstance(rev_values,dict), not rev_values  ]):
					return FAILED_TO_GET_DATA

				return list(map(lambda opInc_vals,rev_vals: round( (opInc_vals / rev_vals)*100 ,ndigits=2  ),OpInc_values, rev_values ))			
			
			#continue after check
			for lists in returned_list:
				if set(lists).intersection(set(revenue.values)):
					revenue.values = lists
				elif set(lists).intersection(set(interest.values)):
					interest.values = lists
				else:
					income.values = lists

#			keep this commented out variable it is identifying which is operating_income in operating_income_margin			
			operating_income = map(lambda interest_vals,income_vals: interest_vals + income_vals, interest.values,income.values )
			
			operating_income_margin = list(map(lambda opInc_vals,rev_vals: round((opInc_vals/rev_vals)*100  ,ndigits=2 ), operating_income, revenue.values)		)

			return np.flip(operating_income_margin)


	#if first main check doesnt apply continue here MAIN CHECK CONTIUATION MARK	/ if interest hasnt been removed the use this block
	if not rev_class.revenue_list: #checking if attribute revenue list is None if it is non run this block if its not skip block continuation is marked
		
		longest_list_length = max([len(rev_class.SaleOfGoods_arr),len(rev_class.service_revenue_arr),len(OpInc_class.OpIncome_arr)])

		if len(rev_class.SaleOfGoods_arr) >= longest_list_length:
			master_df = rev_class.SaleOfGoods_df
			slave_df = rev_class.service_revenue_df
			slave2_df = OpInc_class.OpIncome_df
		
		elif len(rev_class.service_revenue_df) >= longest_list_length:
			master_df = rev_class.service_revenue_df
			slave_df = rev_class.SaleOfGoods_df
			slave2_df = OpInc_class.OpIncome_df
		else:
			master_df = OpInc_class.OpIncome_df
			slave_df = rev_class.SaleOfGoods_df
			slave2_df = rev_class.service_revenue_df
		
		service = namedtuple('service','values')
		sales = namedtuple('sales','values')
		OpInc = namedtuple('OpInc','values')
		
		service.values = rev_class.service_revenue_arr
		sales.values = rev_class.SaleOfGoods_arr
		OpInc.values = OpInc_class.OpIncome_arr
		
		returned_list = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,df_slave2=slave2_df,returning_lists=True,isolate=True)		
		
		#stop and check 
		if any([ not returned_list[0], not returned_list[1],not returned_list[2] ]):
			
			from IncomeStatement.OperatingIncome import OpIncome
			from IncomeStatement.revenue import Revenue
			
			OpInc = OpIncome(OpInc_class.ticker)	
			OpInc_values = OpInc.get_OpIncome_values(company_facts,start_fork=True)

			rev = Revenue(rev_class.ticker)
			rev_values = filter(lambda values: values != 0, rev.get_revenue_values(company_facts,start_fork=True) ) #removing zero from divisor
		
			if any([ isinstance(OpInc_values,dict), isinstance(rev_values,dict), not rev_values  ]):
				return FAILED_TO_GET_DATA
			
			return list(map(lambda opInc_vals,rev_vals: round( (opInc_vals / rev_vals)*100 ,ndigits=2  ),OpInc_values,rev_values ))
		
		#continue after check
		for lists in returned_list:
			if set(lists).intersection(set(service.values)):
				service.values = lists
			elif set(lists).intersection(set(sales.values)):
				sales.values = lists
			else:
				OpInc.values = lists
		
#		total_revenue = map(lambda service,sales: service + sales, service.values,sales.values )
		
		opInc_to_revenue = list(map(lambda opInc,revenue: round((opInc / revenue) *100,ndigits=2)  , OpInc.values, map(lambda service,sales: service + sales, service.values,sales.values ) ))
		
		return np.flip(opInc_to_revenue)
	
	#if revenue list is not none continue here	
	longest_list_length = max([len(OpInc_class.OpIncome_arr),len(rev_class.revenue_list)])
	
	if len(OpInc_class.OpIncome_arr) >= longest_list_length:
		master_df = OpInc_class.OpIncome_df
		slave_df = rev_class.revenue_df
	else:
		master_df = rev_class.revenue_df
		slave_df = OpInc_class.OpIncome_df
 	
	OpInc = namedtuple('OpInc','values')
	revenue = namedtuple('revenue', 'values')
 	
	OpInc.values = OpInc_class.OpIncome_arr
	revenue.values = rev_class.revenue_list
	
	returned_list = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,returning_lists=True,isolate=True)
	
	#stop and check
	if any([not returned_list[0], not returned_list[1]  ]):
		
		from IncomeStatement.OperatingIncome import OpIncome
		from IncomeStatement.revenue import Revenue
		
		OpInc = OpIncome(OpInc_class.ticker)	
		OpInc_values = OpInc.get_OpIncome_values(company_facts,start_fork=True)

		rev = Revenue(rev_class.ticker)
		rev_values = list(filter(lambda values: values != 0, rev.get_revenue_values(company_facts,start_fork=True) )) #removing zero from divisor
			
		if any([ isinstance(OpInc_values,dict), isinstance(rev_values,dict), not rev_values  ]):
			return FAILED_TO_GET_DATA
		
		return list(map(lambda opInc_vals,rev_vals: round( (opInc_vals / rev_vals)*100 ,ndigits=2  ),OpInc_values,rev_values ))

	#continue here
	for lists in returned_list:
		if set(lists).intersection(set(OpInc.values)):
			OpInc.values = lists
		else:
			revenue.values = lists
	
	OpInc_to_rev_ratio = list(map(lambda opInc,revenue : round((opInc / revenue) * 100,ndigits=2), OpInc.values,revenue.values  ))

	return np.flip(OpInc_to_rev_ratio)


