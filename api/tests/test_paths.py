import os
import unittest
from unittest import mock

from src.paths import _generate_random_string, generate_random_media_filepath, get_data_path, get_database_path, get_media_directory, get_thumbnails_directory, initialize_paths

FAKE_ENVIROMENT = {'DATA_DIR': '/media/data', 'FRONTEND_URL': 'http://localhost:5000'}

class TestPaths(unittest.TestCase):
	@mock.patch.dict(os.environ, FAKE_ENVIROMENT)
	def setUp(self):
		initialize_paths()

	def test_generate_random_string(self):
		self.assertEqual(len(_generate_random_string(10)), 10)
		self.assertEqual(len(_generate_random_string(5)), 5)
		self.assertEqual(len(_generate_random_string(13)), 13)


	def test_generate_random_media_filepath(self):
		self.assertTrue(generate_random_media_filepath('.jpeg').endswith('.jpeg'))
		self.assertTrue(generate_random_media_filepath('.png').endswith('.png'))
		self.assertTrue(generate_random_media_filepath('.mp4').endswith('.mp4'))


	def test_get_data_path(self):
		self.assertEqual(get_data_path(), '/media/data')
	

	def test_get_database_path(self):
		self.assertEqual(get_database_path(), '/media/data/everything.db')


	def test_get_media_directory(self):
		self.assertEqual(get_media_directory(), '/media/data/media')


	def test_get_thumbnails_directory(self):
		self.assertEqual(get_thumbnails_directory(), '/media/data/.thumbnails')
