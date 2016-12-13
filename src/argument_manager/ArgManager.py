# -*- coding: utf-8 -*-
"""
Adapted from Alexa Skill sample color-expert-python
"""

from __future__ import print_function


# import context manager
# import query manager
# import intent objects

# importing objects for local testing
# import sys, os
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# from user_intent.inform_object import InformObject

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
            raiseValueError("Invalid intent")
            ##might want to pass to end_session function here

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


# is the idea behind this method to handle sessions started when the user is using the skill for the first time?
def on_blank_session_started(session):
    speech_output = "Welcome to Alexa Immigration Support!"
    reprompt_text = "You can ask me things like, Alexa, how do I move to Canada? Or you \
    can say Alexa, what are jobs like in Australia? Currently, I can answer questions about \
    jobs, moving, and general facts for Canada, Australia, and the UK."
    session_attributes = session.get('attributes', {})
    return build_response(session_attributes, build_speechlet_response('Test', speech_output, reprompt_text, False))


def on_session_started(session):
    session_attributes = {'conversation': []}

    speech_output = "Welcome to Alexa Immigration Support! " \
                    "You can ask me things like, Alexa, how do I move to Canada? Or you " \
                    "can say Alexa, what are jobs like in Australia? Currently, I can answer questions about" \
                    "jobs, moving, and general facts for Canada, Australia, and the UK."

    # todo: we might not need to provide example questions, Alexa might do that for us. Need to look into that
    reprompt_text = "You can ask me things like, Alexa, how do I move to Canada? Or you " \
                    "can say Alexa, what are jobs like in Australia? Currently, I can answer questions about " \
                    "jobs, moving, and general facts for Canada, Australia, and the UK."

    should_end_session = False

    return build_response(session_attributes,
                          build_speechlet_response('Welcome', speech_output, reprompt_text, should_end_session))


def ask_clarification(session):
    """This function sends a response asking the speaker to repeat their question
       This function is used in situations where an intent cannot be understood """

    speech_output = "Sorry, I didn't understand what you said." \
                    "You can ask me things like, Alexa, how do I move to Canada? or " \
                    "can say Alexa, what are jobs like in Australia?" \
                    "Currently, I can answer questions about jobs, moving," \
                    "and general facts for Canada, Australia, and the UK."

    reprompt_text = "Sorry, I didn't understand what you said." \
                    "You can ask me things like, Alexa, how do I move to Canada? or you" \
                    "can say Alexa, what are jobs like in Australia?" \
                    "Currently, I can answer questions about jobs, moving," \
                    "and general facts for Canada, Australia, and the UK."

    session_attributes = session.get('attributes', {})
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response('Test', speech_output, reprompt_text, should_end_session))


def on_intent_question_asked(fact, session, intentObject):
    """This function takes a fact string created in response to an intent
        and builds a response to send back to Alexa"""

    # gets fact, session, intent object(optional?)
    speech_output = fact + " What else would you like to know?"  # continue the conversation
    reprompt_text = "Would you like to learn anything else?"

    # add current session attributes to the list of session attributes
    session['attributes']['questions'].append({"country": intentObject.getCountry(), "city": intentObject.getCountry(), \
                                               "intent": intentObject.getIntent(),
                                               "fact": fact})  # possibly using it for card
    session_attributes = session.get('attributes')

    return build_response(session_attributes, build_speechlet_response(intentObject.getCountry(), \
                                                                       speech_output, reprompt_text, False))


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
    """Responds to Launch Requests"""
    if session['new']:
        return on_session_started(session)
    else: # when a request was made with no intent, and it's not the beginning of a session
        return ask_clarification(session)


def on_intent(intent_request, session, is_new_session):
    am = ArgumentManager(event['request']['intent'], context)
    # sending the intents and context element to argurment manager

    # get my outgoing object from the contextmanager
    if is_new_session:
        # additionally send user info from LinkAccount card
        userId = am.buildUserInfo(session)
        unambiguousObject = am.getContextObject(am.createIntentObject(), True,
                                                None)  # (of type intentObject) # 'None' bit is User
    else:
        unambiguousObject = am.getContextObject(am.createIntentObject(), False, None)

    ##query_db
    fact = am.query_db(unambiguousObject)
    return on_intent_question_asked(fact, session)


def on_session_ended(self, session):
    # make a card collecting all the intents, countries and topics discussed during
    # the session
    card_title = "Session Ended == Your Conversation Today"
    #speech_output = "Thank you for using Immigration Support. You will receive a card " \
                    #"with all the information you asked about today. " \
                    #"Have a nice day!"
    conversation = session['attributes']['questions']

    #countries = list(set([question.get('country') for question in conversation]))
    #cities = list(set([question.get('city') for question in conversation if question.get('city') is not None]))
    #topics = list(set([question.get('topic') for question in conversation if question.get('topic') is not None]))
    #intents = list(set([question.get('intent') for question in conversation if question.get('intent') != 'INFORM']))
    facts = list(set([question.get('fact') for question in conversation if question.get('fact') is not None]))

    # covers only facts so far
    speech_output = "These are the facts we covered: %s. " % (' '.join(facts))

    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


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