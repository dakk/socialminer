import copy
import logging
import sys
import os
import json
import time
import shelve
from queue import Queue
from threading import Lock, Thread
from . import config, reporter
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

		if report.user in self.reportsDict[report.adapter]:
			#logger.info ('%s: User %s already reported, updating', report.adapter, report.user)#print (str (report))
			# Update shared resources
			for tid in report.resources:
				if not tid in self.reportsDict[report.adapter][report.user].resources:
					self.reportsDict[report.adapter][report.user].resources[tid] = report.resources[tid]

			# Update geolocalization
			if self.reportsDict[report.adapter][report.user].geolocalization == None and report.geolocalization != None:
				self.reportsDict[report.adapter][report.user].geolocalization = report.geolocalization

		else:
			logger.info ('%s: Reporting user %s', report.adapter, report.user)#print (str (report))
			self.reportsDict[report.adapter][report.user] = report

		self.reportsDict[report.adapter][report.user].confidence = len (self.reportsDict[report.adapter][report.user].resources)

		self.db = shelve.open ('./reports.db')
		self.db['reports'] = self.reportsDict
		self.db.sync ()
		self.db.close ()

		self.reportLock.release ()


	def startReporter (self):
		self.reporter = reporter.Reporter (self.conf['p2p']['port'], self.conf['p2p']['seeds'], self.reportHandler)
		t = Thread(target=self.announce, args=())
		t.start ()

	def announce (self):
		i = 0
		rd = copy.deepcopy (self.reportsDict)

		for k in rd:
			data = {}
			data[k] = {}
			for kk in rd[k]:
				i += 1
				self.reporter.announce (rd[k][kk])
		logger.debug ('Announced %s accounts to network', i)


	def reportHandler (self, report, broadcast=True):
		self.queue.put ((report, broadcast))


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


	def dump (self):
		rd = copy.deepcopy (self.reportsDict)

		for k in rd:
			data = {}
			data[k] = {}
			for kk in rd[k]:
				data[k][kk] = rd[k][kk].serialize ()

			f = open ('reports_' + k + '.json', 'w')
			f.write (json.dumps (data, indent=4, separators=(',', ': ')))
			f.close ()


	def loop (self):
		i = 0
		for adapter in self.adapters:
			thread = Thread(target=adapter.loop, args=())
			self.threads.append (thread)
			thread.start ()
			logger.info ('Started thread for adapter %s', adapter.NAME)

		while True:
			i += 1
			t = True
			while t:
				try:
					(report, broadcast) = self.queue.get_nowait ()
					self.report (report)
					if broadcast:
						self.reporter.announce (d)
				except:
					t = False

			rac = 0
			for ad in self.reportsDict:
				logger.debug ('%s -> %d accounts', ad, len (self.reportsDict[ad]))
				rac += len (self.reportsDict[ad])

			logger.debug ('Running, %d suspicious accounts detected', rac)

			self.reporter.stats ()
			time.sleep (10)

			if i % 6 == 0:
				t = Thread(target=self.announce, args=())
				t.start ()
			if i % 12 == 0:
				t = Thread(target=self.dump, args=())
				t.start ()

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
	sm.startReporter ()
	sm.loop ()
