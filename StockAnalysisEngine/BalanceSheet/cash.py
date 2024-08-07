import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent) )   


import pandas as pd
import key_handler.key_handler as kh
import get_arr.get_arr as get_arr
import forks.forks as fork



class cash:
	def __init__(self,ticker):
		self.ticker = ticker
		self.cash_key = None
		self.cash_df = None
		self.cash_arr = None
		self.unit = None
		self.forked = False
		
	def get_cash_values(self,company_facts,start_fork=False):
		
		if start_fork == True:
			self.forked = True
			self.cash_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=['Cash And Cash Equivalents'])
			if isinstance(self.cash_arr,dict):
				self.cash_arr = {'from cash':'cant make calculations'}
			return self.cash_arr
		
		possible_cash_key = ['CashAndCashEquivalentsAtCarryingValue','CashAndCashEquivalents']
		accounting_key = kh.get_accounting_key(company_facts,possible_cash_key)
		self.cash_key = list(filter(lambda key: key.strip() in company_facts['facts'][accounting_key[0]].keys(), possible_cash_key  ))

		if not self.cash_key:
			self.forked = True
			self.cash_arr = fork.fork(ticker_id=self.ticker,statement='balance_sheet',keys=['Cash And Cash Equivalents'])
			if isinstance(self.cash_arr,dict):
				self.cash_arr = {'from cash':'cant make calculations'}
			return self.cash_arr
		

		if len(self.cash_key) > 1:
			self.cash_key = kh.sort_out_multiple_reporting_keys(company_facts,accounting_key,self.cash_key)
			
		self.unit = kh.set_unit_key(company_facts,accounting_key,self.cash_key)
		
		self.cash_df = pd.DataFrame(company_facts['facts'][accounting_key[0]][self.cash_key[0]]['units'][self.unit[0]]  ).drop_duplicates(subset='end')
		
		try:
			self.cash_arr = get_arr.get_arr(self.cash_df)

		except AttributeError:
			self.cash_arr = get_arr.get_arr_without_start_date(self.cash_df)
		
		return self.cash_arr




# from pathlib import PurePath as ppath

# dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
# single_file = 'AAPL.json'
# final_path = dir_path / single_file
# ticker = single_file[0:-5]
# with open(final_path,'r') as fr:
# 	local_file = fr.read()
# 	local_json = json.loads(local_file)
# 	c = cash(ticker)
# 	cv = c.get_cash_values(local_json,start_fork=True)
# 	print(cv)			


#dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
#dir_path = ppath('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/json_files')
#for file_name in sorted(os.listdir(dir_path)):
#	file_path = dir_path.joinpath(file_name)
#	with open(file_path,'r') as fr:
#		local_file = fr.read()	
#		local_json = json.loads(local_file)
#		ticker = file_name[0:-5]
#		print(ticker)
#		c = cash(ticker)
#		cv = c.get_cash_values(local_json)
#		print(cv)			









#headers = {'User-Agent': 'thorntonbill343@gmail.com'}
#url = 'https://www.sec.gov/files/company_tickers.json'
#response = requests.get(url,headers=headers)
#json = response.json()
#df = pd.DataFrame(json).T	



##########################################
#df.index = df.ticker
#sample = df.loc['LTMAY']
#sample_cik = str(sample.cik_str).zfill(10)
#sample_ticker = sample.ticker
#url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'


#response = requests.get(url,headers=headers)

#c = cash(sample_ticker)
#test = c.get_cash_values(response.json())
##print(test)

#try:
#	for key in response.json()['facts']['us-gaap'].keys():
#		if 'Cash' in key:
#			print(key)
#except KeyError:
#	for key in response.json()['facts']['ifrs-full'].keys():
#		if 'Cash' in key:
#			print(key)

#	
#for num in range(70,100):
#	
#	sample = df.iloc[num]
#	sample_cik = str(sample.cik_str).zfill(10)
#	sample_ticker = sample.ticker
#	url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'
#	print(sample_ticker)
#	response = requests.get(url,headers=headers)

#	try:
#		data = response.json()
#	except:
#		continue
#	c = cash(sample_ticker)
#	test = c.get_cash_values(response.json())

#	print(test)
#	time.sleep(1)
	













