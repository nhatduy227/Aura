import pyttsx3
import speech_recognition as sr

def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # 0 is male, 1 is female
    engine.setProperty('voice', voices[1].id)

    engine.say(audio)

    # Blocks while processing all the queued command
    engine.runAndWait()

def takeQuery():
    hello()

    while True:
        query = takeCommand().lower()

        if "Hello" in query:
            speak("Hello! How are you today?")
        elif "hungry" in query:
            speak("I'm hungry too!")
        elif "bye" in query:
            speak("Goodbye!")
        else:
            speak("Can you repeat?")

def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening...')

        r.pause_threshold = 0.7
        audio = r.listen(source)

        try:
            print('Recognizing')
            query = r.recognize_google(audio, language='en-US')
            print('Query:', query)
        except Exception as e:
            print(e)
            return "None"
        return query

def hello():
    speak('Hi! I am your virtual assistant! How can I help you today?')

def main():
    takeQuery()

if __name__ == '__main__':
    main()
