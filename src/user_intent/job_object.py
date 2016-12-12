from intent_object import IntentObject
from intents import Intent
from slots import Slots

class JobObject(IntentObject):
    def __init__(self, country=None, city=None):
        super(JobObject, self).__init__(Intent.JOB, country)
        self.setSlot(Slots.CITY, city)

    #def isComplete(self):
    #    if self.intent == None or self.country == None:
    #        return False
    #    else:
    #        return True

    def getCity(self):
        return self.getSlot(Slots.CITY)

    def setCity(self, city):
        self.setSlot(Slots.CITY, city)

if __name__ == "__main__":
    job = JobObject()
    assert not job.isComplete()
    job.setSlot(Slots.COUNTRY, "Canada")
    assert job.isComplete()
