#!/Users/ksg/miniconda2/bin/python2.7
'''Find words'''

def findwords(keyword, indexarray):
    '''Takes: Keryword and array of words from podcast
    Returns: Label with timestamps where word is said'''
    timestamp = "Word found at:"
    for _ in indexarray:
        if keyword == _[2]:
            miliseconds = str(_[1])[-3:-1]
            temptime = formattime(_[1]//1000)
            timestamp += " " + temptime + "." + miliseconds + ","
    if timestamp.endswith(":"):
        return "Word not found"

    # Removes "," in the end of the labels
    if timestamp.endswith(','):
        return timestamp[:-1]

    return timestamp

def formattime(seconds):
    '''Takes: Seconds
    Returns: hh.mm.ss'''
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    time = "%d:%02d:%02d" % (hours, minutes, seconds)
    return time
