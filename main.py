import numpy as np
from definition import Song, Music
from read import songs
from tool import *
import pickle as pkl

debug = False
Num = 8  # 生成的旋律数

table_chord_loc = np.zeros([7, 8, 88])  # 存储概率分布
table_chord_pre = np.zeros([7, 88, 88])
table_chord_pre_next = np.zeros([7, 88, 88, 88])


def Calculate():
    for song in songs:
        tune_lenth = len(song.tune)
        for l in range(tune_lenth):
            tune = song.tune[l]
            chord_level = Chord_Level(tune[0])
            for i in range(8):
                # 统计表：和弦级数+音符位置
                note_i = tune[1][i] + tune[2][i] * 12 + 39
                table_chord_loc[chord_level][i][note_i] += 1

                # 统计表：和弦级数+前一个音符
                if i % 2 == 0:
                    if i != 0:
                        note_pre = tune[1][i - 2] + tune[2][i - 2] * 12 + 39
                        table_chord_pre[chord_level][note_pre][note_i] += 1
                    if i == 0 and l != 0:
                        note_pre = song.tune[l - 1][1][6] + song.tune[l - 1][2][6] * 12 + 39
                        table_chord_pre[chord_level][note_pre][note_i] += 1

                # 统计表：和弦级数+前后的音符
                if i % 2 == 1:
                    note_pre = tune[1][i - 1] + tune[2][i - 1] * 12 + 39
                    if i != 7:
                        note_next = tune[1][i + 1] + tune[2][i + 1] * 12 + 39
                    if i == 7:
                        if l != tune_lenth - 1:
                            note_next = song.tune[l + 1][1][0] + song.tune[l + 1][2][0] * 12 + 39
                        else:
                            note_next = 0
                    table_chord_pre_next[chord_level][note_pre][note_next][note_i] += 1

    file = open('net.pkl', 'wb')
    pkl.dump([table_chord_loc, table_chord_pre, table_chord_pre_next], file)
    file.close()


def stat_prob(p):  # 计算概率
    p_sum = p.sum()
    if p_sum == 0:
        return False, p
    for i in range(88):
        p[i] /= p_sum
    return True, p


class MarkovState:
    def __int__(self):
        self.tune = np.zeros((8, 8), dtype=int)
        self.loc = 0
        self.policy = None
        self.note = 0
        self.exist_policy = False


def markov_search(state, i, j, pre, next):
    note_list = [int(i) for i in range(88)]
    chord_level = Chord_Level(ChordList[i])
    if i == 0 and j == 0:
        flag, prob = stat_prob(table_chord_loc[chord_level][0])
        if flag:
            note_gen = np.random.choice(note_list, size=1, p=prob)
        else:
            note_gen = Chord_Seq(ChordList[i])[j]


def markov_prob(s):
    # calculate that p(next|now,next_chord)
    chord_level = Chord_Level(ChordList[s.next_i])
    tune = s.tune
    note_now = tune[s.now_i][1][s.now_j] + tune[s.now_i][2][s.now_j] * 12 + 39
    note_next = tune[s.next_i][1][s.next_j] + tune[s.next_i][2][s.next_j] * 12 + 39
    return stat_prob(table_chord_pre[chord_level][note_now])


def markov_initial(chord_level):
    _, prob = stat_prob(table_chord_loc[chord_level][0])
    a = 39 # np.random.choice([int(i) for i in range(88)], size=1, p=prob)[0]
    s_new = MarkovState()
    s_new.loc = 0
    s_new.note = a
    s_new.tune = np.zeros((8, 8), dtype=int)
    s_new.tune[0][0] = a
    s_new.exist_policy, s_new.policy = stat_prob(table_chord_pre[chord_level][a])
    return s_new


