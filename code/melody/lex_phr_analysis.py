import pandas as pd
import numpy as np
import statistics
from IPython.display import display


df = pd.read_csv('./data/melody/lex_phr.csv')

unvoiced_df = pd.DataFrame(columns=[
    'Mora', 'Duration', 'Pitch Accent', 
    'Mean', 'Mode', 'Median', 'Line Duration',
    'Indx', 'Song ID'])


def analyze_unvoiced(df, unvoiced_df, mode=0):
    for indx, row in df.iterrows():
        for m_indx, mora in enumerate(row[f'Pitch Accent {mode}'].split()):
            if '.' in mora:
                row_durs = np.array(row['Duration Calc.'].split(), dtype=float)
                unvoiced_df.loc[len(unvoiced_df.index)] = [
                    row['Reading'][m_indx],
                    row_durs[m_indx],
                    mora,
                    np.mean(row_durs),
                    np.median(row_durs),
                    statistics.mode(tuple(row_durs)),
                    row['Duration Calc.'],
                    m_indx,
                    row['Song ID'],
                ]
            
analyze_unvoiced(df, unvoiced_df)
display(unvoiced_df)
