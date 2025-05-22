import pickle
import os

class Song:
    def __init__(self):
        self.name=""
        self.singer=""
        self.style=""
        self.tune=[]

song=Song()
song.name=""
song.singer={""}
song.style={}
song.tune=[
    ['',
     [],
     [0,0,0,0,0,0,0,0]],
    ['',
     [],
     [0,0,0,0,0,0,0,0]],
    ['',
     [],
     [0,0,0,0,0,0,0,0]],
    ['',
     [],
     [0,0,0,0,0,0,0,0]],
    ['',
     [],
     [0,0,0,0,0,0,0,0]],
    ['',
     [],
     [0,0,0,0,0,0,0,0]],
    ['',
     [],
     [0,0,0,0,0,0,0,0]],
    ['',
     [],
     [0,0,0,0,0,0,0,0]]]

file=open('.pkl','wb')
pickle.dump(song,file)
file.close()
