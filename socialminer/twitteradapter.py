import tweepy
import logging
from . import config
from .socialadapter import SocialAdapter, Report

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
			logger.info ('Adapter %s successfully logged as %s', self.NAME, self.api.me().name)
			return True

		except Exception as e:
			logger.critical ('Bad authentication %s', e)
			return False
