fields = ['state','category','date', 'deathrate']

ent = 'state new-york&new-jersey date 1999-2020 category murder deathrate 1998'
print_cat_dict = dict()
dict1 = dict()
dict2 = dict()
dict3 = dict()
rangelist = list()

s = ent.split()
for item in s:
	if item == 'category':
		loc = s.index(item)
		print_cat_dict[item] = [value.replace('-',' ') for value in s[loc+1].split('&')]
#		print(print_cat_dict)
		
	elif item in fields and item != 'category':
		if not dict1.keys():
			loc = s.index(item)
			dict1[item] = [value.replace('-',' ') for value in s[loc+1].split('&')]	
#			print(dict1)
		elif dict1.keys and not dict2.keys():
			loc = s.index(item)
			dict2[item] = [value.replace('-',' ') for value in s[loc+1].split('&')] 
#			print(dict2)
		else:
			loc = s.index(item)
			dict3[item] = [value.replace('-',' ') for value in s[loc+1].split('&')]
#			print(dict3)
						
# checking for date range in dictionary		
for items in dict1.values():
	for item in items:
		if item[0:4].isdigit():
			for key in dict2.keys():
				dict1[key] = item.split(' ')
				if len(dict1[key]) > 1:
					rangelist.clear()
					for num in range(int(dict1[key][0]), int(dict1[key][1]) +1):
						rangelist.append(num)
					
print(dict1)

# checking for date range in dictionary
for items in dict2.values():
	for item in items:
		if item[0:4].isdigit():
			for key in dict2.keys():
				dict2[key] = item.split(' ')
				if len(dict2[key]) > 1:
					rangelist.clear()
					for num in range(int(dict2[key][0]),int(dict2[key][1]) +1):
						rangelist.append(num)

print(dict2)
# checking for date range in dictionary
for items in dict3.values():
	for item in items:
		if item[0:4].isdigit():
			for key in dict3.keys():
				dict3[key] = item.split(' ')
				if len(dict3[key]) > 1:
					rangelist.clear()
					for num in range(int(dict3[key][0]),int(dict3[key][1]) +1):
						rangelist.append(num)

print(dict3)					
				
		
print(rangelist)	

