# -*- coding: UTF-8 -*-
###############################################################################
##                                                                           ##
##   ##  ##   #####   ###   ##   ##       ##      ####     ####  ###   ##    ##
##   ## ##    ##      ## ## ##   ##     ##  ##    ##  ##    ##   ## ## ##    ##
##   ####     #####   ##  ####   ##    ##    ##   ##   ##   ##   ##  ####    ##
##   ## ##    ##      ##   ###   ##     ##  ##    ## ##     ##   ##   ###    ##
##   ##  ##   #####   ##    ##   #####    ##      ###      ####  ##    ##    ##
##                                                                           ##
##  @author : Schrapnell                                                     ##
##  @project : pyBack                                                        ##
##  @file : Logs.py         												 ##
##  @since : 0.1                                                             ##
###############################################################################

import logging
import smtplib

class Logs():
  def __init__(self, config, mails):
    self.prod = 2
    if config["env"] == "dev":
      self.prod = 0
    elif config["env"] == "preprod":
      self.prod = 1
    self.mailDict = {}
    for key, value in mails:
      self.mailDict[key] = value
    # Display the exact hour of the log, set the output file
    self.filepath = config["folder"] + "/" + config["file"]
    if self.prod > 0:
      logging.basicConfig(filename=self.filepath,
	  		  format='%(asctime)s -- %(levelname)s : %(message)s',
			  datefmt='%d/%m/%Y %H:%M:%S',
			  level=logging.INFO)
    else:
      logging.basicConfig(format='%(asctime)s -- %(levelname)s : %(message)s',
			  datefmt='%d/%m/%Y %H:%M:%S',
			  level=logging.DEBUG)

  def sendEmail(self, msg):
    server = smtplib.SMTP('localhost')
    for key, value in self.mailDict:
      server.sendmail("logsystem@pyback.fr", key, msg)
    server.quit()

  def debug(self, msg):
    # Used during debug mode, ignored during production
    logging.debug(msg)

  def info(self, msg):
    # Just a small thing to notify in the logfile
    logging.info(msg)

  def warning(self, msg):
    # Small error => no email ?
    logging.warning(msg)

  def error(self, msg):
    # Something important that should not happen => email during (pre)prod
    logging.error(msg)
    if self.prod > 0:
      self.sendEmail(msg)

