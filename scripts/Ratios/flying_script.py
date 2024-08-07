import sys
##for gedit 
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/webpage/bin')
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/scripts')
sys.path.append('/home/jdubzanon/Dev_projects/sec_project/webpage/lib/python3.10/site-packages')
sys.path.append('/home/jdubzanon/hdd/Dev_projects/sec_project/scripts')
sys.path.append('/home/jdubzanon/hdd/envornments/webpage/lib/python3.10/site-packages')


from Assets.CurrentAssets import CurrentAssets

from pathlib import Path as path
from pathlib import PurePath as ppath
import os
import json
dir_path = ppath('/home/jdubzanon/Dev_projects/sec_project/scripts/json_files')
list_of_json_files = list()
for file_name in os.listdir(dir_path):
	file_path = dir_path.joinpath(file_name)
	with open(file_path,'r') as fr:
		local_file = fr.read()	
		local_json = json.loads(local_file)
#		list_of_json_files.append(local_json)
		ticker = file_name[0:-5]
		ca = CurrentAssets(ticker)
		test = ca.get_CurrentAsset_values(local_json)
		print(test)		
