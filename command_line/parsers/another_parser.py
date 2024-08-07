fields = ['state','category','date']

ent = 'state alabama&new-york category murder&burglary date 1999-2020'
d = dict()
s = ent.split()
d_list = []
for item in s:
	if item in fields:
		loc = s.index(item)		
		d[item] = {x:x.split('-') if x[0:3].isdigit() else x.replace('-',' ') for x in  s[loc+1].split('&')}
		
for keys in d.keys():
	for items in d[keys]:
		if items[0:3].isdigit():
			for i in range(int(d[keys][items][0]), int(d[keys][items][1]) + 1):
				d_list.append(i)

print(d_list)	

