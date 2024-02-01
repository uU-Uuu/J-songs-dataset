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
            pitch_acc = np.nan
        else:
            pitch_acc = ','.join(['1' if x =='0' else '0' if x in '123456' else '' for x in line_tu])
        finally:
            df.loc[index, 'Pitch accent'] = pitch_acc



def jodoushi_pitch_assign()
    jodoushi = df[df['POS'].apply(lambda x: string2tuple(x)[0] == '助動詞')]
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
                pitch_acc = ','.join(el for el in pitch_acc_li)
            finally:
                df.loc[index, 'Pitch accent'] = pitch_acc
                    


    # try:
    #     line_tu = tuple(line.split(','))
    # except AttributeError:
    #     pitch_acc = np.nan
    # else:
    #     pitch_acc = ','.join(['1' if x =='0' else '0' if x in '123456' else '' for x in line_tu])
    # finally:
    #     df.loc[index, 'Pitch accent'] = pitch_acc



"""
check if nan assigned correctly

check if the same song, same line

export as new csv after all processing

!!! jodoushi - full code bc might not corresp. to pattern (e.g. 0000)

go through all verb forms and adj, not those in NaN only

particles 副詞　ば　どう　・・・
"""


"""
if index - 1 == '1' >>  10*
if index - 1 == '0' >> 00*
'だ'
'です' 
'だろう'
'でしょう'
'だろ'
'でし'
 

'ましょ' 10
'ます' 10
'ませ' 10
'たく' 10
'たい' 10
'まい' 10

'ず' 0

'ぬ' 1
 
'せる' 11

'られる' 110
'れる'　>> 11 (if patt 0) ; 10 (if pat 1+)



'れ' 
'し' 
'た' 
'な' 
'せ' 


'き'   

'つ' 
 
'てる' 
'とる' 

'す'

"""