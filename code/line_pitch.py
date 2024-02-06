import pandas as pd
from IPython.display import display
import numpy as np
from numpy import ma

from matplotlib import pyplot as plt
from matplotlib.cm import plasma

from jap_handle import ignore_length_small


def str2tuple_pitch_int(src_line):
    return tuple(int(x) for x in src_line.split(','))

def conv_line_pitch(pitch_accents, tokens):
    li = []
    indx = 0
    for pitches in pitch_accents:
        token = tokens[indx]
        token_pitch = []

        for pitch in pitches:

            if pitch == 0: 
                tkn_pitch = '0' + '1' * (ignore_length_small(token) - 1)
            elif pitch== 1: 
                tkn_pitch = '1' + '0' * (ignore_length_small(token) - 1)
            elif pitch == 2:
                tkn_pitch = '01' + '0' * (ignore_length_small(token) - 2)
            elif pitch == 3:
                tkn_pitch = '011' + '0' * (ignore_length_small(token) - 3)
            elif pitch == 4: 
                tkn_pitch = '0111' + '0' * (ignore_length_small(token) - 4)
            elif pitch == 5:
                tkn_pitch = '01111' + '0' * (ignore_length_small(token) - 5)
            elif pitch == 6:
                tkn_pitch = '011111' + '0' * (ignore_length_small(token) - 6)
            elif pitch == -1:
                tkn_pitch = '9'
            else:
                tkn_pitch = pitch

            token_pitch.append(tkn_pitch)

        li.append(token_pitch)
        indx += 1

    return(li)


def plt_line_pitch(song_id, line, src_li, tokens):
    li_mora_token = [mora for mora in ''.join(tokens)]

    fig, ax = plt.subplots()

    colormap = plasma
    norm = plt.Normalize(0, len(src_li))

    li_el_len = [len(el[0]) for el in src_li]

    for indx, elmnts in enumerate(src_li):
        for el in elmnts:
            el_pitch = np.array([int(e) for e in el])
            y = np.arange(sum(li_el_len[:src_li.index(elmnts)]), sum(li_el_len[:src_li.index(elmnts)]) + len(el_pitch))

            masked_condtn = (el_pitch == 9)
            masked_data = ma.masked_where(masked_condtn, el_pitch)

            stems = ax.stem(y, masked_data, basefmt=" ", linefmt='-')
            plt.setp(stems, color=colormap(norm(indx)))

            inx = elmnts.index(el)
            if inx >= 1:
                marker = 'o' if inx == 1 else 'X'
                ax.scatter(y, el_pitch, edgecolors='k', linewidths=3, marker=marker)


    plt.xticks(np.arange(sum(li_el_len)), li_mora_token, fontname="MS Gothic")
    plt.yticks([])
    plt.title(f'Song ID: {song_id}\nLine No. {line}', loc='left')

    plt.show()


def plt_line_pitch_song(song_id, line, pitch_accents, tokens):
    pitch_acc_li = conv_line_pitch(pitch_accents, tokens)
    plt_line_pitch(song_id, line, pitch_acc_li, tokens)


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

pitch = df_song_line_pitch.loc[485]['Pitch accents']
line_no = df_song_line_pitch.loc[485]['Line']
song_id = df_song_line_pitch.loc[485]['Song ID']
token = df_song_line_pitch.loc[485]['Tokens']

plt_line_pitch_song(song_id, line_no, pitch, token)