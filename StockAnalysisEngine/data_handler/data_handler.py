#class of attributes to organize all returned data


class DataOrganizer:
	def __init__(self):
		self.ticker_CashLiabilitiesRatio = dict() 
		self.IndustryAvg_CashLiabilitiesRatio = dict()

		self.ticker_CurrentRatio = dict() 
		self.IndustryAvg_CurrentRatio = dict()

		self.ticker_DebtToEquityRatio = dict() 
		self.IndustryAvg_DebtToEquityRatio = dict()

		self.ticker_DebtRatio = dict()		
		self.IndustryAvg_DebtRatio = dict()

		self.ticker_CashflowRatio = dict()
		self.IndustryAvg_CashflowRatio = dict()
		

		self.ticker_IntExpenseOpIncomeRatio = dict()
		self.IndustryAvg_IntExpenseOpIncomeRatio = dict()

		self.ticker_LongTermDebtNetIncomeRatio = dict()
		self.IndustryAvg_LongTermDebtNetIncomeRatio = dict()

		self.ticker_OperatingProfitMarginRatio = dict()
		self.IndustryAvg_OperationProfitMarginRatio = dict()

		self.ticker_PretaxGrowthRatio = dict()
		self.IndustryAvg_PretaxGrowthRatio = dict()

		self.ticker_ReceivablesRevenueRatio = dict()
		self.IndustryAvg_ReceivablesRevenueRatio = dict()

		self.ticker_ReturnOnAssetsRatio = dict()
		self.IndustryAvg_ReturnOnAssetsRatio = dict()

		self.ticker_ReturnOnCapitalRatio = dict()
		self.IndustryAvg_ReturnOnCapitalRatio = dict()

		
		self.CashLiabilitiesRatio_failed = False
		self.CurrentRatio_failed = False
		self.DebtEquityRatio_failed = False
		self.DebtRatio_failed = False
		self.CashflowRatio_failed = False
		self.IntExpenseOpIncomeRatio_failed = False
		self.LongTermDebtNetIncomeRatio_failed = False
		self.OperatingProfitMargin_failed = False
		self.PretaxGrowthRatio_failed = False
		self.ReceivablesRevenueRatio_failed = False
		self.ReturnOnAssets_failed = False
		self.ReturnOnCapitalRatio_failed = False
		
		
