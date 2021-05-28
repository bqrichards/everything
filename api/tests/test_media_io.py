import unittest
from datetime import datetime

from src.media_io import _format_date_to_touch, _modify_date_unix_command


class FakeMedia:
	def __init__(self, date: datetime, filepath: str):
			self.date = date
			self.filepath = filepath


class TestMediaIO(unittest.TestCase):
	def test_format_date_to_touch(self):
		a = datetime(2020, 5, 5, 10, 1, 0)
		self.assertEqual(_format_date_to_touch(a), '202005051001.00')
	

	def test_modify_date_unix_command(self):
		a = datetime(2020, 5, 5, 10, 1, 0)
		fake_media = FakeMedia(a, '/media/data/media/filepath.png')

		self.assertEqual(
			_modify_date_unix_command(fake_media), 
			'touch -a -m -t 202005051001.00 /media/data/media/filepath.png'
		)
