# -*- coding: UTF-8 -*-
###############################################################################
##                                                                           ##
##   ##  ##   #####   ###   ##   ##       ##      ####     ####  ###   ##    ##
##   ## ##    ##      ## ## ##   ##     ##  ##    ##  ##    ##   ## ## ##    ##
##   ####     #####   ##  ####   ##    ##    ##   ##   ##   ##   ##  ####    ##
##   ## ##    ##      ##   ###   ##     ##  ##    ## ##     ##   ##   ###    ##
##   ##  ##   #####   ##    ##   #####    ##      ###      ####  ##    ##    ##
##                                                                           ##
###############################################################################
##                                                                           ##
##  Fichier de configuration de l'application.                               ##
##    * Configuration de la base de donnée                                   ##
##    * Configuration du réseau                                              ##
##    * Configuration du système de log                                      ##
##                                                                           ##
###############################################################################

class Config:
	
	def database(self):
		return {
			"driver": "mysql", 
			"host": "localhost", 
			"username": "root", 
			"password": "", 
			"database": "test", 
			"prefix": ""
			}
		
	def network(self):
		return {
			"port": "8080",
			"listen": 5
			}
			
	def logs(self):
		return {
			"env": "dev", 
			"folder": "./",
			"file": "meslogspersos"
		}

	def logEmail(self):
		return {
			"azmimik@gmail.com": 5,
			"cderbois@gmail.com": 3,
			"antoine.decevins@gmail.com": 4
		}
