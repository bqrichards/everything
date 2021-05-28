from datetime import datetime
import sys
import subprocess
from src.db import Media


def _format_date_to_touch(datetime: datetime) -> str:
	"""Returns datettime in Date Modified format for touch command

	Format: YYYYMMDDhhmm.SS

	See: https://www.thegeekstuff.com/2012/11/linux-touch-command/
	"""
	return datetime.strftime('%Y%m%d%H%M.%S')


def _modify_date_unix_command(media: Media) -> str:
	"""Returns command to modify Date Modified for macOS and Linux

	Command: `touch -a -m -t YYYYMMDDhhmm.SS filename`

	See: https://smallbusiness.chron.com/change-file-date-mac-finder-46835.html
	"""
	return f'touch -a -m -t {_format_date_to_touch(media.date)} {media.filepath}'


def write_date_to_media(media: Media):
	command = None

	if sys.platform in ['darwin', 'linux', 'linux2']:
		command = _modify_date_unix_command(media)
	else:
		raise ValueError(f'Running on unsupported OS {sys.platform}')

	# Run command
	subprocess.run(command, shell=True, check=True)
