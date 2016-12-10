#!/usr/bin/env python
from intent_object import IntentObject

class MoveObject(IntentObject):
    def __init__(self, country=None, city=None):
        super(MoveObject, self).__init__("MOVE", country)
        self.city = city

    def is_complete(self):
        return not self.country is None and not self.intent is None

    def get_city(self):
	return self.city

    def set_city(self, city):
        self.city = city


if __name__ == "__main__":
    move = MoveObject()
    assert not move.is_complete()
    move.set_country("Canada")
    assert move.is_complete()
