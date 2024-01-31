import pandas as pd
import numpy as np
from IPython.display import display


def string2tuple(src_line):
    f = src_line.strip('()').split(', ')
    return tuple(x.strip("'") for x in f)

df = pd.read_csv('Data.csv', encoding='utf-8')
del df['Unnamed: 0']

joshi = df[df['POS'].apply(lambda x: string2tuple(x)[0] == '助詞')]
# display(joshi)

def joshi_pitch_assign():
    for index, row in joshi.iterrows():
        line = df.loc[index - 1, 'Pitch accent']

        try:
            line_tu = tuple(line.split(','))
        except AttributeError:
            count += 1
            pitch_acc = np.nan
        else:
            pitch_acc = ','.join(['1' if x =='0' else '0' if x in '123456' else '' for x in line_tu])
        finally:
            df.loc[index, 'Pitch accent'] = pitch_acc

"""
check if nan assigned correctly

check if the same song, same line

export as new csv after all processing
"""

