# Libs
import dotenv
import typer
import json
import time
from typing import Optional, List,Tuple
from datetime import datetime

# files
import utils
import extract
from utils import JSON
import logger
import silae
import parser
import opapi


# Fonction générique pour charger l'API en fonction du type choisi
def load_api(domain: str, api_type: str):
    api_class = opapi.api_map.get(api_type)
    if not api_class:
        raise typer.Exit(f"Type '{api_type}' non supporté")
    return api_class(opapi.openpaye_auth(domain))

def creerMultiples(domain: str, item_type: str, items: dict) -> list[dict]:
    logger.printProgress(f"MULTI CREATE ==== {len(items)} new {item_type}")
    successList: list[dict] = []
    for item in items:
        jsonStr = json.dumps(item["data"])
        jsonParams = json.dumps(item["params"]) if item["params"] else None
        response, status_code = create(domain, item_type, jsonStr, jsonParams)
        if utils.valid(status_code):
            if item_type == opapi.__VARIABLESREPRISEDOSSIER__:
                if response.isdigit():
                    successList.append(response)
            else:
                createdItem = json.loads(response)
                successList.append(createdItem)
        else:
            logger.printErr(f"Exception lors de la création d'un item type '{item_type}' : {item}")
        if item_type == opapi.__VARIABLESREPRISEDOSSIER__: time.sleep(0.1)
    return successList

def updateMultiples(domain: str, item_type: str, items: dict) -> list[dict]:
    logger.printProgress(f"MULTI UPDATE ==== {len(items)} updated {item_type}")
    successList: list[dict] = []
    for item in items:
        dataStr = json.dumps(item["data"])
        paramStr = json.dumps(item["params"]) if item["params"] else None
        response = update(domain, item_type, dataStr, paramStr)
        if response:
            createdItem = json.loads(response)
            successList.append(createdItem)
        else:
            logger.printErr(f"Exception lors de la création de l'item {item_type} {item.get('code')}")
            # raise Exception("Interruption")
    return successList

def readMultiples(domain:str,item_type:str, ids:list) -> list[dict]:
    logger.printProgress(f"MULTI READ ==== {len(ids)} {item_type}")
    successList: list[dict] = []
    response = read(domain, item_type,ids,mute=True)
    if response:
        successList = [json.loads(item) for item in response.split(";")]
        # print(successList)
    else:
        logger.printErr(f"Exception lors de la lecture des items {len(ids)} {item_type} ")
    return successList

def readAndLog(domain, item_type, items,start_time, directLog: bool=False):
    if directLog: 
        utils.migrationLog(items,item_type,start_time)
        return
    itemIds = [item["id"] for item in items]
    itemRecap = readMultiples(domain,item_type,itemIds)
    utils.migrationLog(itemRecap,item_type,start_time)

app = typer.Typer(pretty_exceptions_short=True,pretty_exceptions_show_locals=False)

@app.command()
def create(domain: str, api_type: str, dataJson: str, paramsJson: Optional[str]) -> Tuple[Optional[str],int]:
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
    response, status_code = api.create(item,params)
    if not utils.valid(status_code):
        if api_type != opapi.__VARIABLESREPRISEDOSSIER__: 
            logger.printErr(f"{api_type} Erreur lors de la création de {item}")
        else:
            logger.printErr(f"{api_type} variable : {params["nomVariable"]} Erreur lors de la création")
        return None, status_code
    createdItem = json.loads(response)
    if api_type != opapi.__VARIABLESREPRISEDOSSIER__: 
        logger.printSuccess(f"{api_type} id {createdItem["id"]} Créés avec succès")
    else:
        logger.printSuccess(f"{api_type} variable : {params["contratId"]} {params["nomVariable"]} = {createdItem} Créés avec succès")
    return response, status_code

