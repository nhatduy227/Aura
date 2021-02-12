MODES = set(["one", "two", "three", "four", "1", "2", "3", "4", "for"])
MODES_MAP = {'one': 1, '1': 1, 'two': 2, '2': 2, 'three': 3, '3': 3, 'four': 4, '4': 4, 'for': 4}


def extractModeFromCommand(command):
    words = command.split()
    for i in range(len(words) - 2):
        if words[i] == 'select' and words[i + 1] == 'mode':
            return words[i + 2]
    return "None"


def isValidMode(mode):
    return mode in MODES
