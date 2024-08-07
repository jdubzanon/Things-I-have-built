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
from multiprocessing import Process, Manager
import sys

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
from Ratios import GetAverages

class StockMetrics:
	def __init__(self,ticker):
		self.ticker = ticker #company searched
		
		#from request_handler module		
		self.ticker_json = None  #company searched
		self.competitor_jsons = None #competitors json files
		self.CompanyName_to_TickerMap = None
		self.Ticker_to_CompanyName = dict()
		
#		IncomeStatement
		self.revenue = Revenue(self.ticker)
		self.revenue_values = None
		self.InterestExpense = InterestExpense(self.ticker)
		self.InterestExpense_vaules = None		
		self.OpIncome = OpIncome(self.ticker)
		self.OpIncome_values = None
		self.OpExpense = OpExpense(self.ticker)
		self.OpExpense_values = None
		self.cogs = Cogs(self.ticker)
		self.cogs_values = None
		self.NetProfit = NetProfit(self.ticker)
		self.NetProfit_values = None#		
		self.TaxesPaid = TaxesPaid(self.ticker)
		self.TaxesPaid_values = None
		self.sga = sga(self.ticker)
		self.sga_values = None


#		BalanceSheet
		self.LongTermDebt = LongTermDebt(self.ticker)
		self.LongTermDebt_values = None
		self.Shareholders_eq = ShareholdersEquity(self.ticker)
		self.Shareholders_eq_values = None
		self.TotalLiabilities = TotalLiabilities(self.ticker)
		self.TotalLiabilities_values = None
		self.RetainedEarnings = RetainedEarnings(self.ticker)
		self.RetainedEarnings_values = None
		self.cash = cash(self.ticker)
		self.cash_values = None
		self.CurrentAssets = CurrentAssets(self.ticker)
		self.CurrentAssets_values = None
		self.CurrentLiabilities = CurrentLiabilities(self.ticker)
		self.CurrentLiabilities_values = None
		self.inventory = inventory(self.ticker)
		self.inventory_values = None
		self.LiabilitiesAndStockholdersEquity = LiabilitiesAndStockholdersEquity(self.ticker)
		self.LiabilitiesAndStockholdersEquity_values = None
		self.NonCurrentAssets = NonCurrentAssets(self.ticker)
		self.NonCurrentAssets_values = None
		self.NonCurrentLiabilities = NonCurrentLiabilities(self.ticker)
		self.NonCurrentLiabilities_values = None
		self.receivables = receivables(self.ticker)
		self.receivables_values = None
		self.SharesOutstanding = SharesOutstanding(self.ticker)
		self.SharesOutstanding_values = None
		self.TotalAssets = TotalAssets(self.ticker)
		self.TotalAssets_values = None
#		CashflowStatement		
		self.capex = capex(self.ticker)
		self.capex_values = None
		self.CashflowOperations = cashflow_operations(self.ticker)
		self.CashflowOperations_values = None
		self.Dividends = Dividends(self.ticker)
		self.Dividends_values = None

		self.ticker_CashLiabilitiesRatio = dict() #current year value 
		self.ticker_CurrentRatio = dict() #5 yrs avg
		self.ticker_DebtToEquityRatio = dict() #5 yrs avg
		self.ticker_DebtRatio = dict()		
		self.ticker_CashflowRatio = dict()
		self.ticker_IntExpenseOpIncomeRatio = dict()
		self.ticker_LongTermDebtNetIncomeRatio = dict()
		self.ticker_OperatingProfitMarginRatio = dict()
		self.ticker_PretaxGrowthRatio = dict()
		self.ticker_ReceivablesRevenueRatio = dict()
		self.ticker_ReturnOnAssetsRatio = dict()
		self.ticker_ReturnOnCapitalRatio = dict()
		
		
		
		repsone = RequestHandler(ticker)
		response_data = repsone.main()
		self.ticker_json = response_data[0] #{main_ticker:json}
		self.competitor_jsons = response_data[1] #{competitors:jsons}
		self.CompanyName_to_TickerMap = response_data[2] #{CompanyName:ticker}
		if self.CompanyName_to_TickerMap:
			for CompanyName,Ticker in self.CompanyName_to_TickerMap.items():
				self.Ticker_to_CompanyName[Ticker] = CompanyName
