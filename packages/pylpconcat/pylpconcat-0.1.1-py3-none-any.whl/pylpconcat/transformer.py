"""

Concatenation transformer.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import os
import pylp


class concat(pylp.Transformer):

	# Constructor
	def __init__(self, filename, **options):
		super().__init__()

		self.filename = filename
		self.sep = options.get('sep', '\n')

		self.files = []


	# Function called when a file need to be transformed
	async def transform(self, file):
		if file.contents:
			self.files.append(file)


	# Function called when all files are transformed
	async def flush(self):
		# No files to concatenate
		if len(self.files) == 0:
			return

		# Sort files
		self.files.sort(key=lambda file: file.order)

		# Concat contents
		buffer = ""
		for file in self.files:
			buffer += file.contents + self.sep

		# Append the result file into the stream
		file = self.files[0]
		self.append(pylp.File(
			os.path.join(file.base, self.filename),
			contents = buffer,
			cwd = file.cwd,
			base = file.base
		))
