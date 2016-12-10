from intent_object import IntentObject
from intents import Intent

class JobObject(IntentObject):
    def __init__(self, country=None, city=None):
        super(JobObject, self).__init__(Intent.JOB, country)
        self.city = city

    def isComplete(self):
        if self.intent == None or self.country == None:
            return False
        else:
            return True

    def getCity(self):
        return self.city

    def setCity(self):
        self.city = city

if __name__ == "__main__":
    job = JobObject()
    assert not job.isComplete()
    job.setCountry("Canada")
    assert job.isComplete()
