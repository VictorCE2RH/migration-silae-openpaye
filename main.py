# Libs
import dotenv
import typer
import json
import sys
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
    api_class = opapi.api_map.get(api_type.lower())
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
    if not item:
        typer.echo("Aucun fichier fourni")
        raise typer.Exit()
    params = None
    if paramsJson:
        params = json.loads(paramsJson)
        response = api.create(item,params)
    if item:
        typer.echo(f"Ajouté dans OpenPaye : {json.dumps(item)}")
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
def update(domain: str, api_type: str, item_id: str, file: Optional[str] = None) -> Optional[str]:
    """
    Mettre à jour un élément existant dans l'API OpenPaye.
    """
    api = load_api(domain, api_type)

    try:
        data = utils.load_data_from_file(file)
    except Exception as e:
        typer.echo(f"Erreur interceptée {e}")
        raise typer.Exit()

    response = api.update(item_id, data)
    item = json.loads(response)
    if item:
        utils.saveJsonData(f"res_{domain}_{api_type}", item)
        typer.echo(f"item modifié : {utils.formatJson(item)}")
    else:
        typer.echo(f"Erreur lors de la mise à jour de {item_id}")
    return item

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
def exportSilae(domain: str,numeros: Optional[str], fakeit: bool = True, max: int = -1) -> Optional[str]:
    typer.echo("Export des dossiers depuis Silae")
    dossiersMap = silae.getDossiers(domain)
    if len(numeros) > 0:
        numList = numeros.split(',')
        typer.echo(f"numeros = {numList}")
        newDossiers: JSON = {}
        newDossiers = {numero: dossier for numero, dossier in dossiersMap.items() if numero in set(numList)}
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
            
    file = f"list-employeurs-{domain}.xlsx"
    contactMap = extract.excel_vers_dictionnaire_multi_colonnes(
        file,
        ligneEntete=3,
        colonne_cle="Dossier",
        colonnes_valeurs=extract.contactsColonnes(),
    )
    op_dossiersList = parser.parseDossiers(dossiersMap, contactMap, max)
    if not fakeit:
        dossiersCrees = creerMultiples(domain, opapi.__DOSSIERS__, op_dossiersList)
        codeDict = dict(list(map(lambda dossier: (dossier["code"],dossier["id"]), dossiersCrees)))
        
        if len(dossiersCrees) < len(op_dossiersList):
            #TODO: start modification with op_dossiersList
            typer.echo("Problème de création de dossiers, voir les logs pour identifier le problème")
            raise typer.Abort()
        
        # Etablissements
        etabMap = silae.getInfosEtablissements(domain, dossiersMap)
        eta_DetailsMap = silae.getEtablissementDetails(domain, etabMap) # return list[etabDict]
        op_Etablissements = parser.parseEtablissements(etabMap,eta_DetailsMap, codeDict) # return map[numero]
        etabCrees = creerMultiples(domain, opapi.__ETABLISSEMENTS__,op_Etablissements) # return list[etabDict + ['id']]
        print(f"{len(etabCrees)} Etablissements Créés sur le domaine {domain} openpaye")
        
        # Salaries
        sal_DetailsMap = silae.getInfosSalaries(domain,codeDict) # return map[numero][matricule] = salariesdetails
        op_salaries = parser.parseSalaries(sal_DetailsMap,codeDict) # return list[salDict]
        salariesCrees = creerMultiples(domain,opapi.__SALARIES__,op_salaries) # return list[salDict + ['id']] 
        print(f"{len(salariesCrees)} Salariés Créés sur le domaine {domain} openpaye")
        
        # Emploi 
        emp_detailsMap = silae.getInfosEmplois(domain,sal_DetailsMap)
        op_contrats = parser.parseEmplois(emp_detailsMap,codeDict)
        contratsCrees = creerMultiples(domain,opapi.__CONTRATS__,op_contrats)
        
@app.command()
def testSalaries(numero:str):
    codeDict = dict()
    codeDict[numero] = 27166
    silae.getInfosSalaries("E2RH", codeDict)
    
def creerMultiples(domain: str, item_type: str, items: dict) -> list[dict]:
    print(f"Tentative d'ajout de {len(items)} {item_type} vers l'API openpaye")
    successList: list[dict] = []
    for item in items:
        jsonStr = json.dumps(item["data"])
        jsonParams = json.dumps(item["params"])
        response = create(domain, item_type, jsonStr, jsonParams)
        if response:
            createdItem = json.loads(response)
            successList.append(createdItem)
        else:
            print(f"Exception lors de la création de l'item {item_type} {item.get('code')}")
            raise Exception("Interruption")

    return successList

currentDir: str

if __name__ == "__main__":
    print("================== Application Start Session ==================")
    
    print(f"Mise en relation avec l'API E2RH...")
    try:
        silae.ping()
    except Exception as e:
        print(f"Le serveur est OFF ou n'est pas accessible")
        exit(1)
    dotenv.load_dotenv()
    print(app())