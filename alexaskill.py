"""
Antlexa using Amazon Alexa Skills Kit

"""

from __future__ import print_function
from antlexa import *

# --------------- Helpers that build all of the responses ----------------------

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


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ 
    Initialize the session to have some attributes and welcome the user
    Only invoked when no stop id is given
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Antlexa Express, please say a bus stop I.D. " \
                    "to get the bus times."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me the bus stop where you'd want to hear" \
                    "the bus times at, if you would like to see the list please say see list"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# test session end, usual request will end without calling this
def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Don't be late to your bus!" 
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# create stop id attributes 
def create_stop_id_attribute(stop_id):
    return {"stopID": stop_id}

# get bus times function, calls function in antlexa.py file  

def get_bus_times_in_session(intent, session):
    """ 
    Calls another python script which calls the API to get the bus times 
    to save into the session and then return to the user.  
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'stops' in intent['slots']:

        numTimes = len(intent['slots']['stops']
            ['resolutions']['resolutionsPerAuthority'][0]['values'])
	
	# returned more than one stop id, must exit and ask user for more
        if numTimes > 1:
	    speech_output = "I got more than one stop I.D. please try again."
	    reprompt_text = "I'm getting more than one stop I.D. " \
                            "Please try again or check the documentation for available bus stops."
			    
        # exactly one stop id, call python function to get string of bus times
	else:
	    stopID = intent['slots']['stops']['resolutions']
            	['resolutionsPerAuthority'][0]['values'][0]['value']['name']
	    should_end_session = True	
        session_attributes = create_stop_id_attribute(stopID)
	    speech_output = getTimes(stopID) 
    # error in recognizing bus stop id or wrong input
    else:
        speech_output = "I'm not sure what bus stop that is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what bus stop you are trying to say. " \
                        "You can look at the available bus stops in " \
                        "the documentation."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetBusTimesAtStop":
        return get_bus_times_in_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ 
    Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """ TESTING PHASE
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function. 
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

        
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
