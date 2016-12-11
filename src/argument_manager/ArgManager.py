# -*- coding: utf-8 -*-
"""
Adapted from Alexa Skill sample color-expert-python
"""

from __future__ import print_function
#from context_manager import ContextManager
# get dialog manager somehow
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__))))
from user_intent.inform_object import InformObject


class ArgumentManager: # not sure if we really need the event session info
    def __init__(self, intent, context=None):
        self.intent = intent
        self.context = context

    def createIntentObject(self):
        intent_name  = self.intent['name']

        slots = self.intent['slots']
        if 'country' in slots and 'value' in slots['country']:
            country = slots['country']['value']
        else:
            country = None
        if 'city' in slots and 'value' in slots['city']:
            city = slots['city']['value']
        else:
            city = None
        if 'topic' in slots and 'value' in slots['topic']:
            topic = slots['topic']['value']
        else:
            topic = None

        if intent_name == "INFORM":
            intent_object = InformObject(country, city, topic)
        elif intent_name == "MOVE":
            intent_object = MoveObject(country, city)
        elif intent_name == "JOB":
            intent_object = JobObject(country, city)
        else:
            raiseValueError("Invalid intent")

        return intent_object

    def getContextObject(self):
        #argObject = self.createIntentObject()
        #contextManager = ContextManager()
        # context manager methods
        #return contextObject
        pass

    def contextCleanUp(self, contextObject):
        # take a context object, and remove unneccessary information
        pass

    def createArgumentObject(self):
        #contextObject = self.getContextObject()
        #argObject = self.contextCleanUp(contextObject)

        #return argObject
        pass

if __name__ == '__main__':
    intent = {
      "name": "INFORM",
      "slots": {
        "country": {
          "name": "country",
          "value": "Canada"
        },
        "city": {
          "name": "city"
        },
        "topic": {
          "name": "topic",
          "value": "the economy"
        }
      }
    }
    argMan = ArgumentManager(intent)
    arguments = argMan.createIntentObject()
    print(arguments.isComplete())
