import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np
from gtts import gTTS
import subprocess
mytext = 'Welcome to me'
language = 'en'
# from os.path import join, dirname
# import matplotlib.pyplot as plt
# ^ matplotlib is great for visualising data and for testing purposes but usually not needed for production
openai.api_key='sk-proj-I0t0UH51c4Rrq91M2Y2ZT3BlbkFJM11mxN4hgSgw9EEMZvY6'
load_dotenv()
#model = 'gpt-3.5-turbo'
model = 'gpt-4o'
# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()
# voice = engine.getProperty('voices')[1]
# engine.setProperty('voice', voice.id)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-70)
name = "Divy"
greetings = "hello there"


def listen_question(source):
    try:
        # Listen for audio input with a timeout of 30 seconds
        print("Listening for Question")
        audio = r.listen(source, 15)
        audio_text = r.recognize_google(audio)
        return audio_text
    except sr.UnknownValueError:
        # engine.say("I didn't catch that. Can you please repeat the Question?")
        # engine.runAndWait()
        return listen_question(source)
    except sr.RequestError as e:
        engine.say(f"Could not request results; {e}")
        engine.runAndWait()
        return None

def listen_confirmation(source):
    try:
        # Listen for confirmation with a timeout of 10 seconds
        print("Listening for Confirmation")
        answer_audio = r.listen(source, 10)
        answer_text = r.recognize_google(answer_audio)
        return answer_text
    except sr.UnknownValueError:
        engine.say("I didn't catch that. Can you please give the Confirmation by saying Yes?")
        engine.runAndWait()
        return listen_confirmation(source)
    except sr.RequestError as e:
        engine.say(f"Could not request results; {e}")
        engine.runAndWait()
        return None

def listen_interpret(source):
    audio_text = listen_question(source)
    if not audio_text or "hello" in audio_text.lower():
        engine.say("I am sorry. Can you ask the question again")
        engine.runAndWait()
        return listen_interpret(source)

    engine.say("Did you ask " + audio_text)
    engine.runAndWait()

    answer_text = listen_confirmation(source)
    if "yes" not in answer_text.lower():
        engine.say("I am sorry for not getting your question. Can you ask the question again")
        engine.runAndWait()
        return listen_interpret(source)

    return audio_text

