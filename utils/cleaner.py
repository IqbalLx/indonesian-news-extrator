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
        return_char = curr_char if curr_char not in string.whitespace else " "

        if not (prev_char == " " and return_char == " "):
            yield return_char

        prev_char = return_char
        i += 1


def clean_unicode(text):
    """A function to clean unsee unicode character like \\u2xxx
    Args:
        text (str): Can be news title or news body
    Returns:
        [str]: A unicode-free string
    """
    clean_text = text.encode("ascii", errors="replace").strip().decode("ascii")
    clean_text = clean_text.replace("?", ' ')
    return clean_text


def clean_html(text):
    """A function to remove HTML tag
    Args:
        text (str):  Can be news title or news body
    Returns:
        [str]: A HTML-free string
    """
    cleanr = re.compile("<.*?>")
    clean_text = re.sub(cleanr, "", text)
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
        text = "".join(text)
        no_ucode = clean_unicode(text)
        no_space = "".join(clean_whitespaces(no_ucode.strip()))
        text = no_space.strip()

    return text


def extract_date(raw_dates):
    exp = r"\b(?:(?:3[01]|[12][0-9]|0?[1-9])[/.-](?:1[0-2]|0?[1-9])[/.-][0-9]{4}|(?:3[01]|[12][0-9]|0?[1-9])-(?:1[0-2]|0?[1-9])-[0-9]{4}|(?:3[01]|[12][0-9]|0?[1-9])[\t ]+(?:Jan|Januari|Feb|Februari|Mar|Maret|Apr|April|Mei|Mei|Jun|Juni|Jul|Juli|Aug|Agustus|Sep|September|Oct|Oktober|Nov|November|Dec|Desember)|(?:2[0-3]|[01]?[0-9])[\t ]+(?:Jan|January|Feb|February|Mar|March|Apr|April|May|May|Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|Nov|November|Dec|December)|(?:3[01]|[12][0-9]|0?[1-9])[/.-](?:1[0-2]|0?[1-9]))\b"
    
    extracted_dates = []
    for raw_date in raw_dates:
        extracted_date = re.findall(exp, raw_date)
        if extracted_date:
            extracted_date = extracted_date[0]
            extracted_dates.append(clean_date(extracted_date))
    
    return extracted_dates


def clean_date(extracted_date):
    MONTH = {
        '1': 'Januari',
        '2': 'Februari',
        '3': 'Maret',
        '4': 'April',
        '5': 'Mei',
        '6': 'Juni',
        '7': 'Juli',
        '8': 'Agustus',
        '9': 'September',
        '10': 'Oktober',
        '11': 'November',
        '12': 'Desember'
    }

    splitted_date = extracted_date.split(' ')
    if len(splitted_date) == 2:
        return f"{splitted_date[0]} {splitted_date[1]}"
    else:
        splitted_date = extracted_date.split("/")
        return f"{splitted_date[0]} {MONTH.get(splitted_date[1])}"


def clean_dataset(text):
    unalloweds = ['"', "'"]
    for unallowed in unalloweds:
        text = text.replace(unallowed, '')
    return text


if __name__ == "__main__":
    # demo purpose
    text = "  Hello,  Iqbal!   \u2100 https://iqbal.com/main  tes. "
    print(f"Before: {text}")
    print(f"After: '{clean_all(text)}'")