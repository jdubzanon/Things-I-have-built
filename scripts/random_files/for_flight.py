#main_stock = 'TTFNF'
#main_company_name = 'TotalEnergies SE'

#stocks = [('TTFNF', 'TotalEnergies SE'), ('SHEL', 'Shell plc'), ('TTE', 'TotalEnergies SE'), ('RYDAF', 'Shell plc'), ('PCCYF', 'PETROCHINA CO LTD')]


#for index,stock in enumerate(stocks[1:],start=1):
#	if stock[0] == main_stock or stock[1] == main_company_name:
#		stocks.pop(index)
#print(stocks)
	
#import sqlite3
#import requests
#import json
#db_path = '/home/jdubzanon/hdd/Dev_projects/sec_project/databases/sector_tables.db'


#con = sqlite3.connect(db_path)
#cur = con.cursor()

##cur.execute('CREATE TABLE "American Depositary Receipts"(ticker,CompanyName,MarketCap)')
##con.commit()

#cur.execute('SELECT cik_number FROM cik_data WHERE ticker="AAPL"')
#tickers = cur.fetchone()
#cik_num = str(tickers[0]).zfill(10)
#con.close()
#header = {'User-Agent':"thorntonbill343@gmail.com"}
#print(cik_num)


####################making json_files#################

#from pathlib import Path as path
#import time
#import requests
#import json
#import pandas as pd

#header = {'User-Agent':"thorntonbill343@gmail.com"}
#data_frame_url = 'https://www.sec.gov/files/company_tickers.json'
#response = requests.get(data_frame_url,headers=header)
#json_obj = response.json()
#df = pd.DataFrame(json_obj).T
#for index, cik_num in enumerate(df.cik_str[0:100]):
#	json_url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{str(cik_num).zfill(10)}.json'
#	print(df.iloc[index].ticker)
#	json_response = requests.get(json_url,headers=header)
#	try:
#		json_data = json_response.json()
#		base_path = path('/home/jdubzanon/hdd/testfolder')
#		add_file = path(f'{df.iloc[index].ticker}.json')
#		full_path = path(f'{base_path}/{add_file}')
#		if not full_path.exists():
#			full_path.touch()
#			with open(full_path,'w') as f:
#				data = json.dumps(json_data)
#				f.write(data)
#	except:
#		continue
#	time.sleep(.5)

#####################end making json files###################

#####reading the json file stored on computer	
from pathlib import Path as path
from pathlib import PurePath as ppath
import os
import json
dir_path = ppath('/home/jdubzanon/hdd/testfolder')
list_of_json_files = list()
for file_name in os.listdir(dir_path):
	file_path = dir_path.joinpath(file_name)
	with open(file_path,'r') as fr:
		local_file = fr.read()	
		local_json = json.loads(local_file)
		list_of_json_files.append(local_json)

#		print(local_json.keys())	
	
	
	
	
	
	
	
	
	
	
	
	
