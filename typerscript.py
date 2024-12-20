# Libs
import dotenv
import typer
import json
import time
import requests
from wakepy import keep
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
    logger.progress(f"MULTI CREATE ==== {len(items)} new {item_type}")
    successList: list[dict|str] = []
    for item in items:
        jsonStr = json.dumps(item["data"])
        jsonParams = json.dumps(item["params"]) if item["params"] else None
        response, status_code = create(domain, item_type, jsonStr, jsonParams)
        if utils.valid(status_code):
            if item_type == opapi.__VARIABLESREPRISEDOSSIER__:
                successList.append(response)
            else:
                createdItem = json.loads(response)
                successList.append(createdItem)
        else:
            logger.error(f"Exception lors de la création d'un item type '{item_type}' : {response}")
        if item_type == opapi.__VARIABLESREPRISEDOSSIER__: time.sleep(0.05)
    return successList

def creerMultiplesParLots(domain: str, item_type: str, items: list[dict], taille_lot: int = 100) -> list[dict]:
    """
    Crée des items par lots pour optimiser les performances avec un grand nombre d'items.
    
    Args:
        domain: Le domaine de l'API
        item_type: Le type d'item à créer
        items: La liste des items à créer
        taille_lot: Nombre d'items par lot
    
    Returns:
        Liste des items créés avec succès
    """
    logger.progress(f"MULTI CREATE ==== {len(items)} new {item_type} (par lots de {taille_lot})")
    successList: list[dict|str] = []
    
    # Diviser les items en lots
    for i in range(0, len(items), taille_lot):
        lot = items[i:i + taille_lot]
        lot_tasks = []
        
        # Créer une session requests pour réutiliser les connexions
        with requests.Session() as session:
            api = load_api(domain, item_type)
            api.session = session  # Utiliser la session réutilisable
            
            for data in lot:
                item = data["data"]
                params = data["params"]
                try:
                    response, status_code = api.create(item, params)
                    if utils.valid(status_code):
                        if item_type == opapi.__VARIABLESREPRISEDOSSIER__:
                            successList.append(response)
                            logger.success(f"{item_type} variable : {params["contratId"]} {params["nomVariable"]} = {response} Créés avec succès")
                        else:
                            createdItem = json.loads(response)
                            successList.append(createdItem)         
                            logger.success(f"{item_type} id {createdItem["id"]} Créés avec succès")
                    else:
                        if status_code != 409:
                            if item_type != opapi.__VARIABLESREPRISEDOSSIER__: 
                                logger.error(f"{item_type} Erreur lors de la création de {item}")
                            else:
                                logger.error(f"{item_type} variable : {params["nomVariable"]} Erreur lors de la création")
                except Exception as e:
                    logger.error(f"Exception lors de la création d'un item type '{item_type}' : {e}")
                
                # if item_type == opapi.__VARIABLESREPRISEDOSSIER__:
                #     time.sleep(0.05)  # Réduit le délai entre les requêtes
        
        logger.progress(f"Lot {i//taille_lot + 1}/{(len(items) + taille_lot - 1)//taille_lot} terminé")
    return successList

def updateMultiples(domain: str, item_type: str, items: dict) -> list[dict]:
    logger.progress(f"MULTI UPDATE ==== {len(items)} updated {item_type}")
    successList: list[dict] = []
    for item in items:
        dataStr = json.dumps(item["data"])
        paramStr = json.dumps(item["params"]) if item["params"] else None
        response = update(domain, item_type, dataStr, paramStr)
        if response:
            createdItem = json.loads(response)
            successList.append(createdItem)
        else:
            logger.error(f"Exception lors de la mise à jour de l'item {item_type} {item.get('code')}")
            # raise Exception("Interruption")
    return successList

def readMultiples(domain:str,item_type:str, ids:list) -> list[dict]:
    logger.progress(f"MULTI READ ==== {len(ids)} {item_type}")
    successList: list[dict] = []
    response = read(domain, item_type,ids,mute=True)
    if response:
        successList = [json.loads(item) for item in response.split(";")]
        #logger.print(successList)
    else:
        logger.error(f"Exception lors de la lecture des items {len(ids)} {item_type} ")
    return successList

