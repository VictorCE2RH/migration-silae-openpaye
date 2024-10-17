import pandas as pd


def contactsColonnes():
    colonnes = [
        "Numéro interne",
        "Raison sociale",
        "Adresse",
        "Code postal",
        "Ville",
        "E-mail",
        "Téléphone",
        "Siret",
        "Code NAF",
        "Agence",
        "Employeur",
        "Qualité",
        "Expert comptable",
        "Chef de mission",
        "Collaborateur comptable",
        "Collaborateur paie",
    ]
    
    return colonnes

def excel_vers_dictionnaire_multi_colonnes(
    fichier_excel: str, ligneEntete: int, colonne_cle: str, colonnes_valeurs: list[str]
) -> dict[str, dict[str, str]]:
    file = r"C:\Users\e2rh0\Victor_E2RH\workspace\open-paye-migration\data"
    file += f"\\{fichier_excel}"
    skip = ligneEntete - 1
    df = pd.read_excel(file, skiprows=skip)
    df.fillna("")

    if colonne_cle not in df.columns:
        raise ValueError(
            f"La colonne clé '{colonne_cle}' n'existe pas dans le fichier."
        )

    for colonne in colonnes_valeurs:
        if colonne not in df.columns:
            raise ValueError(f"La colonne '{colonne}' n'existe pas dans le fichier.")

    # Créer le dictionnaire avec la colonne clé et les autres colonnes en sous-dictionnaires
    dictionnaire: dict[str, dict[str, str]] = (
        df.fillna("").set_index(colonne_cle)[colonnes_valeurs].to_dict(orient="index")
    )

    return dictionnaire
