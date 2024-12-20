from datetime import datetime,date,timedelta
import requests
import logger
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
        logger.log(f" Erreur ping serveur {api_E2RH} : {response.status_code} {response.text}")
    else:
        logger.log("Connecté à l'API E2RH !")
        return True
    
    return False

def silaeGet(url,headers,data=None,params=None) -> tuple[any,int]:
    '''
        Get weither what inside api E2RH 'data' response
        
        returns : json like object containing the response, status_code int
        Exception : Raise an error with the content of 'errors' in response
    '''
    try:    
        response = requests.get(url,headers=headers,data=data,params=params)

        if response.status_code == 200:
            dossiersJson = response.json()["Data"]
            return dossiersJson, 200 
        else:
            try:
                respJson = response.json()
            except:
                return None, response.status_code
            if respJson.get("errors"):
                raise Exception(f"{response.status_code} - {respJson.get("errors",response.text)}")
    except Exception as e:
        logger.error(f" API E2RH: Exception raised : {e} ")
        return (None, 500)
        
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
            logger.log(f"Dossier Creation from json not possible : {e}")

def _getDossiersList(domain):
    dossiers = []
    dossiersJson, _ = silaeGet(URL_DOSSIER, getDomainHeader(domain))
    if not dossiersJson:
        return None

    for doss in dossiersJson:
        dossiers.append(Dossier(doss))
    return dossiers


def getCcnForNums(numeros:list[str],headers):
    url = api_E2RH + "/extras/ccns"
    logger.log(f"url : {url}")
    response = requests.get(url, headers=headers,data=json.dumps(numeros))
    if utils.valid(response.status_code):
        ("liste ccns récupérées avec succès depuis l'API Silae.")
        collectionCCN = json.loads(response.text)
        return collectionCCN["Data"]
    else:
        logger.error(f"Erreur lors de la récupération des données: {response.text}")
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
    url = f"{api_E2RH}/dossiers/{numero}/collab"
    silae_data, _ = silaeGet(url, headers=headers)
    if not silae_data:
        return None
    
    contact = silae_data.get("listeUtilisateursDossierPaie")
    if contact:
        logger.log(f"Numero : {numero}  collab : {contact.get("prenom")} {contact.get("nom")}")
        return contact
    return None
def getDossiers(domain: str) -> dict[str, Dossier]:
    silae_data = _getDossiersList(domain)
    dossiers = filtreDossiers(silae_data)
    dossierMap: dict[str, Dossier] = {}
    if not dossiers:
        logger.log("No folders Found (filtered)")
        exit(1)

    for dossier in dossiers:
        dossierMap[dossier.numero] = dossier

    return dossierMap

def getDossiersDetails(domain: str, dossiersMap:dict[str, Dossier]):
    res = {}
    for numero, _ in dossiersMap.items():
        url = f"{api_E2RH}/dossiers/{numero}/details"
        dossiersJson, _ = silaeGet(url,getDomainHeader(domain))
        if not dossiersJson:
            raise Exception(f"dossier {numero} : Aucun détails Trouvés")
        res[numero] = dossiersJson["reponsesInfosPaie"]
    return res

def getInfosEtablissements(domain: str, dossiersMap: dict[str, Dossier]):
    logger.log(f"Export des etablissements de chaque dossier")
    res:dict = {}
    for numero, dossier in dossiersMap.items():
        url = f"{api_E2RH}/dossiers/{numero}/etablissements"
        try:
            response = requests.get(url, headers=getDomainHeader(domain))
            if response.status_code == 200:
                etabJson = response.json().get("Data")
                res[numero] = etabJson
                logger.log(f"Dossier {numero} Etablissement(s) récupéré(s)")
            else:
                logger.error(f"Dossier : {dossier.numero} Erreur récupération établissement {response.text}")
        except Exception as e:
            logger.error(f"API E2RH : getInfosEtablissements : exception raised {e}")
            raise e
    return res

def getEtablissementDetails(domain: str, etabMap: dict):
    logger.log(f"Export des détails d'etablissement de chaque dossier")
    etabDetailsMap = dict()
    for numero, etabs in etabMap.items():
        etabDetailsMap[numero] = dict()
        i = 1
        for etab in etabs['informationsEtablissements']:
            nomInterne = etab["nomInterne"]
            i += 1
            url = f"{api_E2RH}/dossiers/{numero}/etablissements/{nomInterne}/details"
            try:
                response = requests.get(url, headers=getDomainHeader(domain))
                if response.status_code == 200:
                    etabJson = response.json().get("Data")
                    logger.log(f"Dossier : {numero} Etablissement {nomInterne}, détails récupérés")
                    etabDetailsMap[numero][nomInterne] = etabJson["reponsesInfosPaie"]
                else:
                    logger.log(f"Dossier : {numero} Etablissement {nomInterne}, Erreur récupération établissement {response.text}")
            except Exception as e:
                logger.log(f"{url} : exception raised {e}")

    return etabDetailsMap

