import sys
##for gedit 
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/webpage/bin')
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/scripts')
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/webpage/lib/python3.10/site-packages')
sys.path.append('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts')
sys.path.append('/home/jdubzanon/hdd/envornments/webpage/lib/python3.10/site-packages')

import time
import requests
import numpy as np
import pandas as pd

from Requests_handler.Requests_handler import RequestHandler 
#balance sheet
from BalanceSheet.cash import cash
from BalanceSheet.CurrentAssets import CurrentAssets
from BalanceSheet.CurrentLiabilities import CurrentLiabilities
from BalanceSheet.inventory import inventory
from BalanceSheet.LiabilitiesAndStockholdersEquity import LiabilitiesAndStockholdersEquity
from BalanceSheet.LongTermDebt import LongTermDebt
from BalanceSheet.NonCurrentLiabilities import NonCurrentLiabilities
from BalanceSheet.NonCurrentAssets import NonCurrentAssets
from BalanceSheet.receivables import receivables
from BalanceSheet.RetainedEarnings import RetainedEarnings
from BalanceSheet.ShareholdersEquity import ShareholdersEquity
from BalanceSheet.SharesOutstanding import SharesOutstanding
from BalanceSheet.TotalAssets import TotalAssets
from BalanceSheet.TotalLiabilities import TotalLiabilities
#income statement
from IncomeStatement.cogs import Cogs
from IncomeStatement.EarningsPerShare import EarningsPerShare
from IncomeStatement.InterestExpense import InterestExpense
from IncomeStatement.NetProfit import NetProfit
from IncomeStatement.OperatingExpense import OpExpense
from IncomeStatement.OperatingIncome import OpIncome
from IncomeStatement.revenue import Revenue
from IncomeStatement.sga import sga
from IncomeStatement.TaxesPaid import TaxesPaid
#cashflow statement
from CashflowStatement.capex import capex
from CashflowStatement.CashflowOperations import cashflow_operations
from CashflowStatement.Dividends import Dividends
#ratios
from Ratios import CashLiabilitiesRatio 
from Ratios import CurrentRatio 
from Ratios import DebtEquityRatio
from Ratios import DebtRatio
from Ratios import FreeCashflow
from Ratios import GrossProfitRevenueRatio
from Ratios import IntExpenseOpIncomeRatio
from Ratios import LongTermDebtNetIncomeRatio
from Ratios import OperatingProfitMargin
from Ratios import Pretax
from Ratios import PretaxEPS
from Ratios import ReceivablesRevenueRatio
from Ratios import ReturnOnAssets
from Ratios import ReturnOnCapital



class StockMetrics:
	def __init__(self,ticker):
		self.ticker = ticker
		
		#from request_handler module		
		self.ticker_json = None  #company searched
		self.competitor_jsons = None #competitors json files
		self.CompanyName_to_TickerMap = None
		self.Ticker_to_CompanyName = dict()
		
		#from revenue module
		self.Revenue = Revenue(self.main_ticker)
		self.revenue_values = None

#		#from interest_expense module
		self.IntExp = IntExp(self.main_ticker)
		self.IntExp_vaules = None		
#		
#		#from OpIncome module
		self.OpIncome = op(self.main_ticker)
		self.OpIncome_values = None

#		#from cogs module (Cost Of Goods Sold)
		self.cogs = Cogs(self.main_ticker)
		self.cogs_values = None
#		
#		#from net profit module
		self.net_profit = NetProfit(self.main_ticker)
		self.net_profit_values = None
#		
#		#from longtermdebt module
		self.long_term_debt = LongTermDebt(self.main_ticker)
		self.long_term_debt_values = None
#		
#		#from ShareholdersEquity module
		self.Shareholders_eq = ShareholdersEquity(self.main_ticker)
		self.Shareholders_eq_values = None
#		
#		#from TotalLiabilities module
		self.TotalLiabilities = TotalLiabilities(self.main_ticker)
		self.TotalLiabilities_values = None
#		
#		#from RetainedEarnings module
		self.RetainedEarnings = RetainedEarnings(self.main_ticker)
		self.RetainedEarnings_values = None
