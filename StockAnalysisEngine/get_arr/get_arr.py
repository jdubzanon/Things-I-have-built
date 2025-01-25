import numpy as np
import pandas as pd


def get_arr_without_start_date(generic_dataframe):
	'''long term liabilites category doesnt report a start date so i altered the way i get the values from the data frame and i dropped duplicates  '''
	possible_form = ['20-F','40-F','10-K','20-F/A']
	form = list(np.unique( list(filter(lambda forms: forms in possible_form, generic_dataframe.form   ))  ))
	
	if not form:
		return {'mean_all(W/O start_date)': 'No information available', 'mean_last_five': 'no information available'}
	
	else:
		get_arr_info = np.flip(np.array(generic_dataframe[generic_dataframe.form == form[0]].drop_duplicates(subset='end')['val']     )    )
		
		return list(get_arr_info)
	


def get_arr(generic_dataframe):
	columns = ['start','end','val','form']
	possible_form = ['20-F','40-F','10-K','20-F/A']
	form = list(np.unique(list(filter(lambda forms: forms in possible_form, generic_dataframe.form))))

	if not form:
		return {'mean_all_no_form_get_arr_norm': 'No information available', 'mean_last_five_no_form_get_arr_norm': 'no information available'}
	
	get_info_arr = np.flip(  np.array(  generic_dataframe[(generic_dataframe.form == form[0]) & 
						
						(( pd.to_datetime(generic_dataframe.end) -  pd.to_datetime(generic_dataframe.start) ) > "300 days" )   ].drop_duplicates()['val']   )   )				
			
	return list(get_info_arr)
	


