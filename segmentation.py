from pydub import AudioSegment
from pydub.silence import split_on_silence

def segmentwords(filename):
    '''Takes: Filename
    Creates: segments of words'''
    sound_file = AudioSegment.from_wav(filename)
    audio_chunks = split_on_silence(sound_file, min_silence_len=70, silence_thresh=-16)

    for i, chunk in enumerate(audio_chunks):
        out_file = ".//splitAudio//chunk{0}.wav".format(i)
        print "exporting", out_file
        chunk.export(out_file, format="wav")
        