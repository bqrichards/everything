import logging
import os


"""Error code for DATA_DIR enviroment variable not being set"""
ERROR_DATA_DIRECTORY_NOT_SET = 123


"""Error code for FRONTEND_URL enviroment variable not being set"""
ERROR_FRONTEND_NOT_SET = 111


def _shutdown_server(status_code: int):
	"""Shut down Flask webserver
	
	Parameters:
		status_code (int): Status code to exit program with
	"""
	os._exit(status_code)


def exit_everything(error_code: int, error_message: str):
	"""Logs error and exits program with `error_code`
	
	Parameters:
		error_code (int): The error code as defined in `errors.py`
		error_message (str): The error message to log
	"""
	logging.error(f'EC{error_code}: {error_message}')
	_shutdown_server(error_code)

