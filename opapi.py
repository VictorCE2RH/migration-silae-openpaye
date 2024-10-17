import requests
import env
import utils
from etablissement import Etablissment
from urllib.parse import urlencode
from enum import Enum
from OP_registre import OPDossier

api_openpaye = "https://api.openpaye.co"
URL_DOSSIERS = api_openpaye + "/dossiers"
URL_ETAB = "/v1/FicheSociete/ListeEtablissementsDossierPaie"

from typing import Any, Dict, Optional

class BaseAPI:
    BASE_URL = "https://api.openpaye.co"  # URL de base de ton API

    def __init__(self, resource: str, auth_key: tuple[str,str]):
        self.resource = resource  # Le thème (endpoint) comme "Absences", "Contrats", etc.
        self.headers = {
            "Content-Type": "application/json"
        }
        self.auth = auth_key

    def create(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        url = f"{self.BASE_URL}/{self.resource}"
        response = requests.post(url, auth=self.auth, json=data, headers=self.headers)
        return self._handle_response(response)

    def read(self, item_id: str) -> Optional[Dict[str, Any]]:
        url = f"{self.BASE_URL}/{self.resource}/{item_id}"
        response = requests.get(url, auth=self.auth, headers=self.headers)
        return self._handle_response(response)

    def update(self, item_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        url = f"{self.BASE_URL}/{self.resource}/{item_id}"
        response = requests.put(url, auth=self.auth, json=data, headers=self.headers)
        return self._handle_response(response)

    def delete(self, item_id: str) -> Optional[Dict[str, Any]]:
        url = f"{self.BASE_URL}/{self.resource}/{item_id}"
        response = requests.delete(url, auth=self.auth, headers=self.headers)
        return self._handle_response(response)

    def list(self,params: dict = None) -> Optional[Dict[str, Any]]:
        url = f"{self.BASE_URL}/{self.resource}"
        if params:
            url += "?" + urlencode(params) 
        response = requests.get(url, auth=self.auth, headers=self.headers)
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> Optional[Dict[str, Any]]:
        if response.status_code in [200, 201]:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
        
class AbsencesEP(BaseAPI):
    def __init__(self, auth_key: tuple[str,str]):
        super().__init__("Absences", auth_key)
class BulletinsPaiesEP(BaseAPI):
    def __init__(self, auth_key: tuple[str,str]):
        super().__init__("BulletinsPaies", auth_key)
class ContratsEP(BaseAPI):
    def __init__(self, auth_key: tuple[str,str]):
        super().__init__("Contrats", auth_key)
class ContratSortantEP(BaseAPI):
    def __init__(self, auth_key: tuple[str,str]):
        super().__init__("ContratSortant", auth_key)
class DossiersEP(BaseAPI):
    def __init__(self, auth_key: tuple[str,str]):
        super().__init__("Dossiers", auth_key)
    def list(self) :
        print("liste de tous les dossier")
        page = 0
        params = {"page":page}
        dossiersInfos = super().list(params)
        dossiers = dossiersInfos.get("dossiers")
        total_dossiers = int(dossiersInfos.get("total_count"))
        total_pages = dossiersInfos.get("total_pages")
        while page < total_pages:
            page += 1
            params = {"page":page}
            dossiersInfos = super().list(params)
            dossiers = dossiers + dossiersInfos.get("dossiers")
        if len(dossiers) != total_dossiers:
            raise Exception(f"[List Dossiers] Récupération erronée , dossiers récupérés  : {len(dossiers)} != dossiers stockés :{dossiersInfos.get("total_count")}")
        return dossiers
class EditionsEP(BaseAPI):
    def __init__(self, auth_key: tuple[str,str]):
        super().__init__("Editions", auth_key)
class EtablissementsEP(BaseAPI):
    def __init__(self, auth_key: tuple[str,str]):
        super().__init__("Etablissements", auth_key)
class HeuresSupplementairesEP(BaseAPI):
    def __init__(self, auth_key: tuple[str,str]):
        super().__init__("HeuresSupplementaires", auth_key)
class OptionsEP(BaseAPI):
    def __init__(self, auth_key: tuple[str,str]):
        super().__init__("Options", auth_key)
class PrimesEP(BaseAPI):
    def __init__(self, auth_key: tuple[str,str]):
        super().__init__("Primes", auth_key)
class SalariesEP(BaseAPI):
    def __init__(self, auth_key: tuple[str,str]):
        super().__init__("Salaries", auth_key)
class SoldeToutComptesEP(BaseAPI):
    def __init__(self, auth_key: tuple[str,str]):
        super().__init__("SoldeToutComptes", auth_key)
class VariablesEP(BaseAPI):
    def __init__(self, auth_key: tuple[str,str]):
        super().__init__("Variables", auth_key)
class VariablesBulletinsEP(BaseAPI):
    def __init__(self, auth_key: tuple[str,str]):
        super().__init__("VariablesBulletins", auth_key)


# Pour chaque thème (Dossiers, Etablissements...), initialiser une API
api_map = {
    "absences":  AbsencesEP,
    "bulletinspaies":  BulletinsPaiesEP,
    "contrats":  ContratsEP,
    "contratsortant":  ContratSortantEP,
    "dossiers":  DossiersEP,
    "editions":  EditionsEP,
    "etablissements":  EtablissementsEP,
    "heuressupplementaires":  HeuresSupplementairesEP,
    "options":  OptionsEP,
    "primes":  PrimesEP,
    "salaries":  SalariesEP,
    "soldetoutcomptes":  SoldeToutComptesEP,
    "variables":  VariablesEP,
    "variablesbulletins":  VariablesBulletinsEP
}

def OpDossierListFromJson(jsonDoss: list[dict[str, any]]) -> list[OPDossier]:
    dossierList: list[OPDossier] = []
    for dossier in jsonDoss:
        dossierList.append(OPDossier(dossier))

    return dossierList

def openpaye_auth(domain: str):
    # username, password
    return env.getLogs(domain)

def createEtablissements(domain: str, etablissements: list[Etablissment]) -> dict[str, list[str]]:
    print(
        f"Tentative d'ajout de {len(etablissements)} etablissements vers l'API openpaye"
    )
    successList = {"POSTED": []}
    for etablissement in etablissements:
        try:
            encodedEtab = utils.encoderJson(etablissement)
            if POST(domain, URL_ETAB, json=encodedEtab):
                successList.get("POSTED").append(f"{etablissement.id}")
        except Exception as e:
            print(f"createEtablissement: Exception Raised {e}")
