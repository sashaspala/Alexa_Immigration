from abc import ABCMeta, abstractmethod, abstractproperty

class IntentObject:
    """
    An abstract class to represent a user's question.
    """
    __metaclass__ = ABCMeta

    def __init__(self, intent, country):
        self.intent = intent
        self.country = country

    def get_intent(self):
        return self.intent

    def get_country(self):
        return self.country

    def set_country(self, country):
        self.country = country

    @abstractmethod
    def is_complete(self):
        """
        Check if all the needed slots to answer the question are filled
        """
        raise NotImplementedError("is_complete is not implemented")
