class Song:
    def __init__(self):
        self.name = ""  # 歌名
        self.singer = {}  # 歌手
        self.style = {}  # 风格
        self.tune = []  # 只记录部分副歌


class Stress:
    def __init__(self):
        self.chord = 0  # 7种和弦
        self.pos = 0  # 4种位置
        self.tone = 0  # 36中单音


class Music:
    def __init__(self):
        self.chord = 'C'
        self.tune = []
        self.octave = 0
