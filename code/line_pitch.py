import pandas as pd
from IPython.display import display
import numpy as np
from numpy import ma

from matplotlib import pyplot as plt


def str2tuple_pitch_int(src_line):
    return tuple(int(x) for x in src_line.split(','))


df = pd.read_csv('code/output/Data_1.csv', encoding='utf-8')

df['Pitch accent'] = df['Pitch accent'].fillna('-1') # NaN -> -1

li = []
for song_id, group in df.groupby('Song ID'):

    for line_no, group_line in group.groupby('Line'):
        li.append({'Song ID': song_id, 'Line': line_no, 
                   'Pitch accents': [str2tuple_pitch_int(el) for el in group_line['Pitch accent']],
                   'Tokens': [wrd for wrd in group_line['Reading']]})
        # print({'Song ID': song_id, 'Line': line_no, 
        #        'Pitch accents': [str2tuple_pitch_int(el) for el in group_line['Pitch accent']],
        #        'Tokens': [wrd for wrd in group_line['Reading']]})

df_song_line_pitch = pd.DataFrame(li)

# display(df_song_line_pitch.to_string())



pitch =  [(2, 1), (0,), (0,), (3, 0), (1,)]
line_no = df_song_line_pitch.loc[1]['Line']
song_id = df_song_line_pitch.loc[1]['Song ID']
token = df_song_line_pitch.loc[1]['Tokens']

def plt_line_pitch(line, song, pitch_accents, tokens):
    li = []

    indx = 0
    for pitches in pitch_accents:
        token = tokens[indx]
        token_pitch = []

        for pitch in pitches:

            if pitch == 0: 
                tkn_pitch = '0' + '1' * (len(token) - 1)
            elif pitch== 1: 
                tkn_pitch = '1' + '0' * (len(token) - 1)
            elif pitch == 2:
                tkn_pitch = '01' + '0' * (len(token) - 2)
            elif pitch == 3:
                tkn_pitch = '011' + '0' * (len(token) - 3)
            elif pitch == 4: 
                tkn_pitch = '0111' + '0' * (len(token) - 4)
            elif pitch == 5:
                tkn_pitch = '01111' + '0' * (len(token) - 5)
            elif pitch == 6:
                tkn_pitch = '011111' + '0' * (len(token) - 6)
            elif pitch == -1:
                tkn_pitch = '9'
            else:
                tkn_pitch = pitch

            token_pitch.append(tkn_pitch)

        li.append(token_pitch)
        indx += 1
    print(li)

    # line_pitch_01 = ''.join(li)
    # print(line_pitch_01)
    # line_pitch_arr = np.array([int(el) for el in line_pitch_01 if el != ' '])
    # masked_condtn = (line_pitch_arr == 9)
    # masked_data = ma.masked_where(masked_condtn, line_pitch_arr)
    # print(masked_data)
    # plt.plot(masked_data)
    # plt.show()
    


plt_line_pitch(line_no, song_id, pitch, token)

