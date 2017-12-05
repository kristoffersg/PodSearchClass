#!/Users/ksg/miniconda2/bin/python2.7
'''Classification of words'''
import os
import time
from python_speech_features import mfcc
import scipy.io.wavfile as wav
import numpy as np
from sklearn.externals import joblib

def knnfunc(stamp):
    '''Takes: list of segmented words
    Returns: Array with timestamp for each labeled word'''
    # Pre-set testing variables:
    # K = 5               # Number of nearest neighbors
    num_files = False   # Number of instances of each keyword in training. False for all files
    # padding = "Edge"    # Choose padding method. Either "Zero", "Edge" or "Mean"
    # feature = "MFCC"    # Choose feature ("MFCC" or "Filterbank")

    # # Supervised learning algorithms_____________________________________________________________
    knn_timer = []

    # #Load K-nearest neighbors classifier:
    knn = joblib.load("Classifiers/clf_KNN(MFCC_ZERO_K=5)")

    print "Now beginning tests:"

    if num_files is False:
        num_files = len([f for f in os.listdir("splitAudio") if
                         os.path.isfile(os.path.join("splitAudio", f))]) # amount of files

    output = []
    for _ in range(num_files-1):
        (rate, sig) = wav.read("splitAudio/chunk" + str(_) + ".wav")
        mfcc_feat = mfcc(sig, rate)                                        # mfcc feature extraction
        mfcc_feat = [item for sublist in mfcc_feat for item in sublist]    # Flattening
        x_test = np.lib.pad(mfcc_feat, (0, 3000-len(mfcc_feat)), 'mean')   # Mean padding

        start_time = time.time()  # _______________________________________________________________

        # K Nearest Neighbor:
        knn_answer = knn.predict([x_test])
        elapsed_time_knn = time.time() - start_time
        print "KNN Prediction: ", knn_answer

        piece = stamp[_]
        piece.extend(knn_answer)
        output.append(piece)

        knn_timer.append(elapsed_time_knn)

    return output
