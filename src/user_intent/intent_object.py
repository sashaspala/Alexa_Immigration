from abc import ABCMeta, abstractmethod, abstractproperty
from slots import Slots

class IntentObject:
    """
    An abstract class to represent a user's question.
    """
    __metaclass__ = ABCMeta

    def __init__(self, intent, country):
        #self.requiredSlots = {Slots.INTENT : intent, Slots.COUNTRY : country}
        #self.optionalSlots = {}
        self.slots = {Slots.INTENT : intent, Slots.COUNTRY : country}
        self.userInfo = {}
        self.requiredSlots = [Slots.INTENT, Slots.COUNTRY]

    def getIntent(self):
        #return self.requiredSlots[Slots.INTENT]
        return self.slots[Slots.INTENT]

    def getCountry(self):
        #return self.requiredSlots[Slots.COUNTRY]
        return self.slots[Slots.COUNTRY]

    def getSlot(self, slotName):
        #if slotName in self.requiredSlots:
        #    return self.requiredSlots[slotName]
        #if slotName in self.optionalSlots:
        #    return self.optionalSlots[slotName]
        return self.slots.get(slotName, None)

    def getSlots(self):
        """
        Return all the slots, including required and optional slots, 
        empty slots' values would be None.
        """
        #result = self.requiredSlots.copy()
        #for k, v in self.optionalSlots.items():
        #    result[k] = v
        #return result
        return self.slots

    #def setRequiredSlot(self, slotName, slotValue):
    #    self.requiredSlots[slotName] = slotValue

    #def setOptionalSlot(self, slotName, slotValue):
    #    self.optionalSlots[slotName] = slotValue

    def setSlot(self, slotName, slotValue):
        self.slots[slotName] = slotValue

    def isComplete(self):
        """
        Check if all the needed slots to answer the question are filled
        """
        #for k,v in self.requiredSlots.items():
        #    if v is None:
        #        return False
        #return True
        for slotName in self.requiredSlots:
            if self.getSlot(slotName) is None:
                return False
        return True

    def getEmptySlots(self):
        # return [k for k,v in self.requiredSlots.items() if v is None]
        return [k for k in self.requiredSlots if self.getSlot(k) is None]

    def setAsRequired(self, slotName):
        self.requiredSlots.append(slotName)

    #def getOptEmptySlots(self):
    #    return [k for k,v in self.optionalSlots.items() if v is None]

    def getUserInfo(self):
        return self.userInfo

    def setUserInfo(self, name, value):
        self.userInfo[name] = value
