from sudachipy import tokenizer
from sudachipy import dictionary

import pandas as pd


df = pd.read_csv('Data/Data_init.csv', encoding='utf-8')

tokenizer_obj = dictionary.Dictionary(dict_type='full').create()
mode = tokenizer.Tokenizer.SplitMode.A

sagashi = ''
 
print(tokenizer_obj.tokenize(sagashi, mode)[0].normalized_form())

line_token_list = [m.surface() for m in tokenizer_obj.tokenize(sagashi, mode)]
for tok in line_token_list:
    m = tokenizer_obj.tokenize(tok, mode)[0]
    token_info_list =[m.surface(), m.reading_form(), m.dictionary_form(), m.part_of_speech()]
    print(token_info_list)


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
