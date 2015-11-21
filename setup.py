from setuptools import find_packages
from setuptools import setup

setup(name='socialminer',
	version='0.1',
	description='',
	author='Davide Gessa',
	setup_requires='setuptools',
	author_email='gessadavide@gmail.com',
	packages=['socialminer', 'reportserver'],
	entry_points={
		'console_scripts': [
			'socialminer=socialminer.socialminer:main'
		],
	},
	install_requires=open ('requirements.txt', 'r').read ().split ('\n')
)
