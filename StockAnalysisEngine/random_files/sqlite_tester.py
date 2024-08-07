import sqlite3
import json
import pandas as pd
import numpy as np
import pathlib
import aiohttp
import asyncio
import time
from functools import lru_cache




def url_builder(tickers,session): #passing in ticker list from get_competitors function
	CompanyName_Tickermap = dict()	
	cik_number_list = list()

#   creating a dictionary mapping company name to ticker symbol
	for ticker in tickers:
		CompanyName_Tickermap[ticker[1].strip()] = ticker[0].strip()		
		current_path = pathlib.Path.cwd().parent.parent
		file_path = f"{current_path}/databases/sector_tables.db"

#		open datbase get cik numbers
		con = sqlite3.connect(file_path)
		cur = con.cursor()
		cur.execute(f'SELECT cik_number FROM cik_data WHERE ticker="{ticker[0]}"')
		cik_number_list.append(cur.fetchone())
	con.close()	

#	bulding urls
	if not session:
		url_list = None
	
	else:
		url_list = list()
		for cik_number in np.array(cik_number_list).flatten():
			url_list.append(session.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{str(cik_number).zfill(10)}.json") )
	#		url_list.append(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{str(cik_number).zfill(10)}.json") 		
		
	return (url_list,CompanyName_Tickermap)		


@lru_cache(maxsize=128) #if they use the same ticker again 
def get_competitors(ticker):
	current_path = pathlib.Path.cwd().parent.parent
	file_path = f"{current_path}/databases/sector_tables.db"

	#getting market cap
	con = sqlite3.connect(file_path)
	cur = con.cursor()
	cur.execute(f'SELECT sector FROM cik_data WHERE ticker="{ticker}"')
	sector = cur.fetchone() # returns (sector,)
	cur.execute(f'SELECT length(MarketCap), CompanyName FROM "{sector[0]}" WHERE Ticker="{ticker}"')
	m_cap_length = cur.fetchone()[0]

	#getting competitors 
	comp_list = list()
	
	
	count = 0
	while len(comp_list) < 5:

		cur.execute(
		
		f'SELECT Ticker, CompanyName FROM "{sector[0]}" WHERE length(MarketCap)={(m_cap_length+2) - count} AND Ticker != "{ticker}" ')
		comp_list.extend(cur.fetchall()
		
		)
		
		count += 1
		
		
		if count > 20:
	 		break
	cur.execute(f'SELECT ticker,CompanyName FROM "{sector[0]}" WHERE Ticker="{ticker}"')	
	comp_list.append(cur.fetchone())
	con.close()
	return comp_list




async def make_request():
	comp = get_competitors('CHD')
	header = {'User-Agent':'thorntonbill343@gmail.com'}
	json_list = list()
	
	async with aiohttp.ClientSession(headers=header) as session:
			task = url_builder(comp,session) 
			responses = await asyncio.gather(*task[0])
			for response in responses:
				json_list.append(await response.json())			
					
	return json_list	

def main(ticker):
	json_response_map = dict()
	competitors = get_competitors(ticker)
	TickerComapanyNameMapper = url_builder(tickers=competitors,session=None)[1]
	response_list = asyncio.run(make_request()) 
	for json in response_list:
		json_response_map[TickerComapanyNameMapper[json['entityName'.strip()]]] = json
				
	return json_response_map
	
#b = time.time()

#MAP = main('CHD')
#print(MAP.keys())
#print(MAP['CCYC']['entityName'])

#e = time.time()
#print(e-b)










