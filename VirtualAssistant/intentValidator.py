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

def isWhereAmICommand(command):
    return 'where am i' in command