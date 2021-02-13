# Purpose: Find the user's intention

def isGreetingCommand(command):
    greetingWords = ['hello', 'hi', 'hey']
    if any([word in command for word in greetingWords]):
        return True
    return False


def isByeCommand(command):
    byeWords = ['bye', 'goodbye']
    if any([word in command for word in byeWords]):
        return True
    return False


def isWhereIsCommand(command):
    return 'where is' in command


def isSelectModeCommand(command):
    return 'select mode' in command


def isShowInstructionCommand(command):
    return 'instruction' in command


def isWakeUpCommand(command):
    # TODO: hey Aura is difficult to pronounce lol
    # Putting hey Google here for testing purpose
    # Should change to hey Aura later
    return 'hey Google' in command or 'hey google' in command
