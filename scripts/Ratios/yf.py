import yfinance as yf
import pandas as pd
import requests
#i can use this for also for P/E ratio calculations

#can use for news as well

ms = yf.Ticker('AAPL')

#info = ms.info
#print(info.keys())

#ms_hstry = pd.DataFrame(ms.history(period='5y', interval='1mo'),columns=['Close'])

#print(ms.income_stmt.loc['Operating Revenue'])

for key in ms.balance_sheet.index:
	print(key)

#print(ms.balance_sheet.loc['Common Stock'])


#df = ms_inc.loc['Total Non Current Assets']
#print(df)

#revenue = ms_inc.loc['Total Revenue']
#print(revenue.values)
