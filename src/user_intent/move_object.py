#!/usr/bin/env python
class MoveObject(IntentObject):
    def __init__(self, intent, country=None):
        super(MoveObject, self).__init__(intent)
        self.country = country

    def is_complete(self):
        return self.
