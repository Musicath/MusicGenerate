import numpy as np
import pickle
import os
import play
import time

alpha=[2,1,1]#和弦和谐度参数
beta=[4,1,2,1,2,1,2,1]#小节和谐度参数
sev2twl={1:0,12:1,2:2,23:3,
         3:4,4:5,45:6,5:7,
         56:8,6:9,67:10,7:11}#简谱记法改为五线谱记法
cho2twl={'C':[0,4,7],'Cm':[0,3,7],
         'D':[2,6,9],'Dm':[2,5,9],
         'E':[4,8,11],'Em':[4,7,11],
         'F':[5,9,0],'Fm':[5,8,0],
         'G':[7,11,2],'Gm':[7,10,2],
         'A':[9,1,4],'Am':[9,0,4],
         'B':[11,3,6],'Bm':[11,2,6]}
CSET=[[0,3,7],[0,4,7],
      [2,5,9],[2,6,9],
      [4,7,11],[4,8,11],
      [5,8,0],[5,9,0],
      [7,10,2],[7,11,2],
      [9,0,4],[9,1,4],
      [11,2,6],[11,3,6]]#和弦集
songs=[]

class Song:
    def __init__(self):
        self.name=""#歌名
        self.singer={}#歌手
        self.style={}#风格
        self.tune=[]#只记录部分副歌

def Tune_Init(songs):
    for song in songs:
        for t in song.tune:
           for i in range(8):
               t[1][i]=sev2twl[t[1][i]]
    return songs

def Tune_Play(songs):
    for song in songs:
        print("正在播放：",song.name)
        play.tune_play(song.name)
        time.sleep(20)
'''
在该程序同级目录下创建一个song文件夹
将song.pkl系列文件放入文件夹内即可读取
'''
for i in os.listdir('song'):
    file=open('song'+os.sep+i,'rb')
    song=pickle.load(file)
    file.close()
    songs.append(song)

songs=Tune_Init(songs)
Tune_Play(songs)
for song in songs:
    print(song.name)
    print(song.singer)
    print(song.style)
    print(song.tune)
