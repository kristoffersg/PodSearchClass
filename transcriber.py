'''This module is transcribing audio'''
import shutil
import os
from os import path
from wav_splitter import readwave, writewave, split
import speech_recognition as sr

def transcribe(filename):
    '''This function transcribes the audio
    Takes: filepath
    Return: Transcription of file (string)'''

    # Pre-coding___________________________________________________________________________________
    if os.path.isdir('res'):                            # Clear directory "res"
        shutil.rmtree('res')

    # Splitting audio file_________________________________________________________________________
    interval_ = 14                                      # Podcast splitting interval in seconds
    overlap_ = 2                                        # Overlap in seconds

    data = readwave(filename)                           # extract data from wav file
    [splitted, iterations] = split(data, interval_-overlap_, overlap_)

    # save 1-second interval to output as individual files
    writewave('res/output-1-', splitted)

    # Transcribe for every 20-seconds audio file created___________________________________________
    transcription = ""
    for i in range(0, iterations):
        # Obtain path to audio files
        audio_file = path.join(path.dirname(path.realpath(__file__)), "res/output-1-" + str(i) + ".wav")

        # Use the audio file as the audio source
        rec = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = rec.record(source)  # read the entire audio file

        # Recognize speech using Google Speech Recognition
        try:
            #encode is for euro signs and other unicode
            googletranscription = rec.recognize_google(audio).encode('utf-8')
            transcription += " -- " + googletranscription

        except sr.UnknownValueError:
            print "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            print "Could not request results from Google Speech Recognition service; {0}".format(e)

    return transcription
