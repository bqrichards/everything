import logging
import typing
import os
from db import Media
from scan import media_directory, is_image, THUMBNAIL_DIRECTORY_NAME
import subprocess

THUMBNAIL_DIRECTORY = os.path.join(media_directory, THUMBNAIL_DIRECTORY_NAME)
THUMBNAIL_WIDTH = 96


def get_thumbnail_path(media: Media) -> str:
	"""Get the path of a thumbnail of media"""
	return os.path.join(THUMBNAIL_DIRECTORY, f'{media.id}.jpg')


def _does_thumbnail_exist(media: Media) -> bool:
	"""Returns if a thumbnail already exists for media"""
	thumbnail_path = get_thumbnail_path(media)
	return os.path.isfile(thumbnail_path)


def _generate_thumbail_image_command(input_path: str, output_path: str):
	"""Returns command to generate thumbnail from image
	
	Command: `ffmpeg -i input.jpg -vf scale="360:-1" output.jpg`
	"""
	return f'ffmpeg -i {input_path} -vf scale="{THUMBNAIL_WIDTH}:-1" {output_path}'


def _generate_thumbnail_video_command(input_path: str, output_path: str):
	"""Returns command to generate thumbnail from video
	
	Command: `ffmpeg -i filename -ss 00:00:01.000 -vframes 1 -vf scale="360:-1" output.jpg`
	"""
	return f'ffmpeg -i {input_path} -ss 00:00:01.000 -vframes 1 -vf scale="{THUMBNAIL_WIDTH}:-1" {output_path}'


def _generate_thumbnail(media: Media):
	"""Generates a thumbnail for media"""
	output = get_thumbnail_path(media)
	try:
		command = None
		if is_image(media.filepath):
			command = _generate_thumbail_image_command(media.filepath, output)
		else:
			command = _generate_thumbnail_video_command(media.filepath, output)
		
		subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		logging.info(f'Generated thumbnail for media {media.filepath}')
	except subprocess.CalledProcessError as e:
		logging.error(f'Couldn\'t generate thumbnail for media {media.filepath}', exc_info=e)


def make_thumbnails_directory():
	"""Generates the directory used to store thumbnails"""
	try:
		os.mkdir(THUMBNAIL_DIRECTORY)
		logging.info('Generated thumbnails directory')
	except FileExistsError:
		logging.info('Thumbnail directory exists')


def generate_thumbnails(media_list: typing.List[Media]):
	"""Generate thumbnails for passed media items"""
	logging.info('Generating thumbnails')
	for media in media_list:
		if not _does_thumbnail_exist(media):
			_generate_thumbnail(media)
	logging.info('Finished generating thumbnails')
