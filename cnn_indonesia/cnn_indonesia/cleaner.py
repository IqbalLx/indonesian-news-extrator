import string
import re

special = "\u00a0\u2028"

def remove_punc(text):
    length = len(text)
    i = 0
    prev_char = None
    while i < length:
        curr_char = text[i]
        return_char = curr_char if curr_char not in string.punctuation+special else ' '
        
        if not (prev_char == ' ' and return_char == ' '):
            yield return_char.lower()

        prev_char = return_char
        i+= 1

def clean_punc(text):
    clean_text = ''.join(remove_punc(text.strip()))
    return clean_text

def clean_html(text):
  cleanr = re.compile('<.*?>')
  clean_text = re.sub(cleanr, '', text)
  return clean_text

def clean_all(text):
    no_html = clean_html(text)
    no_punc = clean_punc(no_html)
    return no_punc

if __name__ == '__main__':
    # demo purpose
    text = "  Hello,  Iqbal!   https://iqbal.com/main  tes. "
    print(f"Before: {text}")
    print(f"After: {clean_punc(text)}")