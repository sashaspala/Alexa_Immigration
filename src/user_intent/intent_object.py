from abc import ABCMeta, abstractmethod, abstractproperty

class IntentObject:
    """
    An abstract class to represent a user's question.
    """
    __metaclass__ = ABCMeta

    def __init__(self, intent, country):
        self.intent = intent
        self.country = country

    def getIntent(self):
        return self.intent

    def getCountry(self):
        return self.country

    def setCountry(self, country):
        self.country = country

    @abstractmethod
    def isComplete(self):
        """
        Check if all the needed slots to answer the question are filled
        """
        raise NotImplementedError("isComplete is not implemented")
