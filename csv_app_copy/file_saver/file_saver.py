import pathlib


class Save:
	def __init__(self,ent_var,data):
		self.file_name = ent_var.split()[1]
		self.directory = 'saved_files'
		self.pure_path = pathlib.PurePath(pathlib.Path.cwd()) / self.directory / self.file_name
		self.path = pathlib.Path(self.pure_path)
		self.data = data
		
		
	def to_file(self):
		self.path.touch(exist_ok=True)
		with self.path.open(mode='a+') as new_file:
			count = 1
			for data in self.data:
				new_file.write(f'\nmatch {count} {data} \n')
				count += 1
