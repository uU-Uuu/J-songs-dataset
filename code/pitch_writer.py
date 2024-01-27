import pandas as pd
from IPython.display import display

from lyr_tokenizer import df
from pitch_reader import get_pitch_accent_dict


def hira_kata_conv(txt, mode='h2k'):
    """
    Convert 
        hiragana to katakana: mode="h2k" (default)
        katakana to hiragana: mode="k2h"

    Copyright (c) 2016, Mads Sørensen Ølsgaard, olsgaard.dk
    """
    katakana_chart = "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶヽヾ"
    hiragana_chart = "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖゝゞ"
    hir2kat = str.maketrans(hiragana_chart, katakana_chart)
    kat2hir = str.maketrans(katakana_chart, hiragana_chart)
    return txt.translate(kat2hir) if mode == "k2h" else txt.translate(hir2kat)
    

pitch_accent_dict = get_pitch_accent_dict()

for indx, row in df.iterrows():

    line = row['Dict. form'], hira_kata_conv(row['Reading'], 'k2h')
    for key in pitch_accent_dict.keys():
        if line[0] in key or line[1] in key:
            df.at[indx, 'Pitch accent'] = pitch_accent_dict[key]
            break
print(df['Pitch accent'].isna().sum()) #324
display(df.loc[df.isnull().any(axis=1)])




# display(df)