from inputOutput import takeCommand, initSpeakEngine, speak
from intentValidator import *
from executor import *


def processQuery(engine, query):
    foundIntent = False
    for isIntent, execute in COMMANDS:
        if isIntent(query):
            execute(engine, query)
            foundIntent = True
            break

    if not foundIntent:
        executeUnknownCommand(engine, None)


COMMANDS = [(isGreetingCommand, executeGreeting),
            (isWhereIsCommand, executeWhereIsCommand), (isWhereAmICommand, excuteWhereAmICommand)]

if __name__ == '__main__':
    engine = initSpeakEngine('female')

    executeGreeting(engine, None)

    while True:
        query = takeCommand().lower()
        if isByeCommand(query):
            executeByeCommand(engine)
            break

        processQuery(engine, query)
