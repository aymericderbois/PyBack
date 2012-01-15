#!/usr/bin/env python
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
##  @file : pyBack.py													     ##
##  @version : 0.1															 ##
##  @since : 0.1                                                             ##
###############################################################################

import glob
import sys

sys.path.append("Core/")

from Sockets import Server
from Routing import Routing
import Controller
import Model

class PyBack:
	
	# C'est le point d'entrée du programme.
	def run(self):
		self.load() # Load les controllers/models/...
		self.Routing = Routing(self.controllers)
		self.Server = Server(self.Routing, self.databaseConfig)
		self.init() # S'occupe d'initialiser les controllers/models/...
		self.Server.run()
		
	
	####################################################################
	#	   Chargement des configs/models/controllers/compnents         #
	####################################################################
	
	def load(self):
		self.loadConfig()
		self.loadModels()
		self.loadComponents()
		self.loadController()
		
		
	# Charge et instancie les models contenu dans App/Models
	# Pour cela on ajoute le dossier App/Model au PATH et ensuite on liste
	# l'ensemble des fichiers .py pour pouvoir charger à la volé les models.
	# Cette method instancie les models
	def loadModels(self):
		self.models = {}
		sys.path.append("App/Models/")
		filesModel = glob.glob("App/Models/*.py")
		for f in filesModel:
			f = f.replace(".py", "")
			f = f.split("/")
			_className = f[len(f)-1]
			_class = getattr(__import__(_className), _className)
			_className = _className.replace("Model", "")
			self.models[_className] = _class()
	
	
	# Charge les components contenus dans App/Controllers/Components
	# Comme pour models sauf que les components ne sont pas instancié
	def loadComponents(self):
		self.components = {}
		sys.path.append("App/Controllers/Components")
		filesComponents = glob.glob("App/Controllers/Components/*.py")
		for f in filesComponents:
			f = f.replace(".py", "")
			f = f.split("/")
			_className = f[len(f)-1]
			_class = getattr(__import__(_className), _className)
			self.components[_className] = _class
	
	
	# Charge l'ensemble des controllers. Comme les models, les controllers
	# sont persistants tout au long du programme.
	def loadController(self):
		self.controllers = {}
		sys.path.append("App/Controllers/")
		filesController = glob.glob("App/Controllers/*.py")
		for f in filesController:
			f = f.replace(".py", "")
			f = f.split("/")
			_className = f[len(f)-1]
			_class = getattr(__import__(_className), _className)
			_className = _className.replace("Controller", "")
			self.controllers[_className] = _class(self.models, self.components)
	

	# S'occupe d'appeller les fonctions qui chargent les informations
	# de configuration. 
	# S'occupe d'enregistrer ces configurations dans des attributs de la
	# classe.
	# 
	# @param config Instance de la classe contenant les configurations
	# @return Dictionnaire contenant les infos de connexion de la DB
	def loadConfig(self):
		sys.path.append("App/Config/")
		_class = getattr(__import__("Config"), "Config")
		_config = _class()
		self.databaseConfig = self.loadDatabaseConfig(_config)
		self.networkConfig = self.loadNetworkConfig(_config)
		self.logsConfig = self.loadLogsConfig(_config)
		self.logEmailConfig = self.loadLogEmailConfig(_config)


	# Charge les informations de la base de données. Si certaines infos
	# ne sont pas fournies c'est celle par default qui seront utilisées
	# 
	# @param config Instance de la classe contenant les configurations
	# @return Dictionnaire contenant les infos de connexion de la DB
	def loadDatabaseConfig(self, config):
		_config = {
			"driver": "mysql", 
			"host": "localhost", 
			"username": "root", 
			"password": "", 
			"database": "pyBack", 
			"prefix": ""
			}
		_config.update(config.database())
		return _config

		
	# Charge les informations pour les sockets. Si certaines infos ne 
	# sont pas fournies c'est les infos par default qui seront choisies
	# 
	# @param config Instance de la classe contenant les configurations
	# @return Dictionnaire contenant les infos du réseau
	def loadNetworkConfig(self, config):
		_config = {
			"port": "8080",
			"listen": 5
			}
		_config.update(config.network())
		return _config
	
	def loadLogsConfig(self, config):
		_config = {
			"env": "prod",
			"folder": "./",
			"file": "logpyback.log"
			}
		_config.update(config.logs())
		return _config
	
	
	# Charge les emails auquels doivent-être envoyés les mails des logs
	# 
	# @param config Instance de la classe contenant les configurations
	# @return Dictionnaire contenant les emails pour les logs
	def loadLogEmailConfig(self, config):
		_config = {}
		_config.update(config.logEmail())
		return _config
		
	
	####################################################################
	#	   Init des controllers 									   #
	####################################################################
	
	# S'occupe d'envoyer au controller l'objet Server.
	def init(self):
		for key in self.controllers:
			getattr(self.controllers[key], 'setInfos')(self.Server)
	
	####################################################################
	#	  Tools for testing                                            #
	####################################################################
	
	# Permet d'afficher les configurations pour les tests
	def writeConfig(self):
		print self.databaseConfig
		print self.networkConfig
		print self.logsConfig
		print self.logEmailConfig
		
Project = PyBack()
Project.run()
#Project.loadConfig()
#Project.writeConfig()
