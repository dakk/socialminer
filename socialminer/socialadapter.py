class Resource:
	def __init__ (self, type, id, link, body, confidence):
		self.type = type
		self.ID = id
		self.link = link
		self.body = body
		self.confidence = confidence

	def serialize (self):
		return { 'type': self.type, 'id': self.ID, 'link': self.link, 'body': self.body, 'confidence': self.confidence }

	def __repr__ (self):
		return "<Resource Type=%s ID=%s Link=%s Body=%s Confidence=%f>" % (self.type, self.ID, self.link, self.body, self.confidence)

class Report:
	def __init__ (self, adapter, user, resources, confidence = 0.0, geolocalization = None):
		self.adapter = adapter
		self.user = user
		self.confidence = confidence
		self.geolocalization = geolocalization
		self.resources = resources

	def serialize (self):
		return { 'adapter': self.adapter, 'user': self.user, 'resources': self.resources.map (lambda r: r.serialize ()), 'confidence': self.confidence, 'geolocalization': self.geolocalization }

	def __repr__ (self):
		r = "<%sReport User=%s Confidence=%s Geolocalization=%s Resources=%d>\n" % (self.adapter, self.user, self.confidence, self.geolocalization, len(self.resources))
		for res in self.resources:
			r += '\t' + r + '\n'
		r += '</%sReport>'



# Adapter for social network
class SocialAdapter:
	NAME = 'None'

	def __init__ (self, authkeys, reporthandler):
		pass

	def authenticate (self):
		pass
