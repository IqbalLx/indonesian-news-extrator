from news_parser import CNNParser, CNBCParser
import ner
import wikipedia as wiki
from cleaner import extract_date


cnn_url = "https://www.cnnindonesia.com/nasional/20201214083527-32-581674/fadli-zon-siap-jamin-penangguhan-penahanan-rizieq-shihab"
cnbc_url = "https://www.cnbcindonesia.com/news/20201215174238-4-209332/idi-217-dokter-146-perawat-meninggal-akibat-covid-19"

# original_news = CNNParser(url=cnn_url).parse()
original_news = CNBCParser(url=cnbc_url).parse()

print(original_news)

entities, date_entities = ner.extract(original_news)

print("\nMentioned Date in Article:\n")
print(f"Raw date(s) found: {date_entities}")

extracted_dates = extract_date(date_entities)
for date in extracted_dates:
    print(f"{date} - Find out what happen on this date: {wiki.get_date(date)}")


print("\nMentioned Entities in Article:\n")
for entity in entities:
    entity_name = entity.get("name")
    entity_type = entity.get("type")

    print(f"Searching {entity_name} on wikipedia id. Detected type: {entity_type}")
    entity_metadata = wiki.get_match(entity_name)
    print(f"About {entity_metadata.get('total')} results ({entity_metadata.get('time')} seconds)")

    match_id = entity_metadata.get("match_id")
    if match_id is not None:
        entity_info = wiki.get_snippet(match_id)
        print(f"{entity_info.get('title')} - {entity_info.get('url')}")
        print(entity_info.get("content"))
    else:
        print(f"No info from wikipedia. Try: https://www.google.com/search?q={entity_name.replace(' ', '+')}")

    print("\n")

