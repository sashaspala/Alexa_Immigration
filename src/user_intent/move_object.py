#!/usr/bin/env python
from intent_object import IntentObject
from intents import Intent
from slots import Slots

class MoveObject(IntentObject):
    def __init__(self, country=None, city=None):
        super(MoveObject, self).__init__(Intent.MOVE, country)
        self.setOptionalSlot(Slots.CITY, city)

    #def isComplete(self):
    #    return not self.country is None and not self.intent is None

    def getCity(self):
	return self.getSlot(Slots.CITY)


if __name__ == "__main__":
    move = MoveObject()
    assert not move.isComplete()
    move.setRequiredSlot(Slots.COUNTRY, "Canada")
    assert move.isComplete()