def line_up_dates_with_values_for_calculation(df_master,df_slave,df_slave2=None,df_slave3=None,df_slave4=None,subtracting=False,returning_lists=False,isolate=False):
	#put values in a dictionary values organized by dates add them together 
	master_dict = dict()
	master_arr = list()
	
	slave_dict = dict()
	slave_arr = list()
	
	slave2_dict = dict()
	slave2_arr = list()
	
	slave3_dict = dict()
	slave3_arr = list()
	
	slave4_dict = dict()
	slave4_arr = list()
	
	returning_list = list()

	possible_form = ['20-F','40-F','10-K','20-F/A']
	master_form = list(np.unique(list(filter(lambda forms: forms in possible_form, df_master.form))))
	
	if not master_form:
		return {'mean_five':'no info reported'}
	
	if all([ 'start' in df_master.columns, 'end' in df_master.columns ]):
		master_df = df_master.loc[ ( df_master.form == master_form[0])  & (( pd.to_datetime(df_master.end) -  pd.to_datetime(df_master.start) ) > "300 days"  ) ].drop_duplicates(subset='end')
		master_df.index = range(len(master_df))		
		
	else:
		master_df = df_master.loc[(df_master.form == master_form[0])].drop_duplicates()	
		master_df.index = range(len(master_df))
		
	slave_form = list(np.unique(list(filter(lambda forms: forms in possible_form, df_slave.form))))
	
	# slave start
	
	if not slave_form:
		return {'mean_five':'no info reported'}

	if all(['start' in df_slave.columns, 'end' in df_slave.columns  ]):
		slave_df = df_slave.loc[  ( df_slave.form == slave_form[0])  & (( pd.to_datetime(df_slave.end) -  pd.to_datetime(df_slave.start) ) > "300 days" )   ].drop_duplicates(subset='end')
		slave_df.index = range(len(slave_df))

	else:
		slave_df = df_slave.loc[  (df_slave.form == slave_form[0]) ].drop_duplicates(subset='end')
		slave_df.index = range(len(slave_df))

	#slave 2 start
	
	if not df_slave2 is None:
		slave2_form = list(np.unique(list(filter(lambda forms: forms in possible_form, df_slave2.form))))
		
		if not slave2_form:
			return {'mean_five':'no info reported'}
		
		if all(['start' in df_slave2.columns, 'end' in df_slave2.columns  ]):
			slave2_df = df_slave2.loc[  ( df_slave2.form == slave2_form[0])  & (( pd.to_datetime(df_slave2.end) -  pd.to_datetime(df_slave2.start) ) > "300 days" )   ].drop_duplicates(subset='end')
			slave2_df.index = range(len(slave2_df))

		else:
			slave2_df = df_slave2.loc[  (df_slave2.form == slave2_form[0]) ].drop_duplicates(subset='end')
			slave2_df.index = range(len(slave2_df))
	
	#slave3 start
		
	if not df_slave3 is None:
		
		slave3_form =  list(np.unique(list(filter(lambda forms: forms in possible_form, df_slave3.form))))
		
		if not slave3_form:
			return {'mean_five':'no info reported'}	

		if all(['start' in df_slave3.columns, 'end' in df_slave2.columns ]):
			slave3_df = df_slave3.loc[ ( df_slave3.form == slave3_form[0])  & (( pd.to_datetime(df_slave3.end) -  pd.to_datetime(df_slave3.start) ) > "300 days" )  ].drop_duplicates(subset='end')
			slave3_df.index = range(len(slave3_df))
		else:
			slave3_df = df_slave3.loc[ (df_slave3.form == slave3_form[0])  ].drop_duplicates(subset='end')
			slave3_df.index = range(len(slave3_df))

	if not df_slave4 is None:
		
		slave4_form = list(np.unique(list(filter(lambda forms: forms in possible_form, df_slave4.form))))
		
		if not slave4_form:
			return {'mean_five':'no info reported'}
			
		if all(['start' in df_slave4.columns, 'end' in df_slave4.colums    ]):
			slave4_df = df_slave4.loc[ ( df_slave4.form == slave4_form[0])  & (( pd.to_datetime(df_slave4.end) -  pd.to_datetime(df_slave4.start) ) > "300 days" )  ].drop_duplicates(subset='end')
			slave4_df.index = range(len(slave4_df))
		else:
			slave4_df = df_slave4.loc[ (df_slave4.form == slave4_form[0])].drop_duplicates(subset='end')
			slave4_df.index = range(len(slave4_df))

	#have all the same dates with values in dictionary so i can add them up together regardless if they have a value

	for num in slave_df.index: #creating slave dictionary
		slave_tmp_series = slave_df.iloc[num]
		slave_dict[slave_tmp_series.end] = slave_tmp_series.val

	if not df_slave2 is None: #creating slave2 dictionary if it exist
		for num in slave2_df.index:
			slave2_tmp_series = slave2_df.iloc[num]
			slave2_dict[slave2_tmp_series.end] = slave2_tmp_series.val
	
	if not df_slave3 is None:
		for num in slave3_df.index: # creating slave3 dictionary
			slave3_tmp_series = slave3_df.iloc[num]
			slave3_dict[slave3_tmp_series.end] = slave3_tmp_series.val
	
	if not df_slave4 is None:
		for num in slave4_df.index: #creating slave4 dictionary
			slave4_tmp_series = slave4_df.iloc[num]
			slave4_dict[slave4_tmp_series.end] = slave4_tmp_series.val
	
	
	for num in master_df.index:
		master_tmp = master_df.iloc[num] #getting series
		master_dict[master_tmp.end] = master_tmp.val  # creating {date:val}
		if not master_tmp.end in slave_dict.keys():
			slave_dict[master_tmp.end] = 0 #addind dates to other dictionary {date:val}
		
		if not df_slave2 is None:
			if not master_tmp.end in slave2_dict.keys():
				slave2_dict[master_tmp.end] = 0 #addind dates to other dictionary {date:val}

		if not df_slave3 is None:
			if not master_tmp.end in slave3_dict.keys():
				slave3_dict[master_tmp.end] = 0 #addind dates to other dictionary {date:val}
				
		if not df_slave4 is None:
			if not master_tmp.end in slave4_dict.keys():
				slave4_dict[master_tmp.end] = 0	#addind dates to other dictionary {date:val}			

	
	for date in master_dict: #putting values into each respective list
		master_arr.append(master_dict[date])
		slave_arr.append(slave_dict[date])
		if not df_slave2 is None:
			slave2_arr.append(slave2_dict[date])	
		if not df_slave3 is None:
			slave3_arr.append(slave3_dict[date])
		if not df_slave4 is None:
			slave4_arr.append(slave4_dict[date])


