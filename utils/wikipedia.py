import requests
import time

SEARCH_URL = "https://id.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={0}&limit=1"
SNIPPET_URL = "https://id.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&pageids={0}"
ORIGINAL_URL = "https://id.wikipedia.org/?curid={0}"
DATE_URL = "https://id.wikipedia.org/wiki/{0}"


def get_match(keyword):
    init = time.time()
    response = requests.get(SEARCH_URL.format(keyword)).json()
    result = response.get("query")
    final = time.time() - init

    search_result = result.get("search")
    match_id = None
    if search_result:
        match_id = search_result[0].get("pageid")
    
    metadata = {
        "total": result.get("searchinfo").get("totalhits"),
        "time": round(final, 2),
        "match_id": match_id
    }
    
    return metadata


def get_snippet(match_id):
    response = requests.get(SNIPPET_URL.format(match_id)).json()
    response = response.get("query").get("pages").get(str(match_id))

    return_data = {
        "title": response.get("title"),
        "content": response.get("extract"),
        "url": ORIGINAL_URL.format(match_id)
    }

    return return_data


def get_date(date):
    return DATE_URL.format(date.replace(' ', '_'))

    