#		print(self.Ticker_to_CompanyName) ###<--------------------
#GETTING VALUES SECTIONS
#				IncomeStatement
		self.revenue_values = self.revenue.get_revenue_values(self.ticker_json[self.ticker])
		self.InterestExpense_vaules = self.InterestExpense.get_InterestExpense_values(self.ticker_json[self.ticker])		
		self.OpIncome_values = self.OpIncome.get_OpIncome_values(self.ticker_json[self.ticker])
#		self.OpExpense_values = self.OpExpense.get_OpExpense_values(self.ticker_json[self.ticker])
#		self.cogs_values = self.cogs.get_cog_values(self.ticker_json[self.ticker])
		self.NetProfit_values = self.NetProfit.get_NetProfit_values(self.ticker_json[self.ticker])
#		self.sga_values = self.sga.get_sga_values(self.ticker_json[self.ticker])
		self.TaxesPaid_values = self.TaxesPaid.get_TaxesPaid_values(self.ticker_json[self.ticker])	
#				BalanceSheet		
		self.LongTermDebt_values = self.LongTermDebt.get_LongTermDebt_values(self.ticker_json[self.ticker]) #
		self.Shareholders_eq_values = self.Shareholders_eq.get_ShareholdersEquity_values(self.ticker_json[self.ticker])#
		self.TotalLiabilities_values = self.TotalLiabilities.get_TotalLiabilities_values(self.ticker_json[self.ticker])#
		self.RetainedEarnings_values = self.RetainedEarnings.get_RetainedEarnings_values(self.ticker_json[self.ticker])#
		self.cash_values = self.cash.get_cash_values(self.ticker_json[self.ticker])		#
		self.CurrentAssets_values =self.CurrentAssets.get_CurrentAsset_values(self.ticker_json[self.ticker])#
		self.CurrentLiabilities_values = self.CurrentLiabilities.get_CurrentLiabilities_values(self.ticker_json[self.ticker])#
#		self.inventory_values = self.inventory.get_inventory_values(self.ticker_json[self.ticker])#
		self.LiabilitiesAndStockholdersEquity_values = self.LiabilitiesAndStockholdersEquity.get_LiabilitiesAndStockholdersEquity_values(self.ticker_json[self.ticker])#
#		self.NonCurrentAssets_values = self.NonCurrentAssets.get_NonCurrentAsset_values(self.ticker_json[self.ticker])#
#		self.NonCurrentLiabilities_values = self.NonCurrentLiabilities.get_NonCurrentLiabilities_values(self.ticker_json[self.ticker])#
		self.receivables_values = self.receivables.get_receivables_values(self.ticker_json[self.ticker])#
		self.SharesOutstanding_values = self.SharesOutstanding.get_SharesOutstanding_values(self.ticker_json[self.ticker])#
		self.TotalAssets_values = self.TotalAssets.get_TotalAsset_values(self.ticker_json[self.ticker])#
#				CashflowStatement
		self.capex_values = self.capex.get_capex_values(self.ticker_json[self.ticker])
		self.CashflowOperations_values = self.CashflowOperations.get_cashflow_operations_values(self.ticker_json[self.ticker])
		self.Dividends_values = self.Dividends.get_dividend_values(self.ticker_json[self.ticker])
		
#			Company Ratios		
		try:
			self.CompanyCashLiabiltiesCurrentValue = CashLiabilitiesRatio.GetRatio(self.cash,self.CurrentLiabilities,self.ticker_json[self.ticker])[0]
		except KeyError:
			self.CompanyCashLiabiltiesCurrentValue = CashLiabilitiesRatio.GetRatio(self.cash,self.CurrentLiabilities,self.ticker_json[self.ticker])
