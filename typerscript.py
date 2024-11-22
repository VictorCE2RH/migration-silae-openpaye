# Libs
import dotenv
import typer
import json
import sys
import time
from typing import Optional, List

# files
import utils
from utils import JSON
import silae
import parser
import extract
import opapi

app = typer.Typer()

# Fonction générique pour charger l'API en fonction du type choisi
def load_api(domain: str, api_type: str):
    api_class = opapi.api_map.get(api_type)
    if not api_class:
        raise typer.Exit(f"Type '{api_type}' non supporté")
    return api_class(opapi.openpaye_auth(domain))

@app.command()
def create(domain: str, api_type: str, dataJson: str, paramsJson: Optional[str]) -> Optional[str]:
    """
    Créer des éléments dans l'API OpenPaye pour un type donné (dossiers, etablissements, etc.).
    Renvois le json de l'objet créé si succès
    """
    api = load_api(domain, api_type)
    # Charger les données à partir du fichier ou d'un autre source
    item = json.loads(dataJson)
    params = None
    if paramsJson:
        params = json.loads(paramsJson)
        response = api.create(item,params)
    if response:
        createdItem = json.loads(response)
        typer.echo(f"{api_type} id {createdItem["id"]} Créés avec succès")
        return response
    return None


@app.command()
def read(domain: str, api_type: str, item_ids: List[str]) -> Optional[str]:
    """
    Lire un ou plusieurs éléments spécifique par ID depuis l'API OpenPaye.
    """
    api = load_api(domain, api_type)
    itemList: List[str] = []
    for item_id in item_ids:
        item = api.read(item_id)
        if not item:
            typer.echo(f"Item {item_id} does not exist in the database")
            raise typer.Abort(item_id)
        itemList.append(item)
        typer.echo(f"Lecture item : {item}")
    if len(itemList) == 0:
        return None
    return ",".join(itemList)


@app.command()
def update(domain: str, api_type: str, dataJson: str, paramsJson: Optional[str]) -> Optional[str]:
    """
    Mettre à jour un élément existant dans l'API OpenPaye.
    """
    api = load_api(domain, api_type)
    # Charger les données à partir du fichier ou d'un autre source
    item = json.loads(dataJson)
    params = None
    if paramsJson:
        params = json.loads(paramsJson)
        response = api.update(item,params)
    if response:
        updatedItem = json.loads(response)
        typer.echo(f"{api_type} id {updatedItem["id"]} mis à jour avec succés")
        return response
    return None

@app.command()
def delete(domain: str, api_type: str, item_ids: List[str], isCode: bool=False, ask: bool = True):
    """
    Supprimer un élément par ID dans l'API OpenPaye.
    """
    api = load_api(domain, api_type)
    if isCode:
        typer.echo(f"Suppression {api_type} via le numero, recherche de correspondance ")
        items = getList(domain, api_type)
        try :
            foundIds = utils.getIdForNum(json.loads(items),item_ids)
        except Exception as e:
            print(f"aucun(e) {api_type} code {e} trouvés dans la base de données")
            raise typer.Abort()
        typer.echo(f"Pour le(s) numero(s) {item_ids} -> {foundIds}")
        item_ids = foundIds
    typer.echo(f"Tentative de suppression d'item(s) {api_type} {item_ids} : ")
    read(domain, api_type, item_ids)
    if ask == True:
        answer = typer.prompt(
            f"Confirmez la suppression de(s) item(s) ci-dessus : [O]ui/[N]on "
        )
        if answer.lower() != "o" and answer.lower() != "oui":
            typer.echo("Annulation de la requête...")
            raise typer.Abort()
    for item_id in item_ids:
        api.delete(item_id)
        typer.echo(f"Élément {item_id} supprimé avec succès")

@app.command()
def getList(domain: str, api_type: str) -> Optional[str]:
    api = load_api(domain, api_type)
    response = api.list()
    items = json.loads(response)
    utils.saveJsonData(f"res_{domain}_{api_type}", items)
    typer.echo(f"Éléments récupérés : {len(items)}")
    return response

