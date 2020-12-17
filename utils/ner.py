import requests
import json

def extract(text):
    with open("creds.json", "r") as creds:
        creds = json.load(creds)
    
    headers = {
        **creds,
        'Content-Type': 'application/json'
    }

    data = {
        "version": "v2",
        "text": text
    }

    repsonse = requests.post("https://api.prosa.ai/v1/entities",\
                                headers=headers, data=json.dumps(data))
    entities = repsonse.json().get("entities")

    return entities


def postpro(entities):
    selected_type = ["ORG", "PER"]
    date_type = "DTE"

    used_name = set()

    qualified_entities = []
    date_entities = []
    for entity in entities:
        entity_type = entity.get("type")
        entity_name = entity.get("name")
        if entity_type in selected_type:
            if entity_name not in used_name:
                qualified_entities.append(entity)
                
        elif entity_type == date_type:
            if entity_name not in used_name:
                date_entities.append(entity)
        
        used_name.add(entity_name)

    return qualified_entities, date_entities


def to_xml_dataset(text, entities):
    pass

def to_spacy_dataset(text, entities):
    """
    TRAIN_DATA = [
        (
            "<text>",
            {
                "entities": [
                (<start>, <end>, <label), 
                (<start>, <end>, <label), 
                ...
                ]
            }
        ),
        ...
    ]
    """

    entities_reformat = []
    for entity in entities:
        start = entity.get("begin_offset")
        end = start + entity.get("length")
        label = entity.get("type")

        entities_reformat.append((start, end, label))
    
    train_data = (
        text,
        {
            "entities": entities_reformat
        }
    )


    return train_data

