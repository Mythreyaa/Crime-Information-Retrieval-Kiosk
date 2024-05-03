
from ner import *
import speech_recognition as sr

def voice_recognize():
    global text
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print('.............................................Caliberated, now speak')
        
        audio = r.listen(source)
        text = r.recognize_google(audio)
        text = text.lower()
    # text = "3114"
    # print('Results for your query: ', text)
    return text
        #token(text)
def invoke_recognize():
    nlp = spacy.load("en_core_web_lg")
    r = recognizer(nlp)
    res = r.recognize(text,1)
   
    return res

if __name__ == "__main__":
    voice_recognize()
    print(invoke_recognize())



