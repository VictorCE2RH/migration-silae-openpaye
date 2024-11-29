# Libs
import dotenv
import typer
import json
import time
from typing import Optional, List

# files
import utils
from utils import JSON
import logger
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
        response, ok = api.create(item,params)
    if not ok:
        if api_type != opapi.__VARIABLESREPRISEDOSSIER__: 
            logger.printErr(f"{api_type} id {createdItem["id"]} Erreur lors de la création")
        else:
            logger.printErr(f"{api_type} variable : {params["nomVariable"]} Erreur lors de la création")
        return None
    createdItem = json.loads(response)
    if api_type != opapi.__VARIABLESREPRISEDOSSIER__: 
        logger.printSuccess(f"{api_type} id {createdItem["id"]} Créés avec succès")
    else:
        logger.printSuccess(f"{api_type} variable : {params["nomVariable"]} = {createdItem} Créés avec succès")
    return response
        


@app.command()
def read(domain: str, api_type: str, item_ids: List[str]) -> Optional[str]:
    """
    Lire un ou plusieurs éléments spécifique par ID depuis l'API OpenPaye.
    """
    api = load_api(domain, api_type)
    itemList: List[str] = []
    for item_id in item_ids:
        item, ok = api.read(item_id)
        if not ok:
            logger.printErr(f"Item {item_id} does not exist in the database")
            raise typer.Abort(item_id)
        itemList.append(item)
        print(f"Lecture item : {item}")
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
        response,ok = api.update(item,params)
    if ok:
        updatedItem = json.loads(response)
        logger.printSuccess(f"{api_type} id {updatedItem["id"]} mis à jour avec succés")
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
        answer = typer.prompt(f"Confirmez la suppression de(s) item(s) ci-dessus : [O]ui/[N]on ")
        if answer.lower() != "o" and answer.lower() != "oui":
            typer.echo("Annulation de la requête...")
            raise typer.Abort()
    for item_id in item_ids:
        response, ok = api.delete(item_id)
        if ok:
            logger.printSuccess(f"Élément {item_id} supprimé avec succès")
        else:
            logger.printErr(f"Erreur lors de la suppression de l'élement {item_id}")
            
            
@app.command()
def getList(domain: str, api_type: str) -> Optional[str]:
    api = load_api(domain, api_type)
    response, ok = api.list()
    if ok:
        items = json.loads(response)
        utils.saveJsonData(f"res_{domain}_{api_type}", items)
        logger.printStat(f"Éléments récupérés : {len(items)}")
        return response
    else: 
        logger.printErr(f"Erreur lors de la récupération de la liste de {api_type}")
        