#	isolate dates that all have values to add together
	master_isolated_values = list()
	slave_isolated_values = list()
	slave2_isolated_values = list()
	slave3_isolated_values = list()
	slave4_isolated_values = list()
	
	
	if all([isolate == True, df_slave2 is None  ]): #if no df_slave2 then only master and slave
		
		for master,slave in zip(master_arr,slave_arr):
			if all([master != 0, slave !=0 ]):
				master_isolated_values.append(master)
				slave_isolated_values.append(slave)
	
	if all([isolate == True, not df_slave2 is None,df_slave3 is None, df_slave4 is None    ]): #if not df_slave2 is None then master,slave and slave2
		for master,slave,slave2 in zip(master_arr,slave_arr,slave2_arr):
			if all([ master !=0, slave != 0 , slave2 != 0]):
				master_isolated_values.append(master)
				slave_isolated_values.append(slave)
				slave2_isolated_values.append(slave2)
		
				
	if all([ isolate == True, not df_slave2 is None,not df_slave3 is None, df_slave4 is None]): 
		for master,slave,slave2,slave3 in zip(master_arr,slave_arr,slave2_arr,slave3_arr):
			if all([ master !=0, slave != 0 , slave2 != 0,slave3 != 0]):
				master_isolated_values.append(master)
				slave_isolated_values.append(slave)
				slave2_isolated_values.append(slave2)
				slave3_isolated_values.append(slave3)
	
	if all([ isolate == True, not df_slave2 is None, not df_slave3 is None, not df_slave4 is None]):
		for master,slave,slave2,slave3,slave4 in zip(master_arr,slave_arr,slave2_arr,slave3_arr,slave4_arr):
			if all([ master != 0, slave !=0, slave2 != 0,slave3 != 0 ,slave4 != 0]):
				master_isolated_values.append(master)
				slave_isolated_values.append(slave)
				slave2_isolated_values.append(slave2)
				slave3_isolated_values.append(slave3)
				slave4_isolated_values.append(slave4)		
	
	
	if subtracting:
		return list(np.subtract(master_arr,slave_arr)) 
	
	if returning_lists:
		if all([ isolate == True, not df_slave2 is None, not df_slave3 is None, not df_slave4 is None]):
			return (master_isolated_values,
			slave_isolated_values,
			slave2_isolated_values,
			slave3_isolated_values,
			slave4_isolated_values)
		
		elif all([ not isolate, not df_slave2 is None, not df_slave3 is None, not df_slave4 is None]):
			return (master_arr,slave_arr,slave2_arr,slave3_arr,slave4_arr)
		
		elif all([ isolate == True, not df_slave2 is None,not df_slave3 is None, df_slave4 is None]):
			return (master_isolated_values,
			slave_isolated_values,
			slave2_isolated_values,
			slave3_isolated_values)
		
		elif all([isolate == False, not df_slave2 is None,not df_slave3 is None, df_slave4 is None ]):
			return (master_arr,slave_arr,slave2_arr,slave3_arr)
		
		elif all([isolate == True, not df_slave2 is None,df_slave3 is None, df_slave4 is None    ]):
			return (master_isolated_values,
			slave_isolated_values,
			slave2_isolated_values)
		
		elif all([ isolate == False, not df_slave2 is None,df_slave3 is None, df_slave4 is None ]):
			return (master_arr,slave_arr,slave2_arr)
		
		elif all([isolate == True,df_slave2 is None, df_slave3 is None, df_slave4 is None    ]): #working here <---------- receivables to revenue
#			print(master_isolated_values)
			return (master_isolated_values,slave_isolated_values)
		
		
		elif all([isolate == False, df_slave2 is None, df_slave3 is None, df_slave4 is None  ]):
			return (master_arr,slave_arr)
		
#		else:			
#			return ( master_arr,slave_arr  )
	
	return list(np.sum([ master_arr,slave_arr ], axis=0))
	

		

def add_multiple_to_get_values(*args):
#not pretty but it works
	adjusted_list = list()
	shortest_list_length = 100
	for each_list in args:
		if isinstance(each_list,dict):
			return {'from_add_multiple': 'cant_make_calculations'}
		
		if not len(each_list):
			continue
		if len(each_list) < shortest_list_length:
			shortest_list_length = len(each_list)		
	for each_list in args:
		if each_list:
			while len(each_list) > shortest_list_length:
				each_list.pop()
			adjusted_list.append(each_list)
	return list(np.sum(np.array(adjusted_list),axis=0)	)


def subtract_two_arrays(arr1,arr2):

	shortest_list_length = min(len(arr1),len(arr2))
	while len(arr1) > shortest_list_length:
		arr1.pop()
	while len(arr2) > shortest_list_length:
		arr2.pop()
	
	return np.subtract(arr1,arr2)


		
		
		
		
		
		
		
		