@app.command()
def read(domain: str, api_type: str, item_ids: List[str], isCode: bool=False, mute: bool = False) -> Optional[str]:
    """
    Lire un ou plusieurs éléments spécifique par ID depuis l'API OpenPaye.
    """
    if isCode:
        typer.echo(f"Leture {api_type} via le numero, recherche de correspondance ")
        itemString = getList(domain, api_type)
        if not itemString:
            logger.printErr(f"read code : list of {api_type} is None")
            raise typer.Abort()
        items = json.loads(itemString)
        foundIds = utils.getIdForNum(items, item_ids)
        item_ids = foundIds
    api = load_api(domain, api_type)
    itemList: List[str] = []
    for item_id in item_ids:
        item, statusCode = api.read(item_id)
        if not utils.valid(statusCode):
            logger.printErr(f"{api_type} {item_id} : erreur lors de la lecture de l'item")
            # raise typer.Abort(item_id)
            continue
        itemList.append(item)
        if not mute: print(f"Lecture item : {item}")
    if len(itemList) == 0:
        return None
    return ";".join(itemList)

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
    response, statusCode = api.update(item,params)
    if not utils.valid(statusCode):
        logger.printErr(f"{api_type} {item["id"]} : Erreur {statusCode} lors de la mise à jour de l'item: {item}")
        return None
    updatedItem = json.loads(response)
    logger.printSuccess(f"{api_type} id {updatedItem["id"]} mis à jour avec succés")
    return response

@app.command()
def delete(domain: str, api_type: str, item_ids: List[str], isCode: bool=False, f: bool = False):
    """
    Supprimer un élément par ID dans l'API OpenPaye.
    """
    ids = utils.clearList(item_ids)
    api = load_api(domain, api_type)
    if isCode: 
        typer.echo(f"Suppression {api_type} via le numero, recherche de correspondance ")
        itemString = getList(domain, api_type)
        try:
            items = json.loads(itemString)
            foundIds = utils.getIdForNum(items,ids)
            typer.echo(f"Pour le(s) numero(s) {ids} -> {foundIds}")
            ids = foundIds
        except Exception as e:
            print(f"json loads couldn't resolve {e}")
    typer.echo(f"Tentative de suppression d'item(s) {api_type} {ids} : ")
    read(domain, api_type, ids)
    if not f and len(foundIds) > 0:
        answer = typer.prompt(f"Confirmez la suppression de(s) item(s) ci-dessus : [O]ui/[N]on ")
        if answer.lower() != "o" and answer.lower() != "oui":
            typer.echo("Annulation de la requête...")
            raise typer.Abort()
    for item_id in ids:
        response, status_code = api.delete(item_id)
        if utils.valid(status_code):
            logger.printSuccess(f"Élément {item_id} supprimé avec succès")
        else:
            logger.printErr(f"Erreur lors de la suppression de l'élement {item_id}")
            
@app.command()
def getList(domain: str, api_type: str, dossierId: Optional[int] = None, mute: bool=False) -> Optional[str]:
    api = load_api(domain, api_type)
    if dossierId: 
        params = {"dossierId":  dossierId}
        response, status_code = api.getlist(params)
    else:
        response, status_code = api.getlist()
    if utils.valid(status_code):
        items = json.loads(response)
        utils.saveJsonData(f"res_{domain}_{api_type}", items)
        if not mute: logger.printStat(f"Éléments récupérés : {len(items)}")
        return response
    else: 
        if not mute: logger.printErr(f"Erreur lors de la récupération de la liste de {api_type}")

