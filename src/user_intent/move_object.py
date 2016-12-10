#!/usr/bin/env python
from intent_object import IntentObject
from intents import Intent

class MoveObject(IntentObject):
    def __init__(self, country=None, city=None):
        super(MoveObject, self).__init__(Intent.MOVE, country)
        self.city = city

    def isComplete(self):
        return not self.country is None and not self.intent is None

    def getCity(self):
	return self.city

    def setCity(self, city):
        self.city = city


if __name__ == "__main__":
    move = MoveObject()
    assert not move.isComplete()
    move.setCountry("Canada")
    assert move.isComplete()
