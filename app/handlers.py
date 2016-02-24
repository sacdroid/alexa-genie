import logging
from functools import wraps
from app import settings
from app.alexa import AlexaResponse
from app.pointsystem import PointsSystem
from app import kodi
from pycec import CECDevice 
import pickledb
import pychromecast

logger = logging.getLogger(__name__)

cecdevice = CECDevice()
cecdevice.Scan()

cast = pychromecast.get_chromecast()
cast.wait()

pointssystem = PointsSystem();

# Decorators for handler registration
INTENT_HANDLERS = {}
REQUEST_TYPE_HANDLERS = {}


def intent_handler(name):
    """Register an intent handler for the given intent name."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        INTENT_HANDLERS[name] = func
        return wrapper
    return decorator


def request_handler(name):
    """Register an request-type handler for the given request type."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        REQUEST_TYPE_HANDLERS[name] = func
        return wrapper
    return decorator


# Main controller

def dispatch(alexa_request):
    """
    Dispatch the incoming, valid AlexaRequest to the appropriate request-type
    handler.
    """
    request_type = alexa_request.request_type
    request_type_handler = REQUEST_TYPE_HANDLERS.get(request_type)
    if callable(request_type_handler):
        return request_type_handler(alexa_request)
    else:
        logger.error('Unhandled request type: {0}'.format(request_type))
        return AlexaResponse('Sorry, I missed you there.', False)


# Request-type handlers

@request_handler('LaunchRequest')
def welcome(alexa_request):
    return AlexaResponse(
        'I am {0}?'
        .format(settings.SKILL_NAME, settings.SKILL_INVOCATION_NAME), False
    )


@request_handler('IntentRequest')
def intent_dispatcher(alexa_request):
    """Dispatch the incoming AlexaRequest to the appropriate intent handler."""
    intent_name = alexa_request.intent_name
    intent_handler = INTENT_HANDLERS.get(intent_name)
    if callable(intent_handler):
        return intent_handler(alexa_request)
    else:
        logger.error('Unhandled intent: {0}'.format(intent_name))
        return AlexaResponse('Sorry, I missed you there.', False)


@request_handler('SessionEndedRequest')
def session_ended(alexa_request):
    # No response is allowed for a SessionEndedRequest, but just in case Amazon
    # changes their mind about that...
    return AlexaResponse('Good Bye!')


# Intent handlers

@intent_handler('AMAZON.HelpIntent')
def help(alexa_request):
    return AlexaResponse(
        'With {0}, you can control your media center '
        .format(settings.SKILL_NAME)
    )


@intent_handler('AMAZON.CancelIntent')
def stop(alexa_request):
    return AlexaResponse('Good Bye')

@intent_handler('GetKodiCommandEventIntent')
def kodicommand(alexa_request):
    number = alexa_request.slots['Number'].get('value') or 1
    command = alexa_request.slots['Command'].get('value').title()
    number = min(int(number),10)
    for i in range(int(number)):
        if command in dir(kodi):
            getattr(kodi, command)();
        mc = cast.media_controller    
        if command in dir(mc):
            getattr(mc, command)();
    return AlexaResponse('Next?',False)

@intent_handler('GetCECCommandEventIntent')
def ceccommand(alexa_request):
    command = alexa_request.slots['CECCommand'].get('value').title().replace(" ", "")
    command = command_lookup.get(command, command)
    number = alexa_request.slots['Number'].get('value') or default_number_lookup.get(command, 1)
    number = min(int(number),10)
    for i in range(int(number)):
        getattr(cecdevice, command)();
    return AlexaResponse('Done',True)

command_lookup = {'IncreaseVolume':'VolumeUp', 'DecreaseVolume':'VolumeDown', 'SwitchOff': "TurnOff", "SwitchOn":"TurnOn","Unmute":"Mute"}

default_number_lookup = {'VolumeUp':'5', 'VolumeDown':'5'}

@intent_handler('GetSwitchDeviceEventIntent')
def switchdevice(alexa_request):
    device = alexa_request.slots['Device'].get('value').title().replace(" ", "")
    number = code_lookup[device]
    cecdevice.hdmi(number)    
    return AlexaResponse('Done',False)

code_lookup = {'Chromecast':1, 'FireTV':2, 'Kodi':3, "PS4":4}

@intent_handler('UpdateSaraPointsEventIntent')
def points(alexa_request):
    points = alexa_request.slots['Points'].get('value') or 1
    action = alexa_request.slots['Action'].get('value').title().replace(" ", "")
    points = int(points)
    points = pointssystem.points(action, points);
    return AlexaResponse('Updating Sara\'s points to {0}'.format(points),False)

@intent_handler('GetSaraPointsEventIntent')
def getsarapoints(alexa_request):
    points = str(pointssystem.getpoints())
    return AlexaResponse(
        '{0}\'s current points are {1}.'
        .format(settings.POINT_HOLDER_NAME, points)
    )


