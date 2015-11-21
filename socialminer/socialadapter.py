# Report packet
class Report:
    def __init__ (self, adapter, user, resource_type, resource_id, resource_link, resource_body, confidence):
	self.adapter = adapter
	self.user = user
	self.resourceType = resource_type
	self.resourceID = resource_id
	self.resourceLink = resource_link
	self.resourceBody = resource_body
	self.confidence = confidence

    def serialize (self):
	return { 'adapter': self.adapter, 'user': self.user, 'resourceType': self.resourceType, 'resourceID': self.resourceID, 'resourceLink': self.resourceLink, 'resourceBody': self.resourceBody, 'confidence': self.confidence }

    def __repr__ (self):
	return "<%sReport User=%s Confidence=%s RType=%s RID=%s RLink=%s RBody=%s>" % (self.adapter, self.user, self.confidence, self.resourceType, self.resourceID, self.resourceLink, self.resourceBody)

    
# Adapter for social network
class SocialAdapter:
    NAME = 'None'
    
    def __init__ (self, authkeys, reporthandler):
	pass

    def authenticate (self):
	pass
    
