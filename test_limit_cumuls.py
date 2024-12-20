import time
import json
import opapi
import utils
import logger
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from parser import dataWithParams
from typerscript import load_api,creerMultiples


def startLimitTesting(count):
    dossierID = 40592
    contratID = 277601
    cumulBench = []
    
    for _ in range(count):
        params = dict()
        params["contratId"] = contratID
        params["nomVariable"] = "$SAL.CUMULANT_HRS"
        params["valeur"] = str(float("0"))
        cumulBench.append(dataWithParams(None, params))
        
    # start = time.time()
    # creerMultiples("E2RH",opapi.__VARIABLESREPRISEDOSSIER__,cumulBench)
    # timeCurrent = time.time()-start
    start = time.time()
    creerMultiplesParLots("E2RH",opapi.__VARIABLESREPRISEDOSSIER__,cumulBench)
    timeParLot = time.time()-start
    # logger.progress(f"current : {count} cumuls took {timeCurrent:.3f}s to complete")
    logger.progress(f"par lots : {count} cumuls took {timeParLot :.3f}s to complete")

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
                    response, status_code = api.create_with_retry(api, item, params)
                    if utils.valid(status_code):
                        if item_type == opapi.__VARIABLESREPRISEDOSSIER__:
                            successList.append(response)
                            logger.success(f"{item_type} variable : {params["contratId"]} {params["nomVariable"]} = {response} Créés avec succès")
                        else:
                            createdItem = json.loads(response)
                            successList.append(createdItem)         
                            logger.success(f"{item_type} id {createdItem["id"]} Créés avec succès")
                    else:
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


if __name__ == "__main__":
    startLimitTesting(500)