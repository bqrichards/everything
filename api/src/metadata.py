from db import Media
from exif import Image

EXIF_TITLE_TAG = 'ImageDescription'
EXIF_COMMENT_TAG = 'UserComment'
EXIF_DATE_TAG = 'datetime_original'
EXIF_DATE_FORMAT = '%Y:%m:%d %H:%M:%S'

class Metadata:
	title: str
	comment: str
	date: str

	def __init__(self, tags: 'dict[str, str]'):
		self.title = tags.get(EXIF_TITLE_TAG, '')
		self.comment = tags.get(EXIF_COMMENT_TAG, '')
		self.date = tags.get(EXIF_DATE_TAG, None)
	
	def to_exif(self):
		""" Converts this metadata into a dict of EXIF tags """
		return {
			EXIF_TITLE_TAG: self.title,
			EXIF_COMMENT_TAG: self.comment,
			EXIF_DATE_TAG: self.date
		}

	def write_to_image(self, img: Image):
		tags = self.to_exif()
		for key, value in tags.items():
			img[key] = value or ''
	
	@staticmethod
	def from_model(media: Media):
		meta = Metadata({})
		meta.title = media.title
		meta.comment = media.comment
		meta.date = None
		if media.date:
			# Format date
			formatted = media.date.strftime(EXIF_DATE_FORMAT)
			meta.date = formatted
		return meta
