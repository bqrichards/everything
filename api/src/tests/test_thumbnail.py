import os
import unittest
from unittest import mock
from tests import FakeMedia
from everything.thumbnail import _generate_thumbail_image_command, _generate_thumbnail_video_command, get_thumbnail_path
from everything.paths import initialize_paths
from tests.test_paths import FAKE_ENVIROMENT

class TestThumbnail(unittest.TestCase):
	@mock.patch.dict(os.environ, FAKE_ENVIROMENT)
	def setUp(self):
		initialize_paths()


	def test_get_thumbnail_path(self):
		m = FakeMedia(None, '/media/data/hello.png', 10)
		self.assertEqual(get_thumbnail_path(m), '/media/data/.thumbnails/10.jpg')


	def test_generate_thumbnail_image_command(self):
		self.assertEqual(
			_generate_thumbail_image_command('/input/world.png', '/output/.thumbnails/world.jpg'),
			'ffmpeg -i /input/world.png -vf scale="96:-1" /output/.thumbnails/world.jpg'
		)


	def test_generate_thumbnail_video_command(self):
		self.assertEqual(
			_generate_thumbnail_video_command('/input/world.mp4', '/output/.thumbnails/world.jpg'),
			'ffmpeg -i /input/world.mp4 -ss 00:00:01.000 -vframes 1 -vf scale="96:-1" /output/.thumbnails/world.jpg'
		)
