import pandas as pd
import numpy as np
import statut_pro
from typing import Optional


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


def editionCumulColonnes():
    prefixShort = "$SAL."
    prefixDos = "$DOS."
    prefix = prefixShort + "CUMULANT_"
    colonnes = {
        prefix + "HRS": "Heures",
        prefix + "HRSSUP": "HeuresSupp",
        prefix + "BRUT": "Brut",
        prefix + "NET": "Netàpayer",
        prefix + "NETIMPO": "Netimposable",
        prefix + "ABAT": "Abattement",
        prefix + "PMSS": "PMSS",
        prefix + "TA": "TrancheA",
        prefix + "TB": "TrancheB",
        prefix + "TC": "TrancheC",
        prefix + "T2": "Tranche2AFIRCARRCO",
        prefix + "SMICFILLON": "SMICFILLOn",
        prefix + "RNF": "MontantnetfiscaléxonérationsurHSHC",
        prefix + "CP": "ChargesPatronales",
        prefix + "MTPAS": "RetenueAlasource",
        prefix + "BASECPN1": "BaseCPN1",
        prefix + "BASECPPRISN1": "BaseCPPrisN1",
        prefix + "CPN1": "JoursAcquisN1",
        prefix + "CPPRISN1": "JoursPrisN1",
        prefix + "BASECPN": "BaseCPN",
        prefix + "BASECPPRISN": "BaseCPPrisN",
        prefix + "CPN": "JoursAcquisN",
        prefix + "CPPRISN": "JoursPrisN",
        prefixShort + "RTTACQUIS": "RTTACQUIS",
        prefixShort + "RTTPRIS": "RTTPRIS",
    }
    # prefixDos + "DATEREPRISE"  : "DateReprise"
    # AUTRES COLONNES :
    # "BaseCPSoldeN"
    # "BaseCPSoldeN1"
    # "JoursSoldeN1"
    # "JoursSoldN"
    # "RTTSOLDE"
    # "Nom"
    # "Numérodecontrat"
    # "Datededébutdecontrat"
    # "Datededébutdemploi"
    # "SMICheurestravaillées"
    # "TotalReductionGénéraleUrssaf"
    # "TotalReductionGénéraleRetraite"
    return colonnes


def excel_vers_dictionnaire_multi_colonnes(
        fichier_excel: str, ligneEntete: int, colonne_cle: str, colonnes_valeurs: list[str]
) -> dict[str, dict[str, str]]:
    file = r"C:\Users\e2rh0\Victor_E2RH\workspace\open-paye-migration\data\in"
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
            raise ValueError(
                f"La colonne '{colonne}' n'existe pas dans le fichier.")

    # Créer le dictionnaire avec la colonne clé et les autres colonnes en sous-dictionnaires
    dictionnaire: dict[str, dict[str, str]] = (
        df.fillna("").set_index(colonne_cle)[
            colonnes_valeurs].to_dict(orient="index")
    )

    return dictionnaire


def translateCodeV2(fichier_path, nom_feuille, criteres_recherche, defaultline):
    """
    Recherche des données dans un fichier Excel selon des index de colonnes.

    Args:
        fichier_path (str): Chemin du fichier Excel
        nom_feuille (str): Nom de la feuille Excel
        criteres_recherche (dict): Dictionnaire avec index colonnes et valeurs
            Ex: {0: 'valeur1', 2: 'valeur2'}

    Returns:
        DataFrame: Lignes correspondant aux critères
    """
    pd.set_option("display.precision", 0)
    try:
        df = pd.read_excel(fichier_path, sheet_name=nom_feuille, dtype=str)
        masque = pd.Series(True, index=df.index)

        for index_col, valeur in criteres_recherche.items():
            if index_col < len(df.columns):
                # print(f"searching {index_col} {valeur}")
                masque &= df.iloc[:, index_col].astype(
                    str).str.contains(str(valeur), case=False, na=False)
                # print(df.iloc[:, index_col][masque]) 
                
        if not masque.any():  # aucune correspondance
            return defaultline
            
        return df[masque].to_dict('records')[0]

    except Exception as e:
        print(f"Erreur lors de la recherche: {str(e)}")
        return defaultline


