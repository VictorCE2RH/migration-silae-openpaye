import json
import opapi


def dossierDelete(domain: str, file: str):
    path = "C:\\Users\\e2rh0\\Victor_E2RH\\workspace\\open-paye-migration\\data\\out\\"
    path = f"{path.strip()}\\{file}"
    with open(path, "r") as fp:
        jsonFile = json.load(fp)
    listCodes: list[str] = jsonFile.get("POSTED")
    deleteSavedDossiers(domain, set(listCodes))


def deleteSavedDossiers(domain: str, setCodes: set[int]):
    listId: list[int] = []
    dossiers = opapi.getAllDossiers(domain)
    for dossier in dossiers:
        if dossier.code in setCodes:
            if dossier.siret == None:
                listId.append(dossier.id)
            else:
                print(f"leaving {dossier.code} in the list")
                break
    opapi.deleteDossiers(domain, listId)
