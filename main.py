# Libs
import dotenv
import typer
import json
from typing import Optional, List
from datetime import datetime
from itertools import islice

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
def create(domain: str, api_type: str, fromJson: str) -> str:
    """
    Créer des éléments dans l'API OpenPaye pour un type donné (dossiers, etablissements, etc.).
    Renvois le json de l'objet créé si succès
    """
    api = load_api(domain, api_type)
    # Charger les données à partir du fichier ou d'un autre source
    item = json.loads(fromJson)
    if not item:
        typer.echo("Aucun fichier fourni")
        raise typer.Exit()

    response = api.create(item)
    if item:
        typer.echo(f"Element Ajouté dans OpenPaye")
        return response
    return None


@app.command()
def read(domain: str, api_type: str, item_ids: List[str]) -> Optional[str]: 
    """
    Lire un ou plusieurs éléments spécifique par ID depuis l'API OpenPaye.
    """
    api = load_api(domain, api_type)
    itemList:List[str] = []
    for item_id in item_ids:
        item = api.read(item_id)
        if not item:
            typer.echo(f"Item {item_id} does not exist in the database")
            raise typer.Abort(item_id)
        itemList.append(item)
        typer.echo(f"Lecture item : {utils.formatJson(item)}")
    if len(itemList) == 0:
        return None
    return ','.join(itemList)

@app.command()
def update(domain: str, api_type: str, item_id: str, file: Optional[str] = None):
    """
    Mettre à jour un élément existant dans l'API OpenPaye.
    """
    api = load_api(domain, api_type)

    if file:
        # Charger les nouvelles données
        data = load_data_from_file(file)
    else:
        typer.echo("Aucun fichier de mise à jour fourni")
        raise typer.Exit()

    success = api.update(item_id, data)
    utils.saveJsonData(f"res_{domain}_{api_type}", data)
    if success:
        typer.echo(f"item id {item_id} mis à jour avec succès")
    else:
        typer.echo(f"Erreur lors de la mise à jour de {item_id}")


@app.command()
def delete(domain: str, api_type: str, item_ids: List[str], askUser: bool=True):
    """
    Supprimer un élément par ID dans l'API OpenPaye.
    """
    api = load_api(domain, api_type)
    typer.echo(f"Tentative de suppression d'item(s) {api_type} {item_ids} : ")
    read(domain, api_type, item_ids)
    if askUser == True:
        answer = typer.prompt(
            f"Confirmez la suppression de(s) item(s) ci-dessus : [O]ui/[N]on "
        )
    if answer.lower() != "o" and answer.lower() != "oui":
        typer.echo("Annulation de la requête...")
        return
    for item_id in item_ids:
        api.delete(item_id)
        typer.echo(f"Élément {item_id} supprimé avec succès")


@app.command()
def getList(domain: str, api_type: str):
    api = load_api(domain, api_type)
    response = api.list()
    items = json.loads(response)
    utils.saveJsonData(f"res_{domain}_{api_type}", items)
    typer.echo(f"Éléments récupérés : {len(items)}")


# Fonction utilitaire pour charger les données du fichier
def load_data_from_file(file_path: str):
    # Exemple de chargement JSON ou Excel
    if file_path.endswith(".json"):
        with open(file_path, "r") as f:
            return json.load(f)
    elif file_path.endswith(".xlsx"):
        import pandas as pd

        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")
    else:
        typer.echo("Format de fichier non supporté")
        raise typer.Exit()


@app.command()
def exportSilae(domain: str, fakeit: bool = True, max: int = -1):
    typer.echo("Export des dossiers depuis Silae")
    dossiersMap = silae.getDossiers(domain)
    if max > 0:
        i = 0
        newDossiers: dict[str, any] = {}
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
    etabMap = silae.getInfosEtablissements(domain, dossiersMap)
    # extraInfos = silae.getEtablissementsExtrasInfos(domain)
    op_etabList = parser.parseEtablissements(domain, etabMap, contactMap)
    utils.saveJsonData(opapi.__ETABLISSEMENTS__, op_dossiersList)

    if not fakeit:
        dossiersCrees = creerMultiples(domain, opapi.__DOSSIERS__, op_dossiersList)
        codeList = map(dossiersCrees.get, "id")
        utils.saveLogAction(opapi.__DOSSIERS__, codeList)
        codes_etab = creerMultiples(domain, opapi.__ETABLISSEMENTS__, op_etabList)


def creerMultiples(
    domain: str, item_type: str, items: list[dict[str, str]]
) -> list[JSON]:
    print(f"Tentative d'ajout de {len(items)} Dossiers vers l'API openpaye")
    successList: list[JSON] = []
    for item in items:
        try:
            jsonStr = json.dumps(item)
            print(jsonStr)
            response = create(domain, item_type, jsonStr)
            if response:
                jsonResp = json.loads(response)
                successList.append(jsonResp)
            else:
                print(f"Dossier {item.get("code")}, erreur lors de l'import")
        except Exception as e:
            print(f"Exception lors de l'envoi du dossier {item.get('code')}: {e}")

    return successList


def deleteMultiples(domain: str, item_type: str, listIds: list[str]):
    print(f"Tentative de suppression de {len(listIds)} dossiers depuis l'API openpaye")
    try:
        if delete(domain, item_type, [listIds], False):
            print(f"Suppression {item_type} ({id}) sur {domain} Réussie")
    except Exception as e:
        print(f"DeleteDossiers : Exception Raised {e}")


if __name__ == "__main__":
    print("================== Application Start Session ==================")
    dotenv.load_dotenv()
    res = app()
    print(f"Fin de l'execution {res}")