def translateCode(
        chemin_fichier: str,
        code_recherche: any,
        nom_feuille: str,
        colonne_source: int = 0,
        colonnes_cible: list[int] = [1],
        default_value: Optional[any] = None,
) -> list[str]:
    pd.set_option("display.precision", 0)
    df = pd.read_excel(chemin_fichier, sheet_name=nom_feuille, dtype=str)
    
    maskedDf = df[df.iloc[:, colonne_source] == str(code_recherche)]

    resultats = []
    for colonne_cible in colonnes_cible:
        res = maskedDf.iloc[:, colonne_cible]
        if not res.empty and res.iloc[0] != np.nan:
            res = res.iloc[0]
        else:
            # In cases colonne_cible has >1 items we need to return list of default
            if isinstance(default_value, tuple):
                return list(default_value)
            res = str(default_value)
        resultats.append(res)

    return resultats


def translateCodes(chemin_fichier: str, colonnes: list[str], valeurs: list[str], nom_feuille: str, colonne_cible: int, default_res: Optional[str] = None) -> Optional[int]:
    """
    Récupère la valeur dans la colonne cible où les colonnes de conditions ont des valeurs spécifiques.

    Parameters:
    df (pd.DataFrame): Le DataFrame dans lequel chercher
    colonnes_conditions (list): Les colonnes de conditions à vérifier
    valeurs_conditions (list): Les valeurs recherchées dans les colonnes de conditions
    colonne_cible (str): La colonne cible à partir de laquelle récupérer la valeur

    Returns:
    La valeur correspondante dans la colonne cible, ou None si aucune correspondance
    """
    pd.set_option("display.precision", 0)
    df = pd.read_excel(chemin_fichier, sheet_name=nom_feuille, dtype=str)
    # Initialise avec True pour chaque ligne
    masque = pd.Series([True] * len(df))
    for col, val in zip(colonnes, valeurs):
        masque &= df.iloc[:, col] == str(val)
    resultat = df.iloc[masque.values, colonne_cible]
    resultat = df.iloc[masque.values, colonne_cible]

    resultat = df.iloc[masque.values, colonne_cible]

    return int(resultat.iloc[0]) if not resultat.empty else default_res


_tradFile = r"C:\Users\e2rh0\Victor_E2RH\workspace\open-paye-migration\data\in\traduction_code_silae_openpaye.xlsx"


def codeTravail(code: str = None, motif: str = None, typeContrat: int = None, emploiPart: str = None, default_value=None):
    colIndex = []
    values = []
    if code and code.isdigit():
        colIndex.append(1)
        values.append(str(int(code)))
    else:
        raise Exception("code must exist")
    if motif and motif.isdigit():
        colIndex.append(2)
        values.append(motif)
    if typeContrat and typeContrat != 10:
        colIndex.append(3)
        values.append(str(typeContrat))
    if emploiPart and emploiPart[:2].isdigit():
        colIndex.append(4)
        values.append(emploiPart)

    return translateCodes(
        _tradFile,
        colIndex,
        values,
        "type_contrat_travail",
        5,
        default_res=default_value,
    )


def situationFamiliale(codeSilae: int):
    return translateCode(
        chemin_fichier=_tradFile,
        code_recherche=str(codeSilae),
        nom_feuille="situation_familliale",
        default_value=10,
    )[0]


def statutProf(codeTravail):
    return int(translateCode(
        chemin_fichier=_tradFile,
        code_recherche=codeTravail,
        nom_feuille="statut_professionnel",
        default_value=90,
    )[0])


def emploiCCN(classification, statutPro, ccn):
    criteres = {
        0: classification,
        1: statutPro,
    }
    default = {
        "sCode": classification,
        "StatutProfessionnel": statutPro,
        "CCN": ccn,
        "empCode": 9999,
        "statutPro": statut_pro.PAS_STATUT,
        "Libellé": "-"
    }
    res = translateCodeV2(fichier_path=_tradFile, nom_feuille="emploiCCN", criteres_recherche=criteres, defaultline=default)

    return [int(res["CCN"]), int(res["empCode"]), res["statutPro"]]


def idccToOpcc(idcc):
    if isinstance(idcc, str) and idcc.isdigit():
        idcc = int(idcc)
    res = translateCode(
        chemin_fichier=_tradFile, code_recherche=idcc, nom_feuille="IDCCvsOPCC"
    )[0]
    print(f"IDCC {idcc} OPCC {res}")
    if isinstance(res, str) and res.isdigit():
        return int(res)
    return None


def qualite(code: str, default: str):
    return translateCode(
        chemin_fichier=_tradFile,
        code_recherche=code,
        nom_feuille="qualité",
        default_value=default
    )[0]