#			print(self.CompanyCashLiabiltiesCurrentValue)
		self.company_CurrentRatio_avg = GetAverages.GetAvg(CurrentRatio.GetRatio(self.CurrentAssets,self.CurrentLiabilities,self.ticker_json[self.ticker]))		
		self.company_DebtEquityRatio_avg = GetAverages.GetAvg(DebtEquityRatio.GetRatio(self.TotalLiabilities,self.Shareholders_eq,self.ticker_json[self.ticker]))
		self.company_DebtRatio_avg = GetAverages.GetAvg(DebtRatio.GetRatio(self.TotalLiabilities,self.TotalAssets,self.ticker_json[self.ticker]))
		self.company_Cashflow_avg = GetAverages.GetAvg(FreeCashflow.GetRatio(self.CashflowOperations,self.capex,self.ticker_json[self.ticker]))
		self.company_IntExp_to_OpInc_Ratio_avg = GetAverages.GetAvg(IntExpenseOpIncomeRatio.GetRatio(self.InterestExpense,self.OpIncome,self.ticker_json[self.ticker])) 
		self.company_LongTermDebtIncomeRatio_avg = GetAverages.GetAvg(LongTermDebtNetIncomeRatio.GetRatio(self.LongTermDebt,self.NetProfit,self.ticker_json[self.ticker]))
		self.company_OperatingProfitMargin_avg = GetAverages.GetAvg(OperatingProfitMargin.GetRatio(self.OpIncome,self.revenue,self.InterestExpense,self.ticker_json[self.ticker]))
		self.company_pretax_growth_avg = GetAverages.GetAvg(Pretax.GetRatio(self.NetProfit,self.TaxesPaid,self.ticker_json[self.ticker]))
		self.company_pretaxEPS_growth = GetAverages.GetAvg(PretaxEPS.GetRatio(self.NetProfit,self.TaxesPaid,self.SharesOutstanding,self.ticker_json[self.ticker]))
		self.company_ReceivablesRevenueRatio = GetAverages.GetAvg(ReceivablesRevenueRatio.GetRatio(self.revenue,self.receivables,self.ticker_json[self.ticker])) 
		self.company_ReturnOnAssetsRatio = GetAverages.GetAvg(ReturnOnAssets.GetRatio(self.NetProfit,self.TotalAssets,self.ticker_json[self.ticker]))
		self.company_ReturnOnCapitalRatio = GetAverages.GetAvg(ReturnOnCapital.GetRatio(self.LiabilitiesAndStockholdersEquity,self.Dividends,self.NetProfit,self.ticker_json[self.ticker]))				


#all functions below are ran as separate processes 

	def AddCompanyRatiosToDictionary(self,dictionary):
		FAILED_TO_GET_DATA = 'FAILED TO GET DATA'
		if isinstance(self.CompanyCashLiabiltiesCurrentValue,dict):
			dictionary['company_CashLiabiltiesRatio'] = FAILED_TO_GET_DATA	
		else:
			dictionary['company_CashLiabiltiesRatio'] = self.CompanyCashLiabiltiesCurrentValue
		
		if isinstance(self.company_CurrentRatio_avg,dict):
			dictionary['company_CurrentRatio_avg'] = FAILED_TO_GET_DATA
		else:
			dictionary['company_CurrentRatio_avg'] = self.company_CurrentRatio_avg
		if isinstance(self.company_DebtEquityRatio_avg,dict):
			dictionary['company_DebtEquityRatio_avg'] = FAILED_TO_GET_DATA
		else:
			dictionary['company_DebtEquityRatio_avg'] = self.company_DebtEquityRatio_avg
		if isinstance(self.company_DebtRatio_avg,dict):
					dictionary['company_DebtRatio_avg'] = FAILED_TO_GET_DATA			
		else:
			dictionary['company_DebtRatio_avg'] = self.company_DebtRatio_avg
		if isinstance(self.company_Cashflow_avg,dict):
			dictionary['company_Cashflow_avg'] = FAILED_TO_GET_DATA
		else:
			dictionary['company_Cashflow_avg'] = self.company_Cashflow_avg
		if isinstance(self.company_IntExp_to_OpInc_Ratio_avg,dict):
			dictionary['company_IntExpenseOpIncomeRatio'] = FAILED_TO_GET_DATA						
		else:	
			dictionary['company_IntExpenseOpIncomeRatio'] = self.company_IntExp_to_OpInc_Ratio_avg
		if isinstance(self.company_LongTermDebtIncomeRatio_avg,dict):
			dictionary['company_LongTermDebtIncomeRatio_avg'] = FAILED_TO_GET_DATA	
		else:
			dictionary['company_LongTermDebtIncomeRatio_avg'] = self.company_LongTermDebtIncomeRatio_avg
		if isinstance(self.company_OperatingProfitMargin_avg,dict):
			dictionary['company_OperatingProfitMargin_avg'] = FAILED_TO_GET_DATA
		else:	
			dictionary['company_OperatingProfitMargin_avg'] = self.company_OperatingProfitMargin_avg
		if isinstance(self.company_pretax_growth_avg,dict):
			dictionary['company_pretax_growth_avg'] = FAILED_TO_GET_DATA			
		else:
			dictionary['company_pretax_growth_avg'] = self.company_pretax_growth_avg
		if isinstance(self.company_pretaxEPS_growth,dict):
			dictionary['company_pretaxEPS_growth'] = FAILED_TO_GET_DATA
		else:			
			dictionary['company_pretaxEPS_growth'] = self.company_pretaxEPS_growth
		if isinstance(self.company_ReceivablesRevenueRatio,dict):
			dictionary['company_ReceivablesRevenueRatio'] = FAILED_TO_GET_DATA
		else:	
			dictionary['company_ReceivablesRevenueRatio'] = self.company_ReceivablesRevenueRatio
		if isinstance(self.company_ReturnOnAssetsRatio,dict):
			dictionary['company_ReturnOnAssetsRatio'] = FAILED_TO_GET_DATA
		else:		
			dictionary['company_ReturnOnAssetsRatio'] = self.company_ReturnOnAssetsRatio
		if isinstance(self.company_ReturnOnCapitalRatio,dict):
			dictionary['company_ReturnOnCapitalRatio'] = FAILED_TO_GET_DATA
		else:		
			dictionary['company_ReturnOnCapitalRatio'] = self.company_ReturnOnCapitalRatio
		if isinstance(self.RetainedEarnings_values,dict):
			dictionary['company_RetainedEarningGrowth'] = FAILED_TO_GET_DATA
		else:
			dictionary['company_RetainedEarningGrowth'] = self.RetainedEarnings_values
		return dictionary
		
		
