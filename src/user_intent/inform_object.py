from intent_object import IntentObject
from intents import Intent

class InformObject(IntentObject):
	def __init__(self, country=None, city=None, topic=None):
		super(InformObject, self).__init__(Intent.INFORM, country)
		self.topic = topic
		self.city = city

	def isComplete(self):
		if self.intent == None or self.country == None or self.topic == None:
			return False
		else:
			return True

	def getTopic(self):
		return self.topic
        
        def setTopic(self, topic):
                self.topic = topic

	def getCity(self):
		return self.city

        def setCity(self):
                self.city = city

if __name__ == "__main__":
    inform = InformObject()
    assert not inform.isComplete()
    inform.setCountry("Canada")
    inform.setTopic("weather")
    assert inform.isComplete()
