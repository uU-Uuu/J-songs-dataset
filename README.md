# J-songs-dataset  <img src='https://img.shields.io/badge/Python-3.8-blue?style=for-the-badge&logo=Python&logoColor=%23bae1ff&label=Python&labelColor=%232a4d69&color=%23457399'/>


## Overview
The analysis of Japanese pitch accent patterns in songs


## Data Description
- **Variables**: Token, Reading form, Dictionary form, Part of speech, Line no., Song ID, Pitch accent
- **Size**: 31 songs, 3530 entries
- **Genres covered**: Enka

## Data Format
.csv

## Data Source
- ピアノ伴奏シリーズ　ザ・歌伴　昭和の演歌名曲編　昭和４５〜６３年
- various Internet sources
- the pitch accent notation provided by Uros O. through his free database

## Data Examples
```
  Token,Reading,Dict. form,POS,Line,Song ID,Pitch accent
  夢,ユメ,夢,"('名詞', '普通名詞', '一般', '*', '*', '*')",13,9,"1,0"
  の,ノ,の,"('助詞', '格助詞', '*', '*', '*', '*')",13,9,"0,1"
  中,ナカ,中,"('名詞', '普通名詞', '副詞可能', '*', '*', '*')",13,9,1
```

## Data Visualisation
- stacked histogram: the proportion of pitch accent patterns within parts of speech
- lollipop chart: the sequence of pitch accents of a particular line (without regard to context)


## External Libraries and Dependencies
[Sudachipy](https://github.com/WorksApplications/sudachi.rs) - a Japanese morphological analyzer

[Kanjium](https://github.com/mifunetoshiro/kanjium) - the free database provided by Uros O. for pitch accent notation, verb particle data, phonetics, and homonyms.


