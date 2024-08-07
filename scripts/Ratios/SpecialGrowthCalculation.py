

def GrowthCalculate(vals):
	list_of_values = list()

	for index,val in enumerate(vals):
		if index == len(vals)-1:
			break
		jump_forward = index + 1
		
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
	return list_of_values
