import json


# Encoder : Convertir un objet Python en JSON
def encoderJson(objet):
    try:
        # Utilise json.dumps pour convertir un objet en JSON
        return json.dumps(
            objet, default=lambda o: o.__dict__, ensure_ascii=False, indent=4
        )
    except TypeError as e:
        print(f"Erreur lors de l'encodage en JSON: {e}")
        return None
