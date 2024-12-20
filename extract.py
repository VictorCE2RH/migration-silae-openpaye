import pandas as pd
import numpy as np
import statut_pro as sp
import logger
import requests
from typing import Optional

IDCC_SHEET = "IDCCvsOPCC"

# Global dictionary to store sheets
_LOADED_SHEETS = {}

_tradFile = r"C:\Users\e2rh0\Victor_E2RH\workspace\open-paye-migration\data\in\traduction_code_silae_openpaye.xlsx"
def load_translation_file():
    """Load all sheets from the translation file into memory"""
    global _LOADED_SHEETS
    excel_file = pd.ExcelFile(_tradFile)
    for sheet_name in excel_file.sheet_names:
        _LOADED_SHEETS[sheet_name] = pd.read_excel(excel_file, sheet_name=sheet_name, dtype=str)
    excel_file.close()


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
        prefix + "CP": "ChargesPatronales",
        prefix + "MTPAS": "RetenueAlasource",
        # prefix + "RNF": "",
        prefixShort + "REDUCTIONURSSAF" : "TotalReductionGénéraleUrssaf",
        prefixShort + "REDUCTIONRETRAITE" : "TotalReductionGénéraleRetraite",
        prefix + "BASECPN1": "BaseCPN1",
        prefix + "BASECPPRISN1": "BaseCPPrisN1",
        prefix + "BASECPSOLDEN1": "BaseCPSoldeN1",
        prefix + "CPN1": "JoursAcquisN1",
        prefix + "CPPRISN1": "JoursPrisN1",
        prefix + "SOLDECPN1": "JoursSoldeN1",
        prefix + "BASECPN": "BaseCPN",
        prefix + "BASECPPRISN": "BaseCPPrisN",
        prefix + "BASECPSOLDEN": "BaseCPSoldeN",
        prefix + "CPN": "JoursAcquisN",
        prefix + "CPPRISN": "JoursPrisN",
        prefix + "SOLDECPN": "JoursSoldN",
        prefixShort + "RTTACQUIS": "RTTACQUIS",
        prefixShort + "RTTPRIS": "RTTPRIS",
        prefix + "RTTSOLDE": "RTTSOLDE",
        prefix + "DEFISCALISATIONHEURESSUPP": "MontantnetfiscaléxonérationsurHSHC"
    }    
    # HRS : HEURES/JOUR
    # HRSSUP : HEURES SUPP
    # BRUT : BRUT
    # NET : NET A PAYER
    # NETIMPO : NET IMPOSABLE
    # ABAT : ABATTEMENT
    # PMSS : PMSS
    # TA : TRANCHE A
    # TB : TRANCHE B
    # TC : TRANCHE C
    # T2 : TRANCHE 2 AGIRC-ARRCO
    # SMICFILLON : SMIC FILLON
    # CP : CHARGES PATRONALES
    # RNF : REVENU NET FISCAL
    # MTPAS : RETENUE A LA SOURCE
    # CPN : JOURS ACQUIS N
    # CPPRISN : JOURS PRIS N
    # SOLDECPN : JOURS SOLDE N
    # BASECPN : BASE CP N
    # BASECPPRISN : BASE CP PRIS N
    # BASECPSOLDEN : BASE CP SOLDE N
    # CPN1 : JOURS ACQUIS N-1
    # CPPRISN1 : JOURS PRIS N-1
    # SOLDECPN1 : JOURS SOLDE N-1
    # BASECPN1 : BASE CP N-1
    # BASECPPRISN1 : BASE CP PRIS N-1
    # BASECPSOLDEN1 : BASE CP SOLDE N-1
    # $SAL RTTACQUIS : RTT ACQUIS
    # $SAL RTTPRIS : RTT PRIS
    # $SAL RTTSOLDE : RTT SOLDE
    # $SAL REPOSACQUIS : REPOS ACQUIS
    # $SAL REPOSPRIS : REPOS PRIS
    # $SAL REPOSSOLDE : REPOS SOLDE
    # $SAL REDUCTIONURSSAF : Reduction URSSAF
    # $SAL REDUCTIONRETRAITE : Reduction Retraite
    # $SAL DEFISCALISATIONHEURESSUPP : Defiscalisation Heures Supp
    # $SAL SALAIRERETABLI : Salaire Retabli
    
    # AUTRES COLONNES :
    # prefixShort + "DEFISCALISATIONHEURESSUPP" : Defiscalisation Heures Supp
    # prefixShort + "SALAIRERETABLI" : Salaire Retabli
    # "Nom"
    # "Numérodecontrat"
    # "Datededébutdecontrat"
    # "Datededébutdemploi"
    # "SMICheurestravaillées"
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

