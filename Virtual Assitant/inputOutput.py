import pyttsx3

VOICE_GENDER = {'male': 0, 'female': 1}

def initSpeakEngine(gender):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[VOICE_GENDER[gender]].id)
    return engine


def speak(engine, audio):
    engine.say(audio)

    # Blocks while processing all the queued command
    engine.runAndWait()