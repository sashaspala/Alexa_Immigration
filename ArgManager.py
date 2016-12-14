# -*- coding: utf-8 -*-
"""
Adapted from Alexa Skill sample color-expert-python
"""

from __future__ import print_function

from src.user_intent.inform_object import InformObject
from src.user_intent.move_object import MoveObject
from src.user_intent.job_object import JobObject
from src.context_manager.ContextManager import ContextManager
from src.query_manager.QueryManager import QueryManager
from src.user_setup.UserSetup import UserSetup
import random


welcome_text = "Welcome to Alexa Immigration Support. "
explanation_text = "You can ask me things like, Alexa, how do I move to Canada? Or you " \
                   "can say Alexa, what are jobs like in Australia? Currently, I can answer questions about" \
                   "jobs, moving, and general facts for Canada, Australia, and the UK. "
thank_you_text = "Thank you for using Alexa Immigration Support. Have a nice day! "


class ArgumentManager:  # not sure if we really need the event session info
    def __init__(self, intent, user_id, context=None):
        self.intent = intent
        self.name = intent['name']
        self.slots = intent['slots']
        self.context = context
        self.user_id = user_id

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
            raise ValueError("Invalid intent")
            ##might want to pass to end_session function here


        return intent_object

    def get_user_id(self):
        return self.user_id

    def get_user_name(self):
        # todo: CLAY, return the name of the person given the user_id
        return QueryManager.get_name(self.user_id)

    def checkForUser(self):
        session = self.context

        if session.get('user') is not None:
            ## already set up the user account
            return (session['user']['userId'], session['user']['accessToken'])
        else:
            return None

    def getContextObject(self, intent_object, user):
        contextManager = ContextManager(user)
        contextObject = contextManager.getContext(intent_object)

        # maybe, if session is not new, we might have to confirm that it's
        # the correct user (might not be needed)
        return contextObject

    def contextCleanUp(self, contextObject):
        # take a context object, and remove unneccessary information
        pass

    def query_db(self, unambiguousObject):
        dict = unambiguousObject.getSlots()
        return QueryManager.getFact(unambiguousObject)

# response builders
# ----------------------------------------------------------------------------
def build_link_account_response():
    return {
      "version": "1.0",
      "response": {
        "outputSpeech": {"type":"PlainText","text":"Please go to your Alexa app and link your account."},
        "card": {
          "type": "LinkAccount"
        }
      }
    }

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

def tell_missing_info(session):
    """Gives a response when required information is missing"""
    speech_output = "I don\'t have enough information. " + explanation_text
    reprompt_text = explanation_text
    card_title = "Not enough information" + explanation_text

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


def on_intent_question_asked(fact, session, intent_object, name):
    """This function takes a fact string created in response to an intent
        and builds a response to send back to Alexa"""

    # gets fact, session, intent object(optional?)
    preamble = ""
    if bool(random.getrandbits(1)):
        preamble = "Ok, " + name + "here's, what I could find."

    content = fact + " What else would you like to know?"  # continue the conversation
    speech_output = preamble + content
    reprompt_text = "Would you like to learn anything else?"

    # add current session attributes to the list of session attributes
    current_session = intent_object.getSlots()
    current_session['fact'] = fact

    session['attributes']['questions'].append(current_session)  # possibly using it for card
    session_attributes = session.get('attributes')

    return build_response(session_attributes, build_speechlet_response(intent_object.getCountry(), \
                                                                       speech_output, reprompt_text, False))


def on_launch(launch_request, session):
    """Responds to Launch Requests"""
    if session['new']:
        return on_session_started(session)
    # when a request was made with no intent, and it's not the beginning of a session
    return ask_clarification(session)


def on_intent(intent_request, session, user_id):
    # redirect 'AMAZON.HelpIntent
    if intent_request['intent']['name'] == "AMAZON.HelpIntent":
        return help_intent(session)

    am = ArgumentManager(intent_request['intent'], session, user_id)
    # sending the intents and context element to argurment manager

    # get my outgoing object from the contextmanager
    unambiguousObject = am.getContextObject(am.createIntentObject(),
                                            am.get_user_id())  # (of type intentObject)

    # if slots are missing and contextManager can't fill them with previous context
    if unambiguousObject.isComplete() == False:
        tell_missing_info(session) # send a response asking to try again

    ##query_db
    fact = am.query_db(unambiguousObject.getSlots()) # feeds a dictionary containing slots and values, returns a string
    return on_intent_question_asked(fact, session, unambiguousObject, am.get_user_name(user_id))


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


    ## FIRST CHECK IF NEW USER
    if 'user' not in event:
        return build_response("link_account", build_link_account_response())

    else:
    ##authenticated?
        user_login_data = event['user']
        if not 'accessToken' in user_login_data:
            ##go back and authenticate
            return build_response("link_account", build_link_account_response())

        new_user = False
        ##check if user's account is complete

        # todo: CLAY, user_account_complete (give user's auth_token) should return false if the user is in db but hasn't completed the setup, or if user is not in db
        if not QueryManager.is_user_account_complete(user_login_data['accessToken']['value']):
            ##create new user_setup object
            user_setup = UserSetup(user_login_data['accessToken']['value'])
            ##send to user_setup_functionality
            response = user_setup.add_characteristic_to_db(event['request']['slots'])
            if response is None:
                #default to new_session_response
                return on_session_started(event['session'])
            return response

        if event['request']['type'] == "LaunchRequest":
            # this is a new session and you didn't have any special request
            return on_launch(event['request'], event['session'])

        elif event['request']['type'] == "IntentRequest":

            # todo possibly implement new session functionality
           # if event['session']['new']:
                # new session, need to update user object
                return on_intent(event['request'], event['session'], event['user'])

        elif event['request']['type'] == "SessionEndedRequest":
            return on_session_ended(event['request'], event['session'])