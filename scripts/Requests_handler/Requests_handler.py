import sys
##for gedit 
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/webpage/bin')
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/scripts')
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/webpage/lib/python3.10/site-packages')
sys.path.append('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts')
sys.path.append('/home/jdubzanon/hdd/envornments/webpage/lib/python3.10/site-packages')

import unicodedata
import sqlite3
import json
import numpy as np
import pathlib
import aiohttp
import asyncio
from functools import lru_cache
import time

class RequestHandler:
	def __init__(self,ticker):
		self.ticker = ticker
		
	
	
	def url_builder(self,tickers,session):
		CompanyName_Tickermap = dict()	
		cik_number_list = list()
#   creating a dictionary mapping company name to ticker symbol
		for ticker in tickers:
			CompanyName_Tickermap[ticker[1].strip()] = ticker[0].strip()		
			current_path = pathlib.Path.cwd().parent.parent
			file_path = f"{current_path}/databases/StocksDatabase.db"

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
	def get_competitors(self):
		current_path = pathlib.Path.cwd().parent.parent
		file_path = f"{current_path}/databases/StocksDatabase.db"

		#getting market cap of company being searched
		con = sqlite3.connect(file_path)
		cur = con.cursor()
		cur.execute(f'SELECT sector FROM cik_data WHERE ticker="{self.ticker}"')
		sector = cur.fetchone() # returns (sector,)
		cur.execute(f'SELECT length(MarketCap), CompanyName FROM "{sector[0]}" WHERE Ticker="{self.ticker}"')
		try:
			m_cap_length = cur.fetchone()[0]
			if m_cap_length is None:
				m_cap_length = 10
		except TypeError:
			return None
		#getting competitors by market cap 
		comp_list = list()
		#adding given stock to comp_list
		cur.execute(f'SELECT ticker,CompanyName FROM "{sector[0]}" WHERE Ticker="{self.ticker}"')	
		comp_list.append(cur.fetchone())
		count = 0
		while len(comp_list) < 5:

			cur.execute(f'SELECT Ticker, CompanyName FROM "{sector[0]}" WHERE length(MarketCap)={(m_cap_length+2) - count} AND Ticker != "{self.ticker}" ')
			
			comp_list.extend(cur.fetchall())
			
			count += 1
			
			
			if count > 20:
		 		break
		con.close()
		
		while len(comp_list) > 10:
			comp_list.pop()
#		print(comp_list) ##<-----------------------get list of competitors
		#getting rid of duplicates in list of competitors
		main_stock = comp_list[0][0]
		main_company_name = comp_list[0][1]
		for index,stock in enumerate(comp_list[1:],start=1):
			if stock[0] == main_stock or stock[1] == main_company_name:
				comp_list.pop(index)
		return comp_list
		
		
		
		
	async def make_request(self):
		competitors = self.get_competitors()
		if competitors:
			header = {'User-Agent':'email'}
			json_list = list()
			company_ticker_map = None
			async with aiohttp.ClientSession(headers=header) as session:
					urls = self.url_builder(competitors,session) #returns list of urls and a dictionary mappig company name to tickers 
					company_ticker_map = urls[1]
					responses = await asyncio.gather(*urls[0])
					for response in responses:
						json_list.append(await response.json())			
							
			return json_list,company_ticker_map	
		else:
			return None
	
	def main(self):
		user_ticker_dict = dict()
		competitor_tickers_dict = dict()
		competitors = self.get_competitors()
		user_ticker = dict()
		if competitors:
			response_list = asyncio.run(self.make_request()) #returns jsons from request and comapany_ticker_map
			for json in response_list[0]:
				if response_list[1][unicodedata.normalize('NFKD',json['entityName'].strip())] == self.ticker:
#					user_ticker_dict[response_list[1][json['entityName']]] = json
					user_ticker_dict[response_list[1][unicodedata.normalize('NFKD',json['entityName'])]] = json									
				
				elif response_list[1][unicodedata.normalize('NFKD',json['entityName'].strip())] != self.ticker:
					competitor_tickers_dict[response_list[1][unicodedata.normalize('NFKD',json['entityName'])]] = json

	#			json_response_map[response_list[1][json['entityName'.strip()]]] = json
			
			
			return user_ticker_dict,competitor_tickers_dict,response_list[1] ##returns {main ticker:json},{competitors:jsons} {company_names : tickers}
		else: #if there are no competitors 
			return None

	
#request = RequestHandler('MDLZ')
#comp = request.get_competitors()
#url = request.url_builder(comp,session=None)
#request.main()

#print(comp)
	
	
	
	
	
	
