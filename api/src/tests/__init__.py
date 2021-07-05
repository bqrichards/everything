from datetime import datetime


class FakeMedia:
	def __init__(self, date: datetime, filepath: str, id: int):
			self.date = date
			self.filepath = filepath
			self.id = id