@app.command()
def exportSilae(domain: str, numeros: Optional[List[str]]) -> Optional[str]:
    step = 0
    log_file_suffix = f"{domain}_{datetime.today().strftime('%Y%m%d%H%M')}"
    # log_file_suffix = datetime.today().strftime('%Y-%m-%d_%Hh%Mm%Ss')
    
    logger.printProgress(f"STEP {step} ==== Suppression Dossiers Existants  ====")
    if len(numeros) > 0:
        numeros = utils.clearList(numeros)
        typer.echo(f"Vérification de la liste de dossiers, annulation si Dossier existant")
        listString = getList(domain, opapi.__DOSSIERS__, mute=True)
        items = json.loads(listString)
        foundIds = utils.getIdForNum(items, numeros)
        if len(foundIds) > 0:
            logger.printErr(f"un ou plusieurs dossiers cible de la migrations sont déjà présent sur le domaine : {[item["code"] for item in items if item["id"] in foundIds]}")
            raise typer.Abort()
    logger.printProgress(f"STEP {step} FIN ==== Suppression Dossiers Existants ====")

    step += 1
    
    logger.printProgress(f"STEP {step} ==== Export des dossiers depuis Silae ====")
    dossiersMap = silae.getDossiers(domain)
    if len(numeros) > 0:
        newDossiers: JSON = {}
        newDossiers = {numero: dossier for numero, dossier in dossiersMap.items() if numero in set(numeros)}
        typer.echo(f"Liste de numeros de dossiers indiquées, récupération avec succès de {len(newDossiers)} dossiers depuis Silae")
        dossiersMap = newDossiers
    dossiersDetails = silae.getDossiersDetails(domain, dossiersMap)
    print(f"STEP {step} ======== Parsing des dossiers ========")
    op_dossiersList = parser.parseDossiers(domain, dossiersMap, dossiersDetails)
    dossiersCrees = creerMultiples(domain, opapi.__DOSSIERS__, op_dossiersList)
    codesDict = dict(list(map(lambda dossier: (dossier["code"],dossier["id"]), dossiersCrees)))
    logger.printProgress(f"STEP {step} FIN ======== {len(dossiersCrees)} Dossiers Créés sur le domaine {domain} openpaye ======== \n")
    
    step+=1
    
    logger.printProgress(f"STEP {step} ======== Export des Etablissements depuis Silae  ======== ")
    # Etablissements
    if len(dossiersCrees) < len(op_dossiersList):
        #TODO: start modification with op_dossiersList
        logger.printErr("Problème de création de dossiers, voir les logs pour identifier le problème")
        raise typer.Abort()
    etabMap = silae.getInfosEtablissements(domain, dossiersMap)
    eta_DetailsMap = silae.getEtablissementDetails(domain, etabMap)
    print(f"STEP {step} ==== Parsing des Etablissements ====")
    op_Etablissements = parser.parseEtablissements(etabMap,eta_DetailsMap, codesDict)
    etabCrees = creerMultiples(domain, opapi.__ETABLISSEMENTS__,op_Etablissements)
    logger.printProgress(f"STEP {step} ======== {len(etabCrees)} Etablissements Créés sur le domaine {domain} openpaye ======== \n")

    step+=1
    
    logger.printProgress(f"STEP {step} ======== Export des Organismes depuis Silae  ======== ")
    etabDict = parser.buildEtabDict(op_Etablissements,etabCrees,codesDict)
    organismesMap = silae.getOrganismesList(domain, codesDict)
    op_organismes = parser.parseOrganismes(organismesMap,etabDict)
    utils.dict_to_excel(organismesMap,f".\\data\\out\\migration_log\\organismesMap_{log_file_suffix}.xlsx",'numero')
    organismesCrees = []
    # organismesCrees = creerMultiples(domain,opapi.__CAISSECOTISATIONS__,op_organismes)
    logger.printProgress(f"STEP {step} FIN ======== {len(organismesCrees)} Organismes Créés sur le domaine {domain} openpaye ======== \n")
    
    step+=1
    
    logger.printProgress(f"STEP {step} ======== Export des Salariés depuis Silae  ======== ")
    # Salaries
    sal_DetailsMap = silae.getInfosSalaries(domain,codesDict) # return map[numero][matricule] = salariesdetails
    print(f"STEP {step} ==== Parsing des Salariés ==== ")
    op_salaries = parser.parseSalaries(sal_DetailsMap,codesDict) # return list[salDict]
    salariesCrees = creerMultiples(domain,opapi.__SALARIES__,op_salaries) # return list[salDict + ['id']] 
    logger.printProgress(f"STEP {step} ======== {len(salariesCrees)} Salariés créés sur le domaine {domain} openpaye ======== \n")

    step+=1
    
    logger.printProgress(f"STEP {step} ======== Export des Contrats depuis Silae  ======== ")
    # Emploi/Contrat
    emp_detailsMap = silae.getInfosEmplois(domain,sal_DetailsMap)
    # Ajouter vérification pour CCN à sous spécifications (T026, M110)
    # 1 récupérer les etabCrees & details emplois
    # up_up_etablissements = parser.updateSpecificsCcns(op_Etablissements,emp_detailsMap)
    # 2 vérifier si etabCrees == CCN spé
    # 3 en fonction du code emplois, changer la convention collective
    logger.printProgress(f"STEP {step} ==== Parsing des Contrats ==== ")
    op_contrats = parser.parseEmplois(emp_detailsMap,eta_DetailsMap,codesDict)
    contratsCrees = creerMultiples(domain,opapi.__CONTRATS__,op_contrats)
    logger.printProgress(f"STEP {step} ======== {len(op_contrats)} Contrats créés sur le domaine {domain} openpaye ======== \n")
    
    
    step+=1
    
    # cumuls
    logger.printProgress(f"STEP {step} ======== Export des Cumuls depuis Silae  ======== ")
    matriculeContratId = dict(list(map(lambda contratCree: (contratCree["matricule_salarie"],{"id":contratCree["id"],"date_debut_contrat":contratCree["date_debut_contrat"]}),contratsCrees)))
    cumul_detailsMap = silae.getCumulsContrats(domain,codesDict)
    print(f"STEP {step} ==== Parsing des Cumuls ==== ")
    op_cumuls, op_contratsIdToDSN = parser.parseCumuls(cumul_detailsMap, matriculeContratId)
    # Modify Contrats (add contrat DSN)
    print(f"STEP {step} ==== Modifications numeros Contrats ==== ")
    up_op_contrats = parser.updateContrats(contratsCrees,op_contratsIdToDSN)
    contratsModif = updateMultiples(domain,opapi.__CONTRATS__, up_op_contrats)
    cumulsCrees = creerMultiples(domain,opapi.__VARIABLESREPRISEDOSSIER__, op_cumuls)
    print(f"STEP {step} ======== {len(cumulsCrees)} Cumuls créés sur le domaine {domain} openpaye ======== \n")
    
    if len(numeros) > 0:
        readAndLog(domain,opapi.__DOSSIERS__+"_Target", numeros,log_file_suffix,directLog=True)
    readAndLog(domain,opapi.__DOSSIERS__, dossiersCrees,log_file_suffix)
    readAndLog(domain,opapi.__CAISSECOTISATIONS__+"_ajout_manuel",op_organismes,log_file_suffix,directLog=True)
    readAndLog(domain,opapi.__ETABLISSEMENTS__, etabCrees,log_file_suffix)
    readAndLog(domain,opapi.__SALARIES__, salariesCrees,log_file_suffix)
    readAndLog(domain,opapi.__CONTRATS__,contratsCrees,log_file_suffix)
    readAndLog(domain,opapi.__CONTRATS__+"modif_manuelle",up_op_contrats,log_file_suffix,directLog=True)
    # readAndLog(domain,opapi.__VARIABLESREPRISEDOSSIER__, cumulsCrees,log_file_suffix,directLog=True)

