EXIF_TITLE_TAG = 'Exif.Image.ImageDescription'
EXIF_COMMENT_TAG = 'Exif.Photo.UserComment'
EXIF_DATE_TAG = 'Exif.Image.DateTime'

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
