from datetime import datetime
import unittest

from everything.scan import get_extension, is_image, is_media_file, mime_from_ext

class TestScan(unittest.TestCase):
	def test_get_extension(self):
		self.assertEqual(get_extension('/media/hello.png'), '.png')
		self.assertEqual(get_extension('/media/hello.mp4'), '.mp4')
		self.assertEqual(get_extension('/media/hello.mov'), '.mov')
		self.assertEqual(get_extension('/media/nested/world.jpg'), '.jpg')
		self.assertEqual(get_extension('/home/everything/data/hello.jpeg'), '.jpeg')

	def test_mime_from_ext(self):
		self.assertEqual(mime_from_ext('/media/hello.png'), 'image/png')
		self.assertEqual(mime_from_ext('/media/hello.mp4'), 'video/mp4')
		self.assertEqual(mime_from_ext('/media/hello.mov'), 'application/octet-stream')
		self.assertEqual(mime_from_ext('/media/nested/world.jpg'), 'image/jpeg')
		self.assertEqual(mime_from_ext('/home/everything/data/hello.jpeg'), 'image/jpeg')

	def test_is_image(self):
		self.assertTrue(is_image('/media/hello.png'))
		self.assertFalse(is_image('/media/hello.mp4'))
		self.assertFalse(is_image('/media/hello.mov'))
		self.assertTrue(is_image('/media/nested/world.jpg'))
		self.assertTrue(is_image('/home/everything/data/hello.jpeg'))

	def test_is_media_file(self):
		self.assertTrue(is_media_file('/media/hello.png'))
		self.assertTrue(is_media_file('/media/hello.mp4'))
		self.assertTrue(is_media_file('/media/hello.mov'))
		self.assertTrue(is_media_file('/media/nested/world.jpg'))
		self.assertTrue(is_media_file('/home/everything/data/hello.jpeg'))
		self.assertFalse(is_media_file('/media/hello.txt'))
		self.assertFalse(is_media_file('/media/hello.heic'))
		self.assertFalse(is_media_file('/media/hello.pdf'))
		self.assertFalse(is_media_file('/media/nested/world.mp3'))
		self.assertFalse(is_media_file('/home/everything/data/hello.docx'))

