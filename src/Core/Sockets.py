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
##  @file : Sockets.py                                                       ##
##  @since : 0.1                                                             ##
###############################################################################

import select
import socket
import json
import hashlib
import time
class Server:
	
	# Contructeur de la class Server.
	#
	# @param port Port de connexion
	# @param listen Nombre de connexion en attente max
	def __init__(self, routing, options):
		self.Routing = routing
		_options = {"port" : 35890, "listen" : 5}
		_options.update(options)
		# Initialisation of attr
		self.nbClients = 0	# Nb client connected
		self.clients = {}	# List of client with somes informations
		self.sockets = []	# List of client's socket
		
		# Lauching of the server / Creating socket
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.setblocking(0)
		self.socket.bind(('',_options["port"]))
		self.socket.listen(_options["listen"])



	# Surcouche de la fonction socket.recv
	# On utilise le systeme d'exeption de recv pour savoir si il reste
	# des donnees a lire
	#
	# @param socket Socket sur lequelle il faut recuperer les donnee
	# @return Donnee envoyee par le client
	def receive(self, socket):
		buf = "" # Variable dans laquelle on stocke les donnees
		_hasData = True # Nous permet de savoir si il y de donnees a lire
		test = 1
		while _hasData:
			socket.setblocking(0)
			try:
				_data = socket.recv(256)
				if(_data):
					buf += _data
				else:
					# Deconnexion du client
					_hasData = False
			except:
				_hasData = False
		return buf



	# Fonction qui lance les sockets et s'occupe des clients
	def run(self):
		# Adding of sockent in self.inputs for the selector
		self.sockets.append(self.socket)
		# Go
		while True:
			# Getting clients who writing to server. We only used readReady
			try:
				readReady ,writeReady, nothing = select.select(self.sockets, [], [])
			except select.error, e:
				# TODO: Systeme de log
				break
			except socket.error, e:
				#TODO: Systeme de log
				break
			
			# Getting input from client (or socket !)
			for sock in readReady:
				if sock == self.socket:
					# New client connected
					print "New client connected"
					client, address = self.socket.accept()
					# Forme du token :
					# sha512(time())+sha512(socket)+sha512(addr)
					timeHash = hashlib.sha224(str(time.time())).hexdigest()
					sockHash = hashlib.sha224(str(client)).hexdigest()
					addrHash = hashlib.sha224(str(address)).hexdigest()
					_infos = {
						"sock": client,
						"addr": address,
						"token": timeHash+sockHash+addrHash
						}
					print _infos['token']
					self.clients[client] = _infos
					self.nbClients += 1
					self.sockets.append(client)
					# TODO : Call Routing for onConnect Action
				else:
					# A client have send a request !
					try:
						data = self.receive(sock)
						if data:
							# On appelle le Routing
							error = self.Routing.callAction(self.clients[sock], data)
							if error:
								sock.send(json.dumps(error))
						else:
							print "client deconnecte"
							self.nbClients -= 1
							self.clients[sock] = None
							self.sockets.remove(sock)
					except socket.error, e:
						self.nbClients -= 1
						self.clients[sock] = None
						self.sockets.remove(sock)
