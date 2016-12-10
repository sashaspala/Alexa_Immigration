from abc import ABCMeta, abstractmethod, abstractproperty

class IntentObject():

    __metaclass__ = ABCMeta

    def __init__(self, intent):
        self.intent = intent

    def get_intent(self):
        return self.intent

    @abstractmethod
    def is_complete(self):
        raise NotImplementedError("is_complete is not implemented")
