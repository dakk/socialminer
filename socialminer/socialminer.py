import logging
import sys
import os
import json
import time
from threading import Lock, Thread
from . import config
from .twitteradapter import TwitterAdapter

logger = logging.getLogger('socialminer')
logger.setLevel (10)


class SocialMiner:
	def __init__ (self, conf):
		self.conf = conf
		self.adapters = []
		self.threads = []
		self.reportLock = Lock ()
		self.reportsDict = {}
		self.reports = []

	def reportHandler (self, report):
		self.reportLock.acquire ()
		print (report)
		self.reportsDict[report.adapter][report.user] = report
		self.reports.append (report)
		self.reportLock.release ()


	def startAdapters (self):
		adapts = []
		for adn in self.conf['adapters']:
				opts = self.conf['adapters'][adn]

				if adn == 'Twitter':
					 tw = TwitterAdapter (opts, self.reportHandler)
					 adapts.append (tw)

		for adapter in adapts:
			if adapter.authenticate ():
				self.reportsDict [adapter.NAME] = {}
				self.adapters.append (adapter)


	def loop (self):
		while True:
			logger.debug ('Running, %d suspicious accounts detected', len (self.reports))
			for ad in self.reportsDict:
				logger.debug ('\t%s -> %d accounts', ad, len (self.reportsDict[ad]))
			time.sleep (10)

def main ():
	logger.debug ('Starting socialminer.')

	if not os.path.exists(config.DATA_DIR+'/socialminer.json'):
		logger.warning ('Configuration file %s not present', config.DATA_DIR+'/socialminer.json')
		f = open (config.DATA_DIR+'/socialminer.json', 'w')
		f.write (json.dumps (config.BASE_CONF, indent=4, separators=(',', ': ')))
		f.close ()
		logger.warning ('Configuration file %s created', config.DATA_DIR+'/socialminer.json')
		print ('Edit your configuration file and restart socialminer.')
		sys.exit (0)

	f = open (config.DATA_DIR+'/socialminer.json', 'r')
	conf = f.read ()
	f.close ()

	jconf = json.loads (conf)
	logger.info ('Configuration file %s loaded', config.DATA_DIR+'/socialminer.json')

	sm = SocialMiner (jconf)
	sm.startAdapters ()
	sm.loop ()
