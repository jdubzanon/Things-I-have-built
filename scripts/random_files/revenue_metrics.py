#getting revenue for the designated ticker

import pandas as pd
import requests
import json
import numpy as np

ticker = 'NVDA'

#data frame for all tickers includes (ticker, company name, cik number)
HEADER = {'User-Agent': 'thorntonbill343@gmail.com'}
req = requests.get('https://www.sec.gov/files/company_tickers.json', headers=HEADER)
ciks = req.json()
ticker_df = pd.DataFrame(ciks).T
ticker_df.index = ticker_df['ticker']
#print(ticker_df)


#getting the cik number function

def cik_getter(ticker,d_frame):
    df = d_frame
    return df.loc[ticker]['cik_str']

#cikk = cik_getter(ticker,ticker_df)
#print(cikk)
    

def company_facts_end_point_api_call(ticker,d_frame,header):
	cikk = cik_getter(ticker,d_frame)
	base_url = 'https://data.sec.gov/api/xbrl/companyfacts/CIK'
	full_url = base_url + str(cikk).zfill(10) + '.json'
	api_call = requests.get(full_url,headers=header)
	data = api_call.json()
	return data




#getting the sector of tickers

def sector_getter(cikk,header):
    url = "https://data.sec.gov/submissions/CIK" + str(cikk).zfill(10) + '.json'
    req = requests.get(url, headers=header)
    j_son = req.json()
    return j_son['sicDescription']
    
#revenue calculations return all years and 5 yr avgs

def revenue_getter(ticker,d_frame,header):
#	cikk = cik_getter(ticker,d_frame)
#	base_url = 'https://data.sec.gov/api/xbrl/companyfacts/CIK'
#	full_url = base_url + str(cikk).zfill(10) + '.json'
#	api_call = requests.get(full_url,headers=header)
	data = data = company_facts_end_point_api_call(ticker,ticker_df,header)
	rev_arr = list()
	rev_columns = ['start','end','val','form']
	rev_df = pd.DataFrame(data['facts']['us-gaap']['Revenues']['units']['USD'],columns=rev_columns)
	rev_df.iloc[0]
	counter = 0

	for form in rev_df['form'][:]:
		if form == '10-K':
		    start_date = pd.to_datetime(rev_df.iloc[counter]['start'])
		    end_date = pd.to_datetime(rev_df.iloc[counter]['end'])
		    if all([((end_date - start_date).days > 300), rev_df.iloc[counter]['val'] not in rev_arr]):
		        #date_vals[df2.iloc[counter]['start']] = df2.iloc[counter]['val']
		        rev_arr.append(rev_df.iloc[counter]['val'])
		counter += 1


	
	return {'rev_mean_all_years': round(np.array(rev_arr).mean()),
			'rev_mean_last_five_years':  round(np.array(rev_arr[-5:]).mean()) }
	
	
rev_test = revenue_getter(ticker,ticker_df,HEADER)
print(rev_test)	
	
	
def cog_getter(ticker,d_frame,header):
	cogs_arr = list()
	cogs_columns = ['start','end','val','form']
	data = company_facts_end_point_api_call(ticker,d_frame,header)
	cogs_df = pd.DataFrame(data['facts']['us-gaap']['CostOfRevenue']['units']['USD'],columns=cogs_columns)
	counter = 0

	for cogs_form in cogs_df['form'][:]:
		if cogs_form == '10-K':
		    cogs_start_date = pd.to_datetime(cogs_df.iloc[counter]['start'])
		    cogs_end_date = pd.to_datetime(cogs_df.iloc[counter]['end'])
		    if all([(cogs_end_date - cogs_start_date).days > 300, cogs_df.iloc[counter]['val'] not in cogs_arr]):
		        cogs_arr.append(cogs_df.iloc[counter]['val'])
		counter += 1
		    # print(cogs_df['start'],cogs_df['end'])
	cogs_mean_all_years = round(np.array(cogs_arr).mean())
	cogs_mean_last_five_years = round(np.array(cogs_arr[-5:]).mean())
	
	return {"cogs_mean_all_years": round(np.array(cogs_arr).mean()),
			"cogs_mean_last_five_years ": round(np.array(cogs_arr[-5:]).mean())}

cog_test = cog_getter(ticker,ticker_df,HEADER)
print(cog_test)






































    
