import re
import sys

CYRILLIC_TO_LATIN = {
    'йе': 'e', 'ЙЕ': 'E', 'Йе': 'E',
    'а': 'a', 'А': 'A',
    'ә': 'á', 'Ә': 'Á',
    'б': 'b', 'Б': 'B',
    'в': 'v', 'В': 'V',
    'г': 'g', 'Г': 'G',
    'д': 'd', 'Д': 'D',
    'е': 'e', 'Е': 'E',
    'ё': 'yo', 'Ё': 'Yo',
    'ж': 'j', 'Ж': 'J',
    'з': 'z', 'З': 'Z',
    'и': 'i', 'И': 'I',
    'й': 'y', 'Й': 'Y',
    'к': 'k', 'К': 'K',
    'л': 'l', 'Л': 'L',
    'м': 'm', 'М': 'M',
    'н': 'n', 'Н': 'N',
    'ң': 'ń', 'Ң': 'Ń',
    'о': 'o', 'О': 'O',
    'ө': 'ó', 'Ө': 'Ó',
    'п': 'p', 'П': 'P',
    'р': 'r', 'Р': 'R',
    'с': 's', 'С': 'S',
    'т': 't', 'Т': 'T',
    'у': 'u', 'У': 'U',
    'ү': 'ú', 'Ү': 'Ú',
    'ф': 'f', 'Ф': 'F',
    'х': 'x', 'Х': 'X',
    'ц': 'c', 'Ц': 'C',
    'ч': 'ch', 'Ч': 'Ch',
    'ш': 'sh', 'Ш': 'Sh',
    'щ': 'sh', 'Щ': 'Sh',
    'ъ': '', 'Ъ': '',
    'ь': '', 'Ь': '',
    'э': 'e', 'Э': 'E',
    'ю': 'yu', 'Ю': 'Yu',
    'я': 'ya', 'Я': 'Ya',
    'ў': 'w', 'Ў': 'W',
    'қ': 'q', 'Қ': 'Q',
    'ғ': 'ǵ', 'Ғ': 'Ǵ',
    'ҳ': 'h', 'Ҳ': 'H',
    'ы': 'ı', 'Ы': 'Í',
}

OLD_LATIN_TO_LATIN_2016 = {
    "A'": 'Á', "a'": 'á',
    'A‘': 'Á', 'a‘': 'á',

    "G’": 'Ǵ', "g’": 'ǵ',
    'G`': 'Ǵ', 'g`': 'ǵ',
    "G‘": 'Ǵ', "g‘": 'ǵ',
    'G’': 'Ǵ', 'g’': 'ǵ',
    "G'": 'Ǵ', "g'": 'ǵ',

    'Ğ': 'Ǵ', 'ğ': 'ǵ',
    'Ġ': 'Ǵ', 'ġ': 'ǵ',

    # 'I': 'Í', 'ı': 'ı',
    'İ': 'I', 'i':'i',

    "N’": 'Ń', "n’": 'ń',
    'N`': 'Ń', 'n`': 'ń',
    "N‘": 'Ń', "n‘": 'ń',
    'N’': 'Ń', 'n’': 'ń',
    "N'": 'Ń', "n'": 'ń',

    "O’": 'Ó', "o’": 'ó',
    'O`': 'Ó', 'o`': 'ó',
    "O‘": 'Ó', "o‘": 'ó',
    'O’': 'Ó', 'o’': 'ó',
    "O'": 'Ó', "o'": 'ó',
    
    "U’": 'Ú', "u’": 'ú',
    'U`': 'Ú', 'u`': 'ú',
    "U‘": 'Ú', "u‘": 'ú',
    'U’': 'Ú', 'u’': 'ú',
    "U'": 'Ú', "u'": 'ú',
    
    'TS': 'C', 'Ts':'C', 'ts': 'c',

    "I’": 'Í', "i’": 'ı',
    'I`': 'Í', 'i`': 'ı',
    "I‘": 'Í', "i‘": 'ı',
    'I’': 'Í', 'i’': 'ı',
    "I'": 'Í', "i'": 'ı',
    
    # 'YE': 'E', 'ye': 'e', 'Ye': 'E',
    "WO’": 'Ó', "wo’": 'ó', "Wo’": 'Ó',
    'WO`': 'Ó', 'wo`': 'ó', 'Wo`': 'Ó',
    "WO‘": 'Ó', "wo‘": 'ó', "Wo‘": 'Ó',
    'WO’': 'Ó', 'wo’': 'ó', 'Wo’': 'Ó',
    "WO'": 'Ó', "wo'": 'ó', "Wo'": 'Ó',

    'WO': 'O', 'wo': 'o', 'Wo': 'O',

    'Ő': 'Ó', 'ő':'ó',
    'Ō': 'Ó', 'ō':'ó',
    'Õ': 'Ó', 'õ':'ó',
}

DOUBLE_LETTER_CYRILLIC = {'Ё', 'Ч', 'Ш', 'Щ', 'Ю', 'Я'}

def to_latin(text):
    text = re.sub(r'ь([ио])', r'y\1', text)
    text = re.sub(r'Ь([ИО])', r'Y\1', text)
    
    result = []
    i = 0
    while i < len(text):
        if i < len(text) - 1 and text[i] == 'ъ' and text[i + 1] in 'еЕ':
            result.append('y' + CYRILLIC_TO_LATIN.get(text[i + 1], text[i + 1]))
            i += 2
        elif i < len(text) - 1 and text[i] == 'Ъ' and text[i + 1] in 'еЕ':
            result.append('Y' + CYRILLIC_TO_LATIN.get(text[i + 1], text[i + 1]))
            i += 2
        else:
            cyrillic_char = text[i]
            if cyrillic_char in CYRILLIC_TO_LATIN:
                latin_chars = CYRILLIC_TO_LATIN[cyrillic_char]
                if cyrillic_char in DOUBLE_LETTER_CYRILLIC:
                    if i < len(text) - 1 and text[i + 1].isupper():
                        latin_chars = latin_chars.upper()
                    elif i == len(text) - 1 and text[i - 1].isupper():
                        latin_chars = latin_chars.upper()
                    
                result.append(latin_chars)
            else:
                result.append(cyrillic_char)
            i += 1
    
    text = ''.join(result)

    # Transliterate from Latin (1996) to Latin (2016)
    text = re.sub(
        r'(%s)' % '|'.join(OLD_LATIN_TO_LATIN_2016.keys()),
        lambda x: OLD_LATIN_TO_LATIN_2016[x.group(1)],
        text,
        flags=re.U
    )

    # Handle 'ye' and 'Ye' separately
    text = re.sub(r'([Ъъ])([Ee])', lambda x: 'y' + x.group(2), text)
    text = re.sub(r'([Йй][Ее])', lambda x: 'e', text)

    return text