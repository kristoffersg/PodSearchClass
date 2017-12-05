#!/Users/ksg/miniconda2/bin/python2.7
'''This module is the GUI and some functions'''
from Tkinter import Tk, Button, Frame, Label, LEFT, RIGHT, BOTTOM, TOP, BOTH, YES, Entry
from os.path import basename
from tkFileDialog import askopenfilename
import ttk
from searchwords import findwords
from transcriber import transcribe
from worder import wordcloud_create
from PIL import ImageTk, Image
from removeoverlap import removerlap
from segmentation import segmentwords
from classification import knnfunc


class PodSearch(object):
    '''This is the GUI class'''

    # Initialization of variables
    filename = ""

    # Initialization of GUI
    def __init__(self, master):
        '''Init of the GUI'''
        # Frame for progress bar
        self.bottomframe = Frame(master, highlightbackground="green", highlightcolor="green",
                                 highlightthickness=1, width=500, height=200)
        self.bottomframe.pack(side=BOTTOM)

        # Frame for buttons and entry
        self.leftframe = Frame(master, highlightbackground="blue", highlightcolor="blue",
                               highlightthickness=1, width=400, height=400)
        self.leftframe.pack(side=LEFT)

        # Sub frame  for buttons
        self.leftsubframe_top = Frame(self.leftframe, highlightbackground="yellow",
                                      highlightcolor="yellow", highlightthickness=1)
        self.leftsubframe_top.pack(side=TOP)

        # Sub frame for entry
        self.leftsubframe_bot = Frame(self.leftframe, highlightbackground="purple",
                                      highlightcolor="purple", highlightthickness=1)
        self.leftsubframe_bot.pack(side=BOTTOM)

        # Frame for wordcloud
        rightframe = Frame(master, highlightbackground="red", highlightcolor="red",
                           highlightthickness=1, width=250, height=250)
        rightframe.pack(side=RIGHT)

        # Browse button
        self.browsebtn = Button(self.leftsubframe_top, text="Browse", command=self.browse)
        self.browsebtn.pack(side=LEFT)

        # Quit button
        self.quitbtn = Button(self.leftsubframe_top, text="Quit", command=self.leftframe.quit)
        self.quitbtn.pack(side=LEFT)

        # Filepath label
        self.pathlabel = Label(self.leftsubframe_bot, text="filename")
        self.pathlabel.pack()

        # Textbox
        self.searchentry = Entry(self.leftsubframe_bot)
        self.searchentry.pack()
        self.searchentry.bind('<Return>', lambda _: self.search())

        # Search button
        self.searchbtn = Button(self.leftsubframe_bot, text="Search", command=self.search)
        self.searchbtn.pack()

        # Working Label
        self.workinglabel = Label(self.bottomframe)
        self.workinglabel.pack()

        # Progress Bar
        self.pbar_det = ttk.Progressbar(self.bottomframe, orient="horizontal", length=400,
                                        mode="indeterminate")

        # Wordcloud preparation
        self.imagefile = "wordcloudTools/black_background.png"
        self.imagefile = Image.open(self.imagefile)
        self.image1 = self.imagefile.resize((400, 400), Image.ANTIALIAS)
        self.image1 = ImageTk.PhotoImage(self.image1)

        self.panel1 = Label(rightframe, image=self.image1)
        self.display = self.image1
        self.panel1.pack(side=TOP, fill=BOTH, expand=YES)

        # Non GUI initializations
        self.duration = 0
        self.transcription = ""
        self.stemmed = ""
        self.transcription = ""
        self.imagefile2 = 0
        self.image2 = 0


    # Browse function
    def browse(self):
        '''browse for file'''
        self.filename = askopenfilename()  # openfile dialog and put file in filename
        if not self.filename:  # leave method if cancel is clicked
            self.pathlabel.config(text="")
            return
        self.pathlabel.config(text=basename(self.filename))  # show filename as label
        self.workinglabel.config(text="WORKING", font=(
            "Helvetica", 20))  # Show WORKING when transcribing
        self.pbar_det.pack()  # show the progress bar
        self.pbar_det.start()  # Start the progress bar
        root.update()
        self.transcription = transcribe(self.filename)  # Call transcribe

        wordcloud_path = wordcloud_create(self.transcription)
        self.transcription = removerlap(self.transcription.split(' '))
        self.new_image(wordcloud_path)
        stamp = segmentwords(self.filename)
        self.indexarray = knnfunc(stamp)

        self.workinglabel.config(text="")  # remove working label
        self.pbar_det.stop()  # Stop progress bar
        self.pbar_det.pack_forget()  # Remove progress bar

    # Search function
    def search(self):
        '''Search using text domain'''
        if not self.transcription == '':
            if not self.searchentry.get() == '':
                keyword = self.searchentry.get()  # Get entry from textbox
                timestamp = findwords(keyword, self.indexarray)
                self.workinglabel.config(text=timestamp, font=(
            "Helvetica", 14))
            else:
                self.workinglabel.config(text="Enter word in search field")
        else:
            self.workinglabel.config(text="No file selected")

    def new_image(self, path):
        '''Word Cloud image'''
        self.imagefile2 = Image.open(path)
        self.image2 = self.imagefile2.resize((400, 400), Image.ANTIALIAS)
        self.image2 = ImageTk.PhotoImage(self.image2)
        self.panel1.configure(image=self.image2)
        self.display = self.image2

root = Tk()
b = PodSearch(root)
root.title("Podcast Searcher Classification")
root.geometry("650x450+0+200")
root.mainloop()