@app.command()
def exportSilae(domain: str,numeros: Optional[List[str]], max: int = -1) -> Optional[str]:
    step = 0
    
    typer.echo(f"STEP {step} ==== Export des dossiers depuis Silae ====")
    dossiersMap = silae.getDossiers(domain)
    if len(numeros) > 0:
        newDossiers: JSON = {}
        newDossiers = {numero: dossier for numero, dossier in dossiersMap.items() if numero in set(numeros)}
        typer.echo(f"Liste de numeros de dossiers indiquées, récupération avec succès de {len(newDossiers)} dossiers depuis Silae")
        dossiersMap = newDossiers
    elif max > 0:
        i = 0
        newDossiers: JSON = {}
        for numero, dossier in dossiersMap.items():
            i += 1
            newDossiers[numero] = dossier
            if max == i:
                dossiersMap = newDossiers
                break
    dossiersDetails = silae.getDossiersDetails(domain, dossiersMap)
    typer.echo(f"STEP {step} ======== Parsing des dossiers ========")
    op_dossiersList = parser.parseDossiers(dossiersMap, dossiersDetails, max)
    dossiersCrees = creerMultiples(domain, opapi.__DOSSIERS__, op_dossiersList)
    codeDict = dict(list(map(lambda dossier: (dossier["code"],dossier["id"]), dossiersCrees)))
    print(f"STEP {step} FIN ======== {len(dossiersCrees)} Dossiers Créés sur le domaine {domain} openpaye ======== \n")
    step+=1
    
    typer.echo(f"STEP {step} ======== Export des Etablissements depuis Silae  ======== ")
    if len(dossiersCrees) < len(op_dossiersList):
        #TODO: start modification with op_dossiersList
        typer.echo("Problème de création de dossiers, voir les logs pour identifier le problème")
        raise typer.Abort()
    
    # Etablissements
    etabMap = silae.getInfosEtablissements(domain, dossiersMap)
    eta_DetailsMap = silae.getEtablissementDetails(domain, etabMap)
    typer.echo(f"STEP {step} ==== Parsing des Etablissements ====")
    op_Etablissements = parser.parseEtablissements(etabMap,eta_DetailsMap, codeDict)
    etabCrees = creerMultiples(domain, opapi.__ETABLISSEMENTS__,op_Etablissements)
    print(f"STEP {step} ======== {len(etabCrees)} Etablissements Créés sur le domaine {domain} openpaye ======== \n")

    step+=1
    
    typer.echo(f"STEP {step} ======== Export des Salariés depuis Silae  ======== ")
    # Salaries
    sal_DetailsMap = silae.getInfosSalaries(domain,codeDict) # return map[numero][matricule] = salariesdetails
    typer.echo(f"STEP {step} ==== Parsing des Salariés ==== ")
    op_salaries = parser.parseSalaries(sal_DetailsMap,codeDict) # return list[salDict]
    salariesCrees = creerMultiples(domain,opapi.__SALARIES__,op_salaries) # return list[salDict + ['id']] 
    print(f"STEP {step} ======== {len(salariesCrees)} Salariés créés sur le domaine {domain} openpaye ======== \n")
    
    step+=1
    
    typer.echo(f"STEP {step} ======== Export des Contrats depuis Silae  ======== ")
    # Emploi 
    emp_detailsMap = silae.getInfosEmplois(domain,sal_DetailsMap)
    typer.echo(f"STEP {step} ==== Parsing des Contrats ==== ")
    op_contrats = parser.parseEmplois(emp_detailsMap,codeDict)
    contratsCrees = creerMultiples(domain,opapi.__CONTRATS__,op_contrats)
    print(f"STEP {step} ======== {len(op_contrats)} Contrats créés sur le domaine {domain} openpaye ======== \n")
    
    step+=1
    
    # cumuls
    typer.echo(f"STEP {step} ======== Export des Cumuls depuis Silae  ======== ")
    matriculeContratId = dict(list(map(lambda contratCree: (contratCree["matricule_salarie"],{"id":contratCree["id"],"date_debut_contrat":contratCree["date_debut_contrat"]}),contratsCrees)))
    cumul_detailsMap = silae.getCumulsContrats(domain,codeDict)
    typer.echo(f"STEP {step} ==== Parsing des Cumuls ==== ")
    op_cumuls, op_contratsIdToDSN = parser.parseCumuls(cumul_detailsMap, matriculeContratId)
    # Modify Contrats (add contrat DSN)
    up_op_contrats = parser.updateContrats(contratsCrees,op_contratsIdToDSN)
    contratsCrees = updateMultiples(domain,opapi.__CONTRATS__, up_op_contrats)
    print(f"STEP {step} ======== FIN : CREATION CUMULS COMMENTES ============ ")
    
    # cumulsCrees = creerMultiples(domain,opapi.__VARIABLESREPRISEDOSSIER__, op_cumuls)
    # print(f"STEP {step} ======== {len(cumulsCrees)} Cumuls créés sur le domaine {domain} openpaye ======== \n")
    
def creerMultiples(domain: str, item_type: str, items: dict) -> list[dict]:
    print(f"MULTI CREATE ==== {len(items)} new {item_type}")
    successList: list[dict] = []
    for item in items:
        jsonStr = json.dumps(item["data"])
        jsonParams = json.dumps(item["params"])
        response = create(domain, item_type, jsonStr, jsonParams)
        time.sleep(0.2)
        if response:
            if response.isdigit():
                successList.append(response)
            else:
                createdItem = json.loads(response)
                successList.append(createdItem)
        else:
            print(f"Exception lors de la création de l'item {item_type} {item.get('code')}")
            raise Exception("Interruption")
    return successList

def updateMultiples(domain: str, item_type: str, items: dict) -> list[dict]:
    print(f"MULTI UPDATE ==== {len(items)} updated {item_type}")
    successList: list[dict] = []
    for item in items:
        dataStr = json.dumps(item["data"])
        paramStr = json.dumps(item["params"])
        response = update(domain, item_type, dataStr, paramStr)
        if response:
            createdItem = json.loads(response)
            successList.append(createdItem)
        else:
            print(f"Exception lors de la création de l'item {item_type} {item.get('code')}")
            raise Exception("Interruption")
    return successList

if __name__ == "__main__":
    print("================== Application Start Session ==================")
    start = time.time()
    print(f"Mise en relation avec l'API E2RH...")
    try:
        silae.ping()
    except Exception as e:
        print(f"Le serveur est OFF ou n'est pas accessible")
        exit(1)
    dotenv.load_dotenv()
    print(app())
    print(time.time() - start)