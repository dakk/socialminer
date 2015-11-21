class Resource:
	def __init__ (self, datetime, type, id, link, body, geolocalization = None, confidence = 1):
		self.type = type
		self.ID = id
		self.link = link
		self.body = body
		self.confidence = confidence
		self.datetime = datetime
		self.geolocalization = geolocalization

	def serialize (self):
		return { 'datetime': str (self.datetime), 'type': self.type, 'id': self.ID, 'link': self.link, 'body': self.body, 'confidence': self.confidence, 'geolocalization': str(self.geolocalization) }

	def __repr__ (self):
		return "<Resource DateTime=%s Type=%s ID=%s Link=%s Body=%s Confidence=%f Geo=%s>" % (str(self.datetime), self.type, self.ID, self.link, self.body, self.confidence, (self.geolocalization))

class Report:
	def __init__ (self, adapter, user, resources, datetime, avatar, confidence = 0.0, geolocalization = None):
		self.adapter = adapter
		self.user = user
		self.avatar = avatar
		self.confidence = confidence
		self.geolocalization = geolocalization
		self.resources = resources
		self.datetime = datetime

	def serialize (self):
		r = { 'adapter': self.adapter, 'avatar': self.avatar, 'user': self.user, 'resources': [], 'confidence': self.confidence, 'geolocalization': self.geolocalization, 'datetime': self.datetime }
		for res in self.resources:
			r['resources'].append (self.resources[res].serialize ())
		return r

	def __repr__ (self):
		r = "<%sReport User=%s DateTime=%s Avatar=%s Confidence=%s Geolocalization=%s Resources=%d>\n" % (self.adapter, self.user, str(self.datetime), self.avatar, self.confidence, str (self.geolocalization), len(self.resources))
		for res in self.resources:
			r += '\t' + str (self.resources[res]) + '\n'
		r += '</%sReport>' % self.adapter
		return r



# Adapter for social network
class SocialAdapter:
	NAME = 'None'

	def __init__ (self, authkeys, reporthandler):
		pass

	def authenticate (self):
		pass

	def loop (self):
		pass
