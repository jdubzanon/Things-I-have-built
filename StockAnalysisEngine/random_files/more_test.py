import numpy as np

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
#####reading the json file stored on computer	
#file_path = path('/home/jdubzanon/hdd/testfolder/test.json')
#with open(file_path,'r') as fr:
#	local_file = fr.read()	
#	local_json = json.loads(local_file)
	
	
#vals = [-214000000, -3068000000, 5562000000, 14966000000, 70400000000, 98330000000, 96364000000, 92284000000, 87152000000, 104256000000, 101289000000, 62841000000, 37169000000, 19538000000, 13845000000]

#new_vals =[13845000000, 37169000000, 19538000000, 62841000000, 101289000000, 104256000000, 87152000000, 92284000000, 96364000000, 98330000000, 70400000000, 14966000000, 5562000000, -3068000000, -214000000]
#new_vals = np.flip(vals)
#p_list = list()

#for index,value in enumerate(new_vals,start=1):
#			
#	if index == len(new_vals):
#		break
#	num1 = value
#	num2 = new_vals[index]


#	# first and second are negative, first less than second
#	if all([num1 < 0,num1 < 0, num1 < num2]):
#		diff = abs(abs(num1) - abs(num2))
#		per = diff / abs(num1)
#		p_list.append(per)
#		print('first',num1,num2,diff,per)
#	# first and second negative first greater than second
#	if all([num1<0,num2<0,num1>num2 ]):
#		diff = abs(abs(num1) - abs(num2))
#		per = diff / num1
#		p_list.append(per)
#		print('2nd',num1,num2,diff,per)

#	#first number negative second number positive
#	if all([num1 < 0,num2 > 0]):
#		diff = abs(num1)+abs(num2)
#		per = diff / abs(num1) 
#		p_list.append(per)
#		print('3rd',num1,num2,diff,per)

#	# first number positive second negative
#	if all([num1>0,num2<0]):
#		diff = abs(num1)+abs(num2)
#		per = (diff / num1) * -1
#		p_list.append(per)
#		print('4th',num1,num2,diff,per)

#	# both numbers positive first number less than second number
#	if all([num1 < num2,num1>0,num2>0]):
#		diff = num2 - num1
#		per = diff / num1  
#		p_list.append(per)
#		print('5th',num1,num2,diff,per)
#	# both positive first number greater than second number
#	if all([num1 > num2, num1>0,num2>0]):
#		diff = num1 - num2
#		per = (diff / num1) * -100
#		p_list.append(per)
#		print('6th',num1,num2,diff,per)

#print(p_list)

#from collections import namedtuple

#test = namedtuple('start','finish')

#test.name = 5
#test.finish = [3,5,6,7]


#print(test.name)
#print(test.finish)

#lists = [1,1,1,1,1,1,1,1,1,1]
#for index,value in enumerate(lists,start=1):
#	print(index,len(lists))

#unsorted_dict = {'2013-09-28': 8165000000, '2014-09-27': 9571000000, '2015-09-26': 11247000000, '2016-09-24': 12734000000, 
#'2017-09-30': 12451000000, '2018-09-29': 13313000000, '2019-09-28': 10495000000, '2020-09-26': 7309000000, '2021-09-25': 11085000000, 
#'2022-09-24': 10708000000, '2007-09-29': 0, '2008-09-27': 0, '2009-09-26': 0, '2010-09-25': 0, '2011-09-24': 0, '2012-09-29': 0}

#new_dict = dict(sorted(unsorted_dict.items()))

#print(new_dict)

#print(unsorted_dict)
#import requests
#url = 'https://data.sec.gov/api/xbrl/companyfacts/CIK0000933974.json'
#headers = {'User-Agent': 'thorntonbill343@gmail.com'}
#response = requests.get(url,headers=headers)
#print(response.json()['entityName'])


vals = [-214000000, -3068000000, 5562000000, -14966000000, 45898000000, 70400000000, 98330000000, 96364000000, 92284000000, 87152000000, 104256000000, 101289000000, 62841000000, 37169000000, 19538000000]
											#  ^changed to neg
list_of_values = list()

for index,val in enumerate(vals):
	if index == len(vals)-1:
		break
	jump_forward = index + 1
	
#	print(val,vals[jump_forward])
	
	if all([val < 0, vals[jump_forward] < 0, abs(val) < abs(vals[jump_forward])]): #growth
		diff = abs(vals[jump_forward]) - abs(val)
		decimal = (diff / abs(val)) * 100
		list_of_values.append(round(decimal,ndigits=2))
	if all([val < 0, vals[jump_forward] < 0, abs(val) > abs(vals[jump_forward])]): #decline
		diff = abs(val) - abs(vals[jump_forward])
		decimal = (diff / val) * 100
		list_of_values.append(round(decimal,ndigits=2))
		
	if all([val < 0, vals[jump_forward] > 0]): #decline
		diff = abs(val - vals[jump_forward])
		decimal = (diff / val)*100
		list_of_values.append(round(decimal,ndigits=2))#growth
	if all([val > 0, vals[jump_forward] < 0  ])	:
		diff = val + abs(vals[jump_forward])
		decimal = (diff / val) * 100
		list_of_values.append(round(decimal,ndigits=2))
	if any([all([val > 0, vals[jump_forward] > 0, val > vals[jump_forward]]), all([val > 0, vals[jump_forward] > 0, val < vals[jump_forward]])     ]): #growth/decline
		diff = val - vals[jump_forward]
		decimal = (diff / val) * 100
		list_of_values.append(round(decimal,ndigits=2))


print(list_of_values)






	
	



