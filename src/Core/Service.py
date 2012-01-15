# -*- coding: UTF-8 -*-
###############################################################################
##                                                                           ##
##   ##  ##   #####   ###   ##   ##       ##      ####     ####  ###   ##    ##
##   ## ##    ##      ## ## ##   ##     ##  ##    ##  ##    ##   ## ## ##    ##
##   ####     #####   ##  ####   ##    ##    ##   ##   ##   ##   ##  ####    ##
##   ## ##    ##      ##   ###   ##     ##  ##    ## ##     ##   ##   ###    ##
##   ##  ##   #####   ##    ##   #####    ##      ###      ####  ##    ##    ##
##                                                                           ##
##  @author : Arx                                                            ##
##  @project : pyBack                                                        ##
##  @file : Service.py                                                       ##
##  @since : 0.1                                                             ##
###############################################################################

import sys

class Service:
	
	_instance = None
    
	def __new__(_class): 
		if _class.instance is None:
			_class.instance = object.__new__(_class)
		return _class.instance
		
	def add(self, options):
		_folder = options['folder']
		_file = options['file'].replace(".py", "")
		if 'class' in options:
			_class = options['class']
		else:
			_class = _file
		if 'params' in options:
			_params = options['params']
		else:
			_params = {}
			
		sys.path.append(_folder)
		
		_instance = getattr(__import__(_file), _class)(**_params)

		if hasattr(self, _class):
			return False
		else:
			setattr(self, _class, _instance)
			return True
	
# Exemple d'utilisation		
# s = Service()
# s.add({'folder': './', 'file': 'test.py', 'class': 'Test', 'params': {'toto': 'crotte'}})
# s.Test.test()