#company_facts is self.ticker_json[self.ticker]
#competitor company facts is self.competitor_jsons[ticker]
	
	def ReturnOnCapital_process(self,dictionary):
		ReturnOnCapital_tracker = list()
		FAILED_TO_GET_DATA = 'FAILED_TO_GET_DATA'
		for ticker in self.competitor_jsons:
			competitor_LiabilitiesStockholder = LiabilitiesAndStockholdersEquity(ticker)
			competitor_LiabilitiesStockholder_values = competitor_LiabilitiesStockholder.get_LiabilitiesAndStockholdersEquity_values(self.competitor_jsons[ticker])
			competitor_NetProfit = NetProfit(ticker)
			competitor_NetProfit_values = competitor_NetProfit.get_NetProfit_values(self.competitor_jsons[ticker])
			competitor_Dividends = Dividends(ticker)
			competitor_Dividends_values = competitor_Dividends.get_dividend_values(self.competitor_jsons[ticker])
			if isinstance(self.company_ReturnOnCapitalRatio,dict):
				dictionary['IndustryAvg_ReturnOnCapitalRatio'] = FAILED_TO_GET_DATA
			else:
				tempvar1 = GetAverages.GetAvg(ReturnOnCapital.GetRatio(competitor_LiabilitiesStockholder,competitor_Dividends,competitor_NetProfit,self.competitor_jsons[ticker]))			
				if not isinstance(tempvar1,dict):
					ReturnOnCapital_tracker.append(tempvar1)
		if ReturnOnCapital_tracker:
			dictionary['IndustryAvg_ReturnOnCapitalRatio'] = GetAverages.GetIndustryAvg(ReturnOnCapital_tracker)
		else: 
			dictionary['IndustryAvg_ReturnOnCapitalRatio'] = FAILED_TO_GET_DATA
		return dictionary
	
	
	def ReceivablesRevenueRatio_and_FreeCashFlow(self,dictionary):
		FAILED_TO_GET_DATA = 'FAILED_TO_GET_DATA'
		ReceivablesRevenueRatio_tracker = list()
		FreeCashflow_tracker = list()
		for ticker in self.competitor_jsons:
			competitor_capex = capex(ticker)
			competitor_capex_values = competitor_capex.get_capex_values(self.competitor_jsons[ticker])
			competitor_CashflowOperations = cashflow_operations(ticker)
			competitor_CashflowOperations_values = competitor_CashflowOperations.get_cashflow_operations_values(self.competitor_jsons[ticker])
			competitor_revenue = Revenue(ticker)
			competitor_revenue_values = competitor_revenue.get_revenue_values(self.competitor_jsons[ticker])
			competitor_receivables = receivables(ticker)
			competitor_receivables_values = competitor_receivables.get_receivables_values(self.competitor_jsons[ticker])
		
			if isinstance(self.company_ReceivablesRevenueRatio,dict):
				dictionary['IndustryAvg_ReceivablesRevenueRatio'] = FAILED_TO_GET_DATA
			else:
				tempvar1 = GetAverages.GetAvg(ReceivablesRevenueRatio.GetRatio(competitor_revenue,competitor_receivables,self.competitor_jsons[ticker]))			
				if not isinstance(tempvar1,dict):
					ReceivablesRevenueRatio_tracker.append(tempvar1)
			if isinstance(self.company_Cashflow_avg,dict):
				dictionary['IndustryAvg_CashflowRatio'] = FAILED_TO_GET_DATA
			else:
				tempvar2 = GetAverages.GetAvg(FreeCashflow.GetRatio(competitor_CashflowOperations,competitor_capex,self.competitor_jsons[ticker]))
				if not isinstance(tempvar2,dict):
					FreeCashflow_tracker.append(tempvar2)
					
		if ReceivablesRevenueRatio_tracker:
			dictionary['IndustryAvg_ReceivablesRevenueRatio'] = GetAverages.GetIndustryAvg(ReceivablesRevenueRatio_tracker)
		else:
			dictionary['IndustryAvg_ReceivablesRevenueRatio'] = FAILED_TO_GET_DATA
			
		if FreeCashflow_tracker:
			dictionary['IndustryAvg_CashflowRatio'] = GetAverages.GetIndustryAvg(FreeCashflow_tracker)
		else: 
			dictionary['IndustryAvg_CashflowRatio'] = FAILED_TO_GET_DATA
		return dictionary
	


	def IntExpenseOpIncomeRatio_and_OperatingProfitMargin(self,dictionary):
			IntExpenseOpIncomeRatio_tracker = list()
			OperatingProfitMargin_tracker = list()
			FAILED_TO_GET_DATA = 'FAILED_TO_GET_DATA'
			
			for ticker in self.competitor_jsons:
				competitor_InterestExpense = InterestExpense(ticker)
				competitor_InterestExpense_values = competitor_InterestExpense.get_InterestExpense_values(self.competitor_jsons[ticker])
				competitor_OpIncome = OpIncome(ticker)
				competitor_OpIncome_values = competitor_OpIncome.get_OpIncome_values(self.competitor_jsons[ticker])
				competitor_revenue = Revenue(ticker)
				competitor_revenue_values = competitor_revenue.get_revenue_values(self.competitor_jsons[ticker])
				
				if isinstance(self.company_IntExp_to_OpInc_Ratio_avg,dict):
					dictionary['IndustryAvg_IntExpenseOpIncomeRatio'] = FAILED_TO_GET_DATA
				else:
					tempvar1 = GetAverages.GetAvg(IntExpenseOpIncomeRatio.GetRatio(competitor_InterestExpense,competitor_OpIncome,self.competitor_jsons[ticker]))	
					if not isinstance(tempvar1,dict):
						IntExpenseOpIncomeRatio_tracker.append(tempvar1)	
	
				if isinstance(self.company_OperatingProfitMargin_avg,dict):
					dictionary['IndustryAvg_OperatingProfitMargin']	= FAILED_TO_GET_DATA
				else: 
					tempvar2 = GetAverages.GetAvg(OperatingProfitMargin.GetRatio(competitor_OpIncome,competitor_revenue,competitor_InterestExpense,self.competitor_jsons[ticker]))
					if not isinstance(tempvar2,dict):
						OperatingProfitMargin_tracker.append(tempvar2)
			if IntExpenseOpIncomeRatio_tracker:
				dictionary['IndustryAvg_IntExpenseOpIncomeRatio'] = GetAverages.GetIndustryAvg(IntExpenseOpIncomeRatio_tracker)
			else:
				dictionary['IndustryAvg_IntExpenseOpIncomeRatio'] = FAILED_TO_GET_DATA
			
			if OperatingProfitMargin_tracker:
				dictionary['IndustryAvg_OperatingProfitMargin'] = GetAverages.GetIndustryAvg(OperatingProfitMargin_tracker)
			else:
				dictionary['IndustryAvg_OperatingProfitMargin'] = FAILED_TO_GET_DATA
			return dictionary



	def CashLiabilitiesRatio_and_CurrentRatio(self,dictionary):
		CashLiabilitiesRatio_tracker = list()
		CurrentRatio_tracker = list()
		FAILED_TO_GET_DATA = 'FAILED TO GET DATA'
		for ticker in self.competitor_jsons:
			competitor_CurrentLiabilities = CurrentLiabilities(ticker)
			competitor_CurrentLiabilities_values = competitor_CurrentLiabilities.get_CurrentLiabilities_values(self.competitor_jsons[ticker]) 
			competitor_cash = cash(ticker)
			competitor_cash_values = competitor_cash.get_cash_values(self.competitor_jsons[ticker])
			competitor_CurrentAssets = CurrentAssets(ticker)			
			competitor_CurrentAssets_values = competitor_CurrentAssets.get_CurrentAsset_values(self.competitor_jsons[ticker])
			if isinstance(self.CompanyCashLiabiltiesCurrentValue,dict):
				dictionary['IndustryAvg_CashLiabilitiesRatio'] = FAILED_TO_GET_DATA
			else:
				tempvar1 = GetAverages.GetAvg(CashLiabilitiesRatio.GetRatio(competitor_cash,competitor_CurrentLiabilities,self.competitor_jsons[ticker]))
				if not isinstance(tempvar1,dict):
					CashLiabilitiesRatio_tracker.append(tempvar1)
			if isinstance(self.company_CurrentRatio_avg,dict):
				dictionary['IndustryAvg_CurrentRatio'] = FAILED_TO_GET_DATA
			else:
				tempvar2 = GetAverages.GetAvg(CurrentRatio.GetRatio(competitor_CurrentAssets,competitor_CurrentLiabilities,self.competitor_jsons[ticker]     )     )
				if not isinstance(tempvar2,dict):
					CurrentRatio_tracker.append(tempvar2)
		
		if CashLiabilitiesRatio_tracker:
			dictionary['IndustryAvg_CashLiabilitiesRatio'] = GetAverages.GetIndustryAvg(CashLiabilitiesRatio_tracker)
		else:
			dictionary['IndustryAvg_CashLiabilitiesRatio'] = FAILED_TO_GET_DATA

		if CurrentRatio_tracker:
			dictionary['IndustryAvg_CurrentRatio'] = GetAverages.GetIndustryAvg(CurrentRatio_tracker)
		else:
			dictionary['IndustryAvg_CurrentRatio'] = FAILED_TO_GET_DATA
		return dictionary

	def DebtEquityRatio_and_DebtRatio(self,dictionary):
		DebtEquityRatio_tracker = list()
		DebtRatio_tracker = list()
		FAILED_TO_GET_DATA = 'FAILED TO GET DATA'
		for ticker in self.competitor_jsons:
			competitor_TotalLiabilities = TotalLiabilities(ticker)
			competitor_TotalLiabilities_values = competitor_TotalLiabilities.get_TotalLiabilities_values(self.competitor_jsons[ticker])
			competitor_TotalAssets = TotalAssets(ticker)
			competitor_TotalAssets_values = competitor_TotalAssets.get_TotalAsset_values(self.competitor_jsons[ticker])
			competitor_Shareholders_eq = ShareholdersEquity(ticker)
			competitor_Shareholders_eq_values = competitor_Shareholders_eq.get_ShareholdersEquity_values(self.competitor_jsons[ticker])
			
			
			if isinstance(self.company_DebtEquityRatio_avg,dict):
				dictionary['IndustryAvg_DebtEquityRatio'] = FAILED_TO_GET_DATA
			else:
				tempvar1 = GetAverages.GetAvg(DebtEquityRatio.GetRatio(competitor_TotalLiabilities,competitor_Shareholders_eq,self.competitor_jsons[ticker]))		
				if not isinstance(tempvar1,dict):
					DebtEquityRatio_tracker.append(tempvar1)
			if isinstance(self.company_DebtRatio_avg,dict):
				dictionary['IndustryAvg_DebtRatio'] = FAILED_TO_GET_DATA
			else:
				tempvar2 = GetAverages.GetAvg(DebtRatio.GetRatio(competitor_TotalLiabilities,competitor_TotalAssets,self.competitor_jsons[ticker]))		
				if not isinstance(tempvar2,dict):
					DebtRatio_tracker.append(tempvar2)
		if DebtEquityRatio_tracker:
			dictionary['IndustryAvg_DebtToEquityRatio'] = GetAverages.GetIndustryAvg(DebtEquityRatio_tracker)
		else:
			dictionary['IndustryAvg_DebtEquityRatio'] = FAILED_TO_GET_DATA
		if DebtRatio_tracker:
			dictionary['IndustryAvg_DebtRatio'] = GetAverages.GetAvg(DebtRatio_tracker)
		else:
			dictionary['IndustryAvg_DebtRatio'] = FAILED_TO_GET_DATA

		return dictionary

	
	def PretaxGrowth_and_PretaxEPS(self,dictionary):
		PretaxGrowth_tracker = list()
		PretaxEPS_tracker = list()
		FAILED_TO_GET_DATA = 'FAILED_TO_GET_DATA'
		for ticker in self.competitor_jsons:
			competitor_NetProfit = NetProfit(ticker)
			competitor_NetProfit_values = competitor_NetProfit.get_NetProfit_values(self.competitor_jsons[ticker])
			competitor_TaxesPaid = TaxesPaid(ticker)
			competitor_TaxesPaid_values = competitor_TaxesPaid.get_TaxesPaid_values(self.competitor_jsons[ticker])
			competitor_SharesOutstanding = SharesOutstanding(ticker)
			competitor_SharesOutstanding_values = competitor_SharesOutstanding.get_SharesOutstanding_values(self.competitor_jsons[ticker])
			
			if isinstance(self.company_pretax_growth_avg,dict):
				dictionary['IndustryAvg_Pretax_growth'] = FAILED_TO_GET_DATA
			else:
				tempvar1 = GetAverages.GetAvg(Pretax.GetRatio(competitor_NetProfit,competitor_TaxesPaid,self.competitor_jsons[ticker]))
				if not isinstance(tempvar1,dict):
					PretaxGrowth_tracker.append(tempvar1)
			if isinstance(self.company_pretaxEPS_growth,dict):
				dictionary['IndustryAvg_PretaxEPS_growth'] = FAILED_TO_GET_DATA
			else: 
				tempvar2 = GetAverages.GetAvg(PretaxEPS.GetRatio(competitor_NetProfit,competitor_TaxesPaid,competitor_SharesOutstanding,self.competitor_jsons[ticker]))
				if not isinstance(tempvar2,dict):
					PretaxEPS_tracker.append(tempvar2)
		if PretaxGrowth_tracker:
			dictionary['IndustryAvg_Pretax_growth'] = GetAverages.GetIndustryAvg(PretaxGrowth_tracker)
		else:
			dictionary['IndustryAvg_Pretax_growth'] = FAILED_TO_GET_DATA
		
		if PretaxEPS_tracker:
			dictionary['IndustryAvg_PretaxEPS_growth'] = GetAverages.GetIndustryAvg(PretaxEPS_tracker)
		else:
			dictionary['IndustryAvg_PretaxEPS_growth'] = FAILED_TO_GET_DATA
		return dictionary


	def LongTermDebtNetIncome_and_ReturnOnAssets(self,dictionary):
		LongTermDebtNetIncome_tracker = list()
		ReturnOnAssets_tracker = list()
		FAILED_TO_GET_DATA = 'FAILED_TO_GET_DATA'
		for ticker in self.competitor_jsons:
			competitor_TotalAssets = TotalAssets(ticker)
			competitor_TotalAssets_values = competitor_TotalAssets.get_TotalAsset_values(self.competitor_jsons[ticker])
			competitor_LongTermDebt = LongTermDebt(ticker)			
			competitor_LongTermDebt_values = competitor_LongTermDebt.get_LongTermDebt_values(self.competitor_jsons[ticker])
			competitor_NetProfit = NetProfit(ticker)
			competitor_NetProfit_values = competitor_NetProfit.get_NetProfit_values(self.competitor_jsons[ticker])
			if isinstance(self.company_LongTermDebtIncomeRatio_avg,dict):
				dictionary['IndustryAvg_LongTermDebtIncomeRatio'] = FAILED_TO_GET_DATA
			else: 
				tempvar1 = GetAverages.GetAvg(LongTermDebtNetIncomeRatio.GetRatio(competitor_LongTermDebt,competitor_NetProfit,self.competitor_jsons[ticker]))
				if not isinstance(tempvar1,dict):
					LongTermDebtNetIncome_tracker.append(tempvar1)
			if isinstance(self.company_ReturnOnAssetsRatio,dict):
				dictionary['IndustryAvg_ReturnOnAssetsRatio'] = FAILED_TO_GET_DATA
			else:
				tempvar2 = GetAverages.GetAvg(ReturnOnAssets.GetRatio(competitor_NetProfit,competitor_TotalAssets,self.competitor_jsons[ticker]))
				if not isinstance(tempvar2,dict):
					ReturnOnAssets_tracker.append(tempvar2)
		if LongTermDebtNetIncome_tracker:
			dictionary['IndustryAvg_LongTermDebtIncomeRatio'] = GetAverages.GetIndustryAvg(LongTermDebtNetIncome_tracker)
		else:
			dictionary['IndustryAvg_LongTermDebtIncomeRatio'] = FAILED_TO_GET_DATA
			
		if ReturnOnAssets_tracker:
			dictionary['IndustryAvg_ReturnOnAssetsRatio'] = GetAverages.GetIndustryAvg(ReturnOnAssets_tracker)
		else:
			dictionary['IndustryAvg_ReturnOnAssetsRatio'] = FAILED_TO_GET_DATA
		return dictionary







