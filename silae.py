import requests
from etablissement import *

# URLs des APIs
api_silae = "https://payroll-api.silae.fr/payroll"
api_E2RH = "http://127.0.0.1:8080"
URL_DOSSIER = api_E2RH + "/dossiers"


def getDomainHeader(domain: str):
    return {"domain": domain}


class Dossier:
    numero: str
    raisonSociale: str
    siret: str

    def __init__(self, fromJson):
        try:
            self.numero = fromJson.get("numero")
            self.siret = fromJson.get("siret")
            self.raisonSociale = fromJson.get("raisonSociale")
        except Exception as e:
            print(f"Dossier Creation from json not possible : {e}")


NumToDossierDict = dict[str, Dossier]
NumToEtablissements = dict[str, list[Etablissment]]
NumContactDict = dict[str, dict[str, str]]


def _getDossiersList(headers):
    try:
        response = requests.get(URL_DOSSIER, headers=headers)
        if response.status_code == 200:
            print("Données récupérées avec succès de l'API Silae.")
            dossiersJson = response.json().get("data", [])
            dossiers = []
            for doss in dossiersJson:
                dossiers.append(Dossier(doss))
            return dossiers
        else:
            respJson = response.json()
            print(
                f"Erreur lors de la récupération des données: {respJson.get("errors")}"
            )
            return None
    except Exception as e:
        print(f"Exception lors de la récupération des données: {e.args[0]}")
        return None

def filtreDossiers(dossiers):
    filteredList: list[Dossier] = []
    for dossier in dossiers:
        if dossier.numero.startswith("99"):
            print(f"Dossier retiré : {dossier.numero}")
            continue
        filteredList.append(dossier)

    return filteredList

def _getContactFromNum(numero, headers):
    try:
        response = requests.get(
            f"http://localhost:8080/dossiers/{numero}/collab", headers=headers
        )
        if response.status_code == 200:
            silae_data = response.json().get("data")
            contact = silae_data.get("listeUtilisateursDossierPaie")
            if contact:
                print(
                    f"Numero : {numero}  collab : {contact.get("prenom")} {contact.get("nom")}"
                )
                if contact:
                    return contact
                else:
                    print("Aucun contact trouvé pour ce dossier.")
                    return None
        else:
            print(
                f"Erreur lors de la récupération des contacts: {response.status_code}"
            )
            return None

    except Exception as e:
        print(f"Exception lors de la récupération des contacts: {e}")
        return None

def getDossier(domain: str) -> NumToDossierDict:
    silae_data = _getDossiersList(getDomainHeader(domain))
    dossiers = filtreDossiers(silae_data)
    dossierMap: NumToDossierDict = {}
    if not dossiers:
        print("No folders Found (filtered)")
        exit(1)

    for dossier in dossiers:
        dossierMap[dossier.numero] = dossier

    return dossierMap

def getInfosEtablissements(domain: str, dossiersMap: NumToDossierDict, contactMap: NumContactDict):
    print(f"Export des informations d'etablissement de chaque dossier")
    for numero, dossier in dossiersMap.items():
        url = f"{api_E2RH}/dossiers/{numero}/etablissements"
        try:
            response = requests.get(url, headers=getDomainHeader(domain))
            if response.status_code == 200:
                etabJson = response.json().get("data")
                print(
                    f"Dossier : {dossier.numero}, {len(etabJson)} etablissements récupérés"
                )
                return etabJson
            else:
                print(
                    f"Dossier : {dossier.numero} Erreur récupération établissement {str(response)}"
                )
        except Exception as e:
            print(f"getInfosEtablissements : exception raised {e}")



def getEtablissementExtrasInfos(domain: str, dossiersMap: NumToDossierDict, contactMap: NumContactDict):
    print(f"Export des informations d'etablissement de chaque dossier")
    for numero, dossier in dossiersMap.items():
        url = f"{api_E2RH}/dossiers/{numero}/etablissements"
        try:
            response = requests.get(url, headers=getDomainHeader(domain))
            if response.status_code == 200:
                etabJson = response.json().get("data")
                print(
                    f"Dossier : {dossier.numero}, {len(etabJson)} etablissements récupérés"
                )
                contact = contactMap[numero]
                NumToEtablissements[numero] = Etablissment(None, etabJson.get("nomInterne"),contact.get("Raison sociale"),etabJson.get("etablissementPrincipal"),etabJson.get("siret"),Adresse(etabJson.get("adresse_postale"),"","",contact.get("Code postal"),contact.get("Ville"),"","","FR"),"","","",contact.get("Code NAF"),"",)
                return etabJson
            else:
                print(
                    f"Dossier : {dossier.numero} Erreur récupération établissement {str(response)}"
                )
        except Exception as e:
            print(f"getInfosEtablissements : exception raised {e}")
