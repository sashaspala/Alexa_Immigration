# -*- coding: utf-8 -*-
"""
Adapted from Alexa Skill sample color-expert-python
"""

from __future__ import print_function

# import sys, os
# sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
# from src.user_intent.inform_object import InformObject
# from src.user_intent.move_object import MoveObject
# from src.user_intent.job_object import JobObject
# from ContextManager import ContextManager
# from QueryManager import QueryManager


welcome_text = "Welcome to Alexa Immigration Support. "
explanation_text = "You can ask me things like, Alexa, how do I move to Canada? Or you " \
                   "can say Alexa, what are jobs like in Australia? Currently, I can answer questions about" \
                   "jobs, moving, and general facts for Canada, Australia, and the UK. "
thank_you_text = "Thank you for using Alexa Immigration Support. Have a nice day! "


class ArgumentManager:  # not sure if we really need the event session info
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
            # raise ValueError("Invalid intent")
            ##might want to pass to end_session function here
            on_session_ended
        return intent_object

    def checkForUser(session):
        if session.get('user') is not None:
            ## already set up the user account
            return (session['user']['userId'], session['user']['accessToken'])
        else:
            return None

    def getUserInfo(self, session):
        # user = checkForUser(session):
        # if user is not None:
        pass

    def getContextObject(self, intent_object, is_new_session, user):
        contextManager = ContextManager()
        contextObject = contextManager.getContext(intent_object)

        # maybe, if session is not new, we might have to confirm that it's
        # the correct user (might not be needed)
        return contextObject

    def contextCleanUp(self, contextObject):
        # take a context object, and remove unneccessary information
        pass

    def query_db(self, unambiguousObject):
        return QueryManager.getCountryInfo(unambiguousObject)  # get actual fact


# response builders
# ----------------------------------------------------------------------------

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


def build_final_speechlet_response(title, speech_output, reprompt_text, card_output, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': speech_output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + card_output
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


# functions for dialogue manager
# --------------------------------------------------------------------------

# is the idea behind this method to handle sessions started when the user is using the skill for the first time?
def on_blank_session_started(session):
    session_attributes = {'questions': []}
    speech_output = welcome_text + explanation_text
    reprompt_text = explanation_text
    card_title = "Welcome"

    # todo: what information would we need to get from the user?

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, False))


def on_session_started(session):
    # create a list in attributes that stores all fact dictionaries in current session
    # this will allow us to return a card at the end with a summary of the facts discussed

    # todo: we might need to redirect a user to on_blank_session_started if the user
    # todo: is using the app for the first time


    session_attributes = {'questions': []}
    speech_output = welcome_text + explanation_text

    # todo: we might not need to provide example questions, Alexa might do that for us. Need to look into that
    reprompt_text = explanation_text
    card_title = "Welcome"
    should_end_session = False

    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def ask_clarification(session):
    """This function sends a response asking the speaker to repeat their question
       This function is used in situations where an intent cannot be understood """

    speech_output = "Sorry, I didn't understand what you said. " + explanation_text

    reprompt_text = "Sorry, I didn't understand what you said." + explanation_text
    card_title = "Need clarification: "

    session_attributes = session.get('attributes', {})
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def help_intent(session):
    """Returns a response in the event of an AMAZON.HelpIntent"""

    session_attributes = session.get('attributes', {})
    speech_output = explanation_text
    reprompt_text = explanation_text
    card_title = "Help: "

    should_end_session = False

    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def on_intent_question_asked(fact, session, intentObject):
    """This function takes a fact string created in response to an intent
        and builds a response to send back to Alexa"""

    # gets fact, session, intent object(optional?)
    speech_output = fact + " What else would you like to know?"  # continue the conversation
    reprompt_text = "Would you like to learn anything else?"

    # add current session attributes to the list of session attributes
    session['attributes']['questions'].append({"fact": fact})  # possibly using it for card
    session_attributes = session.get('attributes')

    return build_response(session_attributes, build_speechlet_response(intentObject.getCountry(), \
                                                                       speech_output, reprompt_text, False))


def on_launch(launch_request, session):
    """Responds to Launch Requests"""
    if session['new']:
        return on_session_started(session)
    else:  # when a request was made with no intent, and it's not the beginning of a session
        return ask_clarification(session)


def on_intent(intent_request, session, is_new_session):
    # redirect 'AMAZON.HelpIntent
    if intent_request['intent']['name'] == "AMAZON.HelpIntent":
        return help_intent(session)

    am = ArgumentManager(intent_request['intent'], session)
    # sending the intents and context element to argurment manager

    # get my outgoing object from the contextmanager
    if is_new_session:
        # additionally send user info from LinkAccount card
        # todo: buildUserInfo method
        userId = am.buildUserInfo(session)
        unambiguousObject = am.getContextObject(am.createIntentObject(), True,
                                                None)  # (of type intentObject) # 'None' bit is User
    else:
        unambiguousObject = am.getContextObject(am.createIntentObject(), False, None)

    ##query_db
    fact = am.query_db(unambiguousObject)
    return on_intent_question_asked(fact, session)


def create_final_card_output(session):
    if 'questions' not in session.get('attributes', {}):
        card_output = thank_you_text

    else:
        questions = session['attributes']['questions']
        facts = [question.get('fact') for question in questions if question.get('fact') is not None]

        # covers only facts so far
        if facts:
            card_output = "These are the facts we covered in this session: %s. " % ('. '.join(facts))
        else:
            card_output = thank_you_text

    return card_output


def on_session_ended(request, session):
    # make a card collecting all the intents, countries and topics discussed during
    # the session
    card_title = "Session Ended: Your Conversation Today"
    speech_output = "You will receive a card " \
                    "with all the information you asked about today. " \
                    + thank_you_text

    card_output = create_final_card_output(session)

    should_end_session = True
    return build_response({}, build_final_speechlet_response(
        card_title, speech_output, None, card_output, should_end_session))


# lambda handler
# -----------------------------------------------------------------------------

def lambda_handler(event, context):
    # pass intent, context
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
        # this is a new session and you didn't have any special request
        return on_launch(event['request'], event['session'])

    elif event['request']['type'] == "IntentRequest":

        if event['session']['new']:
            # new session, need to update user object
            return on_intent(event['request'], event['session'], True)
        else:
            return on_intent(event['request'], event['session'], False)

    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])