def get_pitch_accent_dict():
    pitch_accent_dict = dict()
    with open('accents.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            pitch_accent_dict.update({tuple(line.split()[0:-1]): line.split()[-1]})
    return pitch_accent_dict


if __name__ == "__main__":
    for key, value in get_pitch_accent_dict().items():
        print(f'{key}    ---    {value}')