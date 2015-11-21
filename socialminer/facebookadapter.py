import logging
import time
import facebook
import requests
from . import config
from .searchterms import SearchTerms
from .socialadapter import SocialAdapter, Report, Resource

logger = logging.getLogger('socialminer')

class FacebookAdapter (SocialAdapter):
	NAME = 'Facebook'

	def __init__ (self, authkeys, reportHandler):
		self.reportHandler = reportHandler
		self.authKeys = authkeys


	def authenticate (self):
		try:
			self.api = facebook.GraphAPI(self.authKeys['access_token'])
			logger.info ('Adapter %s successfully logged', self.NAME)
			return True

		except Exception as e:
			logger.critical ('Bad authentication %s', e)
			return False



	def analyze (self, phrase):
		f = True
		while f:
			try:
				pd = self.api.request ('search', {'type': 'page', 'q': phrase})
				f = False
			except:
				logger.debug ('Reached rate limit or token expired, waiting 60 seconds...')
				time.sleep (60)
				continue

			for page in pd['data']:
				page_ob = self.api.get_object (page['id']+'/feed')

				for post in page_ob['data']:
					msg = ''
					if 'message' in post:
						msg = post['message'][0:128]

					res = Resource (post['created_time'], 'PagePost', post['id'], '', msg)
					r = Report (self.NAME, post['from']['name']+' | '+post['from']['id'], {res.ID: res}, time.time (), '')
					self.reportHandler (r)


	def loop (self):
		while True:
			(phrase_t, phrase) = SearchTerms.generate ()
			self.analyze (phrase)
			self.analyze (phrase_t)
			time.sleep (5)
