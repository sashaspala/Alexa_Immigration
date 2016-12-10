class MoveObject(IntentObject):
	def __init__(self, intent_name, country, city):
		IntentObject.__init__(self, intent_name, country)
		self.city = city

	def isComplete(self):
		if self.intent_name == None or self.country == None:
			return False
		else:
			return True

	def getCountry(self):
		return self.country

	def getCity(self):
		return self.city
