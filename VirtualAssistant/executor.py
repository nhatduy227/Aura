# Purpose: Execute user's command 

from responseConstants import GREETING, UNKNOWN
from inputOutput import speak


def executeGreeting(engine, command=None):
    speak(engine, GREETING)


def executeByeCommand(engine, command=None):
    speak(engine, "Goodbye!")


def executeWhereIsCommand(engine, command):
    speak(engine, 'You want to look for')
    # TODO: Get what the user want to look for
    # TODO: Look for that think -> Instruct the user to that thing


def executeUnknownCommand(engine, command=None):
    speak(engine, UNKNOWN)

def excuteWhereAmICommand(engine, command):
    # TODO
    speak(engine, 'TODO TODO')
