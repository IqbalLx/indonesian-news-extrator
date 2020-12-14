import string
import re


def clean_whitespaces(text):
    """A cheap generator to cLean whitespaces in large string
    Args:
        text (str): Can be news title or news body
    Yields:
        [str]: A filtered char, a clean char from the input string
    """
    length = len(text)
    i = 0
    prev_char = None
    while i < length:
        curr_char = text[i]
        return_char = curr_char if curr_char not in string.whitespace else ' '
        
        if not (prev_char == ' ' and return_char == ' '):
            yield return_char

        prev_char = return_char
        i+= 1


def clean_unicode(text):
    """A function to clean unsee unicode character like \\u2xxx
    Args:
        text (str): Can be news title or news body
    Returns:
        [str]: A unicode-free string
    """
    clean_text = text.encode('ascii', errors='ignore').strip().decode('ascii')
    return clean_text


def clean_html(text):
    """A function to remove HTML tag
    Args:
        text (str):  Can be news title or news body
    Returns:
        [str]: A HTML-free string
    """
    cleanr = re.compile('<.*?>')
    clean_text = re.sub(cleanr, '', text)
    return clean_text


def clean_all(text):
    """A function to call both unicode cleaner and
    whitespace cleaner at once, because this two
    condition is the most likely to appear
    Args:
        text (str):  Can be news title or news body
    Returns:
        [str]: A unicode-and-whitespaces-free string
    """
    # anticipate Null values in columns that will be cleaned
    if text is not None and type(text) is not float:
        text = ''.join(text)
        no_ucode = clean_unicode(text)
        no_space = ''.join(clean_whitespaces(no_ucode.strip()))
        text = no_space.strip()

    return text


if __name__ == '__main__':
    # demo purpose
    text = "  Hello,  Iqbal!   \u2100 https://iqbal.com/main  tes. "
    print(f"Before: {text}")
    print(f"After: '{clean_all(text)}'")