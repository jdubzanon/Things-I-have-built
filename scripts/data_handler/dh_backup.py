import pandas as pd
import requests
import json
import sqlite3
import pathlib
import sys

class InfoPasser:
	def __init__(self,ticker):
		self.ticker = ticker
		self.HEADER = {'User-Agent': 'thorntonbill343@gmail.com'}
		self.sector = None
		self.cikk = None
		self.parent_path = pathlib.Path.cwd().parent.parent
		self.file_path = f"{self.parent_path}/databases/sector_tables.db"

	def _cik_sector_getter(self):
		cik_con = sqlite3.connect(self.file_path)
		cik_cur = cik_con.cursor()
		cik_cur.execute(f'SELECT cik_number,sector FROM cik_data WHERE ticker="{self.ticker}"')
		info = cik_cur.fetchone()  # returns (cik_number,sector)
		self.cikk = info[0]
		self.sector = info[1]
		cik_con.close()

	def _company_facts_end_point_api_call(self):
		base_url = 'https://data.sec.gov/api/xbrl/companyfacts/CIK'
		full_url = f'{base_url}{str(self.cikk).zfill(10)}.json'
		api_call = requests.get(full_url,headers=self.HEADER)
		data = api_call.json()
		return data
		
	def main(self):
		self._cik_sector_getter()
		data = self._company_facts_end_point_api_call()
		return (data)



#info = InfoPasser('NVDA')
#result = info.main()

