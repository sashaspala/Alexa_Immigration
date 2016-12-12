from intent_object import IntentObject
from intents import Intent
from slots import Slots

class InformObject(IntentObject):
	def __init__(self, country=None, city=None, topic=None):
		super(InformObject, self).__init__(Intent.INFORM, country)
		#self.topic = topic
		#self.city = city
                self.setRequiredSlot(Slots.TOPIC, topic)
                self.setOptionalSlot(Slots.CITY, city)

	#def isComplete(self):
	#	if self.intent == None or self.country == None or self.topic == None:
	#		return False
	#	else:
	#		return True

	def getTopic(self):
		return self.getSlot(Slots.TOPIC)
        
	def getCity(self):
		return self.getSlot(Slots.CITY)

if __name__ == "__main__":
    inform = InformObject()
    assert not inform.isComplete()
    inform.setRequiredSlot(Slots.COUNTRY, "Canada")
    inform.setRequiredSlot(Slots.TOPIC, "weather")
    assert inform.isComplete()
