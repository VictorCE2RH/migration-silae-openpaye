import json
#TODO: Json validator 
class OPDossier:
    def __init__(self, fromJson):
        self.id = fromJson.get("id")
        self.code = fromJson.get("code")
        self.siret = fromJson.get("siret")
        self.nom_dossier = fromJson.get("nom_dossier")
        self.adresse_email = fromJson.get("adresse_email")
        self.telephone = fromJson.get("telephone")
        self.nom_contact = fromJson.get("nom_contact")
        self.qualite = fromJson.get("qualite")
        self.annee = fromJson.get("annee")
    
    def toJson(self):
        return vars(self)