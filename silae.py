from datetime import datetime,date,timedelta
import requests
import utils
from etablissement import *

# URLs des APIs
api_silae = "https://payroll-api.silae.fr/payroll"
api_E2RH = "http://127.0.0.1:8080"
URL_DOSSIER = api_E2RH + "/dossiers"


def getDomainHeader(domain: str):
    return {"domain": domain}

def ping():
    response = requests.get(f"{api_E2RH}/ping")
    if response.status_code != 200:
        print(f" Erreur ping serveur {api_E2RH} : {response.status_code} {response.text}")
    else:
        print("Connecté à l'API E2RH !")
        return True
    
    return False

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

def _getDossiersList(headers):
    try:
        response = requests.get(URL_DOSSIER, headers=headers)
        if response.status_code == 200:
            ("liste dossiers récupérées avec succès depuis l'API Silae.")
            dossiersJson = response.json().get("data", [])
            dossiers = []
            for doss in dossiersJson:
                dossiers.append(Dossier(doss))
            return dossiers
        else:
            respJson = response.json()
            print(f"Erreur lors de la récupération des données: {respJson.get("errors")}")
            return None
    except Exception as e:
        print(f"Exception lors de la récupération des données: {e.args[0]}")
        return None

def filtreDossiers(dossiers):
    filteredList: list[Dossier] = []
    i = 0
    for dossier in dossiers:
        if dossier.numero.startswith("99"):
            i += 1
            continue
        filteredList.append(dossier)
    return filteredList

def _getContactFromNum(numero, headers):
    try:
        response = requests.get(
            f"{api_E2RH}/dossiers/{numero}/collab", headers=headers
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

def getDossiers(domain: str) -> dict[str, Dossier]:
    silae_data = _getDossiersList(getDomainHeader(domain))
    dossiers = filtreDossiers(silae_data)
    dossierMap: dict[str, Dossier] = {}
    if not dossiers:
        print("No folders Found (filtered)")
        exit(1)

    for dossier in dossiers:
        dossierMap[dossier.numero] = dossier

    return dossierMap

def getDossiersDetails(domain: str, dossiersMap:dict[str, Dossier]):
    headers = getDomainHeader(domain)
    res = {}
    for numero, _ in dossiersMap.items():
        try:
            url = f"{api_E2RH}/dossiers/{numero}/details"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print("Données récupérées avec succès de l'API Silae.")
                dossiersJson = response.json().get("data", [])
                res[numero] = dossiersJson["reponsesInfosPaie"]
            else:
                respJson = response.json()
                print(
                    f"Erreur lors de la récupération des données: {respJson.get("errors")}"
                )
                return None
        except Exception as e:
            print(f"Exception lors de la récupération des données: {e.args[0]}")
            return None
    return res


def getInfosEtablissements(domain: str, dossiersMap: dict[str, Dossier]):
    print(f"Export des informations d'etablissement de chaque dossier")
    res:dict = {}
    for numero, dossier in dossiersMap.items():
        url = f"{api_E2RH}/dossiers/{numero}/etablissements"
        try:
            response = requests.get(url, headers=getDomainHeader(domain))
            if response.status_code == 200:
                etabJson = response.json().get("data")
                res[numero] = etabJson
            else:
                print(
                    f"Dossier : {dossier.numero} Erreur récupération établissement {response.text}"
                )
        except Exception as e:
            print(f"getInfosEtablissements : exception raised {e}")
    return res

def getEtablissementDetails(domain: str, etabMap: dict):
    print(f"Export des informations d'etablissement de chaque dossier")
    etabDetailsMap = dict()
    for numero, etabs in etabMap.items():
        for etab in etabs['informationsEtablissements']:
            nomInterne = etab["nomInterne"]
            url = f"{api_E2RH}/dossiers/{numero}/etablissements/{nomInterne}/details"
            try:
                response = requests.get(url, headers=getDomainHeader(domain))
                if response.status_code == 200:
                    etabJson = response.json().get("data")
                    print(
                        f"Dossier : {numero} Etablissement {nomInterne}, détails récupérés"
                    )
                    etabDetailsMap[nomInterne] = etabJson["reponsesInfosPaie"]
                else:
                    print(
                        f"Dossier : {numero} Etablissement {nomInterne}, Erreur récupération établissement {response.text}"
                    )
            except Exception as e:
                print(f"{url} : exception raised {e}")

    return etabDetailsMap

def getInfosSalaries(domain: str, codeDict: dict):
    res = dict()
    print(f"Export des informations salariés pour chaque documents")
    for numero, _ in codeDict.items():
        url = f"{api_E2RH}/dossiers/{numero}/salaries"
        try: 
            response = requests.get(url, headers=getDomainHeader(domain))
            if response.status_code == 200:
                respjson = response.json().get("data")
                res[numero] = dict()
                matricules = [matricule["matriculeSalarie"] for matricule in respjson["listeSalariesInformations"]]
                print(f"Dossier {numero} Récupération des détails de {len(matricules)} salariés")
                for mat in matricules:
                    url = f"{api_E2RH}/dossiers/{numero}/salaries/{mat}/details"
                    response = requests.get(url, headers=getDomainHeader(domain))
                    if response.status_code == 200:
                        respjson = response.json().get("data")
                        res[numero][mat] = respjson
                    else:
                        print(response.text)
        except Exception as e:
            print(f"Exception levée : {e}")
    return res

def getInfosEmplois(domain:str,sal_detailsMap: dict):
    res = dict()
    print(f"Export des informations emplois pour chaque documents")
    for numero, salaries in sal_detailsMap.items():
        res[numero] = dict()
        print(f"Dossier {numero} Récupération des détails de {len(salaries)} contrats")
        for matricule, _ in salaries.items():
            url = f"{api_E2RH}/dossiers/{numero}/salaries/{matricule}/emplois"
            try: 
                response = requests.get(url, headers=getDomainHeader(domain))
                if response.status_code == 200:
                    respjson = response.json().get("data")
                    res[numero][matricule] = respjson
                else:
                    print(response.text)

            except Exception as e:
                print(f"Exception levée : {e}")
    return res

def getCumulsContrats(domain:str,codeDict: dict[str,int]):
    res:dict[str,dict[str,str]] = {}
    headers = getDomainHeader(domain)
    headers["Content-Type"] = "application/json"
    for numero, _ in codeDict.items():
        periode = datetime.today()
        url = f"{api_E2RH}/dossiers/{numero}/editions/cumuls"
        DateDebut = f"01/{periode.month-1}/{periode.year}"
        DateFin = f"{periode.month}/{periode.year}"
        try: 
            payload = {
                "code_edition": "EXP OPENPAYE CUMUL",
                "periode_debut": DateDebut,
                "periode_fin": f"01/" + DateFin
            }
            print(f" Cumuls Dossier {numero}, Récupération des données en cours...")
            response = requests.get(url, headers=headers,json=payload)
            if response.status_code == 200 or response.status_code == 201:
                respjson = response.json().get("data")
                res[numero] = {}
                res[numero]["DateReprise"] = DateFin
                res[numero]["Cumul"] = respjson
            else:
                print(response.text)
        except Exception as e:
            print(f"Exception levée : {e}")
    return res 