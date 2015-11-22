from kad import *
import logging
from .socialadapter import Report, Resource

logger = logging.getLogger('socialminer')


class ReporterDHTHandler (kad.DHTRequestHandler):
	reportHandler = None

	def handle_store (self, message):
		v = message ['value']
		ReporterDHTHandler.reportHandler (Report.deserialize (v), False)
		super (ReporterDHTHandler, self).handle_store (message)

# Report accounts to the distributed DB
class Reporter:
	def __init__ (self, port, seeds, reportHandler):
		ReporterDHTHandler.reportHandler = reportHandler
		self.dht = DHT ('', port, requesthandler=ReporterDHTHandler)
		self.dht.bootstrap (list (map (lambda x: (x.split(':')[0],int (x.split(':')[1])), seeds)))
		logger.info ('Reporter bootstrapped from %d peers', len (self.dht.peers ()))

	def stats (self):
		logger.debug ('P2P network connected to %d peers, %d keys stored', len (self.dht.peers ()), len (self.dht.data))

	def announce (self, report):
		self.dht[str (report.adapter) + '|' + str (report.user)] = report.serialize ()
