#!/Users/ksg/miniconda2/bin/python2.7
from python_speech_features import mfcc
import scipy.io.wavfile as wav
import numpy as np
import os
import time
# import winsound
from sklearn.externals import joblib


# Pre-set testing variables:
num_tests = 100                     # The number of tests done on each classification algorithm
interval = 400                      # The interval between each test observation
K = 10                              # Number of nearest neighbors
number_of_files = 2             # Number of instances of each keyword in training. Set to False for all files
padding = "Edge"                    # Choose padding method. Either "Zero", "Edge" or "Mean"
feature = "MFCC"                    # Choose feature ("MFCC" or "Filterbank")
# ____________________________________________________________________________________________________________________

open('tests/CLASS_TEST_KNN (' + feature + ', ' + str(num_tests) + ', ' + str(interval) + ', ' + str(number_of_files) + ', ' + str(padding) + ', K=' + str(K) + ').txt', 'w').close()       #Generate new txt file
open('tests/CLASS_TEST_KNN (' + feature + ', ' + str(num_tests) + ', ' + str(interval) + ', ' + str(number_of_files) + ', ' + str(padding) + ', K=' + str(K) + ').txt', 'a').write("Feature = " + feature + ", Number of tests: " + str(num_tests) + ", Interval: " + str(interval) + ", K = " + str(K) + ", num_files = " + str(number_of_files) + ", Padding = " + str(padding + "\n \n"))

start_time_Overall = time.time()
num_files = number_of_files

# # Supervised learning algorithms______________________________________________________________________________________
KNN_Timer = []
KNN_count = 0

# #Load K-nearest neighbors classifier:
knn = joblib.load("Classifiers/clf_KNN")

print "Now beginning tests:"
# duration = 1000  # millisecond
# freq = 440  # Hz
# winsound.Beep(freq, duration)

if num_files == False:
    num_files = len([f for f in os.listdir("splitAudio") if
                        os.path.isfile(os.path.join("splitAudio", f))])  # how many files in splitAudio

for _ in range(num_files):
    (rate, sig) = wav.read("splitAudio/chunk" + str(_) + ".wav")
    mfcc_feat = mfcc(sig, rate)                                         # mfcc feature extraction
    mfcc_feat = [item for sublist in mfcc_feat for item in sublist]     # Flattening ******************************************* HER KOM VI TIL *******************************************
    X_test = np.lib.pad(mfcc_feat, (0, 3000-len(mfcc_feat)), 'mean')    # Mean padding

    start_time = time.time()  # ______________________________________________________________________________________

    # K Nearest Neighbor:
    KNN_answer = knn.predict([X_test])
    elapsed_time_KNN = time.time() - start_time #- elapsed_time_QDA - elapsed_time_LDA
    print "KNN Prediction: ", KNN_answer

    KNN_Timer.append(elapsed_time_KNN)

    printer = "TEST NUMBER: " + str(_) + "\n KNN Prediction: " + str(KNN_answer) + "\n KNN Time: " + str(elapsed_time_KNN) + "\n"
    open('tests/CLASS_TEST_KNN (' + feature + ', ' + str(num_tests) + ', ' + str(interval) + ', ' + str(number_of_files) + ', ' + str(padding) + ', K=' + str(K) + ').txt', 'a').write(str(printer) + "\n")

# print "SVM got ", SVM_count, " right"
print "Got ", KNN_count, " right"

elapsed_time_Overall = time.time() - start_time_Overall
print "Time for Program: ", elapsed_time_Overall, "\n"  # ____________________________________________________________

average_time_KNN = sum(KNN_Timer)/float(len(KNN_Timer))


final_printer = "\nOVERALL RESULTS: \n" + "\n KNN Result: " + str(KNN_count) + "/" + str(num_tests) + "\n KNN Average Time: " + str(average_time_KNN) + "\n \n Time for program: " + str(elapsed_time_Overall) + "\n"

open('tests/CLASS_TEST_KNN (' + feature + ', ' + str(num_tests) + ', ' + str(interval) + ', ' + str(number_of_files) + ', ' + str(padding) + ', K=' + str(K) + ').txt', 'a').write(str(final_printer))


# freq = 880  # Hz
# winsound.Beep(freq, duration)
# winsound.Beep(440, duration)
# winsound.Beep(freq, duration)