#		
		self.GrossProfit = GrossProfit(self.main_ticker)
		self.GrossProfit_values = None
#		
##		from sga module
		self.sga = sga(self.main_ticker)
		self.sga_values = None
#		
#		#revenue growth calculations
		self.ticker_revenue = dict()
		self.competitor_revenue = dict()
#		
#		#gross_profit_analysis
		self.ticker_GrossProfitMargin = dict()
		self.competitor_gp_percent_of_revenue = dict()
#		
#		#Interest Expense to OperatingIncome ratio
		self.IntExp_OpIncome_ratio = dict()
		self.competitor_IntExp_OpIncome_ratio = dict()
#		
#		#operating income to revenue ratio
		self.OpIncome_revenue_ratio = dict()
		self.competitor_OpIncome_revenue_ratio = dict()
		
#		#net profit growth calculations
		self.net_profit_growth = dict()
		self.competitor_net_profit_growth = dict()
		
#		#long_term_debt to net_profit ratio
		self.ltd_to_net_profit = dict()
		self.comp_ltd_to_net_profit = dict()
		
#		##debt to equit ratio
		self.debt_to_equity_ratio = dict()
		self.competitor_debt_to_equity_ratio = dict()
		
#		#retain_earnings yoy growth 
		self.RetainedEarnings_growth = dict()
#		
#		#gross profit to sga analysis
		self.gross_profit_sga_ratio_value = dict()
		
		
		repsone = RequestHandler(ticker)
		response_data = repsone.main()
		self.main_ticker_json = response_data[0] #{main_ticker:json}
		self.competitor_jsons = response_data[1] #{competitors:jsons}
		self.CompanyName_to_TickerMap = response_data[2] #{CompanyName:ticker}
		if self.CompanyName_to_TickerMap:
			for CompanyName,Ticker in self.CompanyName_to_TickerMap.items():
				self.Ticker_to_CompanyName[Ticker] = CompanyName
	
#				#GETTING VALUES SECTIONS
#		getting revenue values
		self.Revenue.get_revenue_values(self.main_ticker_json[self.main_ticker])
		
#		getting IntExp values
		self.IntExp_vaules = self.IntExp.get_InterestExpense_values(self.main_ticker_json[self.main_ticker]) 

#		getting OpIncome values
		self.OpIncome_values = self.OpIncome.get_OpIncome_values(self.main_ticker_json[self.main_ticker])

#		getting cogs values
		self.cogs_values = self.cogs.get_cog_values(self.main_ticker_json[self.main_ticker])
		
#		getting net profit values
		self.net_profit_values = self.net_profit.get_NetProfit_values(self.main_ticker_json[self.main_ticker])
		
#		getting long_term_debt values
		self.long_term_debt_values = self.long_term_debt.get_LongTermDebt_values(self.main_ticker_json[self.main_ticker]) #<---- do i need this
		
#		gettine shareholders_eq values
#		self.Shareholders_eq_values = self.Shareholders_eq.get_ShareholdersEquity_values(self.main_ticker_json[self.main_ticker])

#		getting TotalLiabilities values
		self.TotalLiabilities_values = self.TotalLiabilities.get_TotalLiabilities_values(self.main_ticker_json[self.main_ticker])
		
#		getting RetainedEarnings values
		self.RetainedEarnings_values = self.RetainedEarnings.get_RetainedEarnings_values(self.main_ticker_json[self.main_ticker])
		
#		getting GrossProfit values
		self.GrossProfit_values = self.GrossProfit.get_GrossProfit_values(self.main_ticker_json[self.main_ticker])
	