@app.command()
def updateCumuls(domain: str, numeros:List[str]):
    if numeros == 0:
        raise typer.Abort("argument numeros vide")

    step = 1
    logger.printProgress(f"STEP {step} ==== Récupération des Dossiers ====")
    dossiersList = json.loads(getList(domain,opapi.__DOSSIERS__,mute=True))
    dossiersList = [dossier for dossier in dossiersList if dossier["code"] in numeros]
    print(dossiersList)
    codesDict = dict(list(map(lambda dossier: (dossier["code"],dossier["id"]), dossiersList)))
    logger.printProgress(f"STEP {step} FIN ======== Récupération des Dossiers ======== \n")
    
    step+=1
    logger.printProgress(f"STEP {step} ======== Récupération des Contrats ======== ")
    contratsList = []
    for dossier in dossiersList:
        contratListStr = getList(domain, opapi.__CONTRATS__,dossierId=dossier["id"],mute=True)
        if contratListStr:
            contratsList += json.loads(contratListStr)["contrats"]
    logger.printProgress(f"STEP {step} FIN ======== Récupération des Contrats ======== \n")
    
    step+=1
    logger.printProgress(f"STEP {step} ======== Export des Cumuls depuis Silae  ======== ")
    matriculeContratId = dict(list(map(lambda contratsList: (contratsList["matricule_salarie"],{"id":contratsList["id"],"date_debut_contrat":contratsList["date_debut_contrat"]}),contratsList)))
    print(matriculeContratId)
    cumul_detailsMap = silae.getCumulsContrats(domain,codesDict)
    print(f"STEP {step} ==== Parsing des Cumuls ==== ")
    op_cumuls, op_contratsIdToDSN = parser.parseCumuls(cumul_detailsMap, matriculeContratId)
    print(f"STEP {step} ==== Insertion des Cumuls ==== ")
    up_op_contrats = parser.updateContrats(contratsList,op_contratsIdToDSN)
    contratsModif = updateMultiples(domain,opapi.__CONTRATS__, up_op_contrats)
    cumulsCrees = creerMultiples(domain,opapi.__VARIABLESREPRISEDOSSIER__, op_cumuls)
    logger.printProgress(f"STEP {step} ======== {len(cumulsCrees)} Cumuls créés sur le domaine {domain} openpaye ======== \n")

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