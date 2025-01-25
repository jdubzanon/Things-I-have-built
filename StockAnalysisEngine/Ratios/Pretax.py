
import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
from collections import namedtuple
import Ratios.YOY_growth as YOY_growth



def GetRatio(net_income_class,tax_exp_class,company_facts):
	FAILED_TO_GET_DATA = {'from pretax_earnings':'cant_make_calculations'} 
	#stop and check
	if any([isinstance(net_income_class.NetProfit_arr,dict), 
			isinstance(tax_exp_class.TaxesPaid_arr,dict),
			net_income_class.forked == True,
			tax_exp_class.forked == True  ]):
			
		from IncomeStatement.TaxesPaid import TaxesPaid
		from IncomeStatement.NetProfit import NetProfit
		
		tax = TaxesPaid(tax_exp_class.ticker)
		tax_values = tax.get_TaxesPaid_values(company_facts,start_fork=True)
		
		income = NetProfit(net_income_class.ticker)
		income_values = income.get_NetProfit_values(company_facts,start_fork=True)
		
		if any([ isinstance(tax_values,dict), isinstance(income_values,dict) ]):
			return FAILED_TO_GET_DATA
		
		pretax_earnings = YOY_growth.growth_calculate(list(map(lambda inc_vals,tax_vals: inc_vals + tax_vals, income_values,tax_values )) ) 
		
		return pretax_earnings
	
	#continue after check
	longest_list_length = max([len(net_income_class.NetProfit_arr),len(tax_exp_class.TaxesPaid_arr)  ])
	
	if len(net_income_class.NetProfit_arr) >= longest_list_length:
		master_df = net_income_class.NetProft_df
		slave_df = tax_exp_class.TaxesPaid_df
	
	else:
		master_df = tax_exp_class.TaxesPaid_df
		slave_df = net_income_class.NetProft_df
	
	returned_list = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,returning_lists=True)

	#stop and check
	if any([not returned_list[0], not returned_list[1]  ]):
		from IncomeStatement.TaxesPaid import TaxesPaid
		from IncomeStatement.NetProfit import NetProfit
		
		tax = TaxesPaid(tax_exp_class.ticker)
		tax_values = tax.get_TaxesPaid_values(company_facts,start_fork=True)
		
		income = NetProfit(net_income_class.ticker)
		income_values = income.get_NetProfit_values(company_facts,start_fork=True)
		
		if any([ isinstance(tax_values,dict), isinstance(income_values,dict) ]):
			return FAILED_TO_GET_DATA
		
		pretax_earnings = YOY_growth.growth_calculate(list(map(lambda inc_vals,tax_vals: inc_vals + tax_vals, income_values,tax_values )) ) 
		
		return pretax_earnings

	#continue after check	
	pretax_earnings_YOY = YOY_growth.growth_calculate(np.flip(np.sum([returned_list[0],returned_list[1]] ,axis=0)))

	return pretax_earnings_YOY


