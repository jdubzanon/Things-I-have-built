import numpy as np
import get_arr.get_arr as get_arr
from collections import namedtuple
import time



def growth_calculate(list_of_values):
	if isinstance(list_of_values,dict):
		return list_of_values
	try:		
		percent_growth = list()
		for index,value in enumerate(list_of_values, start=1):
			if index == len(list_of_values):
				break
			if list_of_values[index] > value:
				diff = list_of_values[index] - value		
				divided = diff / list_of_values[index]
				percent_diff = divided * -100
				percent_growth.append(percent_diff)
			else:
				diff = value - list_of_values[index]
				divided = diff/ value
				percent_diff = divided * 100		
				percent_growth.append(percent_diff)		
		
		return {
					'mean_all' : round(np.array(percent_growth).mean(),2),
					'mean_last_five' : round(np.array(percent_growth[0:5]).mean(),2)
					} if len(percent_growth) > 1 else {'y-o-y growth': "Not enough information available"}
	
	# if nothing is in list_of_values return no information available
	except TypeError:
			return {
					'mean_all_years' : 'No information available',
					'mean_last_five' : 'No information available'
					}
					
					
					
def get_ratio_from_two_arrays_using_array_avgs(arr1,arr2): 
	'''	notes:
	1. arr1 is the arry higher up on the financial statement typically should have largest values

	2. arr2 is the arr lower on the financial statement typically should have smaller values

	3. im dividing arr2 by arr1 at the end of function (arr2 / arr1) '''
	shortest_list_length = min( len(arr2), len(arr1) )
			
	while len(arr2) > shortest_list_length:
		arr2.pop()
	while len(arr1) > shortest_list_length:
		arr1.pop()
		
	avg_arr2 = np.mean(arr2) #numerator
	avg_arr1 = np.mean(arr1) #denominator
	
	arr1_to_arr2_ratio = avg_arr2 / avg_arr1 * 100

	#five year calculations
	if len(arr2) >= 5:
		avg_five_yr_arr2 = sum(arr2[0:5]) / 5	
					
	elif len(arr2) < 5:
		avg_five_yr_arr2 = np.mean(arr2) 
		
	if len(arr1) >= 5:
		avg_five_yr_arr1 = sum(arr1[0:5]) / 5
	
	elif len(arr1) < 5:
		avg_five_yr_arr1 = np.mean(arr1)

	five_yr_ratio = avg_five_yr_arr2 / avg_five_yr_arr1 * 100	
		
	return {
			'mean_all' : round(arr1_to_arr2_ratio,3),
			'mean_last_five' : round(five_yr_ratio,3)
	
	}
	
	
	
def divide_multiple_to_get_ratio(arr1,arr2,percent=False):
	#example longtermdebt / net income  arr1 = longtermdebt and arr2 = net income 
	#arr1 is the divsor      arr2 is the numerator
#	print(arr1)
#	print(arr2)
	if isinstance(arr1,dict):
		return arr1
	
	if isinstance(arr2,dict):
		return arr2	
	
	shortest_list_length = min(len(arr1),len(arr2))
	
	while len(arr1) > shortest_list_length:
		arr1.pop()
	while len(arr2) > shortest_list_length:
		arr2.pop()
	
	if len(arr2) >= 5:
		five_yr_arr2 = arr2[0:5]
					
	else:
		five_yr_arr2 = arr2 
		
	if len(arr1) >= 5:
		five_yr_arr1 = arr1[0:5] 
	
	else:
		five_yr_arr1 = arr1
	
	all_yrs_avg = np.round(np.mean(list(map(lambda divisor, numerator : divisor/numerator, arr1,arr2))), decimals=3) 
	five_yr_avg = np.round(np.mean(list(map(lambda divisor, numerator : divisor/numerator, five_yr_arr1,five_yr_arr2))), decimals=3) 
	
	if percent:
		
		return {'mean_all(divide_multiple)': all_yrs_avg*100, 'mean_five':five_yr_avg*100}
	
	return {'mean_all(divide_multiple)': all_yrs_avg, 'mean_five':five_yr_avg}
	
	
def opInc_to_revenue_ratio(OpInc_class,rev_class):
	pass





