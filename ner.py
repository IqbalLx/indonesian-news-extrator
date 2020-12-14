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

    repsonse = requests.request("POST", "https://api.prosa.ai/v1/entities",\
                                    headers=headers, data=json.dumps(data))
    entities = repsonse.json().get("entities")

    return postpro(entities)


def postpro(entities):
    selected_type = ["ORG", "PER"]

    used_name = set()
    qualified_entity = []
    for entity in entities:
        if entity.get("type") in selected_type:
            name = entity.get("name")
            if name not in used_name:
                qualified_entity.append(entity)
                used_name.add(name)
                

    return qualified_entity