if __name__ == '__main__':
	app=StockMetrics(sys.argv[1])
#	print(app.CompanyCashLiabiltiesCurrentValue)
	with Manager() as manager:
		dictionary = manager.dict()
		processes = [
					
					Process(target=app.AddCompanyRatiosToDictionary,args=(dictionary,)), 
					Process(target=app.CashLiabilitiesRatio_and_CurrentRatio,args=(dictionary,)),
					Process(target=app.DebtEquityRatio_and_DebtRatio,args=(dictionary,)),
					Process(target=app.PretaxGrowth_and_PretaxEPS,args=(dictionary,)),
					Process(target=app.LongTermDebtNetIncome_and_ReturnOnAssets,args=(dictionary,)),
					Process(target=app.IntExpenseOpIncomeRatio_and_OperatingProfitMargin,args=(dictionary,)),
					Process(target=app.ReceivablesRevenueRatio_and_FreeCashFlow,args=(dictionary,)),
					Process(target=app.ReturnOnCapital_process,args=(dictionary,))
					
					]
		for process in processes:
			process.start()
		for process in processes:
			process.join()
		
		print(dictionary)	
			

##@@@@@@@@@@@@@@@@@@@@@@@@@$$$$$$$$$$$$$$$$$$$$$$&&&&&&&&&&&&&&&&&&&&&&&&&&&&&




#headers = {'User-Agent': 'thorntonbill343@gmail.com'}
#url = 'https://www.sec.gov/files/company_tickers.json'
#response = requests.get(url,headers=headers)
#json = response.json()
#df = pd.DataFrame(json).T	

###########################################
#df.index = df.ticker
#sample = df.loc['GOLD']
#sample_cik = str(sample.cik_str).zfill(10)
#sample_ticker = sample.ticker
#url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{sample_cik}.json'
#print(url)
#response = requests.get(url,headers=headers)

#app = StockMetrics(sample_ticker)
#print(app.RetainedEarnings_values)





	
#for num in range(100,200):
#	print(num)
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
#	a = time.time()
#	app = StockMetrics(sample_ticker)
#	print(app.RetainedEarnings_values)
#	b = time.time()
#	print(b-a)
#	
	
		
