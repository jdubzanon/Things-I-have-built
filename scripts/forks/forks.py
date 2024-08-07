import sys
##for gedit 
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/webpage/bin')
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/scripts')
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/webpage/lib/python3.10/site-packages')
sys.path.append('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts')
sys.path.append('/home/jdubzanon/hdd/envornments/webpage/lib/python3.10/site-packages')
#########
import pandas as pd
import json
import numpy as np
import time
import requests
import yfinance as yf

def fork(ticker_id,statement,keys,keep_float=False):
	
	call_ticker = yf.Ticker(ticker_id)
	
	statement_identifier = { 
	'cashflow' : call_ticker.cashflow,
	'income' : call_ticker.income_stmt,
	'balance_sheet' : call_ticker.balance_sheet	
	}
	financial_statement = statement_identifier[statement]
	key = list(filter(lambda key: key in financial_statement.index, keys))
	if key:
		series = financial_statement.loc[key[0]]
		if keep_float:
 			arr = list(series[pd.notna(series)].values)
		else:
			arr = list(map(lambda values: int(values),series[pd.notna(series)].values ))
		return arr
	else:	
		arr =  {'from fork':'cant make calculations'}
		return arr
		










	
