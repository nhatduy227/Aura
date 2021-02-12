# Purpose: Execute user's command

from responseConstants import *
from utility import *
from inputOutput import speak


def executeGreeting(engine, command=None):
    speak(engine, GREETING)


def executeByeCommand(engine, command=None):
    speak(engine, "Goodbye!")


def executeShowInstructionCommand(engine, command):
    speak(engine, SELECT_MODE)


def executeWhereIsCommand(engine, command):
    speak(engine, 'You want to look for')
    # TODO: Get what the user want to look for
    # TODO: Look for that think -> Instruct the user to that thing


def executeUnknownCommand(engine, command=None):
    speak(engine, UNKNOWN)


def excuteWhereAmICommand(engine, command):
    # TODO
    speak(engine, 'TODO TODO')


def executeSelectModeCommand(engine, command):
    mode = extractModeFromCommand(command)
    if not isValidMode(mode):
        speak(engine, INVALID_MODE)
        return

    speak(engine, 'You select mode ' + mode)

    if MODES_MAP[mode] == 1:
        # TODO: Execute mode 1
        speak(engine, 'I will execute mode 1 now')
    elif MODES_MAP[mode] == 2:
        # TODO: Execute mode 2
        speak(engine, 'I will execute mode 2 now')
    elif MODES_MAP[mode] == 3:
        # TODO: Execute mode 3
        speak(engine, 'I will execute mode 3 now')
    else:
        # TODO: Execute mode 4
        speak(engine, 'I will execute mode 4 now')