def getInfosSalaries(domain: str, codeDict: dict):
    res = dict()
    logger.log(f"Export des informations salariés pour chaque documents")
    for numero, _ in codeDict.items():
        url = f"{api_E2RH}/dossiers/{numero}/salaries"
        try: 
            response = requests.get(url, headers=getDomainHeader(domain))
            if response.status_code == 200:
                respjson = response.json().get("Data")
                res[numero] = dict()
                matricules = [matricule["matriculeSalarie"] for matricule in respjson["listeSalariesInformations"]]
                logger.log(f"Dossier {numero} Récupération des détails de {len(matricules)} salariés")
                for mat in matricules:
                    url = f"{api_E2RH}/dossiers/{numero}/salaries/{mat}/details"
                    response = requests.get(url, headers=getDomainHeader(domain))
                    if response.status_code == 200:
                        respjson = response.json().get("Data")
                        res[numero][mat] = respjson
                    else:
                        logger.log(response.text)
        except Exception as e:
            logger.log(f"Exception levée : {e}")
    return res

def getInfosEmplois(domain:str,sal_DetailsMap: dict):
    res = dict()
    logger.log(f"Export des informations emplois pour chaque documents")
    nbEmplois = 0
    for numero, salaries in sal_DetailsMap.items():
        res[numero] = dict()
        logger.log(f"Dossier {numero} Récupération des détails de {len(salaries)} contrats")
        for matricule, _ in salaries.items():
            url = f"{api_E2RH}/dossiers/{numero}/salaries/{matricule}/emplois"
            try: 
                response = requests.get(url, headers=getDomainHeader(domain))
                if utils.valid(response.status_code):
                    respjson = response.json().get("Data")
                    res[numero][matricule] = respjson
                    nbEmplois += len(respjson)
                else:
                    logger.log(response.text)
            except Exception as e:
                logger.log(f"Exception levée : {e}")
    logger.log(f"Dossier {numero} {nbEmplois} emplois récupérés")
    return res

def getCumulsContrats(domain:str,codesDict: dict[str,int],forceDtReprise:datetime = None):
    res:dict[str,dict[str,str]] = {}
    headers = getDomainHeader(domain)
    headers["Content-Type"] = "application/json"
    # Calcul des dates periode de cumuls (indiquer le mois précédent du 1er au dernier jour)
    periode = datetime.today()
    if datetime.today() and periode.month == 1:
        logger.warning(f"Calcul des cumuls non requis pour Janvier")
    periode = datetime.today().replace(day=1) - timedelta(days=1)
    dtDebStr = periode.replace(day=1).strftime("%d/%m/%Y") # 1er jour mois précedent
    dtFinStr = periode.strftime("%d/%m/%Y") # dernier jour mois précédent 
    dtReprise = periode + timedelta(days=1)
    if forceDtReprise:
        dtReprise = forceDtReprise
    logger.statistic(f"Cumuls : debut {dtDebStr} fin {dtFinStr} reprise {dtReprise.strftime("%d/%m/%Y")}")
    payload = {
        "code_edition": "EXP OPENPAYE CUMUL",
        "periode_debut": dtDebStr,
        "periode_fin": dtFinStr,
    }

    for numero, _ in codesDict.items():
        url = f"{api_E2RH}/dossiers/{numero}/editions/cumuls"
        try: 
            logger.log(f" Cumuls Dossier {numero}, Récupération des données en cours...")
            response = requests.get(url, headers=headers,json=payload)
            if utils.valid(response.status_code):
                respjson = response.json().get("Data")
                res[numero] = {}
                res[numero]["DateReprise"] = dtReprise.strftime("%d/%m/%Y")
                res[numero]["Cumul"] = respjson
            else:
                logger.error(response.text)
        except Exception as e:
            logger.error(f"Exception levée : {e}")
    return res

def getOrganismesList(domain:str, codeDict: dict[str,int]): 
    res:dict[str,list[dict]] = {}
    for numero, _ in codeDict.items():
        headers = getDomainHeader(domain)
        headers["Content-Type"] = "application/json"
        url = f"{api_E2RH}/dossiers/{numero}/organismes"
        try:
            response = requests.get(url, headers=headers)
            if utils.valid(response.status_code):
                items:list = json.loads(response.text)["Data"]["listeOrganismes"]
                res[numero] = []
                if items:
                    for _, item in enumerate(items):
                        if not item["nomInterneEtablissement"] or item["nomInterneEtablissement"] == "":
                            logger.warning(f"dossier {numero} : organisme {item["codeOrganisme"]} n'est pas rattaché à un etablissement")
                            continue
                        res[numero].append(item)
                logger.log(f"Dossier {numero} : {len(items)} organismes récupérés")
            else:
                raise Exception(response.text)
        except Exception as e:
            logger.error(f"Silae get organismes : error {e}")
    return res
    
def getCCNListFromIDCC(idcc:str) -> list[dict]:
    url = f"{api_E2RH}/silae/{idcc}/ccn"
    try:
        response = requests.get(url, headers=getDomainHeader(domain="E2RH"))
        ccnList = response.json().get("Data").get("ccn")
        return ccnList
    except Exception as e:
        logger.error(f"Silae get CCN from IDCC : error {e} {response.status_code}")
    
    return []