@app.command()
def exportSilae(domain: str,numeros: Optional[List[str]], max: int = -1) -> Optional[str]:
    step = 0
    
    logger.printProgress(f"STEP {step} ==== Export des dossiers depuis Silae ====")
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
    logger.printProgress(f"STEP {step} ======== Parsing des dossiers ========")
    op_dossiersList = parser.parseDossiers(dossiersMap, dossiersDetails, max)
    dossiersCrees = creerMultiples(domain, opapi.__DOSSIERS__, op_dossiersList)
    codesDict = dict(list(map(lambda dossier: (dossier["code"],dossier["id"]), dossiersCrees)))
    logger.printProgress(f"STEP {step} FIN ======== {len(dossiersCrees)} Dossiers Créés sur le domaine {domain} openpaye ======== \n")
    step+=1
    
    logger.printProgress(f"STEP {step} ======== Export des Etablissements depuis Silae  ======== ")
    if len(dossiersCrees) < len(op_dossiersList):
        #TODO: start modification with op_dossiersList
        logger.printErr("Problème de création de dossiers, voir les logs pour identifier le problème")
        raise typer.Abort()
    
    # Etablissements
    etabMap = silae.getInfosEtablissements(domain, dossiersMap)
    eta_DetailsMap = silae.getEtablissementDetails(domain, etabMap)
    logger.printProgress(f"STEP {step} ==== Parsing des Etablissements ====")
    op_Etablissements = parser.parseEtablissements(etabMap,eta_DetailsMap, codesDict)
    etabCrees = creerMultiples(domain, opapi.__ETABLISSEMENTS__,op_Etablissements)
    logger.printProgress(f"STEP {step} ======== {len(etabCrees)} Etablissements Créés sur le domaine {domain} openpaye ======== \n")

    step+=1
    
    logger.printProgress(f"STEP {step} ======== Export des Salariés depuis Silae  ======== ")
    # Salaries
    sal_DetailsMap = silae.getInfosSalaries(domain,codesDict) # return map[numero][matricule] = salariesdetails
    logger.printProgress(f"STEP {step} ==== Parsing des Salariés ==== ")
    op_salaries = parser.parseSalaries(sal_DetailsMap,codesDict) # return list[salDict]
    salariesCrees = creerMultiples(domain,opapi.__SALARIES__,op_salaries) # return list[salDict + ['id']] 
    logger.printProgress(f"STEP {step} ======== {len(salariesCrees)} Salariés créés sur le domaine {domain} openpaye ======== \n")
    
    step+=1
    
    logger.printProgress(f"STEP {step} ======== Export des Contrats depuis Silae  ======== ")
    # Emploi 
    emp_detailsMap = silae.getInfosEmplois(domain,sal_DetailsMap)
    logger.printProgress(f"STEP {step} ==== Parsing des Contrats ==== ")
    op_contrats = parser.parseEmplois(emp_detailsMap,codesDict)
    contratsCrees = creerMultiples(domain,opapi.__CONTRATS__,op_contrats)
    logger.printProgress(f"STEP {step} ======== {len(op_contrats)} Contrats créés sur le domaine {domain} openpaye ======== \n")
    
    step+=1
    
    # cumuls
    logger.printProgress(f"STEP {step} ======== Export des Cumuls depuis Silae  ======== ")
    matriculeContratId = dict(list(map(lambda contratCree: (contratCree["matricule_salarie"],{"id":contratCree["id"],"date_debut_contrat":contratCree["date_debut_contrat"]}),contratsCrees)))
    cumul_detailsMap = silae.getCumulsContrats(domain,codesDict)
    logger.printProgress(f"STEP {step} ==== Parsing des Cumuls ==== ")
    op_cumuls, op_contratsIdToDSN = parser.parseCumuls(cumul_detailsMap, matriculeContratId)
    logger.printProgress(f"STEP {step} ==== Opening all cumuls pages ==== ")
    utils.openCumulsWebPages(codesDict)
    # Modify Contrats (add contrat DSN)
    logger.printProgress(f"STEP {step} ==== Modifications numeros Contrats ==== ")
    up_op_contrats = parser.updateContrats(contratsCrees,op_contratsIdToDSN)
    contratsCrees = updateMultiples(domain,opapi.__CONTRATS__, up_op_contrats)
    cumulsCrees = creerMultiples(domain,opapi.__VARIABLESREPRISEDOSSIER__, op_cumuls)
    print(f"STEP {step} ======== {len(cumulsCrees)} Cumuls créés sur le domaine {domain} openpaye ======== \n")
    
def creerMultiples(domain: str, item_type: str, items: dict) -> list[dict]:
    logger.printProgress(f"MULTI CREATE ==== {len(items)} new {item_type}")
    successList: list[dict] = []
    for item in items:
        jsonStr = json.dumps(item["data"])
        jsonParams = json.dumps(item["params"])
        response = create(domain, item_type, jsonStr, jsonParams)
        # time.sleep(0.2)
        if response:
            if response.isdigit():
                successList.append(response)
            else:
                createdItem = json.loads(response)
                successList.append(createdItem)
        else:
            logger.printErr(f"Exception lors de la création de l'item {item_type} {item.get('code')}")
            # pas d'exception sur les cumuls 
            if item_type != opapi.__VARIABLESREPRISEDOSSIER__:
                raise Exception("Interruption")
    return successList

def updateMultiples(domain: str, item_type: str, items: dict) -> list[dict]:
    logger.printProgress(f"MULTI UPDATE ==== {len(items)} updated {item_type}")
    successList: list[dict] = []
    for item in items:
        dataStr = json.dumps(item["data"])
        paramStr = json.dumps(item["params"])
        response = update(domain, item_type, dataStr, paramStr)
        if response:
            createdItem = json.loads(response)
            successList.append(createdItem)
        else:
            logger.printErr(f"Exception lors de la création de l'item {item_type} {item.get('code')}")
            raise Exception("Interruption")
    return successList

if __name__ == "__main__":
    logger.printProgress("================== Application Start Session ==================")
    start = time.time()
    print(f"Mise en relation avec l'API E2RH...")
    try:
        silae.ping()
    except Exception as e:
        logger.printErr(f"Le serveur est OFF ou n'est pas accessible")
        exit(1)
    dotenv.load_dotenv()
    app()
    logger.printStat(f"Application took {time.time() - start}s to finish")
    logger.printProgress("================== Application Finish Session ==================")