def readAndLog(domain, item_type, items,start_time, directLog: bool=False):
    if directLog: 
        utils.migrationLog(domain, items,item_type,prefix=start_time)
        return
    itemIds = [item["id"] for item in items]
    itemRecap = readMultiples(domain,item_type,itemIds)
    utils.migrationLog(domain,itemRecap,item_type,start_time)

app = typer.Typer(pretty_exceptions_short=True,pretty_exceptions_show_locals=True)

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
            logger.error(f"{api_type} Erreur lors de la création de {item}")
        else:
            logger.error(f"{api_type} variable : {params["nomVariable"]} Erreur lors de la création")
        return None, status_code
    createdItem = json.loads(response)
    if api_type != opapi.__VARIABLESREPRISEDOSSIER__: 
        logger.success(f"{api_type} id {createdItem["id"]} Créés avec succès")
    else:
        logger.success(f"{api_type} variable : {params["contratId"]} {params["nomVariable"]} = {createdItem} Créés avec succès")
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
            logger.error(f"read code : list of {api_type} is None")
            raise typer.Abort()
        items = json.loads(itemString)
        foundIds = utils.getIdForNum(items, item_ids)
        item_ids = foundIds
    api = load_api(domain, api_type)
    itemList: List[str] = []
    for item_id in item_ids:
        item, statusCode = api.read(item_id)
        if not utils.valid(statusCode):
            logger.error(f"{api_type} {item_id} : erreur lors de la lecture de l'item")
            # raise typer.Abort(item_id)
            continue
        itemList.append(item)
        if not mute:logger.log(f"Lecture item : {item}")
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
        if statusCode != 409:
            logger.error(f"{api_type} {item["id"]} : contenu de l'item : {item}")
        return None
    updatedItem = json.loads(response)
    logger.success(f"{api_type} {updatedItem["id"]} : mis à jour")
    return response

@app.command()
def delete(domain: str, api_type: str, item_ids: List[str], isCode: bool=False, f: bool = False):
    """
    Supprimer un élément par ID dans l'API OpenPaye.
    """
    logger.progress(f" ======================== Suppression {api_type} ========================")
    ids = utils.clearList(item_ids)
    api = load_api(domain, api_type)
    if isCode: 
        typer.echo(f"Suppression {api_type} via le numero, recherche de correspondance ")
        itemString = getList(domain, api_type)
        itemList = []
        try:
            items = json.loads(itemString)
            foundIds = utils.getIdForNum(items,ids)
            ids = foundIds
            itemList = [item for item in items if item["id"] in foundIds]
            for item in itemList:
                logger.log(f"Vous allez supprimer : {logger.StatisticStatement(f"{item["code"]}    {item["nom_dossier"]}")}")
        except Exception as e:
            logger.error(f"json loads couldn't resolve {e}")
    if not f and len(foundIds) > 0:
        answer = typer.prompt(f"Est-ce bien les dossiers à supprimer ? [O]ui/[N]on ")
        if answer.lower() != "o" and answer.lower() != "oui":
            typer.echo("Annulation de la requête...")
            raise typer.Abort()
    for item_id in ids:
        response, status_code = api.delete(item_id)
        if utils.valid(status_code):
            logger.success(f"Élément {item_id} supprimé")
        else:
            logger.error(f"Erreur lors de la suppression de l'élement {item_id}")
            
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
        if not mute: logger.statistic(f"Éléments récupérés : {len(items)}")
        return response
    else: 
        if not mute: logger.error(f"Erreur lors de la récupération de la liste de {api_type}")

