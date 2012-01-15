# -*- coding: UTF-8 -*-
###############################################################################
##                                                                           ##
##   ##  ##   #####   ###   ##   ##       ##      ####     ####  ###   ##    ##
##   ## ##    ##      ## ## ##   ##     ##  ##    ##  ##    ##   ## ## ##    ##
##   ####     #####   ##  ####   ##    ##    ##   ##   ##   ##   ##  ####    ##
##   ## ##    ##      ##   ###   ##     ##  ##    ## ##     ##   ##   ###    ##
##   ##  ##   #####   ##    ##   #####    ##      ###      ####  ##    ##    ##
##                                                                           ##
##  @author : Kokarez / Arx                                                  ##
##  @project : pyBack                                                        ##
##  @file : Routing.py      												 ##
##  @since : 0.1                                                             ##
###############################################################################

import json

class Routing(object):
	
	def __init__(self, controllers):
		self.controllers = controllers

	def callAction(self, user, jsonStr):
		try:
			_result = json.loads(jsonStr)
		except:
			return {'Error':True, 'Message': 'Request isn\'t a valid json'} 
			
		if not 'controller' in _result:
			return {'Error':True, 'Message': 'Controller is missing'}
		if not 'action' in _result:
			return {'Error':True, 'Message': 'Action is missing'}
		if 'params' in _result:
			_params = _result['params']
		else:
			_params = {}
			
		_controller = _result['controller']
		_action = _result['action']
		if _controller in self.controllers:
			if hasattr(self.controllers[_controller], _action):
				try:
					getattr(self.controllers[_controller], _action)(_params)
					return False
				except:
					# L'action a crashé, on fait un log.error
					return {'Error':True, 'Message': 'Action has crashed !'} 
			else:
				return {'Error': True, 'Message': 'This action doesn\'t exist !'}
		else:
			return {'Error': True, 'Message': 'This controller doesn\'t exist !'}
		#return self.controllers[_model]._function

