import pandas as pd
import numpy as np
from IPython.display import display


def string2tuple_pos(src_line):
    f = src_line.strip('()').split(', ')
    return tuple(x.strip("'") for x in f)

df = pd.read_csv('Data/Data.csv', encoding='utf-8')
del df['Unnamed: 0']


def joshi_pitch_assign():
    joshi = df[df['POS'].apply(lambda x: string2tuple_pos(x)[0] == '助詞')]
    # display(joshi)
    for index, row in joshi.iterrows():
        line = df.loc[index - 1, 'Pitch accent']

        try:
            line_tu = tuple(line.split(','))
        except AttributeError:
            pitch_acc = np.nan
        else:
            pitch_acc = ','.join(['1' if x =='0' else '0' if x in '123456' else '' for x in line_tu])
        finally:
            df.loc[index, 'Pitch accent'] = pitch_acc



def jodoushi_pitch_assign():
    jodoushi = df[df['POS'].apply(lambda x: string2tuple_pos(x)[0] == '助動詞')]
    # display(jodoushi.to_string())     

    for index, rows in jodoushi.iterrows():
        line = df.loc[index - 1, 'Pitch accent']
        token = jodoushi.loc[index, 'Token'] 
        prev_token = df.loc[index - 1, 'Reading']

        if token in ('だ','です','だろう','でしょう','だろ','でし'):
            try:
                line_tu = tuple(line.split(','))
            except AttributeError:
                pitch_acc = np.nan
            else:
                pitch_acc_li = []
                for x in line_tu:
                    if x == '0':
                        pitch_acc_li.append('0' * len(token) if len(prev_token) == 1 else '1' + '0' * (len(token) - 1))
                    elif x in '123456':
                        pitch_acc_li.append('0' * len(token) if len(prev_token) > int(x) \
                            else ('1' + '0' * (len(token) - 1) if len(prev_token) == int(x) else ''))
                pitch_acc = ','.join(el for el in set(pitch_acc_li))
            finally:
                df.loc[index, 'Pitch accent'] = pitch_acc
        
        elif token in ('ましょ', 'ます', 'ませ', 'たく', 'たい', 'まい'):
            pitch_acc = '10'
            df.loc[index, 'Pitch accent'] = pitch_acc
        
        elif token in ('ず', 'し'):
            pitch_acc = '0'
            df.loc[index, 'Pitch accent'] = pitch_acc

        elif token in ('ぬ', 'せ', 'れ', 'せる'):
            pitch_acc = '1' * len(token)
            df.loc[index, 'Pitch accent'] = pitch_acc

        elif token == 'られる':
            pitch_acc = '110'
            df.loc[index, 'Pitch accent'] = pitch_acc
                       
        elif token == 'れる' or token in ('てる', 'て', 'た'):
            try:
                line_tu = tuple(line.split(','))
            except AttributeError:
                pitch_acc = np.nan
            else:
                if token == 'れる':
                    pitch_acc = ','.join(['11' if x =='0' else '10' if x in '123456' else '' for x in line_tu])
                elif token in ('てる', 'て', 'た'):
                    pitch_acc = ','.join(['1' * len(token) if x =='0' else '0' * len(token) if x in '123456' else '' for x in line_tu])
            finally:
                df.loc[index, 'Pitch accent'] = pitch_acc


def fukushi_pitch_assign():
    fukushi = df[df['POS'].apply(lambda x: string2tuple_pos(x)[0] == '副詞')]
    # display(fukushi) 

joshi_pitch_assign()
jodoushi_pitch_assign()             



"""
check if nan assigned correctly

check if the same song, same line

export as new csv after all processing - call func first

!!! jodoushi - full code bc might not corresp. to pattern (e.g. 0000)

go through all verb forms and adj, not those in NaN only

adj

"""


if __name__ == "__main__": 
    df.to_csv('Data/Data_handled.csv')