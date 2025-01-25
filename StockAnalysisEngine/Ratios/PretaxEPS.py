import numpy as np
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
from collections import namedtuple
import Ratios.YOY_growth as YOY_growth



def GetRatio(net_income_class,tax_exp_class,sharesoutstanding_class,company_facts):
	FAILED_TO_GET_DATA = {'from pretax_earnings':'cant_make_calculations'}
	
	
	if any([isinstance(net_income_class.NetProfit_arr,dict), 
			isinstance(tax_exp_class.TaxesPaid_arr,dict),	
			isinstance(sharesoutstanding_class.SharesOutstanding_arr,dict),
			net_income_class.forked == True,
			tax_exp_class.forked == True,
			sharesoutstanding_class.forked == True  ]):
		
		from IncomeStatement.TaxesPaid import TaxesPaid
		from IncomeStatement.NetProfit import NetProfit
		from BalanceSheet.SharesOutstanding import SharesOutstanding
		
		taxes = TaxesPaid(tax_exp_class.ticker)
		tax_values = taxes.get_TaxesPaid_values(company_facts,start_fork=True)
		
		NetProf = NetProfit(net_income_class.ticker)
		NetProf_values = NetProf.get_NetProfit_values(company_facts,start_fork=True)
		
		shares = SharesOutstanding(sharesoutstanding_class.ticker)
		shares_values = list(filter(lambda values: values != 0 , shares.get_SharesOutstanding_values(company_facts,start_fork=True)))    #removing zero divisor
		
		if any([isinstance(tax_values,dict),isinstance(NetProf_values,dict),isinstance(shares_values,dict), not shares_values ]):
			return FAILED_TO_GET_DATA
		
		pretax_earnings = map(lambda net_profit,taxes_paid: net_profit + taxes_paid, NetProf_values,tax_values)
		
		pretax_eps_values = YOY_growth.growth_calculate(list(map(lambda EBT,shares: round(EBT / shares,ndigits=2), pretax_earnings,shares_values)))
		
		return pretax_eps_values		
		
	longest_list_length = max([len(net_income_class.NetProfit_arr),len(tax_exp_class.TaxesPaid_arr),len(sharesoutstanding_class.SharesOutstanding_arr)  ])
	
	if len(net_income_class.NetProfit_arr) >= longest_list_length:
		master_df = net_income_class.NetProft_df
		slave_df = tax_exp_class.TaxesPaid_df
		slave2_df = sharesoutstanding_class.SharesOutstanding_df
	elif len(tax_exp_class.TaxesPaid_arr) >= longest_list_length:
		master_df = tax_exp_class.TaxesPaid_df
		slave_df = net_income_class.NetProft_df
		slave2_df = sharesoutstanding_class.SharesOutstanding_df
	else:
		master_df = sharesoutstanding_class.SharesOutstanding_df
		slave_df = net_income_class.NetProft_df
		slave2_df = tax_exp_class.TaxesPaid_df	
	
	
	taxes = namedtuple('taxes','values')
	net_profit = namedtuple('net_profit','values')
	sharesoutstanding = namedtuple('sharesoutstanding','values')
	
	
	taxes.values = tax_exp_class.TaxesPaid_arr
	net_profit.values = net_income_class.NetProfit_arr
	sharesoutstanding.values = sharesoutstanding_class.SharesOutstanding_arr
	
	
	returned_list = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,df_slave2=slave2_df,returning_lists=True)

	#stop and check
	if any([not returned_list[0],not returned_list[1],not returned_list[2]]):
		from IncomeStatement.TaxesPaid import TaxesPaid
		from IncomeStatement.NetProfit import NetProfit
		from BalanceSheet.SharesOutstanding import SharesOutstanding
		
		taxes = TaxesPaid(tax_exp_class.ticker)
		tax_values = taxes.get_TaxesPaid_values(company_facts,start_fork=True)
		
		NetProf = NetProfit(net_income_class.ticker)
		NetProf_values = NetProf.get_NetProfit_values(company_facts,start_fork=True)
		
		shares = SharesOutstanding(sharesoutstanding_class.ticker)
		shares_values = list(filter(lambda values: values != 0 , shares.get_SharesOutstanding_values(company_facts,start_fork=True)))    #removing zero divisor
		
		if any([isinstance(tax_values,dict),isinstance(NetProf_values,dict),isinstance(shares_values,dict), not shares_values ]):
			return FAILED_TO_GET_DATA
		
		pretax_earnings = map(lambda net_profit,taxes_paid: net_profit + taxes_paid, NetProf_values,tax_values)
		
		pretax_eps_values = YOY_growth.growth_calculate(list(map(lambda EBT,shares: round(EBT / shares,ndigits=2), pretax_earnings,shares_values)))
		
		return pretax_eps_values

#	continue after check
#	flipping all the list here for the YOY_growth calculations, im pre-flipping the list  so i dont have to change anything after the for loop 
	for lists in returned_list:
		if set(lists).intersection(set(taxes.values)):
			taxes.values = np.flip(lists)
		elif set(lists).intersection(set(net_profit.values)):
			net_profit.values = np.flip(lists)
		else:
			sharesoutstanding.values = np.flip(lists)

	pretax_earnings = map(lambda net_p,tax_paid: net_p + tax_paid, net_profit.values,taxes.values   )

	def divide(PreTaxEarnings,SharesOutstanding):
		if all([PreTaxEarnings !=0, SharesOutstanding != 0]):
			return round(PreTaxEarnings / SharesOutstanding, ndigits=2)
	
	pretax_eps_values = YOY_growth.growth_calculate(list(filter(lambda values: not values is None, map(divide, pretax_earnings,sharesoutstanding.values ))))
	
	return pretax_eps_values





