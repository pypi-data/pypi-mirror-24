"""

Transformer for renaming files in a stream.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import os
import pylp


# Get the absolute path of the renamed file
def get_abs_path(path, file):
	if not os.path.isabs(path):
		path = os.path.join(file.base, path)
	return path



# Rename transformer
class rename(pylp.Transformer):

	# Constructor
	def __init__(self, name = None, **values):
		super().__init__()

		self.obj = name
		self.values = values

		if isinstance(name, str):
			self.transform = self.transform_str
		elif callable(name):
			self.transform = self.transform_func
		else:
			self.transform = self.transform_values


	# Transform function when 'name' parameter is a string
	async def transform_str(self, file):
		file.set_path(get_abs_path(self.obj, file))
		return file


	# Transform function when 'name' parameter is a function
	async def transform_func(self, file):
		path = self.obj(file.relative)
		if isinstance(path, str) and path:
			 file.set_path(get_abs_path(path, file))
		return file


	# Transform function when 'name' is a None
	async def transform_values(self, file):
		split = os.path.splitext(file.relative)

		dirname = self.values.get("dirname", os.path.dirname(file.relative))
		basename = self.values.get("basename", split[0])
		ext = self.values.get("ext", split[1])
		prefix = self.values.get("prefix", "")
		suffix = self.values.get("suffix", "")

		path = os.path.join(dirname, prefix + basename + suffix + ext)
		file.set_path(get_abs_path(path, file))
		return file
