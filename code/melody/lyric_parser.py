from lxml import etree
from itertools import zip_longest
import re
import pandas as pd
from IPython.display import display
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from sudachipy import tokenizer, dictionary


xml_filename = 'xml\\1-ishikaribanka.xml'
txt_k_filename = 'lyrics\\1-k-ishikaribanka.txt'
txt_h_filename = 'lyrics\\1-h-ishikaribanka.txt'


class LyricsTokenizer:
    parser = etree.XMLParser()
    driver = webdriver.Chrome()

    lyr_tokenizer = dictionary.Dictionary(dict='full').create()
    mode = tokenizer.Tokenizer.SplitMode.C

    @classmethod
    def create_word_df(cls):
        cls.word_df = pd.DataFrame(columns=['Token', 'Reading', 'Dict. Form', 'POS', 'Line', 'Song ID'])

    @classmethod
    def create_lex_ph_df(cls):
        cls.lex_ph_df = pd.DataFrame(columns=[
            'Lex. Phr.', 'Reading', 'Pitch Accent 0', 'Pitch Accent 1',
            'Melody', 'Duration', 'Duration Calc.', 'Melody Full', 'Line', 'Song ID'])
        
    @classmethod
    def melody_file_to_df(cls, k_filename, h_filename, xml_filename):
        zipped_, song_id = cls.zip_words_pitches(
            xml_filename=xml_filename, h_filename=h_filename, k_filename=k_filename)
        for phrase in zipped_:

            phrase_info = [phrase[0], phrase[1].strip('\n'), '', '',
                           cls.parse_melody_short(phrase[2]), 
                           cls.parse_duration(phrase[2]),
                           cls.parse_duration(phrase[2], calc=True),
                           phrase[2], '', song_id]
            cls.lex_ph_df.loc[len(cls.lex_ph_df.index)] = phrase_info
        display(cls.lex_ph_df[['Reading', 'Melody', 'Duration', 'Duration Calc.', 'Melody Full']])

    @classmethod    
    def populate_phrases_pitch(cls):
        for ind, row in cls.lex_ph_df.iterrows():
            row['Pitch Accent 0'] = LyricsTokenizer.scrape_phrase_pitch(row['Lex. Phr.'], mode=0)
            row['Pitch Accent 1'] = LyricsTokenizer.scrape_phrase_pitch(row['Lex. Phr.'], mode=1)

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

    @staticmethod
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
        """Parse melody pitch values from melody_full string

        'ゆ=E5*1/8 め=G5*1/8+A5*1/8' -> 'E5 G5+A5'"""
        re_pattern = r'([A-Z]\d|\+[A-Z]\d)'
        melody_short = ''
        for matched in re.finditer(re_pattern, melody_full):
            sep = (' ', '')[matched.group().startswith('+')]
            melody_short += sep + matched.group()
        return melody_short.lstrip()
    
    @staticmethod
    def parse_duration(melody_full, calc=False):
        """Parse duration values from melody_full string

        ゆ=E5*1/8 め=G5*1/8+A5*1/8 ->
        - calc=False:  1/8 1/8+1/8 
        - calc=True: (0.125, 0.25)"""
        re_pattern = r'(\d\/\d{,2}\+|\d\/\d{,2})'
        duration_raw = '' 
        for matched in re.finditer(re_pattern, melody_full):
            if calc:
                sep = (', ', '')[matched.group().endswith('+')]
            else:
                sep = (' ', '')[matched.group().endswith('+')]
            duration_raw += matched.group() + sep
        return ' '.join(map(str, eval(duration_raw))) if calc else duration_raw.lstrip()
    
    @staticmethod
    def scrape_phrase_pitch(phrase, mode=0):
        """
        mode: 
        - 0 (default): natural (Machine Learning)
        - 1: detailed (Bunsetsu)
        """
        LyricsTokenizer.driver.get('https://www.gavo.t.u-tokyo.ac.jp/ojad/phrasing/index')
        textarea = LyricsTokenizer.driver.find_element(By.XPATH, '//*[@id="PhrasingText"]')
        submit_btn = LyricsTokenizer.driver.find_element(By.XPATH, '//*[@id="phrasing_submit_wrapper"]/div/input')
        textarea.send_keys(phrase)
        mode_selector = Select(LyricsTokenizer.driver.find_element(By.XPATH, '//*[@id="PhrasingEstimation"]'))
        mode_selector.select_by_index(mode)
        submit_btn.click()
        moras_line = LyricsTokenizer.driver.find_element(By.XPATH, '//*[@id="phrasing_main"]/div[9]/div/div[2]')
        moras = moras_line.find_elements(By.XPATH, './*')[:-1]
        moras_classes = [mora.get_attribute('class') for mora in moras]
        decoded = LyricsTokenizer.decode_mora_class(moras_classes, to_str=True)
        return decoded


    @staticmethod
    def decode_mora_class(moras, to_str=False):
        """
        - mola = 0
        - accent_plain = 1
        - accent_top = 1/
        - unvoiced = 0. 1. 1/.
        """
        moras_ = []
        for mora in moras:
            if 'accent_plain' in mora:
                moras_.append('1')
            elif 'accent_top ' in mora:
                moras_.append('1/')
            else:
                moras_.append('0')
            if 'unvoiced' in mora:
                moras_[-1] += '.'
        return ' '.join(moras_) if to_str else moras_ 
    
    @staticmethod
    def save_df_csv(df, filename, index=False):
        df.to_csv(filename, index=index)
            



pd.options.display.min_rows = 100
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)


lyr_tokenizer = LyricsTokenizer()
lyr_tokenizer.create_word_df()
lyr_tokenizer.create_lex_ph_df()
lyr_tokenizer.melody_file_to_df(txt_k_filename, txt_h_filename, xml_filename)
lyr_tokenizer.populate_phrases_pitch()
lyr_tokenizer.save_df_csv(lyr_tokenizer.lex_ph_df, filename='./data/melody/lex_phr.csv')
