'''Module for generating wordcloud'''
from os import path
import random
import numpy as np
from PIL import Image
from wordcloud import WordCloud


def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    '''Set color for cloud'''
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

def wordcloud_create(words):
    '''Takes: Filename
    Returns: path to wordcloud'''
    d = path.dirname(__file__)

    # Read the mask image from
    # https://commons.wikimedia.org/wiki/File:Cloud_font_awesome.svg
    mask = np.array(Image.open(path.join(d, "wordcloudTools/cloud.png")))

    # Preprocessing of stopwords:
    stopwords = open(path.join(d, "wordcloudTools/stopwords.txt")).read() #Loading stopwords file
    stopwords = set(stopwords.split()) #Splitting stopwords file into correct format

    # Wordcloud generation:
    wc = WordCloud(max_words=1000, mask=mask, stopwords=stopwords, margin=10, random_state=1).generate(words)

    # For black/white wordcloud:
    wc.recolor(color_func=grey_color_func, random_state=3)
    wordcloud_path = "wordcloudTools/Wordcloud_result.png"
    wc.to_file(wordcloud_path)

    return wordcloud_path
