import requests 
import asyncio
import json
import yfinance as yf
import time
import pandas as pd


#async def req():
#	ticker = yf.Ticker('brk-b')
#	info = ticker.balance_sheet
#	try:
#		series = info.loc['Inventory']
#	except KeyError:
#		series = {'cant get data':'cant get data'}
#	print(series)

#async def req2():
#	for stocks in ['aapl','brk-b','pg']:
#		ticker = yf.Ticker(stocks)
#		info = ticker.balance_sheet
#		try:
#			series = info.loc['Inventory']
#			arr = list(map(lambda values: int(values),series[pd.notna(series)].values ))	
#		except:
#			arr = {'cant get data':'cant get data'}
#		
#		print(arr)

async def req():
	headers = {'User-Agent': 'thorntonbill343@gmail.com'}
	url = 'https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json'
	res = requests.get(url,headers=headers)
	print(res.json()['entityName'])

async def req2():
	headers = {'User-Agent': 'thorntonbill343@gmail.com'}
	url = 'https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json'
	res = requests.get(url,headers=headers)
	print(res.json()['entityName'])
	


async def count():
	print('one')
	await req()
	await req2()
	print('two')

async def main():
	await asyncio.gather(count(),count(),count())
	
asyncio.run(main())


#for stocks in ['aapl','wmt','pg']:
#	ticker = yf.Ticker(stocks)
#	info = ticker.balance_sheet
#	series = info.loc['Inventory']
#	arr = series[pd.notna(series)].values
#	print(arr)


















