# -*- coding: utf-8 -*-
"""
Adapted from Alexa Skill sample color-expert-python
"""

from __future__ import print_function
from dialog_manager import DialogManager
from context_manager import ContextManager

class ArgumentManager(intent, context):
    def __init__:
        self.intent = intent
        self.context = context

    def createIntentObject(self):
        intent_name  = self.intent['name']
        if intent_name == "INFORM":
            country = self.intent['slots']['country']['value']
            city = self.intent['slots']['city']['value']
            topic = self.intent['slots']['topic']['value']
            intent_object = InformObject(intent_name, country, city, topic)
        elif intent_name = "MOVE":
            country = self.intent['slots']['country']['value']
            city = self.intent['slots']['city']['value']
            intent_object = MoveObject(intent_name, country, city)
        elif intent_name = "JOB":
            country = self.intent['slots']['country']['value']
            city = self.intent['slots']['city']['value']
            intent_object = JobObject(intent_name, country, city)
        else:
            raiseValueError("Invalid intent")

        return intent_object

    def getContextObject(self):
        arg_object = self.createIntentObject()
        context_manager = ContextManager()


    def contextCleanUp(self):
        context_object = self.getContextObject()
        return


# --------------- Main handler ------------------

def lambda_handler(event, context):
""" Route the incoming request based on type (LaunchRequest, IntentRequest,
etc.) The JSON body of the request is provided in the event parameter.
print("event.session.application.applicationId=" +
event['session']['application']['applicationId'])
Uncomment this if statement and populate with your skill's application ID to
prevent someone else from configuring a skill that sends requests to this
function.
"""

    if (event['session']['application']['applicationId'] !=
        "amzn1.echo-sdk-ams.app.[unique-value-here]"):
        raise ValueError("Invalid Application ID")

    dm = DialogManager()
    if event['session']['new']:
    #dm.on_session_started({'requestId': event['request']['requestId']},
       event['session'])

    if event['request']['type'] == "LaunchRequest":
     #return dm.on_launch(event['request'], event['session'])


    elif event['request']['type'] == "IntentRequest":
    #return dm.on_intent(event['request'], event['session'])
    arg_manager = new ArgumentManager(event['request']['intent'], event['session'])
    arg_object = new


    elif event['request']['type'] == "SessionEndedRequest":
    #return dm.on_session_ended(event['request'], event['session'])