def state_transfer(s, a, ChordList):
    s_new = MarkovState()
    pre_note = s.note
    s_new.note = a
    s_new.loc = s.loc + 2
    if s_new.loc == 62:  # 只检查table_chord_pre_next
        chord_level = Chord_Level(ChordList[7])
        flag2, prob2 = stat_prob(table_chord_pre_next[chord_level][pre_note][a])
        if flag2:
            s_new.tune = s.tune
            s_new.tune[s_new.loc // 8][s_new.loc % 8] = a
            pre_note = np.random.choice([int(i) for i in range(88)], size=1, p=prob2)[0]
            s_new.tune[(s_new.loc - 1) // 8][(s_new.loc - 1) % 8] = pre_note
            s_new.exist_policy = True
        else:
            s_new.exist_policy = False
        return s
    else:
        chord_level = Chord_Level(ChordList[s_new.loc // 8])
        flag1, prob1 = stat_prob(table_chord_pre[chord_level][a])
        chord_level = Chord_Level(ChordList[(s_new.loc-1) // 8])
        flag2, prob2 = stat_prob(table_chord_pre_next[chord_level][pre_note][a])
        if flag1 and flag2:
            s_new.policy = prob1
            s_new.tune = s.tune
            s_new.tune[s_new.loc // 8][s_new.loc % 8] = s.note
            pre_note = np.random.choice([int(i) for i in range(88)], size=1, p=prob2)[0]
            s_new.tune[(s_new.loc - 1) // 8][(s_new.loc - 1) % 8] = pre_note
            s_new.exist_policy = True
        else:
            s_new.exist_policy = False
        return s_new


def markov_generate(ChordList):
    # 初始化
    s = [MarkovState() for i in range(32)]
    initial_state = markov_initial(Chord_Level(ChordList[0]))
    s[0] = initial_state
    # print(s[0].policy)
    t = 0
    while t < 31:
        if t < 0:
            print('Warning! Bad initialization!')
            return None
        # print(s[0].policy)
        if s[t].exist_policy:
            # print(s[t].tune)
            # print(t, s[t].loc)
            prob = s[t].policy
            a = np.random.choice([int(i) for i in range(88)], size=1, p=prob)[0]
            next_s = state_transfer(s[t], a, ChordList)
            t = t + 1
            s[t] = next_s
        else:
            a = s[t].note
            t = t - 1
            prob = s[t].policy
            # print(t, s[t].loc)
            prob[a] = 0
            s[t].exist_policy, s[t].policy = stat_prob(prob)

    final_state = s[-1]
    final_state.tune[7][7] = 26 # E和弦的最后一个音
    return final_state

def markov_song(ChordList, state):
    # note_list = [int(i) for i in range(88)]
    tune_lenth = len(ChordList)
    tune_gen = [[] for i in range(tune_lenth)]
    for i in range(tune_lenth):
        tune_gen[i] = (ChordList[i], [], [])
        chord_level = Chord_Level(ChordList[i])
        for j in range(8):
            note_ij = state.tune[i][j]
            tune_gen[i][1].append(Dig_Level((note_ij - 39) % 12))
            tune_gen[i][2].append((note_ij - 39) // 12)
    return tune_gen


def regeneration(ChordList):
    note_list = [int(i) for i in range(88)]
    tune_lenth = len(ChordList)
    tune_gen = [[] for i in range(tune_lenth)]
    for i in range(tune_lenth):
        tune_gen[i] = (ChordList[i], [], [])
        chord_level = Chord_Level(ChordList[i])
        for j in range(8):
            flag, prob = stat_prob(table_chord_loc[chord_level][j])
            if flag:
                note_ij = np.random.choice(note_list, size=1, p=prob)
            else:
                note_ij = Chord_Seq(ChordList[i])[j]
            note_ij = note_ij[0]
            tune_gen[i][1].append(Dig_Level((note_ij - 39) % 12))
            tune_gen[i][2].append((note_ij - 39) // 12)
    return tune_gen


if __name__ == '__main__':
    Calculate()
    ChordList = ['C', 'Am', 'F', 'G', 'C', 'Am', 'F', 'G']
    # music = regeneration(ChordList)
    s_markov = markov_generate(ChordList)
    music = markov_song(ChordList, s_markov)
    print(music)
    song_play(music)
    time.sleep(30)
    # printMusic(music)
