import logging
import os


ERROR_DATA_DIRECTORY_NOT_SET = 123


def _shutdown_server():
	"""Shutdown Flask webserver"""
	os._exit(ERROR_DATA_DIRECTORY_NOT_SET)


def exit_everything(error_code: int, error_message: str):
	"""Logs error that data directory is not set and then exits program
	
	Parameters:
		error_code (int): The error code as defined in `errors.py`
		error_message (str): The error message to log
	"""
	logging.error(f'EC{error_code}: {error_message}')
	_shutdown_server()

