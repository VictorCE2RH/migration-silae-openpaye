import json
from opapi import api_map
from datetime import datetime

JSON = dict[str, any]
NumToJson = dict[str, JSON]


# Encoder : Convertir un objet Python en JSON
def objectEncoderJson(objet):
    try:
        # Utilise json.dumps pour convertir un objet en JSON
        return json.dumps(
            objet, default=lambda o: o.__dict__, ensure_ascii=False, indent=4
        )
    except TypeError as e:
        print(f"Erreur lors de l'encodage en JSON: {e}")
        return None

def formatJson(data: str | dict, spaces: int = 4):
    """
    Format un json (string ou dict) de sorte à visualiser plus facilement les élémentsq
    """
    if type(data) is str:
        dataStr = json.loads(data)
        return json.dumps(dataStr, indent=spaces)
    return json.dumps(data, indent=spaces)

def saveJsonData(name: str, dataJson: any):
    data_repo = ".\\data"
    jsonFile = f"{data_repo}\\{name}.json"
    with open(jsonFile, "w") as fp:
        json.dump(dataJson, fp, indent=4)

def saveLogAction(type_action: str, codes: JSON):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fileName = f"export_{api_map[type_action]}_{timestamp}"
    if len(codes) > 0:
        saveJsonData(fileName, codes)
