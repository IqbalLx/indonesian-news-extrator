import json
from tqdm import tqdm
import argparse


from utils.news_parser import CNNParser, CNBCParser
import utils.ner as ner
from utils.cleaner import clean_dataset


SCRAPPER = {
    "cnn": CNNParser,
    "cnbc": CNBCParser
}

def get_flags():
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--date', required=True, help="Date format: YYYY-MM-DD")
    ap.add_argument('-s', '--site', required=True, help=f"Select between {SCRAPPER.keys()}")
    ap.add_argument('-p', '--pages', default=1, help='Total pages to scrape')

    return ap.parse_args()


def main(flags):
    raw_datas = []
    spacy_datasets = []

    parser = SCRAPPER.get(flags.site)(date=flags.date)
    articles = parser.extract_articles_link(page_num=flags.pages)
    for article in tqdm(articles):
        content = parser.parse(article).clean()

        # store raw
        raw_entities = ner.extract(content)
        raw_data = {
            "text": content,
            "entities": raw_entities
        }
        raw_datas.append(raw_data)

        # store spacy dataset
        filtered_entities = ner.postpro(raw_entities)
        filtered_entities = filtered_entities[0] + filtered_entities[1]

        spacy_dataset = ner.to_spacy_dataset(content, filtered_entities)
        spacy_datasets.append(spacy_dataset)
    
    # save all
    filedate = flags.date.replace('-', '_')
    with open(f"ner_training/dataset/raw/raw_{filedate}.json", "w") as raw_data:
        raw_data.write(json.dumps(raw_datas))
    
    with open(f"ner_training/dataset/spacy/datasets_{filedate}.json", "w") as spacy_data:
        spacy_data.write(json.dumps(spacy_datasets))


if __name__ == "__main__":
    flags = get_flags()
    main(flags)






        
        



# cnn_url = "https://www.cnnindonesia.com/nasional/20201214083527-32-581674/fadli-zon-siap-jamin-penangguhan-penahanan-rizieq-shihab"
# cnbc_url = "https://www.cnbcindonesia.com/news/20201215174238-4-209332/idi-217-dokter-146-perawat-meninggal-akibat-covid-19"

# original_news = CNBCParser(url=cnbc_url).parse()
# print(original_news)

# text = clean_dataset(original_news)
# entities = ner.extract(original_news)
# entities, _ = ner.postpro(entities)

# print(entities)

# train_data = ner.to_spacy_dataset(text, entities)

# train_datas = [train_data]
# with open("ner_training/dataset/dataset.json", "w") as dataset:
#     dataset.write(json.dumps(train_datas, indent=4))