import tweepy
import logging
import time
from . import config
from .searchterms import SearchTerms
from .socialadapter import SocialAdapter, Report, Resource

logger = logging.getLogger('socialminer')

class TwitterAdapter (SocialAdapter):
	NAME = 'Twitter'

	def __init__ (self, authkeys, reportHandler):
		self.reportHandler = reportHandler
		self.authKeys = authkeys


	def authenticate (self):
		try:
			self.auth = tweepy.OAuthHandler (self.authKeys['consumer_key'], self.authKeys['consumer_secret'])
			self.auth.secure = True
			self.auth.set_access_token(self.authKeys['access_token'], self.authKeys['access_token_secret'])
			self.api = tweepy.API (self.auth)
			logger.info ('Adapter %s successfully logged', self.NAME)
			return True

		except Exception as e:
			logger.critical ('Bad authentication %s', e)
			return False


	def reportTweets (self, tweets):
		for tw in tweets:
			gl = None
			if tw.coordinates != None:
				gl = tw.coordinates
			elif tw.place != None:
				gl = tw.place
			elif tw.geo != None:
				gl = tw.geo

			res = Resource (tw.created_at, 'Tweet', tw.id, '', tw.text, geolocalization=gl)
			r = Report (self.NAME, tw.user.screen_name, {res.ID: res}, time.time (), tw.user.profile_image_url_https, geolocalization=gl)
			self.reportHandler (r)


	def analyze (self, phrase):
		f = True
		page = 1
		while f and page < 1499:
			try:
				res = self.api.search (phrase, rpp=100) #, page=page)
			except:
				logger.debug ('Reached rate limit, waiting 60 seconds...')
				time.sleep (60)
				continue

			if len (res) != 0:
				self.reportTweets (res)
				page += 1
				f = False #True
			else:
				f = False

	def loop (self):
		while True:
			(phrase_t, phrase) = SearchTerms.generate ()
			self.analyze (phrase)
			self.analyze (phrase_t)
			time.sleep (5)