#		getting sga values
		self.sga_values = self.sga.get_sga_values(self.main_ticker_json[self.main_ticker])


	def revenue_metrics(self,revenue_list): #go through year by year checking if revenue grew or shrunk return the avg
		
		return call.growth_calculate(revenue_list) #calling from func_4_metrics directoy
	
	def OpInc_to_revenue_ratio(self,revenue_arr,OpInc_arr): #divide operating income avg by revenue avg

		return call.get_ratio_from_two_arrays_using_array_avgs(arr1=revenue_arr,arr2=OpInc_arr)	#calling from func_4_metrics directoy	
	
	def IntExp_to_OpIncome(self,OpIncome_arr,IntExp_arr): # divide IntExp avg by OpIncome avg
		
		return call.get_ratio_from_two_arrays_using_array_avgs(arr1=OpIncome_arr,arr2=IntExp_arr)		

	def NetProfit_growth(self,net_profit_values):
		
		return call.growth_calculate(net_profit_values)

	def long_term_debt_to_net_income_ratio(self,long_term_debt_arr,net_profit_arr): #pass classes,use df to get values and ratio
		
		return call.divide_multiple_to_get_ratio(long_term_debt_arr,net_profit_arr)
	
	def DebtToEquityRatio(self,total_liabilities,shareholders_eq):
		
		return call.divide_multiple_to_get_ratio(total_liabilities,shareholders_eq)
	
	def gross_profit_analysis(self,revenue_df,cogs_df):
	
		return call.GrossProfit_percent_of_revenue(revenue_df,cogs_df)
	
	def retain_earnings_growth(self,RetainedEarnings_values,RetainedEarnings_key):
	
		return call.RetainedEarnings_growth(RetainedEarnings_values,RetainedEarnings_key)
	
	def gross_profit_sga_ratio(self,rev_class,cogs_class,sga_class):
		
		return call.sga_to_gross_profit_ratio(rev_class,cogs_class,sga_class)
	
	def get_all_metrics(self):
###		#revenue growth metrics
		self.main_ticker_revenue[self.main_ticker] = self.revenue_metrics(revenue_list=self.revenue_values)
#				
###		#interest expense to operating income ratio
		self.IntExp_OpIncome_ratio = self.IntExp_to_OpIncome(self.OpIncome_values,self.IntExp_vaules) 	
		for ticker in self.competitor_jsons:
			IntExp = self.IntExp.get_InterestExpense_values(self.competitor_jsons[ticker])
			OpIncome = self.OpIncome.get_OpIncome_values(self.competitor_jsons[ticker])
			self.competitor_IntExp_OpIncome_ratio[ticker] = self.IntExp_to_OpIncome(self.OpIncome_values,self.IntExp_vaules)


###		#net_profit growth_calculate
		self.net_profit_growth[self.main_ticker] = self.NetProfit_growth(self.net_profit_values)
		
####	long_term_debt to net_profit calculations <-- yrs till paid off
		self.ltd_to_net_profit[self.main_ticker] = self.long_term_debt_to_net_income_ratio(self.long_term_debt_values,self.net_profit_values)

####		debt to equity ratio
		self.debt_to_equity_ratio[self.main_ticker] = self.DebtToEquityRatio(self.TotalLiabilities_values,self.Shareholders_eq_values)
		
###		gross profit percent of revenue
		self.main_ticker_gp_percent_of_revenue[self.main_ticker] = self.gross_profit_analysis(self.Revenue.revenue_df,self.cogs.cogs_df)

#		retained earnings growth		


#app=StockMetrics('BRK-B')

#test = app.long_term_debt_to_net_income_ratio(app.long_term_debt_values,app.net_profit_values)
#test = app.gross_profit_sga_ratio(app.Revenue,app.cogs,app.sga)

#print(test)



##@@@@@@@@@@@@@@@@@@@@@@@@@$$$$$$$$$$$$$$$$$$$$$$&&&&&&&&&&&&&&&&&&&&&&&&&&&&&




headers = {'User-Agent': 'thorntonbill343@gmail.com'}
url = 'https://www.sec.gov/files/company_tickers.json'
response = requests.get(url,headers=headers)
json = response.json()
df = pd.DataFrame(json).T	

#########################################
#df.index = df.ticker
#sample = df.loc['COP']
#sample_cik = str(sample.cik_str).zfill(10)
#sample_ticker = sample.ticker
#url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'


#response = requests.get(url,headers=headers)

#OpInc = OpIncome('COP')
#test = OpInc.get_OpIncome_values(response.json())


#print(test)





	
#for num in range(0,10):
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
#	app = StockMetrics(sample.ticker)
#	test = app.gross_profit_sga_ratio(app.Revenue,app.cogs,app.sga)

#	print(test)
	
	
		
