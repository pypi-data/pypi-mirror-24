from setuptools import setup

setup( 
	name = 'taft',
	version = '1.0.1',
	description = 'Technical Analysis For Trading',
	url = 'http://github.com/Savahi/taft',
	author = 'Savahi',
	author_email = 'sh@tradingene.ru',
	license = 'MIT',
	classifiers=[
	    'Development Status :: 3 - Alpha',
	    'Intended Audience :: Developers',
	],	
	packages = ['taft'],
	keywords = 'technical analysis trading',
	install_requires = ['numpy'],
	zip_safe = False )


