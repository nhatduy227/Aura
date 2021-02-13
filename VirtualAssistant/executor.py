# Purpose: Execute user's command
from inputOutput import takeCommand
from intentValidator import *
from responseConstants import *
from utility import *
from inputOutput import speak


def executeGreeting(engine, command=None):
    speak(engine, GREETING)
    return Modes.Waiting


def executeByeCommand(engine, command=None):
    speak(engine, "Goodbye for now! Remember, to wake me up, just say Hey Aura")
    return Modes.Iddle


def executeShowInstructionCommand(engine, command):
    speak(engine, SELECT_MODE)
    return Modes.Waiting


def handleNearestObjectDirection(engine, command):
    # TODO: This is mode 1. A loop here to detect the object until ???
    # Should we terminate when user say Ok or done or somthing like that?
    # Remember to return the new mode here
    pass


def handleFindObject(engine, command):
    speak(engine, 'Please say Where is my, followed by the object name. Or, Where is the, followed by the object name.')

    while True:
        query = takeCommand().lower()
        if isByeCommand(query):
            executeByeCommand(engine)
            return Modes.Iddle
        elif isShowInstructionCommand(query):
            executeShowInstructionCommand(engine)
        elif isWhereIsCommand(query):
            objName = extractObjectFromWhereIsCommand(query)
            if objName:
                speak(engine, 'You want to look for ' + objName)
            # TODO: A loop here to tell the user about the direction of the object
            # Terminate the loop when the object is right in front of the user
            # Speak objName is in front of you before terminate
            return Modes.Waiting
        else:
            executeUnknownCommand(engine)


def handleDescribeView(engine, command):
    # TODO: This is mode 3
    speak(engine, 'A cute cat is in front of you.')
    return Modes.Waiting


def executeUnknownCommand(engine, command=None):
    speak(engine, UNKNOWN)


def executeSelectModeCommand(engine, command):
    mode = extractModeFromCommand(command)
    if not isValidMode(mode):
        speak(engine, INVALID_MODE)
        return

    speak(engine, 'You select mode ' + mode)

    if MODES_MAP[mode] == 1:
        speak(engine, 'In this mode, I will tell you the direction of the closest object')
        return handleNearestObjectDirection(engine, command)
    elif MODES_MAP[mode] == 2:
        speak(engine, 'In this mode, I will help you find the object you want.')
        return handleFindObject(engine, command)
    else:
        speak(engine, 'I will describe what is in front of you')
        return handleDescribeView(engine, command)
