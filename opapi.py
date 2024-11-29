import requests
import json
import env
from urllib.parse import urlencode
import config
from typing import Any, Dict, Optional

api_openpaye = "https://api.openpaye.co"
URL_DOSSIERS = api_openpaye + "/dossiers"

# Pour chaque thème (Dossiers, Etablissements...), initialiser une API
__ABSENCES__ = "absences"
__BULLETINSPAIES__ = "bulletinspaies"
__CONTRATS__ = "contrats"
__CONTRATSORTANT__ = "contratsortant"
__DOSSIERS__ = "dossiers"
__EDITIONS__ = "editions"
__ETABLISSEMENTS__ = "etablissements"
__HEURESSUPPLEMENTAIRES__ = "heuressupplementaires"
__OPTIONS__ = "options"
__PRIMES__ = "primes"
__SALARIES__ = "salaries"
__SOLDETOUTCOMPTES__ = "soldetoutcomptes"
__VARIABLES__ = "variables"
__VARIABLESBULLETINS__ = "variablesbulletins"
__VARIABLESREPRISEDOSSIER__ = "VariablesRepriseDossier"

def openpaye_auth(domain: str):
    # username, password
    return env.getLogs(domain)

class BaseAPI:
    BASE_URL = "https://api.openpaye.co"  # URL de base de ton API

    def __init__(self, resource: str, auth_key: tuple[str, str]):
        self.resource = (
            resource  # Le thème (endpoint) comme "Absences", "Contrats", etc.
        )
        self.headers = {"Content-Type": "application/json"}
        self.auth = auth_key

    def create(self, data:dict, params:dict=None) -> (Optional[str], bool):
        url = f"{self.BASE_URL}/{self.resource}"
        response = requests.post(url, auth=self.auth, json=data, headers=self.headers,params=params)
        return self._handle_response(response)

    def read(self, item_id: str) -> (Optional[str], bool):
        url = f"{self.BASE_URL}/{self.resource}/{item_id}"
        response = requests.get(url, auth=self.auth, headers=self.headers)
        return self._handle_response(response)

    def update(self, data: dict, params:dict=None) -> (Optional[str], bool):
        url = f"{self.BASE_URL}/{self.resource}/"
        response = requests.put(
            url, auth=self.auth, json=data, headers=self.headers, params=params
        )
        return self._handle_response(response)

    def delete(self, item_id: str) -> (Optional[str], bool):
        url = f"{self.BASE_URL}/{self.resource}/{item_id}"
        response = requests.delete(url, auth=self.auth, headers=self.headers)
        return self._handle_response(response)

    def list(self, params: dict = None) -> (Optional[str], bool):
        url = f"{self.BASE_URL}/{self.resource}"
        if params:
            url += "?" + urlencode(params)
        response = requests.get(url, auth=self.auth, headers=self.headers)
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> (Optional[str], bool):
        if response.status_code in [200, 201]:
            return response.text, True
        else:
            print(f"Error {response.url} response : {response.status_code} - {response.text}")
            return None, False


class AbsencesEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__ABSENCES__, auth_key)


class BulletinsPaiesEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__BULLETINSPAIES__, auth_key)


class ContratsEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__CONTRATS__, auth_key)


class ContratSortantEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__CONTRATSORTANT__, auth_key)


class DossiersEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__DOSSIERS__, auth_key)

    def list(self, params:dict=None):
        print("liste de tous les dossiers")
        page = 0
        infos = self.getDossiersList(page)
        if not infos: 
            return None, False
        dossiers = infos[0]; total_pages = infos[1]; total_dossiers = infos[2]
        page += 1
        while page < total_pages:
            nextPageDossiers, _, _ = self.getDossiersList(page)
            dossiers += nextPageDossiers
        if len(dossiers) != total_dossiers:
            raise Exception(
                f"[List Dossiers] Récupération erronée , dossiers récupérés  : {len(dossiers)} != dossiers stockés :{total_dossiers}"
            )
        return json.dumps(dossiers), True

    def getDossiersList(self, num:int) -> tuple[str,int,int]:
        params = {"page": num}
        dossiersInfosStr, ok = super().list(params)
        if not ok:
            return None
        dossiersInfos = json.loads(dossiersInfosStr)
        dossiers = dossiersInfos.get("dossiers")
        total_dossiers = int(dossiersInfos.get("total_count"))
        total_pages = int(dossiersInfos.get("total_pages"))
        return dossiers, total_pages, total_dossiers

class EditionsEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__EDITIONS__, auth_key)


class EtablissementsEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__ETABLISSEMENTS__, auth_key)
    
    def list(self, params:dict=None):
        if params["dossierId"] == None:
            raise Exception()
        print(f"liste de tous les etablissements du etablissement {params["dossierId"]}")
        page = 0
        etablissements, total_pages, total_etablissements = self.getDossiersList(page)
        page += 1
        while page < total_pages:
            nextPage, _, _ = self.getDossiersList(page)
            etablissements += nextPage
        if len(etablissements) != total_etablissements:
            raise Exception(
                f"[List Dossiers] Récupération erronée , etablissements récupérés  : {len(etablissements)} != etablissements stockés :{total_etablissements}"
            )
        return json.dumps(etablissements)

    def getDossiersList(self, id, num:int) -> tuple[str,int,int]:
        params = dict(("dossierId", id),("page", num))
        etablissementsInfosStr, ok = super().list(params)
        if not ok:
            return None
        etablissementsInfos = json.loads(etablissementsInfosStr)
        etablissements = etablissementsInfos.get("etablissements")
        total_etablissements = int(etablissementsInfos.get("total_count"))
        total_pages = int(etablissementsInfos.get("total_pages"))
        return etablissements, total_pages, total_etablissements

class HeuresSupplementairesEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__HEURESSUPPLEMENTAIRES__, auth_key)

class OptionsEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__OPTIONS__, auth_key)


class PrimesEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__PRIMES__, auth_key)


class SalariesEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__SALARIES__, auth_key)


class SoldeToutComptesEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__SOLDETOUTCOMPTES__, auth_key)


class VariablesEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__VARIABLES__, auth_key)


class VariablesBulletinsEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__VARIABLESBULLETINS__, auth_key)

class VariablesRepriseDossierEP(BaseAPI):
    def __init__(self, auth_key: tuple[str,str]):
        super().__init__(__VARIABLESREPRISEDOSSIER__, auth_key)
        
api_map = {
    __ABSENCES__: AbsencesEP,
    __BULLETINSPAIES__: BulletinsPaiesEP,
    __CONTRATS__: ContratsEP,
    __CONTRATSORTANT__: ContratSortantEP,
    __DOSSIERS__: DossiersEP,
    __EDITIONS__: EditionsEP,
    __ETABLISSEMENTS__: EtablissementsEP,
    __HEURESSUPPLEMENTAIRES__: HeuresSupplementairesEP,
    __OPTIONS__: OptionsEP,
    __PRIMES__: PrimesEP,
    __SALARIES__: SalariesEP,
    __SOLDETOUTCOMPTES__: SoldeToutComptesEP,
    __VARIABLES__: VariablesEP,
    __VARIABLESBULLETINS__: VariablesBulletinsEP,
    __VARIABLESREPRISEDOSSIER__: VariablesRepriseDossierEP
}
