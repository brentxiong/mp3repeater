# -*- coding: utf-8 -*-
from Tkinter import *
from pydub import AudioSegment
from pydub import playback
import threading, time
from pydub import silence

song = AudioSegment.from_mp3("/Users/brentxiong/Downloads/vocabulary/unit 01.mp3")
songs = []
timetable = []
startpoint = time.time()
index=0

def playsong():
    global song
    global startpoint
    startpoint = time.time()
    playback.play(song)

def writeToTxt(list_name,file_path):
    try:
        fp = open(file_path,"w+")
        for item in list_name:
            fp.write(str(item)+"\n")
        fp.close()
    except IOError:
        print("fail to open file")

def readFromTxt(file_path):
    try:
        fp = open(file_path,"r")
        lt = fp.readlines()
    except IOError:
        print "fail to open file"
    return lt

def play():
    thread = threading.Thread(target=playsong)
    thread.daemon = True
    thread.start()

def get_text(event):
    global timetable
    global startpoint
    if (event.char) == 'a':
        point = time.time()
        span = int((point - startpoint) * 1000)
        timetable.append(span)
        print span

def savetofile():
    global timetable
    writeToTxt(timetable, 'points.txt')

def readfromfile():
    global songs
    table = readFromTxt('points.txt')
    print  table
    for t in table:
        timetable.append(int(t.replace('\n', '')))
    print timetable

    startpoint = 0
    for sector in timetable:
        songs.append(song[startpoint: sector])
        startpoint = sector
    print len(songs)

def playsigle():
    global songs
    global index
    try:
        song = songs[index]
        playback.play(song)
    except:
        pass

def previoussong():
    global index
    if index >=1:
        index = index - 1
    text.set(str(index))

def nextsong():
    global index
    global songs
    if index < len(songs) - 1:
        index = index + 1
    text.set(str(index))

#GUI
root = Tk()
root.title("MP3 Repeater")
#Label(root, text="请输入...").grid(row=0, column=0)
Button(root, text='Play',command=play).grid(row=1, column=1)
Button(root, text='Save to file', command=savetofile).grid(row=2, column=1)
Button(root, text='Read', command=readfromfile).grid(row=3, column=1)

text = StringVar()
text.set('0')
Button(root, text='Previous', command=previoussong).grid(row=4,column=0)
Label(root, textvariable=text ).grid(row=4, column=1)
Button(root, text='Next', command=nextsong).grid(row=4,column=2)

Button(root, text='Play single',command=playsigle).grid(row=5,column=1)

#text = Text(root)
root.bind("<Key>", get_text)
root.mainloop()