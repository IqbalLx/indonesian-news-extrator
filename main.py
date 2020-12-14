from news_parser import CNNParser
import ner
import wikipedia as wiki

url = "https://www.cnnindonesia.com/nasional/20201118220413-12-571620/kerumunan-rizieq-di-bogor-diperiksa-tim-gabungan-polri"

original_news = CNNParser(url=url).parse()
print(original_news)

entities = ner.extract(original_news)
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

