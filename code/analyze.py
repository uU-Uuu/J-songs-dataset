import pandas as pd
from IPython.display import display

from matplotlib import pyplot as plt

from handle_particles import string2tuple_pos


def get_pos(line):
    return string2tuple_pos(line)[0]

def str2tuple_pitch(src_line):
    return tuple(src_line.split(','))
    




if __name__ == "__main__": 

    df = pd.read_csv('Data/Data_handled.csv', encoding='utf-8')
    # display(df)

    df_pos_pitch = pd.DataFrame(columns=['POS', 'Pitch accent'])

    for ind, row in df.iterrows():
        if isinstance(row['Pitch accent'], str): # ignore nan
            for el in str2tuple_pitch(row['Pitch accent']):
                df_pos_pitch.loc[-1] = [get_pos(row['POS']), el]
                df_pos_pitch.index += 1
                df_pos_pitch = df_pos_pitch.sort_index()


    # display(df_pos_pitch.to_string())


    result_df = df_pos_pitch.groupby('POS')['Pitch accent'].value_counts().unstack(fill_value=0)
    # print(result_df.to_string())

    df_pos_pitch_06 = result_df[list(filter(lambda x: len(x) == 1, result_df.columns))]
    # print(df_pos_pitch_06.to_string())

    df_pos_pitch_not_06 = result_df[list(filter(lambda x: len(x) != 1, result_df.columns))]
    df_pos_pitch_not_06 = df_pos_pitch_not_06.loc[(df_pos_pitch_not_06!=0).any(axis=1)]
    # print(df_pos_pitch_not_06.to_string())

    plt.rcParams['font.family'] = 'MS Gothic'
    df_pos_pitch_06.plot.bar(stacked=True, figsize=(7,7), colormap='plasma')

    plt.show()


    df_pos_pitch.to_csv('Data/POS_pitch.csv')
    df_pos_pitch_06.to_csv('Data/POS_pitch_06.csv')
    df_pos_pitch_not_06.to_csv('Data/POS_pitch_not_06.csv')