@app.command()
def exportSilae(domain: str, numeros: Optional[List[str]]) -> Optional[str]:
    logger.success("================== Export Start Session ==================")
    start = time.time()
    step = 0
    log_file_suffix = f"{domain}_{datetime.today().strftime('%Y%m%d%H%M')}"
    # log_file_suffix = datetime.today().strftime('%Y-%m-%d_%Hh%Mm%Ss')
    
    logger.progress(f"STEP {step} ==== Vérification Dossiers Existants  ====")
    if len(numeros) > 0:
        numeros = utils.clearList(numeros)
        listString = getList(domain, opapi.__DOSSIERS__, mute=True)
        items = json.loads(listString)
        foundIds = utils.getIdForNum(items, numeros)
        if len(foundIds) > 0:
            logger.error(f"un ou plusieurs dossiers cible de la migrations sont déjà présent sur le domaine : {[item["code"] for item in items if item["id"] in foundIds]}")
            raise typer.Abort()
    logger.progress(f"STEP {step} FIN ==== Vérifications Dossiers Existants ====")

    step += 1
    
    logger.progress(f"STEP {step} ==== Export des dossiers depuis Silae ====")
    dossiersMap = silae.getDossiers(domain)
    if len(numeros) > 0:
        newDossiers: JSON = {}
        newDossiers = {numero: dossier for numero, dossier in dossiersMap.items() if numero in set(numeros)}
        typer.echo(f"Liste de numeros de dossiers indiquées, récupération avec succès de {len(newDossiers)} dossiers depuis Silae")
        dossiersMap = newDossiers
    dossiersDetails = silae.getDossiersDetails(domain, dossiersMap)
    logger.log(f"STEP {step} ======== Parsing des dossiers ========")
    op_dossiersList = parser.parseDossiers(domain, dossiersMap, dossiersDetails)
    dossiersCrees = creerMultiples(domain, opapi.__DOSSIERS__, op_dossiersList)
    codesDict = dict(list(map(lambda dossier: (dossier["code"],dossier["id"]), dossiersCrees)))
    logger.progress(f"STEP {step} FIN ======== {len(dossiersCrees)} Dossiers Créés sur le domaine {domain} openpaye ======== \n")
    
    step+=1
    
    logger.progress(f"STEP {step} ======== Export des Etablissements depuis Silae  ======== ")
    # Etablissements
    if len(dossiersCrees) < len(op_dossiersList):
        logger.error("Problème de création de dossiers, voir les logs pour identifier le problème")
        raise typer.Abort()
    etabMap = silae.getInfosEtablissements(domain, dossiersMap)
    eta_DetailsMap = silae.getEtablissementDetails(domain, etabMap)
    logger.log(f"STEP {step} ==== Parsing des Etablissements ====")
    op_Etablissements = parser.parseEtablissements(etabMap,eta_DetailsMap, codesDict)
    etabCrees = creerMultiples(domain, opapi.__ETABLISSEMENTS__,op_Etablissements)
    logger.progress(f"STEP {step} ======== {len(etabCrees)} Etablissements Créés sur le domaine {domain} openpaye ======== \n")

    step+=1

    logger.progress(f"STEP {step} ======== Export des Organismes depuis Silae  ======== ")
    # Organismes
    etabDict = parser.buildEtabDict(op_Etablissements,etabCrees,codesDict)
    organismesMap = silae.getOrganismesList(domain, codesDict)
    op_organismes = parser.parseOrganismes(organismesMap,etabDict)
    utils.list_to_excel([organisme["data"] for organisme in op_organismes],f".\\data\\out\\migration_log\\{domain}\\{log_file_suffix}_organismesMap.xlsx",)
    organismesCrees = []
    # organismesCrees = creerMultiples(domain,opapi.__CAISSECOTISATIONS__,op_organismes)
    logger.progress(f"STEP {step} FIN ======== {len(organismesCrees)} Organismes Créés sur le domaine {domain} openpaye ======== \n")
    
    step+=1
    
    logger.progress(f"STEP {step} ======== Export des Salariés depuis Silae  ======== ")
    # Salaries
    sal_DetailsMap = silae.getInfosSalaries(domain,codesDict) # return map[numero][matricule] = salariesdetails
    logger.log(f"STEP {step} ==== Parsing des Salariés ==== ")
    op_salaries = parser.parseSalaries(sal_DetailsMap,codesDict) # return list[salDict]
    salariesCrees = creerMultiplesParLots(domain,opapi.__SALARIES__,op_salaries,taille_lot=50) # return list[salDict + ['id']] 
    logger.progress(f"STEP {step} ======== {len(salariesCrees)} Salariés créés sur le domaine {domain} openpaye ======== \n")

    step+=1
    
    logger.progress(f"STEP {step} ======== Export des Contrats depuis Silae  ======== ")
    # Emploi/Contrat
    emp_detailsMap = silae.getInfosEmplois(domain,sal_DetailsMap)
    logger.progress(f"STEP {step} ==== Parsing des Contrats ==== ")
    op_contrats = parser.parseEmplois(emp_detailsMap, sal_DetailsMap,eta_DetailsMap,codesDict)
    contratsCrees = creerMultiplesParLots(domain,opapi.__CONTRATS__,op_contrats,taille_lot=50)
    logger.progress(f"STEP {step} ======== {len(op_contrats)} Contrats créés sur le domaine {domain} openpaye ======== \n")
    
    step+=1
    
    # logger.progress(f"STEP {step} ======== Export des Cumuls depuis Silae  ======== ")
    # matriculeContratId = dict()
    # for op_contrat in op_contrats:    
    #     dossierId = op_contrat["params"]["dossierId"]
    #     contratData = op_contrat["data"]
    #     contrat = [contratCree for contratCree in contratsCrees if (contratCree["code_etablissement"], contratCree["matricule_salarie"], contratCree["numero_contrat"]) == (contratData["code_etablissement"],contratData["matricule_salarie"],contratData["numero_contrat"])][0]
    #     numero = [numero for numero,id in codesDict.items() if id == dossierId][0]
    #     key = f"{numero}{contrat["code_etablissement"]}{contrat["matricule_salarie"]}{contrat["numero_contrat"]}"
    #     matriculeContratId[key] = {
    #         "id":contrat["id"],
    #         "date_debut_contrat":contrat["date_debut_contrat"],
    #     }
    # logger.log(matriculeContratId)
    # cumul_detailsMap = silae.getCumulsContrats(domain,codesDict)
    # logger.log(f"STEP {step} =========== Parsing des Cumuls ")
    # op_cumuls, op_contratsIdToDSN = parser.parseCumuls(cumul_detailsMap, emp_detailsMap, matriculeContratId)
    # logger.log(f"STEP {step} =========== Insertion des Cumuls ")
    # cumulsCrees = creerMultiples(domain,opapi.__VARIABLESREPRISEDOSSIER__, op_cumuls)
    # logger.log(f"STEP {step} =========== Modification des Contrats")
    # up_op_contrats = parser.updateContrats(contratsCrees,op_contratsIdToDSN)
    # logger.log(f"{len(up_op_contrats)} contrats à modifier")
    # _ = updateMultiples(domain,opapi.__CONTRATS__, up_op_contrats)
    # logger.progress(f"STEP {step} ======== {len(cumulsCrees)} Cumuls créés sur le domaine {domain} openpaye ======== \n")
    
    updateCumuls(domain,numeros)
    
    readAndLog(domain,opapi.__DOSSIERS__+"_Target", numeros,log_file_suffix,directLog=True)
    readAndLog(domain,opapi.__DOSSIERS__, dossiersCrees,log_file_suffix)
    readAndLog(domain,opapi.__CAISSECOTISATIONS__+"_ajout_manuel",op_organismes,log_file_suffix,directLog=True)
    readAndLog(domain,opapi.__ETABLISSEMENTS__, etabCrees,log_file_suffix)
    readAndLog(domain,opapi.__SALARIES__, salariesCrees,log_file_suffix)
    readAndLog(domain,opapi.__CONTRATS__,contratsCrees,log_file_suffix)
    
    duration = time.time()-start
    logger.success(f"Application took {duration:.3f}s to finish")
    logger.success("================== Export Start Session ==================")

