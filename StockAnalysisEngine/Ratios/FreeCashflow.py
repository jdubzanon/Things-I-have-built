
import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
from collections import namedtuple





#cash flow changes based on fork if forked capex is reported as a minus

def GetRatio(cashflow_class,capex_class,company_facts):
	FAILED_TO_GET_DATA = {'free_cashflow':'cant make calculation'}
	
	
	if any([isinstance(cashflow_class.cashflow_operations_arr,dict),
			isinstance(capex_class.capex_arr,dict),
			cashflow_class.forked == True,
			capex_class.forked == True  ]):
		
		from CashflowStatement.capex import capex
		from CashflowStatement.CashflowOperations import cashflow_operations
	
		capx = capex(capex_class.ticker)
		capx_vals = capx.get_capex_values(company_facts,start_fork=True)
		
		cash_flw = cashflow_operations(cashflow_class.ticker)
		cash_flw_vals = cash_flw.get_cashflow_operations_values(company_facts,start_fork=True)
		
		if any([isinstance(capx_vals,dict), isinstance(cash_flw_vals,dict)  ]):
			return FAILED_TO_GET_DATA
		
		try:
			return list(map(lambda cash_flw_values,capx_values: cash_flw_values + capx_values, cash_flw_vals,capx_vals  ))
		
		except ZeroDivisionError:
			cash_flw_vals = list(filter(lambda values: values != 0, cash_flw_vals))
			capx_vals = list(filter(lambda values: values != 0 , capx_vals))
			
			if any([ not cash_flw_vals, not capx_vals]):
				return FAILED_TO_GET_DATA
			
			return list(map(lambda cash_flw_values,capx_values: cash_flw_values + capx_values, cash_flw_vals,capx_vals  ))
			
	#if none were forked and non are dicts continue here
	longest_list_length = max([len(cashflow_class.cashflow_operations_arr),len(capex_class.capex_arr)  ])
	
	if len(cashflow_class.cashflow_operations_arr) >= longest_list_length:
		master_df = cashflow_class.cashflow_operations_df
		slave_df = capex_class.capex_df
	else:
		master_df = capex_class.capex_df
		slave_df = cashflow_class.cashflow_operations_df
		
	returned_list = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,returning_lists=True,isolate=True)

	#stop here and check
	if any([not returned_list[0],not returned_list[1] ]):
		from CashflowStatement.capex import capex
		from CashflowStatement.CashflowOperations import cashflow_operations
	
		capx = capex(capex_class.ticker)
		capx_vals = capx.get_capex_values(company_facts,start_fork=True)
		
		cash_flw = cashflow_operations(cashflow_class.ticker)
		cash_flw_vals = cash_flw.get_cashflow_operations_values(company_facts,start_fork=True)
		
		if any([isinstance(capx_vals,dict), isinstance(cash_flw_vals,dict)  ]):
			return FAILED_TO_GET_DATA
		
		try:
			return list(map(lambda cash_flw_values,capx_values: cash_flw_values + capx_values, cash_flw_vals,capx_vals  ))
		
		except ZeroDivisionError:
			cash_flw_vals = list(filter(lambda values: values != 0, cash_flw_vals))
			capx_vals = list(filter(lambda values: values != 0 , capx_vals))
			
			if any([ not cash_flw_vals, not capx_vals]):
				return FAILED_TO_GET_DATA
			
			return list(map(lambda cash_flw_values,capx_values: cash_flw_values + capx_values, cash_flw_vals,capx_vals  ))
	
	#continue here
	capex = namedtuple('capex','values')
	cashflow = namedtuple('cashflow','values')
	
	capex.values = capex_class.capex_arr
	cashflow.values = cashflow_class.cashflow_operations_arr
	
	for lists in returned_list:
		if set(lists).intersection(capex.values):
			capex.values = np.flip(lists)
		else:
			cashflow.values = np.flip(lists)
	
	if all([not 'Purchase' in capex_class.capex_key[0], not 'Payments' in capex_class.capex_key[0]]):
		capex_diff = list()
		for index,values in enumerate(capex.values,start=1):
			if index == len(capex.values):
				break
			capex_diff.append(values - capex.values[index])
		
		total_cashflow_values = list(map(lambda cashflow_from_operations,capex_values: cashflow_from_operations - capex_values, cashflow.values,capex_diff ))		
		
	else:
		
		total_cashflow_values = list(map(lambda cashflow_from_operations,capex_values: cashflow_from_operations - capex_values, cashflow.values,capex.values ))		
		
	return np.flip(total_cashflow_values)
		
		
		
		

