# -*- coding: utf-8 -*-
"""
Adapted from Alexa Skill sample color-expert-python
"""

from __future__ import print_function
# get context manager
# get dialog manager somehow

# importing objects for local testing
#import sys, os
#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
#from user_intent.inform_object import InformObject

class ArgumentManager: # not sure if we really need the event session info
    def __init__(self, intent, context=None):
        self.intent = intent
        self.name = intent['name']
        self.slots = intent['slots']
        self.context = context

    def createIntentObject(self):
        country = None
        city = None
        topic = None
        for tag in self.slots:
            ## possible a country, city, topic
            if tag == 'country':
                country = tag['value']
            if tag == 'city':
                city = tag['value']
            if tag == 'topic':
                topic = tag['value']
        ## now we have minimum values for intents/slots
        ## want to create intentObject, then pass to context manager

        if self.name == "INFORM":
            intent_object = InformObject(country, city, topic)
        elif self.name == "MOVE":
            intent_object = MoveObject(country, city)
        elif self.name == "JOB":
            intent_object = JobObject(country, city)
        else:
            raiseValueError("Invalid intent")
            ##might want to pass to end_session function here

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
        contexObject = self.getContextObject()
        #argObject = self.contextCleanUp(contextObject)

        return contextObject


def on_session_started(session):
    speech_output = "Welcome to Alexa Immigration Support!"
    reprompt_text = "You can ask me things like, Alexa, how do I move to Canada? Or you \
    can say Alexa, what are jobs like in Australia? Currently, I can answer questions about \
    jobs, moving, and general facts for Canada, Australia, and the UK."
    session_attributes = session.get('attributes', {})
    return build_response(session_attributes, build_speechlet_response('Test', speech_output, reprompt_text, True))

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def on_launch(launch_request, session):
    if event['session'] == 'new':
        return on_session_started(session)
    else:
        return ask_clarification(session)

def ask_clarification(session):
    speech_output = "Sorry, I didn't understand what you said." \
       "You can ask me things like, Alexa, how do I move to Canada? or " \
       "can say Alexa, what are jobs like in Australia?" \
       "Currently, I can answer questions about jobs, moving," \
       "and general facts for Canada, Australia, and the UK."

    reprompt_text = "Sorry, I didn't understand what you said." \
       "You can ask me things like, Alexa, how do I move to Canada? or " \
       "can say Alexa, what are jobs like in Australia?" \
       "Currently, I can answer questions about jobs, moving," \
       "and general facts for Canada, Australia, and the UK."

    session_attributes = session.get('attributes', {})
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response('Test', speech_output, reprompt_text, should_end_session))


def lambda_handler(event, context):
    #pass intent, context


    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """

    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")


    if event['request']['type'] == "LaunchRequest":
        #this is a new session and you didn't have any special request
        return on_launch(event['request'], event['session'])

    elif event['request']['type'] == "IntentRequest":
        am = ArgumentManager(event['request']['intent'], context)
        if event['session']['new']:
            #new session, need to update user object
            outgoingObject = am.getContextObject(dm.createIntentObject(), True)
        else:
            outgoingObject = am.getContextObject(dm.createIntentObject(), False)

    elif event['request']['type'] == "SessionEndedRequest":
        pass


'''
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
'''