@app.command()
def updateCumuls(domain: str, numeros:List[str]):
    logger.progress("================== update cumul Start Session ==================")
    start = time.time()
    if numeros == 0:
        raise typer.Abort("argument numeros vide")

    step = 1
    logger.progress(f"STEP {step} ==== Récupération des Dossiers ====")
    dossiersList = json.loads(getList(domain,opapi.__DOSSIERS__,mute=True))
    dossiersList = [dossier for dossier in dossiersList if dossier["code"] in numeros]
    logger.log(dossiersList)
    codesDict = dict(list(map(lambda dossier: (dossier["code"],dossier["id"]), dossiersList)))
    logger.progress(f"STEP {step} FIN ======== Récupération des Dossiers ======== \n")
    
    step+=1
    logger.progress(f"STEP {step} =========== Récupération des Salaries et emplois ======== ")
    sal_DetailsMap = silae.getInfosSalaries(domain,codesDict)
    emp_detailsMap = silae.getInfosEmplois(domain,sal_DetailsMap)
    logger.progress(f"STEP {step} FIN ======== Récupération des Salaries et emplois ======== \n")
    
    step+=1
    logger.progress(f"STEP {step} ======== Récupération des Contrats ======== ")
    contratsList = dict()
    for dossier in dossiersList:
        contratListStr = getList(domain, opapi.__CONTRATS__,dossierId=dossier["id"],mute=True)
        if contratListStr:
            contratsList[dossier["code"]] = json.loads(contratListStr)["contrats"]
    logger.progress(f"STEP {step} FIN ======== Récupération des Contrats ======== \n")
    
    step+=1
    logger.progress(f"STEP {step} ======== Export des Cumuls depuis Silae  ======== ")

    dosMatrToContratNum = dict()
    for numero, contrats in contratsList.items():
        dosMatrToContratNum[numero] = {}
        for contrat in contrats:
            matricule = contrat["matricule_salarie"]
            emplois = emp_detailsMap[numero][matricule]
            dosMatrToContratNum[numero][matricule] = {}
            for emploi in emplois:
                numeroContrat = emploi["SEM_DSNNumeroContrat"]
                if numeroContrat == "": numeroContrat = "vide"
                dosMatrToContratNum[numero][matricule].setdefault(numeroContrat, []).append({
                    "id": contrat["id"],
                    "date_debut_contrat":contrat["date_debut_contrat"]
                })

    cumul_detailsMap = silae.getCumulsContrats(domain,codesDict)
    logger.log(f"STEP {step} =========== Parsing des Cumuls")
    op_cumuls, op_contratsIdToDSN = parser.parseCumuls(cumul_detailsMap, emp_detailsMap, dosMatrToContratNum)

    logger.log(f"STEP {step} =========== Modification des Contrats")
    up_op_contrats = parser.updateContrats(contratsList,op_contratsIdToDSN)
    logger.log(f"{len(up_op_contrats)} contrats à modifier")
    _ = updateMultiples(domain,opapi.__CONTRATS__, up_op_contrats)

    logger.log(f"STEP {step} =========== Insertion des Cumuls ")
    cumulsCrees = creerMultiplesParLots(domain,opapi.__VARIABLESREPRISEDOSSIER__, op_cumuls)
    logger.progress(f"STEP {step} ======== {len(cumulsCrees)} Cumuls créés sur le domaine {domain} openpaye ======== \n")
    
    logger.statistic(f"Application took {time.time() - start}s to finish")
    logger.progress("================== Application Finish Session ==================")

if __name__ == "__main__":
    with keep.running():
        logger.log(f"Mise en relation avec l'API E2RH...")
        try:
            silae.ping()
        except Exception as e:
            logger.error(f"Le serveur est OFF ou n'est pas accessible")
            exit(1)
        extract.load_translation_file()
        dotenv.load_dotenv()
        app()