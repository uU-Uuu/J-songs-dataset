from os import stat
from lxml import etree
from itertools import zip_longest
import re
import pandas as pd
from IPython.display import display
from pprint import pprint


from sudachipy import tokenizer, dictionary


parser = etree.XMLParser()

xml_filename = 'xml\\1-ishikaribanka.xml'
txt_k_filename = 'lyrics\\1-k-ishikaribanka.txt'
txt_h_filename = 'lyrics\\1-h-ishikaribanka.txt'



        
# zip_words_pitches()

class LyricsTokenizer:
    lyr_tokenizer = dictionary.Dictionary(dict='full').create()
    mode = tokenizer.Tokenizer.SplitMode.C

    @classmethod
    def create_word_df(cls):
        cls.word_df = pd.DataFrame(columns=['Token', 'Reading', 'Dict. form', 'POS', 'Line', 'Song ID'])

    @classmethod
    def create_lex_ph_df(cls):
        cls.lex_ph_df = pd.DataFrame(columns=['Lex. Phr.', 'Reading', 'Pitch accent', 'Melody full', 'Line', 'Song ID'])

    @classmethod
    def melody_file_to_df(cls, k_filename, h_filename, xml_filename):
        zipped_, song_id = cls.zip_words_pitches(
            xml_filename=xml_filename, h_filename=h_filename, k_filename=k_filename)
        for phrase in zipped_:

            phrase_info = [phrase[0], phrase[1].strip('\n'), '', phrase[2], '', song_id]
            cls.lex_ph_df.loc[len(cls.lex_ph_df.index)] = phrase_info
        display(cls.lex_ph_df)


    @classmethod
    def tokenize_phrase(cls, phrase, line_no, song_id):
        phrase = re.sub(r' |\n|\u3000|「|」……', '', phrase)
        phrase_tokens = [m.surface() for m in cls.lyr_tokenizer.tokenize(phrase, cls.mode)]

        for el in phrase_tokens:
            token = cls.lyr_tokenizer.tokenize(el, cls.mode)[0]
            token_info = [token.surface(), token.reading_form(), token.dictionary_form(), 
                          token.part_of_speech(), line_no, song_id]
            cls.df.loc[len(cls.word_df.index)] = token_info

    @classmethod
    def tokenize_file(cls, k_filename):
        with open(k_filename, 'r', encoding='utf-8') as file:
            song_dir = k_filename.strip('../J-SONGS-DATASET/lyrics\\')
            match_song_id = re.match(r'^\d*', song_dir)
            song_id = match_song_id.group()
            line_no = 1

            for line in file.readlines():
                cls.tokenize_phrase(line, line_no, song_id)
                line_no += 1

    def get_xml_root(xml_filename):
        with open(xml_filename, encoding='utf-8', mode='r') as file:
            xml_str = file.read()
            xml_str = xml_str.encode('utf-8')
            root = etree.fromstring(xml_str)

        title = root.find('title').text
        key = root.find('key').text
        time_signature = root.find('time_signature').text

        return root

    @staticmethod
    def get_mel_xml_lines(root):
        mel_lines = []
        for mel_phr in root.findall('.//melodic_phrase'):
            lex_lines = []
            lex_phrs = mel_phr.getchildren()
            for lex_phr in lex_phrs:
                lex_line = []
                syllables = lex_phr.findall('.//syllable')
                for syll in syllables:
                    lyrics, pitches, durations = tuple(map(lambda x: syll.findall(x), ('.//lyric', './/pitch', './/duration')))
                    lyrics = tuple(map(lambda el: el.text, lyrics))
                    pitches = tuple(map(lambda el: el.text, pitches))
                    durations = tuple(map(lambda el: el.text, durations))

                    lex_line.append(tuple(zip_longest(lyrics, pitches, durations)))
                lex_lines.append(lex_line)
            mel_lines.append(lex_lines)
        return mel_lines


    @staticmethod
    def concat_lex_phrs_xml(xml_filename):
        mel_lines = LyricsTokenizer.get_mel_xml_lines(
            LyricsTokenizer.get_xml_root(xml_filename))
        lex_lines_annotated = []
        for mel_line in mel_lines:
            for lex_line in mel_line:
                lex_line_syllables = []
                for syllable in lex_line:
                    syllable_line = ''
                    for note in syllable:
                        mora, pitch, duration = note
                        if mora:
                            syllable_line += f'{mora}={pitch}*{duration}'
                        else:
                            syllable_line += f'+{pitch}*{duration}'
                    lex_line_syllables.append(syllable_line)
                lex_lines_annotated.append(' '.join(lex_line_syllables))
        return lex_lines_annotated


    @staticmethod
    def parse_k_txt_file(k_filename):
        with open(k_filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        lex_phrs = []
        for line in lines:
            lex_phrs.extend(line.split())
        return lex_phrs

    @staticmethod
    def zip_words_pitches(xml_filename, h_filename, k_filename=None, ignore_blank=True):
        with open(h_filename, 'r', encoding='utf-8') as file:
            song_dir = h_filename.strip('../J-SONGS-DATASET/lyrics\\')
            match_song_id = re.match(r'^\d*', song_dir)
            song_id = match_song_id.group()
            h_lyr_phrs = file.readlines()

        if k_filename:
            k_lyr_phrs = LyricsTokenizer.parse_k_txt_file(k_filename)

        if ignore_blank:
            h_lyr_phrs = list(filter(lambda phr: phr != '\n', h_lyr_phrs))
            k_lyr_phrs = list(filter(lambda phr: phr != '\n', k_lyr_phrs))
        lex_phrs_annotated = LyricsTokenizer.concat_lex_phrs_xml(xml_filename)

        zipped_ = list(zip_longest(k_lyr_phrs, h_lyr_phrs, lex_phrs_annotated))
        return zipped_, song_id
    
    @staticmethod
    def parse_melody_short(melody_full):
        """'ゆ=E5*1/8 め=G5*1/8+A5*1/8' >> 'E5 G5+A5'"""
        re_pattern = r'(\w\d|\+\w\d)'
        melody_short = ''
        for matched in re.finditer(re_pattern, melody_full):
            sep = (' ', '')[matched.group().startswith('+')]
            melody_short += sep + matched.group()
        return melody_short.lstrip()

        

 

pd.options.display.min_rows = 100

lyr_tokenizer = LyricsTokenizer()
# lyr_tokenizer.create_word_df()
# lyr_tokenizer.create_lex_ph_df()
# lyr_tokenizer.melody_file_to_df(txt_k_filename, txt_h_filename, xml_filename)

lyr_tokenizer.parse_melody_short('ゆ=E5*1/8 め=G5*1/8+A5*1/8')

# lyrics_tokenizer.tokenize_file(txt_k_filename)
# display(lyrics_tokenizer.df)

# lyr_tokenizer.parse_k_txt_file(txt_k_filename)