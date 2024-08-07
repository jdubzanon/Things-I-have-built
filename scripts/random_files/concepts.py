#change byte string to dictionary
#import json
#my_string = b'{"hello":"goodbye","goodbye":"hello"}'
#my_string = my_string.decode('utf8').replace("'",'"')
#s = json.loads(my_string)
##print(s['hello'])

#import subprocess
#import time
#file_name = '/home/jdubzanon/hdd/Dev_projects/sec_project/scripts/app/StockMetrics.py' 
#a = time.time()
#x = subprocess.run(['python3',file_name,'PG'],capture_output=True)
#s = x.stdout
##print(s)
#final = json.loads(s.decode('utf8').replace("'",'"'))
#e = time.time()
#print(e-a)
#print(final)


#set Environmental variable
	#nano ~/hdd/envornments/webpage/bin/activate
	#enter
		#export variable=your variable
	#source your/environment/bin/activate
	
#get environment variable
	#import os
	#var = os.getenv('variable')
	#print(var)

