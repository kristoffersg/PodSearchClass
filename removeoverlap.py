#!/Users/ksg/miniconda2/bin/python2.7
'''This module removes overlap in transcription'''
from difflib import SequenceMatcher as sq

def removerlap(words):
    '''Removal of overlap'''
    counter = 1
    cnt = 1
    start = counter
    transcription = ""
    for _ in words[2:len(words)-1]:
        counter += 1
        if _ == "--":
            after = ""
            before = ""
            cnt += 1
            for _ in words[counter:counter + 6]:
                after += " " + _
            if after.startswith(' '):
                after = after[1:]
            for _ in words[counter - 7:counter - 1]:
                before += _ + " "

            # Merge overlap
            if before != "":
                match = sq(None, before, after).find_longest_match(0, len(before), 0, len(after))
                overlap = before + after[match.b+match.size:]

            # Before overlap
            remwords = words[start: counter - 10] if cnt == 2 else words[start + 6: counter - 7]
            transcription += ' '.join(remwords) + ' ' + overlap + ' -- '
            start = counter
            rest = ""
            for _ in words[counter + 6:]:
                rest += _ + " "
            if rest.endswith(' '):
                rest = rest[:-1]

    transcription += rest + "--"

    return transcription
