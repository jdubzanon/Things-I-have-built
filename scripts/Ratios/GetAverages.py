def GetAvg(array):
#	print(array)
	FAILED_TO_GET_DATA = {'from get avg':'FAILED_TO_GET_DATA'}
	if isinstance(array,dict):
		return array
	if len(array) < 2:
		return FAILED_TO_GET_DATA
	if len(array) > 5:
		array = array[0:5]
	return round(sum(array) / len(array),ndigits=2)
	
def GetIndustryAvg(array):
	FAILED_TO_GET_DATA = {'from get avg':'FAILED_TO_GET_DATA'}
	if isinstance(array,dict):
		return array
	if len(array) < 2:
		return FAILED_TO_GET_DATA
	return  round(sum(array) / len(array),ndigits=2)  
	
def GetAllAvg(array):
	FAILED_TO_GET_DATA = {'from get avg':'FAILED_TO_GET_DATA'}
	if isinstance(array,dict):
		return array
	if len(array) < 2:
		return FAILED_TO_GET_DATA	
	return  round(sum(array) / len(array),ndigits=2)  
	
	
	
	
	
	
	
	