def searchExcel(fichier_path, nom_feuille, criteres_recherche, defaultline=None) -> list[dict]:
    global _LOADED_SHEETS
    defaultRes = [defaultline] if defaultline else []
    try:
        df = _LOADED_SHEETS.get(nom_feuille)
        if df is None:
            return defaultRes
            
        masque = pd.Series(True, index=df.index)
        for index_col, valeur in criteres_recherche.items():
            if index_col < len(df.columns):
                masque &= df.iloc[:, index_col].astype(str).str.contains(str(valeur), case=False, na=False)
        
        if not masque.any():
            return defaultRes
        
        res = df[masque].fillna('').to_dict('records')
        if not res:
            return defaultRes
        return res
    except Exception as e:
        logger.error(f"Error searching in sheet: {str(e)}")
        return defaultRes

def translateCode(chemin_fichier: str,code_recherche: any,nom_feuille: str,colonne_source: int = 0,colonnes_cible: list[int] = None,default_value: Optional[any] = None) -> list[str]:
    pd.set_option("display.precision", 0)
    df = pd.read_excel(chemin_fichier, sheet_name=nom_feuille, dtype=str)
    
    maskedDf = df[df.iloc[:, colonne_source] == str(code_recherche)]

    colCibles = colonnes_cible if colonnes_cible != None else [1]
    
    resultats = []
    for colonne_cible in colCibles:
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

def translateCodes(chemin_fichier: str, colonnes: list[str], valeurs: list[str], nom_feuille: str, colonne_cible: int, default_res: Optional[int] = None) -> Optional[int]:
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

    return int(resultat.iloc[0]) if not resultat.empty else default_res

def formeJuridique(code: str):
    if len(code) != 4:
        if len(code) == 0:
            logger.warning(f"Forme juridique: vide")
        else: 
            logger.warning(f"Forme Juridique: '{code}' pas le bon format")
        return 1
    units = list(code)
    if units[0] in ['0','2']:
        return 3
    if units[0] in ['1','3','4','5','6','7','8','E']:
        return 1
    if units[0] == '9':
        return 2
    logger.warning(f"Forme Juridique: Aucune correspondance {code}")
    return 1

