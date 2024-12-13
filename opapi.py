import requests
import json
import env
import logger
from utils import valid
from urllib.parse import urlencode
from typing import Any, Dict, Optional

api_openpaye = "https://api.openpaye.co"
URL_DOSSIERS = api_openpaye + "/dossiers"

# Pour chaque thème (Dossiers, Etablissements...), initialiser une API
__ABSENCES__ = "absences"
__BULLETINSPAIES__ = "bulletinspaies"
__CONTRATS__ = "contrats"
__CAISSECOTISATIONS__ = "caisseCotisations"
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

    def create(self, data: dict, params: dict = None) -> tuple[Optional[str], int]:
        url = f"{self.BASE_URL}/{self.resource}"
        response = requests.post(url, auth=self.auth, json=data, headers=self.headers, params=params)
        return self._handle_response(response)

    def read(self, item_id: str) -> tuple[Optional[str], int]:
        url = f"{self.BASE_URL}/{self.resource}/{item_id}"
        response = requests.get(url, auth=self.auth, headers=self.headers)
        return self._handle_response(response)

    def update(self, data: dict, params: dict = None) -> tuple[Optional[str], int]:
        url = f"{self.BASE_URL}/{self.resource}/"
        response = requests.put(url, auth=self.auth, json=data, headers=self.headers, params=params)
        return self._handle_response(response)

    def delete(self, item_id: str) -> tuple[Optional[str], int]:
        url = f"{self.BASE_URL}/{self.resource}/{item_id}"
        response = requests.delete(url, auth=self.auth, headers=self.headers)
        return self._handle_response(response)

    def getlist(self, params: dict = None) -> tuple[Optional[str], int]:
        url = f"{self.BASE_URL}/{self.resource}"
        if params:
            url += "?" + urlencode(params)
        response = requests.get(url, auth=self.auth, headers=self.headers)
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> tuple[Optional[str], int]:
        if valid(response.status_code):
            return response.text, response.status_code
        if response.status_code == 409:
            logger.printWarn(f"Warning {response.url} response : {response.status_code} - {response.text}")
            return response.text, response.status_code
        logger.printErr(f"Error {response.url} response : {response.status_code} - {response.text}")
        return response.text, response.status_code

class DossiersEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__DOSSIERS__, auth_key)

    # def create(self, data: dict, params:dict = None):
    #     if not data:
    #         raise Exception("Aucune donnée à créer")
    #     response, status_code = super().create(data,params)
    #     if valid(status_code):
    #         return response, status_code
        
    #     if status_code == 409:
    #         logger.printProgress(f"Récupération de l'item existant")
    #         respList, status_code = self.getlist(prints=False)
    #         if valid(status_code):
    #             items = json.loads(respList)
    #             readItem = [item for item in items if item["code"] == data["code"]]
    #             if readItem:
    #                 return json.dumps(readItem[0]), status_code
    
    def getlist(self, prints: bool =True):
        if prints: print("liste de tous les dossiers")
        page = 0
        dossiers,total_pages,total_dossiers, status_code = self.getDossiersList(page,prints=False)
        if not valid(status_code):
            return None, status_code
        while page < total_pages:
            page += 1
            nextPageDossiers, _, _, status_code = self.getDossiersList(page,prints=False)
            if not valid(status_code):
                if prints: logger.printWarn(f"dossiers.getlist : Erreur {status_code} récupération Dossiers page {page}")
                continue
            dossiers += nextPageDossiers
        if len(dossiers) != total_dossiers:
            raise Exception(f"[List Dossiers] Récupération erronée , dossiers récupérés  : {len(dossiers)} != dossiers stockés :{total_dossiers}")
        return json.dumps(dossiers), status_code

    def getDossiersList(self, num: int, prints: bool) -> tuple[str, int, int, int]:
        params = {"page": num}
        dossiersInfosStr, status_code = super().getlist(params)
        if not valid(status_code):
            return None, 0, 0, status_code
        dossiersInfos = json.loads(dossiersInfosStr)
        dossiers = dossiersInfos.get("dossiers")
        total_dossiers = int(dossiersInfos.get("total_count"))
        total_pages = int(dossiersInfos.get("total_pages"))
        if prints: print(f"page {num+1}/{total_pages}")
        return dossiers, total_pages, total_dossiers, status_code

class EtablissementsEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__ETABLISSEMENTS__, auth_key)

    def getlist(self, params: dict = None):
        if params["dossierId"] == None:
            raise Exception()
        dossierId = params["dossierId"]
        print(f"liste de tous les etablissements du etablissement {dossierId}")
        page = 0
        etablissements, total_pages, total_etablissements, status_code = self.getEtabList(dossierId,page)
        if not valid(status_code):
            return None, status_code
        page += 1
        while page < total_pages:
            page += 1
            nextPage, _, _, status_code = self.getEtabList(dossierId,page)
            if not valid(status_code):
                logger.printWarn(f"etablissements.getlist : Erreur {status_code} récupération etablissements dossier {dossierId} page {page}")
                continue
            etablissements += nextPage
        if len(etablissements) != total_etablissements:
            raise Exception(f"[List Etablissements] Récupération erronée , etablissements récupérés  : {len(etablissements)} != etablissements stockés :{total_etablissements}")
        return json.dumps(etablissements), status_code

    def getEtabList(self, id, num: int) -> tuple[list, int, int, int]:
        params = {"dossierId": id, "page": num}
        etablissementsInfosStr, status_code = super().getlist(params)
        if not valid(status_code):
            return None, 0, 0, status_code
        etablissementsInfos = json.loads(etablissementsInfosStr)
        etablissements = etablissementsInfos.get("etablissements")
        total_etablissements = int(etablissementsInfos.get("total_count"))
        total_pages = int(etablissementsInfos.get("total_pages"))
        print(f"page {num+1}/{total_pages}")
        return etablissements, total_pages, total_etablissements, status_code

class AbsencesEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__ABSENCES__, auth_key)

class BulletinsPaiesEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__BULLETINSPAIES__, auth_key)

class CaisseCotisationsEP(BaseAPI):
    def __init__(self, auth_key: tuple[str,str]):
        super().__init__(__CAISSECOTISATIONS__, auth_key)

class ContratsEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__CONTRATS__, auth_key)

    # def create(self, data, params = None):
    #     response, status_code = super().create(data, params)
    #     if not valid(status_code):
    #         if response == "Le code CCN/IDCC n'est pas valide":
    #             logger.printWarn(f"Retry without informations : ccn {data["ccn"]}")
    #             data["ccn"] = None
    #             return super().create(data,params)

class ContratSortantEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__CONTRATSORTANT__, auth_key)

class EditionsEP(BaseAPI):
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__EDITIONS__, auth_key)

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
    def __init__(self, auth_key: tuple[str, str]):
        super().__init__(__VARIABLESREPRISEDOSSIER__, auth_key)

api_map = {
    __ABSENCES__: AbsencesEP,
    __BULLETINSPAIES__: BulletinsPaiesEP,
    __CAISSECOTISATIONS__: CaisseCotisationsEP,
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
    __VARIABLESREPRISEDOSSIER__: VariablesRepriseDossierEP,
}