# Listen for the wake word "hey pos"
def listen_for_wake_word(source):
    print("Listening for 'Hello'...")

    while True:
        audio = r.listen(source, timeout=5)
        try:
            text = r.recognize_google(audio)
            if "hello" in text.lower():
                print("Wake word detected.")
                engine.say(greetings)
                engine.runAndWait()
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass
# Listen for input and respond with OpenAI API
def listen_and_respond(source):

    while True:
        # audio = r.listen(source, timeout=30)
        try:
            audioText = listen_interpret(source)
            # audioText = r.recognize_google(audio)
            # if not audioText or "hello" in audioText.lower():
            #     continue
            # engine.say("Did you ask " + audioText)
            # engine.runAndWait()
            # answerAudio = r.listen(source, timeout=10)
            # answerText = r.recognize_google(answerAudio)
            # if("yes" not in answerText.lower()):
            #     continue
            text = "You are a Data Analyst of Mining Company that uses the given data and give response strictly in less than 30 words.The Question is "
            text += audioText
            text += " ? "
            text += """Data: [Gross , Net weights of Materials represented as Gross Wt (MT), Net Wt (MT) respectively and Tare Wt ,Tare Wt2 represent waiting times respectively.Difference between Tare Wt and Tare Wt2 is the trip duration.Shifts are defined as A Shift: 06:00-14:00, B Shift: 14:00-22:00, C Shift: 22:00-06:00. Trip Id,Vehicle No,Route Name,Transporter Name,Tare Wt (MT),Gross Wt (MT),Net Wt (MT),GrossWt WB Name,Tare Wt Name,Actual Destination,Tare Wt,Loading In,Loading Out,Gross Wt,Unloading In,Unloading Out,Tare Wt 2,Wt Comment,Remarks,Reason For Edit
            1000727905,PCL HP-24,IIND BAND 66 - Crusher-U1,Prism,35.88,84.74,48.86,MMWB02,MMWB04,Crusher-U1,07-06-2024 23:38,07-06-2024 23:41,07-06-2024 23:50,07-06-2024 23:52,07-06-2024 23:53,07-06-2024 23:54,07-06-2024 23:54,,,
            1000727892,PCL HP-23,IIND BAND - Crusher-U1,Prism,35.92,85.9,49.98,MMWB02,MMWB04,Crusher-U1,07-06-2024 23:14,07-06-2024 23:21,07-06-2024 23:48,07-06-2024 23:51,07-06-2024 23:51,07-06-2024 23:52,07-06-2024 23:52,,,
            1000727898,PCL HP-21,IIND BAND 66 - Crusher-U1,Prism,35.22,82.1,46.88,MMWB02,MMWB02,Crusher-U1,07-06-2024 23:24,07-06-2024 23:32,07-06-2024 23:44,07-06-2024 23:46,07-06-2024 23:47,07-06-2024 23:49,07-06-2024 23:49,,,
            1000727888,PCL HP-22,IIND BAND - Crusher-U1,Prism,35.35,84.56,49.21,MMWB02,MMWB02,Crusher-U1,07-06-2024 23:09,07-06-2024 23:17,07-06-2024 23:38,07-06-2024 23:43,07-06-2024 23:43,07-06-2024 23:44,07-06-2024 23:44,,,
            1000727804,PCL HP-25,IIND BAND 66 - Crusher-U1,Prism,35.35,87.68,52.33,MMWB02,MMWB04,Crusher-U1,07-06-2024 20:19,07-06-2024 20:29,07-06-2024 20:41,07-06-2024 20:50,07-06-2024 20:50,07-06-2024 20:54,07-06-2024 20:54,,,
            1000727271,PCL HP-12,IIND BAND - Crusher-U1,Prism,35.27,83.8,48.53,MMWB02,MMWB03,Crusher-U1,07-06-2024 13:36,07-06-2024 20:36,07-06-2024 20:47,07-06-2024 20:51,07-06-2024 20:52,07-06-2024 20:54,07-06-2024 20:54,,,
            1000727811,PCL HP-18,IIND BAND - Crusher-U1,Prism,35.48,87.88,52.4,MMWB02,MMWB03,Crusher-U1,07-06-2024 20:22,07-06-2024 20:26,07-06-2024 20:48,07-06-2024 20:53,07-06-2024 20:53,07-06-2024 20:53,07-06-2024 20:53,,,
            1000727815,PCL HP-11,IIND BAND 66 - Crusher-U1,Prism,35.3,82.75,47.45,MMWB02,MMWB02,Crusher-U1,07-06-2024 20:25,07-06-2024 20:30,07-06-2024 20:45,07-06-2024 20:47,07-06-2024 20:48,07-06-2024 20:48,07-06-2024 20:48,,,
            1000727810,PCL HP-23,IIND BAND - Crusher-U1,Prism,35.95,87.2,51.25,MMWB02,MMWB04,Crusher-U1,07-06-2024 20:23,07-06-2024 20:26,07-06-2024 20:42,07-06-2024 20:45,07-06-2024 20:46,07-06-2024 20:46,07-06-2024 20:46,,,
            1000727809,PCL HP-21,IIND BAND - Crusher-U1,Prism,35.36,87.99,52.63,MMWB02,MMWB04,Crusher-U1,07-06-2024 20:23,07-06-2024 20:25,07-06-2024 20:36,07-06-2024 20:39,07-06-2024 20:40,07-06-2024 20:41,07-06-2024 20:41,,,
            1000727806,PCL HP-20,IIND BAND 66 - STOCK A,Prism,35.48,92.3,56.82,MMWB02,MMWB04,STOCK A,07-06-2024 20:19,07-06-2024 20:28,07-06-2024 20:38,07-06-2024 20:40,07-06-2024 20:41,07-06-2024 20:41,07-06-2024 20:41,,,Vehicle diverted from crusher u-1 to stock-A
            1000727805,PCL HP-22,IIND BAND 66 - Crusher-U1,Prism,35.3,87.32,52.02,MMWB02,MMWB04,Crusher-U1,07-06-2024 20:18,07-06-2024 20:21,07-06-2024 20:31,07-06-2024 20:34,07-06-2024 20:34,07-06-2024 20:34,07-06-2024 20:34,,,
            1000727703,PCL HP-24,IIND BAND 66 - Crusher-U1,Prism,35.7,94.02,58.32,MMWB02,MMWB04,Crusher-U1,07-06-2024 16:48,07-06-2024 20:10,07-06-2024 20:24,07-06-2024 20:32,07-06-2024 20:32,07-06-2024 20:34,07-06-2024 20:34,,,
            1000727796,PCL HP-19,IIND BAND - STOCK C,Prism,35.17,87.72,52.55,MMWB02,MMWB02,STOCK C,07-06-2024 20:03,07-06-2024 20:11,07-06-2024 20:26,07-06-2024 20:30,07-06-2024 20:30,07-06-2024 20:31,07-06-2024 20:31,,,Vehicle divert from crusher u-1 to stock-C
            1000727797,PCL HP-11,IIND BAND 66 - Crusher-U1,Prism,35.3,89.4,54.1,MMWB02,MMWB02,Crusher-U1,07-06-2024 20:04,07-06-2024 20:08,07-06-2024 20:21,07-06-2024 20:24,07-06-2024 20:25,07-06-2024 20:25,07-06-2024 20:25,,,
            1000727788,PCL HP-23,IIND BAND - STOCK C,Prism,35.95,87.3,51.35,MMWB04,MMWB04,STOCK C,07-06-2024 19:48,07-06-2024 19:57,07-06-2024 20:13,07-06-2024 20:19,07-06-2024 20:22,07-06-2024 20:23,07-06-2024 20:23,,,
            1000727782,PCL HP-21,IIND BAND - STOCK C,Prism,35.36,85.12,49.76,MMWB02,MMWB04,STOCK C,07-06-2024 19:39,07-06-2024 19:45,07-06-2024 20:06,07-06-2024 20:18,07-06-2024 20:21,07-06-2024 20:23,07-06-2024 20:23,,,
            1000727791,PCL HP-18,IIND BAND - STOCK C,Prism,35.48,86.32,50.84,MMWB02,MMWB03,STOCK C,07-06-2024 19:52,07-06-2024 19:57,07-06-2024 20:18,07-06-2024 20:22,07-06-2024 20:22,07-06-2024 20:22,07-06-2024 20:22,,,Vehicle divert from crusher u-1 to stock-C
            1000727711,PCL HP-25,IIND BAND 66 - Crusher-U1,Prism,35.35,90.03,54.68,MMWB02,MMWB04,Crusher-U1,07-06-2024 17:04,07-06-2024 19:55,07-06-2024 20:07,07-06-2024 20:18,07-06-2024 20:18,07-06-2024 20:19,07-06-2024 20:19,,,
            1000727794,PCL HP-20,IIND BAND 66 - Crusher-U1,Prism,35.48,86.27,50.79,MMWB02,MMWB04,Crusher-U1,07-06-2024 19:59,07-06-2024 20:02,07-06-2024 20:15,07-06-2024 20:19,07-06-2024 20:19,07-06-2024 20:19,07-06-2024 20:19,,,
            1000727789,PCL HP-22,IIND BAND 66 - Crusher-U1,Prism,35.3,85.65,50.35,MMWB02,MMWB04,Crusher-U1,07-06-2024 19:49,07-06-2024 19:57,07-06-2024 20:08,07-06-2024 20:17,07-06-2024 20:17,07-06-2024 20:18,07-06-2024 20:18,,,
            1000727783,PCL HP-11,IIND BAND 66 - Crusher-U1,Prism,35.3,85.84,50.54,MMWB02,MMWB02,Crusher-U1,07-06-2024 19:39,07-06-2024 19:49,07-06-2024 20:01,07-06-2024 20:03,07-06-2024 20:04,07-06-2024 20:04,07-06-2024 20:04,,,
            1000727772,PCL HP-19,IIND BAND - STOCK C,Prism,35.17,89.64,54.47,MMWB02,MMWB02,STOCK C,07-06-2024 19:28,07-06-2024 19:38,07-06-2024 19:57,07-06-2024 20:02,07-06-2024 20:03,07-06-2024 20:03,07-06-2024 20:03,,,Vehicle divert from crusher u-1 to stock-C
            1000727777,PCL HP-20,IIND BAND 66 - Crusher-U1,Prism,35.48,83.17,47.69,MMWB02,MMWB04,Crusher-U1,07-06-2024 19:34,07-06-2024 19:45,07-06-2024 19:55,07-06-2024 19:57,07-06-2024 19:58,07-06-2024 19:59,07-06-2024 19:59,,,
            1000727769,PCL HP-18,IIND BAND - Crusher-U1,Prism,35.48,83.06,47.58,MMWB02,MMWB03,Crusher-U1,07-06-2024 19:19,07-06-2024 19:23,07-06-2024 19:48,07-06-2024 19:52,07-06-2024 19:52,07-06-2024 19:52,07-06-2024 19:52,,,
            1000727773,PCL HP-22,IIND BAND 66 - Crusher-U1,Prism,35.3,85.6,50.3,MMWB02,MMWB04,Crusher-U1,07-06-2024 19:28,07-06-2024 19:31,07-06-2024 19:43,07-06-2024 19:46,07-06-2024 19:46,07-06-2024 19:49,07-06-2024 19:49,,,
            1000727765,PCL HP-23,IIND BAND - Crusher-U1,Prism,35.95,85.8,49.85,MMWB02,MMWB04,Crusher-U1,07-06-2024 19:09,07-06-2024 19:18,07-06-2024 19:41,07-06-2024 19:44,07-06-2024 19:45,07-06-2024 19:48,07-06-2024 19:48,,,
            1000727771,PCL HP-11,IIND BAND 66 - Crusher-U1,Prism,35.3,83.3,48,MMWB02,MMWB02,Crusher-U1,07-06-2024 19:21,07-06-2024 19:23,07-06-2024 19:36,07-06-2024 19:38,07-06-2024 19:39,07-06-2024 19:39,07-06-2024 19:39,,,
            1000727762,PCL HP-21,IIND BAND - Crusher-U1,Prism,35.36,83.13,47.77,MMWB02,MMWB04,Crusher-U1,07-06-2024 19:04,07-06-2024 19:08,07-06-2024 19:33,07-06-2024 19:37,07-06-2024 19:37,07-06-2024 19:39,07-06-2024 19:39,,,
            1000727766,PCL HP-20,IIND BAND 66 - Crusher-U1,Prism,35.48,87.48,52,MMWB02,MMWB04,Crusher-U1,07-06-2024 19:12,07-06-2024 19:19,07-06-2024 19:29,07-06-2024 19:33,07-06-2024 19:34,07-06-2024 19:34,07-06-2024 19:34,,,
            1000727764,PCL HP-22,IIND BAND 66 - Crusher-U1,Prism,35.3,88.64,53.34,MMWB02,MMWB04,Crusher-U1,07-06-2024 19:08,07-06-2024 19:11,07-06-2024 19:24,07-06-2024 19:26,07-06-2024 19:27,07-06-2024 19:28,07-06-2024 19:28,,,
            1000727757,PCL HP-19,IIND BAND - Crusher-U1,Prism,35.17,87.96,52.79,MMWB02,MMWB02,Crusher-U1,07-06-2024 18:57,07-06-2024 19:00,07-06-2024 19:23,07-06-2024 19:26,07-06-2024 19:27,07-06-2024 19:28,07-06-2024 19:28,,,
            1000727761,PCL HP-11,IIND BAND 66 - Crusher-U1,Prism,35.3,85.26,49.96,MMWB02,MMWB02,Crusher-U1,07-06-2024 19:01,07-06-2024 19:03,07-06-2024 19:17,07-06-2024 19:19,07-06-2024 19:20,07-06-2024 19:21,07-06-2024 19:21,,,
            1000727749,PCL HP-18,IIND BAND - Crusher-U1,Prism,35.48,87.14,51.66,MMWB02,MMWB03,Crusher-U1,07-06-2024 18:36,07-06-2024 18:39,07-06-2024 19:15,07-06-2024 19:18,07-06-2024 19:18,07-06-2024 19:19,07-06-2024 19:19,,,
            1000727748,PCL HP-20,IIND BAND 66 - Crusher-U1,Prism,35.48,84,48.52,MMWB02,MMWB04,Crusher-U1,07-06-2024 18:39,07-06-2024 18:42,07-06-2024 19:10,07-06-2024 19:12,07-06-2024 19:12,07-06-2024 19:12,07-06-2024 19:12,,,
            1000727750,PCL HP-23,IIND BAND - Crusher-U1,Prism,35.95,84.06,48.11,MMWB02,MMWB04,Crusher-U1,07-06-2024 18:44,07-06-2024 18:49,07-06-2024 19:05,07-06-2024 19:08,07-06-2024 19:09,07-06-2024 19:09,07-06-2024 19:09,,,
            1000727744,PCL HP-22,IIND BAND 66 - Crusher-U1,Prism,35.3,87.92,52.62,MMWB02,MMWB04,Crusher-U1,07-06-2024 17:49,07-06-2024 18:41,07-06-2024 19:04,07-06-2024 19:07,07-06-2024 19:07,07-06-2024 19:08,07-06-2024 19:08,,,
            1000727743,PCL HP-21,IIND BAND - Crusher-U1,Prism,35.36,87.87,52.51,MMWB02,MMWB04,Crusher-U1,07-06-2024 17:49,07-06-2024 18:39,07-06-2024 18:59,07-06-2024 19:03,07-06-2024 19:04,07-06-2024 19:04,07-06-2024 19:04,,,
            1000727741,PCL HP-11,IIND BAND 66 - Crusher-U1,Prism,35.3,85.34,50.04,MMWB02,MMWB02,Crusher-U1,07-06-2024 17:45,07-06-2024 18:35,07-06-2024 18:57,07-06-2024 19:00,07-06-2024 19:01,07-06-2024 19:01,07-06-2024 19:01,,,
            1000727737,PCL HP-19,IIND BAND - Crusher-U1,Prism,35.17,88.64,53.47,MMWB02,MMWB02,Crusher-U1,07-06-2024 17:37,07-06-2024 18:37,07-06-2024 18:52,07-06-2024 18:55,07-06-2024 18:56,07-06-2024 18:57,07-06-2024 18:57,,,
            1000727725,PCL HP-23,IIND BAND - STOCK A,Prism,35.95,87.87,51.92,MMWB02,MMWB04,STOCK A,07-06-2024 17:24,07-06-2024 17:30,07-06-2024 17:50,07-06-2024 18:40,07-06-2024 18:40,07-06-2024 18:44,07-06-2024 18:44,,,Vehicle divert from crusher u-1 to stock-A
            1000727708,PCL HP-20,IIND BAND 66 - STOCK A,Prism,35.48,84.02,48.54,MMWB02,MMWB04,STOCK A,07-06-2024 16:59,07-06-2024 17:07,07-06-2024 17:53,07-06-2024 18:38,07-06-2024 18:38,07-06-2024 18:39,07-06-2024 18:39,,,Vehicle divert from crusher u-1 to stock-A
            1000727733,PCL HP-18,IIND BAND - Crusher-U1,Prism,35.48,85.83,50.35,MMWB02,MMWB03,Crusher-U1,07-06-2024 17:30,07-06-2024 17:35,07-06-2024 17:57,07-06-2024 18:35,07-06-2024 18:35,07-06-2024 18:36,07-06-2024 18:36,,,
            1000727728,PCL HP-22,IIND BAND 66 - Crusher-U1,Prism,35.3,87.61,52.31,MMWB02,MMWB04,Crusher-U1,07-06-2024 17:29,07-06-2024 17:33,07-06-2024 17:46,07-06-2024 17:49,07-06-2024 17:49,07-06-2024 17:49,07-06-2024 17:49,,,
            1000727723,PCL HP-21,IIND BAND - Crusher-U1,Prism,35.36,87.99,52.63,MMWB02,MMWB04,Crusher-U1,07-06-2024 17:19,07-06-2024 17:26,07-06-2024 17:45,07-06-2024 17:48,07-06-2024 17:48,07-06-2024 17:49,07-06-2024 17:49,,,
            1000727722,PCL HP-11,IIND BAND 66 - Crusher-U1,Prism,35.3,85.32,50.02,MMWB02,MMWB02,Crusher-U1,07-06-2024 17:19,07-06-2024 17:26,07-06-2024 17:40,07-06-2024 17:41,07-06-2024 17:42,07-06-2024 17:45,07-06-2024 17:45,,,
            1000727717,PCL EV-1,IIND BAND 66 - Crusher-U1,Prism,22.34,70.24,47.9,MMWB02,MMWB02,Crusher-U1,07-06-2024 17:14,07-06-2024 17:19,07-06-2024 17:34,07-06-2024 17:36,07-06-2024 17:37,07-06-2024 17:39,07-06-2024 17:39,,,
            1000727714,PCL HP-19,IIND BAND - Crusher-U1,Prism,35.17,89.06,53.89,MMWB02,MMWB02,Crusher-U1,07-06-2024 17:09,07-06-2024 17:15,07-06-2024 17:34,07-06-2024 17:37,07-06-2024 17:37,07-06-2024 17:37,07-06-2024 17:37,,,
            1000727712,PCL HP-18,IIND BAND - Crusher-U1,Prism,35.48,88.45,52.97,MMWB02,MMWB03,Crusher-U1,07-06-2024 17:04,07-06-2024 17:12,07-06-2024 17:27,07-06-2024 17:30,07-06-2024 17:30,07-06-2024 17:30,07-06-2024 17:30,,,
            1000727713,PCL HP-22,IIND BAND 66 - STOCK A,Prism,35.3,80.93,45.63,MMWB02,MMWB04,STOCK A,07-06-2024 17:08,07-06-2024 17:14,07-06-2024 17:25,07-06-2024 17:27,07-06-2024 17:28,07-06-2024 17:29,07-06-2024 17:29,,,Vehicle divert from crusher u-1 to stock-A
            1000727709,PCL HP-23,IIND BAND - Crusher-U1,Prism,35.95,87.58,51.63,MMWB02,MMWB04,Crusher-U1,07-06-2024 16:59,07-06-2024 17:03,07-06-2024 17:21,07-06-2024 17:24,07-06-2024 17:24,07-06-2024 17:24,07-06-2024 17:24,,,
            1000727706,PCL HP-21,IIND BAND - Crusher-U1,Prism,35.36,86.46,51.1,MMWB02,MMWB04,Crusher-U1,07-06-2024 16:54,07-06-2024 17:01,07-06-2024 17:14,07-06-2024 17:17,07-06-2024 17:18,07-06-2024 17:19,07-06-2024 17:19,,,
            1000727693,PCL HP-11,IIND BAND 66 - Crusher-U1,Prism,35.3,84.28,48.98,MMWB02,MMWB02,Crusher-U1,07-06-2024 16:31,07-06-2024 16:57,07-06-2024 17:16,07-06-2024 17:19,07-06-2024 17:19,07-06-2024 17:19,07-06-2024 17:19,,,
            1000727702,PCL EV-1,IIND BAND 66 - Crusher-U1,Prism,22.34,71.23,48.89,MMWB02,MMWB02,Crusher-U1,07-06-2024 16:49,07-06-2024 16:56,07-06-2024 17:10,07-06-2024 17:13,07-06-2024 17:14,07-06-2024 17:14,07-06-2024 17:14,,,
            1000727704,PCL HP-19,IIND BAND - Crusher-U1,Prism,35.17,84.82,49.65,MMWB02,MMWB02,Crusher-U1,07-06-2024 16:48,07-06-2024 16:54,07-06-2024 17:05,07-06-2024 17:09,07-06-2024 17:09,07-06-2024 17:09,07-06-2024 17:09,,,
            1000727699,PCL HP-22,IIND BAND 66 - STOCK A,Prism,35.3,84.06,48.76,MMWB02,MMWB04,STOCK A,07-06-2024 16:44,07-06-2024 16:52,07-06-2024 17:03,07-06-2024 17:04,07-06-2024 17:05,07-06-2024 17:08,07-06-2024 17:08,,,Vehicle divert from crusher u-1 to stock-A
            1000727700,PCL HP-18,IIND BAND - Crusher-U1,Prism,35.48,89.68,54.2,MMWB02,MMWB03,Crusher-U1,07-06-2024 16:43,07-06-2024 16:46,07-06-2024 16:58,07-06-2024 17:04,07-06-2024 17:04,07-06-2024 17:04,07-06-2024 17:04,,,
            1000727682,PCL HP-25,IIND BAND 66 - Crusher-U1,Prism,35.35,82.36,47.01,MMWB02,MMWB04,Crusher-U1,07-06-2024 16:14,07-06-2024 16:54,07-06-2024 16:58,07-06-2024 17:03,07-06-2024 17:03,07-06-2024 17:04,07-06-2024 17:04,,,
            1000727694,PCL HP-23,IIND BAND - Crusher-U1,Prism,35.95,85.76,49.81,MMWB02,MMWB04,Crusher-U1,07-06-2024 16:38,07-06-2024 16:42,07-06-2024 16:52,07-06-2024 16:56,07-06-2024 16:57,07-06-2024 16:59,07-06-2024 16:59,,,
            1000727688,PCL HP-20,IIND BAND 66 - Crusher-U1,Prism,35.48,83.7,48.22,MMWB02,MMWB04,Crusher-U1,07-06-2024 16:21,07-06-2024 16:24,07-06-2024 16:56,07-06-2024 16:59,07-06-2024 16:59,07-06-2024 16:59,07-06-2024 16:59,,,
            1000727691,PCL HP-21,IIND BAND - Crusher-U1,Prism,35.36,88.74,53.38,MMWB02,MMWB04,Crusher-U1,07-06-2024 16:29,07-06-2024 16:33,07-06-2024 16:49,07-06-2024 16:51,07-06-2024 16:52,07-06-2024 16:54,07-06-2024 16:54,,,
            1000727672,PCL EV-1,IIND BAND 66 - Crusher-U1,Prism,22.34,70.95,48.61,MMWB02,MMWB02,Crusher-U1,07-06-2024 15:44,07-06-2024 16:21,07-06-2024 16:45,07-06-2024 16:47,07-06-2024 16:49,07-06-2024 16:49,07-06-2024 16:49,,,
            1000727689,PCL HP-19,IIND BAND - Crusher-U1,Prism,35.17,84.26,49.09,MMWB02,MMWB02,Crusher-U1,07-06-2024 16:24,07-06-2024 16:30,07-06-2024 16:42,07-06-2024 16:46,07-06-2024 16:47,07-06-2024 16:48,07-06-2024 16:48,,,
            1000727680,PCL HP-24,IIND BAND 66 - STOCK C,Prism,35.7,85.82,50.12,MMWB02,MMWB04,STOCK C,07-06-2024 16:06,07-06-2024 16:40,07-06-2024 16:43,07-06-2024 16:45,07-06-2024 16:46,07-06-2024 16:48,07-06-2024 16:48,,,Vehicle divert from crusher u-1 to stock-C
            1000727683,PCL HP-22,IIND BAND 66 - Crusher-U1,Prism,35.3,88.31,53.01,MMWB02,MMWB04,Crusher-U1,07-06-2024 16:13,07-06-2024 16:17,07-06-2024 16:37,07-06-2024 16:41,07-06-2024 16:41,07-06-2024 16:44,07-06-2024 16:44,,,
            1000727686,PCL HP-18,IIND BAND - Crusher-U1,Prism,35.48,87.18,51.7,MMWB02,MMWB03,Crusher-U1,07-06-2024 16:16,07-06-2024 16:19,07-06-2024 16:35,07-06-2024 16:40,07-06-2024 16:41,07-06-2024 16:43,07-06-2024 16:43,,,
            1000727681,PCL HP-23,IIND BAND - Crusher-U1,Prism,35.95,87.88,51.93,MMWB02,MMWB04,Crusher-U1,07-06-2024 16:08,07-06-2024 16:11,07-06-2024 16:32,07-06-2024 16:38,07-06-2024 16:38,07-06-2024 16:38,07-06-2024 16:38,,,
            1000727678,PCL HP-11,IIND BAND 66 - Crusher-U1,Prism,35.3,88.02,52.72,MMWB02,MMWB02,Crusher-U1,07-06-2024 16:04,07-06-2024 16:08,07-06-2024 16:27,07-06-2024 16:29,07-06-2024 16:30,07-06-2024 16:31,07-06-2024 16:31,,,
            1000727502,PCL HP-21,IIND BAND - Crusher-U1,Prism,35.36,87.62,52.26,MMWB02,MMWB04,Crusher-U1,07-06-2024 16:08,07-06-2024 16:11,07-06-2024 16:25,07-06-2024 16:28,07-06-2024 16:29,07-06-2024 16:29,07-06-2024 16:29,,,
            1000727676,PCL HP-19,IIND BAND - Crusher-U1,Prism,35.17,83.17,48,MMWB02,MMWB02,Crusher-U1,07-06-2024 15:54,07-06-2024 15:59,07-06-2024 16:16,07-06-2024 16:20,07-06-2024 16:21,07-06-2024 16:24,07-06-2024 16:24,,,
            1000727675,PCL HP-20,IIND BAND 66 - Crusher-U1,Prism,35.48,88.31,52.83,MMWB02,MMWB04,Crusher-U1,07-06-2024 15:54,07-06-2024 15:58,07-06-2024 16:16,07-06-2024 16:19,07-06-2024 16:20,07-06-2024 16:21,07-06-2024 16:21,,,
            1000727669,PCL HP-18,IIND BAND - Crusher-U1,Prism,35.48,87.36,51.88,MMWB02,MMWB03,Crusher-U1,07-06-2024 15:39,07-06-2024 15:57,07-06-2024 16:10,07-06-2024 16:14,07-06-2024 16:15,07-06-2024 16:16,07-06-2024 16:16,,,
            1000727265,PCL HP-25,IIND BAND 66 - STOCK A,Prism,35.35,93.71,58.36,MMWB02,MMWB04,STOCK A,07-06-2024 06:21,07-06-2024 16:08,07-06-2024 16:09,07-06-2024 16:13,07-06-2024 16:14,07-06-2024 16:14,07-06-2024 16:14,,,Vehicle divert from crusher u-1 to stock-A
            1000727664,PCL HP-22,IIND BAND 66 - Crusher-U1,Prism,35.3,88.42,53.12,MMWB02,MMWB04,Crusher-U1,07-06-2024 15:29,07-06-2024 16:04,07-06-2024 16:09,07-06-2024 16:12,07-06-2024 16:12,07-06-2024 16:13,07-06-2024 16:13,,,
            1000727620,PCL EV-1,IIND BAND 66 - Crusher-U1,Prism,22.34,67.54,45.2,MMWB02,MMWB02,Crusher-U1,07-06-2024 13:14,07-06-2024 13:23,07-06-2024 13:34,07-06-2024 13:37,07-06-2024 13:38,07-06-2024 13:39,07-06-2024 13:39,,,
            1000727615,PCL HP-23,IIND BAND - Crusher-U1,Prism,35.95,90.11,54.16,MMWB03,MMWB04,Crusher-U1,07-06-2024 13:09,07-06-2024 13:21,07-06-2024 13:30,07-06-2024 13:33,07-06-2024 13:34,07-06-2024 13:34,07-06-2024 13:34,,,
            1000727619,PCL HP-19,IIND BAND 66 - Crusher-U1,Prism,35.12,87.25,52.13,MMWB03,MMWB04,Crusher-U1,07-06-2024 13:14,07-06-2024 13:20,07-06-2024 13:28,07-06-2024 13:30,07-06-2024 13:31,07-06-2024 13:34,07-06-2024 13:34,,,
            1000727614,PCL HP-24,IIND BAND - STOCK C,Prism,35.8,90.01,54.21,MMWB03,MMWB03,STOCK C,07-06-2024 13:02,07-06-2024 13:05,07-06-2024 13:19,07-06-2024 13:21,,,07-06-2024 13:21,,,Gps not capture destination.
            1000727613,PCL HP-11,IIND BAND 66 - Crusher-U1,Prism,34.95,87.12,52.17,MMWB02,MMWB04,Crusher-U1,07-06-2024 13:04,07-06-2024 13:07,07-06-2024 13:18,07-06-2024 13:20,07-06-2024 13:21,07-06-2024 13:21,07-06-2024 13:21,,,
            1000727354,PCL HP-19,IIND BAND 66 - STOCK A,Prism,35.12,88.33,53.21,MMWB03,MMWB04,STOCK A,07-06-2024 06:25,07-06-2024 10:48,07-06-2024 11:15,07-06-2024 11:17,07-06-2024 11:18,07-06-2024 11:18,07-06-2024 11:18,,,
            1000727124,PCL HP-23,IIND BAND - STOCK C,Prism,35.95,87.38,51.43,MMWB02,MMWB04,STOCK C,07-06-2024 06:33,07-06-2024 10:50,07-06-2024 11:06,07-06-2024 11:09,07-06-2024 11:10,07-06-2024 11:12,07-06-2024 11:12,,,Vehicle divert from crusher u-1 to stock-C]."""
            print(f"You said: {audioText}")

            # Send input to OpenAI API
            response = openai.ChatCompletion.create(model="gpt-4o", messages=[{"role": "user", "content": f"{text}"}])
            response_text = response.choices[0].message.content
            print(response_text)
            #myobj = gTTS(text = response_text, lang = language, slow = False)
            #myobj.save("test.wav")
            #os.system("aplay test.wav")
            # Speak the response
            print("speaking")
            response_text = response_text.replace("'", "").replace("(", "").replace(")", "")
            # os.system("espeak ' "+response_text + "'")
            engine.say(response_text)
            engine.runAndWait()


            # if not audio:
            #     listen_for_wake_word(source)
        except sr.UnknownValueError:
            time.sleep(5)
            print("Silence found, shutting up, listening...")
            listen_for_wake_word(source)
            break

        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(f"Could not request results; {e}")
            engine.runAndWait()
            listen_for_wake_word(source)
            break

# Use the default microphone as the audio source
with sr.Microphone() as source:
    listen_for_wake_word(source)
