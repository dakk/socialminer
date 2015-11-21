import logging
import sys
import os
import json
import time
import shelve
from queue import Queue
from threading import Lock, Thread
from . import config
from .twitteradapter import TwitterAdapter
from .facebookadapter import FacebookAdapter

logger = logging.getLogger('socialminer')
logger.setLevel (10)


class SocialMiner:
	def __init__ (self, conf):
		self.conf = conf
		self.adapters = []
		self.threads = []
		self.reportLock = Lock ()
		self.reportsDict = {}
		self.queue = Queue ()

		self.db = shelve.open ('./reports.db')
		if 'reports' in self.db:
			self.reportsDict = self.db['reports']
		self.db.close ()

	def report (self, report):
		self.reportLock.acquire ()

		logger.info ('%s: Reporting user %s', report.adapter, report.user)#print (str (report))

		if report.user in self.reportsDict[report.adapter]:
			for tid in report.resources:
				if not tid in self.reportsDict[report.adapter][report.user].resources:
					self.reportsDict[report.adapter][report.user].resources[tid] = report.resources[tid]
		else:
			self.reportsDict[report.adapter][report.user] = report

		self.db = shelve.open ('./reports.db')
		self.db['reports'] = self.reportsDict
		self.db.sync ()
		self.db.close ()

		self.reportLock.release ()

	def reportHandler (self, report):
		self.queue.put (report)

	def startAdapters (self):
		adapts = []
		for adn in self.conf['adapters']:
				opts = self.conf['adapters'][adn]

				if adn == 'Twitter':
					tw = TwitterAdapter (opts, self.reportHandler)
					adapts.append (tw)

				if adn == 'Facebook':
					fb = FacebookAdapter (opts, self.reportHandler)
					adapts.append (fb)

		for adapter in adapts:
			if adapter.authenticate ():
				if not adapter.NAME in self.reportsDict:
					self.reportsDict [adapter.NAME] = {}
				self.adapters.append (adapter)


	def loop (self):
		for adapter in self.adapters:
			thread = Thread(target=adapter.loop, args=())
			self.threads.append (thread)
			thread.start ()
			logger.info ('Started thread for adapter %s', adapter.NAME)

		while True:
			t = True
			while t:
				try:
					d = self.queue.get_nowait ()
					self.report (d)
				except:
					t = False

			logger.debug ('Running, %d suspicious accounts detected', len (self.reportsDict['Twitter']))
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
