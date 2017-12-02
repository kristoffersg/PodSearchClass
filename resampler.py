#!/Users/ksg/miniconda2/bin/python2.7
import wave
import audioop

def resampler(source_path, output_path):
    audioFile = wave.open(source_path, 'r')
    n_frames = audioFile.getnframes()
    audioData = audioFile.readframes(n_frames)
    originalRate = audioFile.getframerate()
    af = wave.open(output_path, 'w')
    af.setnchannels(1)
    af.setparams((1, 2, 16000, 0, 'NONE', 'Uncompressed'))
    converted = audioop.ratecv(audioData, 2, 1, originalRate, 16000, None)
    af.writeframes(converted[0])
    af.close()
    audioFile.close()