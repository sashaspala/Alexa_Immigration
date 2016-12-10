# -*- coding: utf-8 -*-
"""
Adapted from Alexa Skill sample color-expert-python
"""

from __future__ import print_function
from dialog_manager import DialogManager

class ArgumentManager(event, context):
    def __init__:
        self.event = event
        self.context = context

    def getContextObject(self):
        pass

    def contextCleanUp(self):
        pass

class IntentObject():

class MoveObject(IntentObject):
    pass

class InformObject(IntentObject):
    passf

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
        arg_manager = new ArgumentManager(event, context)



    elif event['request']['type'] == "SessionEndedRequest":
        #return dm.on_session_ended(event['request'], event['session'])