def GrossProfit_percent_of_revenue(revenue_df,cogs_df):

	rev_cog_values = get_arr.line_up_dates_with_values_for_calculation(revenue_df,cogs_df,returning_lists=True) #returns ([revenue_values],[cogs_values])
	
	gross_profit_values = list(map(lambda revenue,cogs : revenue - cogs, rev_cog_values[0],rev_cog_values[1]   ))	
	
	gp_percent_of_revenue = list(map(lambda gross_profit,revenue : (gross_profit / revenue)*100 , gross_profit_values,rev_cog_values[0]   ))
	
	if len(gp_percent_of_revenue) > 5: 
		last_five = gp_percent_of_revenue[0:5]
	else:
		last_five = gp_percent_of_revenue		
	
	return {'last_five': np.round(np.mean(last_five),decimals=2)}


def RetainedEarnings_growth(arr,key):
	if isinstance(arr,dict):
		return arr
	
	if key[0] == 'RetainedEarningsAccumulatedDeficit':
		new_vals = list(np.flip(arr))
		percent_list = list()
		
		for index,value in enumerate(new_vals,start=1):
			
			if index == len(new_vals):
				break
			num1 = value
			num2 = new_vals[index]
			
			# first and second are negative, first less than second
			if all([num1 < 0,num1 < 0, num1 < num2]):
				diff = abs(abs(num1) - abs(num2))
				percent = (diff / abs(num1)) * 100
				percent_list.append(percent)
				
			# first and second negative first greater than second
			if all([num1<0,num2<0,num1>num2 ]):
				diff = abs(abs(num1) - abs(num2))
				percent = (diff / num1) * 100
				percent_list.append(percent)

			#first number negative second number positive
			if all([num1 < 0,num2 > 0]):
				diff = abs(num1)+abs(num2)
				percent = (diff / abs(num1)) * 100 
				percent_list.append(percent)
			
			# first number positive second negative
			if all([num1>0,num2<0]):
				diff = abs(num1)+abs(num2)
				percent = (diff / num1) * -100
				percent_list.append(percent)

			# both numbers positive first number less than second number
			if all([num1 < num2,num1>0,num2>0]):
				diff = num2 - num1
				percent = (diff / num1 ) * 100
				percent_list.append(percent)

			# both positive first number greater than second number
			if all([num1 > num2, num1>0,num2>0]):
				diff = num1 - num2
				percent = (diff / num1) * -100
				percent_list.append(percent)
		
		last_five = np.mean(np.flip(percent_list)[0:5])
		
		return  {'last_five(retain_earn)': round(last_five,ndigits=3)   }
		
	else:
		return growth_calculate(arr)
	
	

		
