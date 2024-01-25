import re
import pandas as pd
from IPython.display import display
from IPython.display import HTML
import glob

from sudachipy import tokenizer
from sudachipy import dictionary



tokenizer_obj = dictionary.Dictionary(dict_type='full').create()

mode = tokenizer.Tokenizer.SplitMode.C


df = pd.DataFrame(columns = ['Token', 'Reading', 'Dict. form', 'POS', 'Line', 'Song ID'])


directory = '../J-SONGS-DATASET/lyrics'
for filename in glob.glob(directory + '/*-k-*.txt'):
    with open(filename, 'r', encoding='utf-8') as f:
        print(f.read())
        print(filename)

with open('lyrics/1-k-ishikaribanka.txt', 'r', encoding='utf-8') as file:
    token_list = []
    line_no, song_id = 1, 1
    for line in file.readlines():
        line =  re.sub(r' |\n', '', line)
        line_token_list = [m.surface() for m in tokenizer_obj.tokenize(line, mode)]
        
        # token_list.append(line_token_list)

        for tok in line_token_list:
            m = tokenizer_obj.tokenize(tok, mode)[0]
            token_info_list = [m.surface(), m.reading_form(), m.dictionary_form(), m.part_of_speech(), line_no, song_id]
            df.loc[len(df)] = token_info_list

        line_no += 1

display(df)


"""
    TODO
        - line no#
    - iterate through files in folder / list of files
    - song id
    - insert pitch accent from file
    
    - duplicates (chorus)
    - analyze by dict form - how word is realized in dif lines/ melodies/ songs/ etc

    = come up with idea to analyze this (w/o melody (save for master))
    = consider moving to Jupiter (for better output display)

    - whole line input 
    - whole lyrics (side by side - merged cell) ?
    - sentiment analysis
"""