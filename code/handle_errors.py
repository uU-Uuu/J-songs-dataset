from sudachipy import tokenizer
from sudachipy import dictionary
from sudachipy import Morpheme

# Morpheme.ge
# t_word_info(self) -> WordInfo i

import pandas as pd
import numpy as np
from IPython.display import display

# from lyr_tokenizer import df
from pitch_reader import get_pitch_accent_dict



df = pd.read_csv('Data.csv', encoding='utf-8')

tokenizer_obj = dictionary.Dictionary(dict_type='full').create()
mode = tokenizer.Tokenizer.SplitMode.C

# start at もう一度 225 NaN-dynamics
sagashi = '九十九折'
 
print(tokenizer_obj.tokenize(sagashi, mode)[0].normalized_form())

line_token_list = [m.surface() for m in tokenizer_obj.tokenize(sagashi, mode)]
for tok in line_token_list:
    m = tokenizer_obj.tokenize(tok, mode)[0]
    token_info_list =[m.surface(), m.reading_form(), m.dictionary_form(), m.part_of_speech()]
    print(token_info_list)
    


pitch_accent_dict = get_pitch_accent_dict()


# line = '探す'
# for key in pitch_accent_dict.keys():
#     if line in key:
#         print(pitch_accent_dict[key])
            # df.at[indx, 'Pitch accent'] = pitch_accent_dict[key]
            # break



# display(df.loc[df['Token'] == 'さがし'])

# df.loc[2885,['Dict. form']] = m.dictionary_form()

# print(df.iloc[2885])
# # print('------', token_info_list)
# # df.iloc[2885] = token_info_list
# display(df.iloc[2885])

# token_info_list = [m.surface(), m.reading_form(), m.dictionary_form(), m.part_of_speech(), line_no, song_id]

# display(df)


"""

!!! 
- check NaN again as they turn out as you handle

- incorrect pos in tokenizing
- change splitining Mode
- split proper nouns (often they're song names)
- unite some proper names back
- search OJAD, dicts for pitch accent only
- search for kanji - unite compound words mistakenly split
- check & delete pitch accent for all particles -　の　て
- write rules for following particles

つかめる　- dialect - let's leave as it is

- analyze proper names individually after
"""