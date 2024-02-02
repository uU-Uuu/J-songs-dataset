import pandas as pd
from IPython.display import display

from handle_particles import string2tuple


def get_pos(line):
    return string2tuple(line)[0]

df = pd.read_csv('Data.csv', encoding='utf-8')
# display(df)


df_pos_pitch = pd.DataFrame().assign(POS=df['POS'].apply(get_pos), Pitch_accent=df['Pitch accent'])
# display(df_pos_pitch.to_string())


def count_patterns(series):
    pattern_counts = series.value_counts()
    return pattern_counts

# Apply the custom function to each group of POS
result_df = df_pos_pitch.groupby('POS')['Pitch_accent'].apply(count_patterns).unstack(fill_value=0)

# df_pos_pitch_groups = df_pos_pitch.groupby('POS', 'Pitch_accent')['Pitch_accent'].count()
print(result_df.to_string())