def sga_to_gross_profit_ratio(rev_class,cogs_class,sga_class):
	#use line_up_dates_with_values_for_calculation
	if any([ rev_class.forked == True, isinstance(cogs_class.cogs_arr,dict), isinstance(sga_class.sga_arr,dict)  ]):
		return {'min_five_fun4met_sga_ratio': 'cant make calculations'}
	
	if all([ not rev_class.revenue_key,not sga_class.sga_key]):
		list_of_lengths = [len(rev_class.SaleOfGoods_arr),len(rev_class.service_revenue_arr),len(sga_class.marketing_arr),len(sga_class.admin_arr)]

	if all([rev_class.revenue_key,sga_class.marketing_key,sga_class.admin_key ]):
		list_of_lengths = [len(rev_class.revenue_list),len(sga_class.marketing_arr),len(sga_class.admin_arr)]
				
	if all([sga_class.sga_key,rev_class.SaleOfGoods_key,rev_class.service_revenue_key]):
		list_of_lengths = [len(sga_class.sga_arr),len(rev_class.SaleOfGoods_arr),len(rev_class.service_revenue_arr)]
	
	if all([sga_class.sga_key,rev_class.revenue_key ]):
		list_of_lengths = [len(sga_class.sga_arr),len(rev_class.revenue_list)]
	
	longest_list_length = max(list_of_lengths)    
	
	
	if all([sga_class.marketing_arr,sga_class.admin_arr,rev_class.service_revenue_arr,rev_class.SaleOfGoods_arr ]):
		print('func_4_metrics 1')
		marketing = namedtuple('marketing','values')		
		admin = namedtuple('admin','values')		
		service = namedtuple('service','values')
		sales = namedtuple('sales','values')
		cogs = namedtuple('cogs','values')
		
		marketing.values = sga_class.marketing_arr 
		admin.values = sga_class.admin_arr
		service.values = rev_class.service_revenue_arr
		sale.values = rev_class.SaleOfGoods_arr
		cogs.values = cogs_class.cogs_arr		
		
		if len(sga_class.marketing_arr) == longest_list_length:
			master_df = sga_class.marketing_df
			slave_df = sga_class.admin_df
			slave2_df = rev_class.service_revenue_df
			slave3_df = rev_class.SaleOfGoods_df
			slave4_df = cogs_class.cogs_df
		elif len(sga_class.admin_arr) == longest_list_length:
			master_df = sga_class.admin_df
			slave_df = sga_class.marketing_df
			slave2_df = rev_class.service_revenue_df
			slave3_df = rev_class.SaleOfGoods_df
			slave4_df = cogs_class.cogs_df
		elif len(rev_class.service_revenue_arr) == longest_list_length:
			master_df = rev_class.service_revenue_df
			slave_df = rev_class.SaleOfGoods_df
			slave2_df = sga_class.marketing_df
			slave3_df = sga_class.admin_df
			slave4_df = cogs_class.cogs_df
		elif len(rev_class.SaleOfGoods_arr) == longest_list_length:
			master_df = rev_class.SaleOfGoods_df
			slave_df = rev_class.service_revenue_df
			slave2_df = sga_class.marketing_df
			slave3_df = sga_class.admin_df
			slave4_df = cogs_class.cogs_df
		else:
			master_df = cogs_class.cogs_df
			slave_df = rev_class.SaleOfGoods_df
			slave2_df = rev_class.service_revenue_df
			slave3_df = sga_class.marketing_df
			slave4_df = sga_class.admin_df
			
		cleaned_values = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,df_slave2=slave2_df,df_slave3=slave3_df,df_slave4=slave4_df,isolate=True,returning_lists=True)	
		
		if isinstance(cleaned_values,dict):
			return cleaned_values
		
		for lists in cleaned_values:
			if set(lists).intersection(set(sales.values)):
				sales.values = lists
			elif set(lists).intersection(set(service.values)):
				service.values = lists
			elif set(lists).intersection(set(marketing.values)):
				marketing.values = lists
			elif set(lists).intersection(set(admin.values)):
				admin.values = lists
			else:
				cogs.values = lists
		total_revenue = np.sum([sales.values,service.values],axis=0)
		total_sga = np.sum([marketing.values,admin.values ],axis=0)
		gross_profit = np.subtract(total_revenue,cogs.values)
		sga_to_gross_profit_ratios = list(map(lambda sga,gp: round((sga / gp) * 100, ndigits=2)  , total_sga,gross_profit   ))	
		
		return np.std(sga_to_gross_profit_ratios)
		
	#add sales.values to service.values <- revenue values
	#add marketing.values to admin.values <- sga values
	#sga values / revenue values
	
	
	elif all([sga_class.marketing_arr,sga_class.admin_arr,rev_class.revenue_list ])	:
		print('func_4_metrics 2')
		
		revenue = namedtuple('revenue','values')		
		marketing = namedtuple('marketing','values')
		admin = namedtuple('admin','values')
		cogs = namedtuple('cogs','values')
		
		revenue.values = rev_class.revenue_list
		marketing.values = sga_class.marketing_arr
		admin.values = sga_class.admin_arr
		cogs.values = cogs_class.cogs_arr
		
		#find longest dataframe for dataframe passing 
		if len(sga_class.marketing_arr) == longest_list_length:
			master_df = sga_class.marketing_df
			slave_df = sga_class.admin_df
			slave2_df = rev_class.revenue_df
			slave3_df = cogs_class.cogs_df
		elif len(sga_class.admin_arr) == longest_list_length:
			master_df = sga_class.admin_df
			slave_df = sga_class.marketing_df
			slave2_df = rev_class.revenue_df
			slave3_df = cogs_class.cogs_df
		elif len(rev_class.revenue_list) == longest_list_length:
			master_df = rev_class.revenue_df
			slave_df = sga_class.marketing_df
			slave2_df = sga_class.admin_df
			slave3_df = cogs_class.cogs_df
		else:
			master_df = cogs_class.cogs_df
			slave_df = rev_class.revenue_df
			slave2_df = sga_class.marketing_df
			slave3_df = sga_class.admin_df			
		
		cleaned_values = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,df_slave2=slave2_df,df_slave3=slave3_df,isolate=True,returning_lists=True)			
		if isinstance(cleaned_values,dict):
			return cleaned_values
		
		for lists in cleaned_values: #reorganizing each list since they got mixed up for dataframe passing
			if set(lists).intersection(set(revenue.values)):
				revenue.values = lists
			elif set(lists).intersection(set(marketing.values)):
				marketing.values = lists
			elif set(lists).intersection(set(admin.values)):
				admin.values = lists
			else:
				cogs.values = lists
		
		gross_profit = np.subtract(revenue.values,cogs.values)
		sga_values = np.sum([marketing.values,admin.values],axis=0)
		sga_to_gross_profit_ratios = list(map(lambda sga,gp: round((sga / gp) * 100, ndigits=2)  , sga_values,gross_profit   ))	
		
		return  np.std(sga_to_gross_profit_ratios)
		
		
	elif all([ sga_class.sga_arr,rev_class.SaleOfGoods_arr,rev_class.service_revenue_arr ]):
		print('func_4_metrics 3')
		
		sga = namedtuple('sga','values')
		sales = namedtuple('sales','values')
		service = namedtuple('service','values')
		cogs = namedtuple('cogs','values')
	
		sga.values = sga_class.sga_arr
		sales.values = rev_class.SaleOfGoods_arr
		service.values = rev_class.service_revenue_arr
		cogs = cogs_class.cogs_arr
		
		if len(sga_class.sga_arr) == longest_list_length:
			master_df = sga_class.sga_df
			slave_df = rev_class.SaleOfGoods_df
			slave2_df = rev_class.service_revenue_df
			slave3_df = cogs_class.cogs_df
		elif len(rev_class.SaleOfGoods_arr) == longest_list_length:
			master_df = rev_class.SaleOfGoods_df
			slave_df = rev_class.service_revenue_df
			slave2_df = sga_class.sga_df
			slave3_df = cogs_class.cogs_df
		elif len(rev_class.service_revenue_arr) == longest_list_length:
			master_df = rev_class.service_rev_df
			slave_df = rev_class.SaleOfGoods_df
			slave2_df = sga_class.sga_df
			slave3_df = cogs_class.cogs_df
		else:
			master_df = cogs_class.cogs_df
			slave_df = sga_class.sga_df
			slave2_df = rev_class.SaleOfGoods_df
			slave3 = rev_class.service_revenue_df
	
		cleaned_values = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,df_slave2=slave2_df,df_slave3=slave3_df,isolate=True,returning_lists=True)
		
		for lists in cleaned_values:
			if set(lists).intersection(set(sga.values)):
				sga.values = lists
			elif set(lists).intersection(set(sales.values)):
				sales.values = lists
			elif set(lists).intersection(set(service.values)):
				service.values = lists
			else:
				cogs.values = lists
			
		total_revenue = np.sum([sales.values,service.values ],axis=0)
		gross_profit = np.subtract(total_revenue,cogs.values)
		sga_to_gross_profit_ratios = list(map(lambda sga,gp: round((sga / gp) * 100, ndigits=2)  , sga.values,total_revenue   ))	
		return np.std(sga_to_gross_profit_ratios)
		
	else:
		print('func_4_metrics 4')
		
		sga = namedtuple('sga','values')
		revenue = namedtuple('sga','values')
		cogs = namedtuple('cogs','values')

		sga.values = sga_class.sga_arr
		revenue.values = rev_class.revenue_list
		cogs.values = cogs_class.cogs_arr		
		
		if len(sga_class.sga_arr) == longest_list_length:
			master_df = sga_class.sga_df
			slave_df = rev_class.revenue_df
			slave2_df = cogs_class.cogs_df
		elif len(rev_class.revenue_df) == longest_list_length:
			master_df = rev_class.revenue_df
			slave_df = sga_class.sga_df
			slave2_df = cogs_class.cogs_df
		else:
			master_df = cogs_class.cogs_df
			slave_df = rev_class.revenue_df
			slave2_df = sga_class.sga_df		
		
		cleaned_values = get_arr.line_up_dates_with_values_for_calculation(df_master=master_df,df_slave=slave_df,df_slave2=slave2_df,isolate=True,returning_lists=True)
		
		for lists in cleaned_values:
			if set(lists).intersection(set(sga.values)):
				sga.values = lists
			elif set(lists).intersection(set(revenue.values)):
				revenue.values = lists
			else:
				cogs.values = lists
			
		gross_profit = np.subtract( revenue.values,cogs.values )
		sga_to_gross_profit_ratios = list(map(lambda sga,gp: round((sga / gp) * 100, ndigits=2)  , sga.values,gross_profit   ))	
		
		
		return np.std(sga_to_gross_profit_ratios[0:6])
			
def TotalLiabilites_to_TotalAssets_ratio(total_liabilities_class,total_assets_class):
	pass
#need to check if there is either a total liabilites key or if there are current liabilites key and non current liabilites keys
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

