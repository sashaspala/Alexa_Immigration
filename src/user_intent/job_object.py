class JobObject(IntentObject):
    def __init__(self, intent, country, city):
        IntentObject.__init__(self, intent, country)
        self.city = city

    def isComplete(self):
        if self.intent == None or self.country == None:
            return False
        else:
            return True

    def get_city(self):
        return self.city
