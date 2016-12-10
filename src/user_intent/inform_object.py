class InformObject(IntentObject):
	def __init__(self, intent_name, country, city, topic):
		IntentObject.__init__(self, intent, country)
		self.topic = topic
		self.city = city

	def isComplete(self):
		if self.intent == None or self.country == None or topic == None:
			return False
		else:
			return True

	def getTopic(self):
		return self.topic

	def getCity(self):
		return self.city
