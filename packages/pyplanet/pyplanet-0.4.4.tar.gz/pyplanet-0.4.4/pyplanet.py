#!/usr/bin/env python3
"""
Bootstrap script of the PyPlanet Controller.
"""
import os

if __name__ == '__main__':
	# Set the local settings module.
	os.environ.setdefault('PYPLANET_SETTINGS_MODULE', 'settings')

	from pyplanet.core.management import execute_from_command_line
	execute_from_command_line()
