from lxml import etree
from itertools import zip_longest
import re
import pandas as pd
from IPython.display import display
from pprint import pprint


from sudachipy import tokenizer, dictionary


parser = etree.XMLParser()

xml_filename = 'xml\\1-ishikaribanka.xml'
txt_filename = 'lyrics\\1-k-ishikaribanka.txt'
txt_h_filename = 'lyrics\\1-h-ishikaribanka.txt'


def get_xml_root(filename):

    with open(filename, encoding='utf-8', mode='r') as file:
        xml_str = file.read()
        xml_str = xml_str.encode('utf-8')
        root = etree.fromstring(xml_str)

    title = root.find('title').text
    key = root.find('key').text
    time_signature = root.find('time_signature').text

    return root


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



def concat_lex_phrs_xml():
    mel_lines = get_mel_xml_lines(get_xml_root(xml_filename))
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



def zip_words_pitches():
    with open(txt_h_filename, 'r', encoding='utf-8') as file:
        lyr_phrs = file.readlines()
        lex_phrs_annotated = concat_lex_phrs_xml()
        zipped_ = list(zip_longest(lyr_phrs, lex_phrs_annotated))
        pprint(zipped_)
        
zip_words_pitches()

class LyricsTokenizer:
    lyr_tokenizer = dictionary.Dictionary(dict='full').create()
    mode = tokenizer.Tokenizer.SplitMode.C

    @classmethod
    def create_df(cls):
        cls.df = pd.DataFrame(columns=['Token', 'Reading', 'Dict. form', 'POS', 'Line', 'Song ID'])

    @classmethod
    def tokenize_phrase(cls, phrase, line_no, song_id):
        phrase = re.sub(r' |\n|\u3000|「|」……', '', phrase)
        phrase_tokens = [m.surface() for m in cls.lyr_tokenizer.tokenize(phrase, cls.mode)]

        for el in phrase_tokens:
            token = cls.lyr_tokenizer.tokenize(el, cls.mode)[0]
            token_info = [token.surface(), token.reading_form(), token.dictionary_form(), 
                          token.part_of_speech(), line_no, song_id]
            cls.df.loc[len(cls.df.index)] = token_info

    @classmethod
    def tokenize_file(cls, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            song_dir = filename.strip('../J-SONGS-DATASET/lyrics\\')
            match_song_id = re.match(r'^\d*', song_dir)
            song_id = match_song_id.group()
            line_no = 1

            for line in file.readlines():
                cls.tokenize_phrase(line, line_no, song_id)
                line_no += 1



pd.options.display.min_rows = 100

# lyrics_tokenizer = LyricsTokenizer()
# lyrics_tokenizer.create_df()
# lyrics_tokenizer.tokenize_file(txt_filename)
# display(lyrics_tokenizer.df)



