# Libs
import dotenv
import typer
import json
from typing import Optional
from datetime import datetime

# files
from OP_registre import OPDossier
import silae
import parser
import extract
import opapi

app = typer.Typer()


def saveJsonData(name: str, dataJson: any):
    data_repo = ".\\data"
    jsonFile = f"{data_repo}\\{name}.json"
    with open(jsonFile, "w") as fp:
        json.dump(dataJson, fp, indent=4)


# Fonction générique pour charger l'API en fonction du type choisi
def load_api(domain: str, api_type: str):
    api_class = opapi.api_map.get(api_type.lower())
    if not api_class:
        raise typer.Exit(f"Type '{api_type}' non supporté")
    return api_class(opapi.openpaye_auth(domain))


@app.command()
def create(domain: str, api_type: str, fromJson: str):
    """
    Créer des éléments dans l'API OpenPaye pour un type donné (dossiers, etablissements, etc.).
    """
    api = load_api(domain, api_type)
    # Charger les données à partir du fichier ou d'un autre source
    item = json.loads(fromJson)
    if not item:
        typer.echo("Aucun fichier fourni")
        raise typer.Exit()

    item = api.create(item)
    if item:
        typer.echo(f"Element Ajouté dans OpenPaye")
        return True
    return None

@app.command()
def read(domain: str, api_type: str, item_id: str):
    """
    Lire un élément spécifique par ID depuis l'API OpenPaye.
    """
    api = load_api(domain, api_type)
    item = api.get(item_id)
    typer.echo(f"Élément récupéré : {item}")


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
    saveJsonData(f"res_{domain}_{api_type}", data)
    if success:
        typer.echo(f"Élément {item_id} mis à jour avec succès")
    else:
        typer.echo(f"Erreur lors de la mise à jour de {item_id}")


@app.command()
def delete(domain: str, api_type: str, item_id: str):
    """
    Supprimer un élément par ID dans l'API OpenPaye.
    """
    api = load_api(domain, api_type)
    success = api.delete(item_id)
    if success:
        typer.echo(f"Élément {item_id} supprimé avec succès")
    else:
        typer.echo(f"Erreur lors de la suppression de {item_id}")


@app.command()
def getList(domain: str, api_type: str):
    api = load_api(domain, api_type)
    items = api.list()

    saveJsonData(f"res_{domain}_{api_type}", items)
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
    print("test Appel autres commandes : list")
    dossiersMap = silae.getDossier(domain)
    file = f"list-employeurs-{domain}.xlsx"
    contactMap = extract.excel_vers_dictionnaire_multi_colonnes(
        file, 3, "Dossier", extract.contactsColonnes()
    )
    openpaye_dossiers = parser.parseDossiers(dossiersMap, contactMap, max)
    if not fakeit:
        codes = creerMultiples(domain, "Dossiers", openpaye_dossiers)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fileName = f"export_dossiers_{timestamp}"
        if len(codes) > 0:
            saveJsonData(fileName, codes)


def creerMultiples(
    domain: str, item_type:str, items: list[dict[str, str]]
) -> dict[str, list[str]]:
    print(f"Tentative d'ajout de {len(items)} Dossiers vers l'API openpaye")
    successList: list[str] = []
    for item in items:
        try:
            jsonStr = json.dumps(item)
            print(jsonStr)
            if create(domain, item_type, jsonStr):
                successList.append(item.get("code"))
            else:
                print(f"Dossier {item.get("code")}, erreur lors de l'import")
        except Exception as e:
            print(f"Exception lors de l'envoi du dossier {item.get('code')}: {e}")

    return successList

def deleteMultiples(domain: str, item_type:str, listIds: list[str]):
    print(
        f"Tentative de suppression de {len(listIds)} dossiers depuis l'API openpaye"
    )
    for id in listIds:
        try:
            if delete(domain, item_type, id):
                print(f"Suppression {item_type} ({id}) sur {domain} Réussie")
        except Exception as e:
            print(f"DeleteDossiers : Exception Raised {e}")

if __name__ == "__main__":
    print("================== Application Start Session ==================")
    dotenv.load_dotenv()
    app()