def codeTravail(code: str = None, motif: str = None, typeContrat: int = None, emploiPart: str = None, default_value=None):
    colIndex = []
    values = []
    if code and code.isdigit():
        colIndex.append(1)
        values.append(str(int(code)))
    else:
        logger.warning(f"codeTravail code is NONE {code} {motif} {typeContrat} {emploiPart}, returning Default 90")
        return default_value
    if motif and motif.isdigit():
        colIndex.append(2)
        values.append(motif)
    if typeContrat and typeContrat != 10:
        colIndex.append(3)
        values.append(str(typeContrat))
    if emploiPart and emploiPart[:2].isdigit():
        colIndex.append(4)
        values.append(emploiPart)
        
    default = int(code) if code and int(code) in [1,2,3,29,32,89] else default_value
    
    return translateCodes(
        _tradFile,
        colIndex,
        values,
        "type_contrat_travail",
        5,
        default_res=default,
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

def emploiCCN(classification:str, statutPro:str, ccn:int):
    criteres = {
        0: classification,
        1: statutPro,
    }
    default = [int(ccn),9999,sp.PAS_STATUT]
    if classification == '':
        logger.warning(f"EmploiCCN : Pas de Classification")
        return default
    rows = searchExcel(fichier_path=_tradFile, nom_feuille="emploiCCN", criteres_recherche=criteres, defaultline=None)
    res = None
    if len(rows) == 0:
        logger.log(f"{criteres} Aucun résultats trouvées. Recherche Classifications correspondantes...")
        criteres = {
            0: classification
        }
        rows = searchExcel(fichier_path=_tradFile, nom_feuille="emploiCCN", criteres_recherche=criteres, defaultline=None)
        emp = None
        if len(rows) == 0:
            return default
    if len(rows) == 1:
        res = rows[0]
        logger.progress(f"Classification trouvée : {res['Statut Professionnel']}")
        try:
            opcc = int(res["OPCC"])
            code = int(res["Code"]) if res["Code"] != '' else 9999
            statut = res["Statut"] if res["Statut"] != '' else sp.PAS_STATUT
            return [opcc, code, statut]
        except Exception as e:
            logger.error(f"Exception string to int conversion : {e}")
            logger.warning(f"Application ccn emploi default : '{default}'")
            return default
    for row in rows:
        logger.statistic(f"toutes lignes correspondantes : {row}")
        if row['code silae'] == classification and row['Statut Professionnel'] == statutPro:
            res = row
    if not res:
        logger.warning(f"Aucune Ligne correspondante à {criteres}")
        return default 
    opcc = int(res["OPCC"])
    code = int(res["Code"]) if res["Code"] != '' else 9999
    statut = res["Statut"] if res["Statut"] != '' else sp.PAS_STATUT
    
    return [opcc, code, statut]

def civilite(civilite):
    if isinstance(civilite,str) and civilite.isdigit():
        civilite = int(civilite)
    res = translateCode(chemin_fichier=_tradFile,code_recherche=civilite, nom_feuille="civilite",default_value=None)[0]
    if isinstance(res,str) and res.isdigit():
        return int(res)
    return None

def _existInTradFile(data,sheet_name):
    criteres = {0: data}
    rows = searchExcel(fichier_path=_tradFile, nom_feuille=sheet_name, criteres_recherche=criteres, defaultline=None)
    return len(rows) != 0

def translateToOpcc(ccn, idcc, userInput:bool = False):
    if idcc == '':
        return None
    idccStr = str(idcc).zfill(4)
    ccnSupported = _existInTradFile(ccn, IDCC_SHEET)
    if not ccnSupported:
        logger.warning(f"La CCN {ccn} n'est pas supporté dans cette version du fichier")
    criteres = {
        1: idccStr
    }
    rows = searchExcel(fichier_path=_tradFile, nom_feuille=IDCC_SHEET, criteres_recherche=criteres, defaultline=None)
    if len(rows) == 0:
        return None
    if len(rows) == 1:
        return rows[0]["opcc"]
    if userInput and ccn in ["T026","R003","H019","V001","V002"]:
        msg = f"CCN Cas specifique : entrer l'index pour selectionner le code à utiliser :"
        for i,row in enumerate(rows):
            msg += f"\n{i} : {row}"
        msg += "\nVotre Choix : "
        choice = input(logger.ProgressStatement(msg))
        if choice.isdigit():
            logger.success(f"Selection de : {rows[int(choice)]}")
            return int(rows[int(choice)]["opcc"])
        else:
            raise Exception("Entrer un entier")
    for row in rows:
        if row["ccn"] == ccn: 
            return int(row["opcc"])
        
    logger.warning(f"aucun code correspondant avec silae code {ccn} {rows}")
    return None

def opccToIdcc(opcc):
    if isinstance(opcc, str) and opcc.isdigit():
        opcc = int(opcc)
    res = translateCode(chemin_fichier=_tradFile, code_recherche=opcc,colonne_source=1,colonnes_cible=[0], nom_feuille="IDCCvsOPCC")[0]
    if isinstance(res,str) and res.isdigit():
        return int(res)
    return res

def qualite(code: str, default: str):
    return translateCode(
        chemin_fichier=_tradFile,
        code_recherche=code,
        nom_feuille="qualité",
        default_value=default
    )[0]

def regimeRetraite(regime):
    if isinstance(regime, str) and regime.isdigit():
        regime = int(regime)
    res = translateCode(
        chemin_fichier=_tradFile, code_recherche=regime, nom_feuille="regime_retraite"
    )[0]
    if isinstance(res, str) and res.isdigit():
        return int(res)
    return None

def _normalize_code_risque(code):
    """
    Normalise le code risque en ajoutant un point après les 2 premiers caractères
    si nécessaire et en mettant en majuscules.
    
    Args:
        code (str): Le code risque à normaliser
        
    Returns:
        str: Le code risque normalisé
    """
    code = code.upper()
    # Si le code n'a pas de point après les 2 premiers caractères
    if len(code) >= 3 and code[2] != '.':
        code = f"{code[:2]}.{code[2:]}"
    return code

def nomNatureCotisation(codeNature:str):
    criteres = {
        0: codeNature,
    }
    res = searchExcel(fichier_path=_tradFile, nom_feuille="cotisation_nature", criteres_recherche=criteres, defaultline=None)[0]
    return res["Nom"]

def paiementPeriodicite(code:int):
    codes = ["Mensuelle","Trimestrielle","Annuelle","Semestrielle"]
    if code >= len(codes):
        return None
    return codes[code]

def typePrelevement(code:int):
    # codes = ["Chèque","Virement", "Télépaiement"]
    codes = [None, "Chèque","Virement", "Prélèvement"]
    return codes[code]

def getTauxAT(code_risque, annee,recursed=False):
    """
    Récupère le taux AT/MP pour un code risque et une année donnés. Si la source n'est pas existante, Essaye avec la source de l'année Précédante
    
    Args:
        code_risque (str): Le code risque à rechercher
        annee (int): L'année pour laquelle rechercher le taux
        
    Returns:
        dict: Les informations complètes de la ligne si trouvée
    """
    try:
        # Construction de l'URL avec l'année
        url = f"https://raw.githubusercontent.com/betagouv/taux-collectifs-cotisation-atmp/refs/heads/master/taux-{annee}.json"
        
        # Récupération des données
        response = requests.get(url)    
        response.raise_for_status()  # Lève une exception si la requête échoue
        data = response.json()
        
        # Normalisation du code risque fourni
        code_normalise = _normalize_code_risque(code_risque)
                
        # Recherche avec le code normalisé
        for entry in data:
            entry_code = _normalize_code_risque(entry['Code risque'])
            if entry_code == code_normalise:
                return float(entry['Taux net'].replace(",",".").replace("%",""))
                
        return None
        
    except requests.RequestException as e:
        logger.warning(f"Erreur lors de la récupération des données: {e}")
        if not recursed:
            logger.progress(f"Essai avec la base de l'année précédente : {annee-1}")
            return getTauxAT(code_risque,annee-1)
        else:
            return None