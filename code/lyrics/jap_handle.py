from unicodedata import normalize

def ignore_length_small(text):
    """
    IGNORING SMALL MORA'S LENGTH
    """
    normalized_text = normalize('NFC', text)
    len_w = 0
    small = ['ぁ', 'ぃ', 'ぅ','ぇ','ぉ','っ',
                  'ゃ','ゅ','ょ','ゎ',
                  'ァ','ィ','ゥ','ェ','ォ','ッ',
                  'ャ','ュ','ョ','ヮ','ヵ','ヶ']

    for mora in normalized_text:
        if mora not in small:
            len_w += 1
    
    return len_w
