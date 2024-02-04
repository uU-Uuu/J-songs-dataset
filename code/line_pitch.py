import pandas as pd
from IPython.display import display


def str2tuple_pitch_int(src_line):
    return tuple(int(x) for x in src_line.split(','))


df = pd.read_csv('code/output/Data_1.csv', encoding='utf-8')

df['Pitch accent'] = df['Pitch accent'].fillna('-1') # NaN -> -1

li = []
for song_id, group in df.groupby('Song ID'):

    for line_no, group_line in group.groupby('Line'):
        li.append({'Song ID': song_id, 'Line': line_no, 'Pitch accent': [str2tuple_pitch_int(el) for el in group_line['Pitch accent']]})
        print({'Song ID': song_id, 'Line': line_no, 'Pitch accent': [str2tuple_pitch_int(el) for el in group_line['Pitch accent']]})

df_song_line_pitch = pd.DataFrame(li)

display(df_song_line_pitch)


# len(reading)
