# -*- coding: UTF-8 -*-
###############################################################################
##                                                                           ##
##   ##  ##   #####   ###   ##   ##       ##      ####     ####  ###   ##    ##
##   ## ##    ##      ## ## ##   ##     ##  ##    ##  ##    ##   ## ## ##    ##
##   ####     #####   ##  ####   ##    ##    ##   ##   ##   ##   ##  ####    ##
##   ## ##    ##      ##   ###   ##     ##  ##    ## ##     ##   ##   ###    ##
##   ##  ##   #####   ##    ##   #####    ##      ###      ####  ##    ##    ##
##                                                                           ##
##  @author : Kokarez                                                        ##
##  @project : pyBack                                                        ##
##  @file : Controller.py    												 ##
##  @since : 0.1                                                             ##
###############################################################################

class Controller(dict):

	def __init__(self,models,components):
		self.__models = []
		self.__components = []
		self.init()
		self.makeModels(models)
		self.makeComponents(components)

	def setInfos(self, server):
		self._Server = server
		print server

	def makeModels(self,models):
		for name in models:
			setattr(self, name + 'Model', models[name])

	def makeComponents(self,components):
		for name in components:
			setattr(self, name + 'Component', components[name])

	def sendAll(self, data):
		for client in self._Server.clients:
			socket = self._Server.clients[client]['sock']
			socket.send(data);
	
	
	def send(self, who, data):
		for w in who:
			token = who[w]
			for client in self._Server.clients:
				if token == self._Server.clients[client]['token']:
					socket = self._Server.clients[client]['sock']
					socket.send(data);

	def init(self):
		print "init is not overwritted"
