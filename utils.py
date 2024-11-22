import json
import csv
import base64
import unicodedata
from collections import defaultdict
from datetime import datetime, date, timedelta

JSON = dict[str, any]


# Encoder : Convertir un objet Python en JSON
def objectEncoderJson(objet):
    try:
        # Utilise json.dumps pour convertir un objet en JSON
        return json.dumps(
            objet, default=lambda o: o.__dict__, ensure_ascii=False, indent=4
        )
    except TypeError as e:
        print(f"Erreur lors de l'encodage en JSON: {e}")
        return None

def formatJson(data: str | dict, spaces: int = 4):
    """
    Format un json (string ou dict) de sorte à visualiser plus facilement les élémentsq
    """
    if type(data) is str:
        dataStr = json.loads(data)
        return json.dumps(dataStr, indent=spaces)
    return json.dumps(data, indent=spaces)

def saveJsonData(name: str, dataJson: any):
    out_repo = ".\\data\\out"
    jsonFile = f"{out_repo}\\{name}.json"
    with open(jsonFile, "w") as fp:
        json.dump(dataJson, fp, indent=4)

def saveLogAction(type_action: str, codes: JSON):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fileName = f"export_{type_action}_{timestamp}"
    if len(codes) > 0:
        saveJsonData(fileName, codes)

def getIdForNum(items:dict, numList: list) -> list:
    res = []
    for num in numList:
        for item in items:
            found = False
            if item["code"] == num:
                res.append(item["id"])
                found = True
                break
        if found == False:
            raise Exception(f"{num}")
    return res


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
        raise Exception()
    
def del_none(d):
    """
    Delete keys with the value ``None`` in a dictionary, recursively.

    This alters the input so you may wish to ``copy`` the dict first.
    """
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d  # For convenience

def filterEmptyResData(res: list): 
    for i in range(len(res)):
        for key, data in res[i]["data"].items():
            if isinstance(data, dict):
                for subKey, subData in data.items():
                    if isinstance(subData, str) and subData == '':
                        res[i]["data"][key][subKey] = None
                        print(f"empty subKey {key} {subKey} replaced with None")
            if isinstance(data, str) and data == '':
                res[i]["data"][key] = None
                print(f"empty {key} replaced with None")
    return res

def _getCountryMap():
    pays_vers_code = {
        "Afghanistan": "AF", "Afrique du Sud": "ZA", "Albanie": "AL", "Algérie": "DZ",
        "Allemagne": "DE", "Andorre": "AD", "Angola": "AO", "Anguilla": "AI",
        "Antigua-et-Barbuda": "AG", "Antilles néerlandaises": "AN", "Arabie saoudite": "SA",
        "Argentine": "AR", "Arménie": "AM", "Aruba": "AW", "Australie": "AU",
        "Autriche": "AT", "Azerbaïdjan": "AZ", "Bahamas": "BS", "Bahreïn": "BH",
        "Bangladesh": "BD", "Barbade": "BB", "Belgique": "BE", "Belize": "BZ",
        "Bermudes": "BM", "Bhoutan": "BT", "Bolivie": "BO", "Bosnie-Herzégovine": "BA",
        "Botswana": "BW", "Brunéi Darussalam": "BN", "Brésil": "BR", "Bulgarie": "BG",
        "Burkina Faso": "BF", "Burundi": "BI", "Bélarus": "BY", "Bénin": "BJ",
        "Cambodge": "KH", "Cameroun": "CM", "Canada": "CA", "Cap-Vert": "CV",
        "Chili": "CL", "Chine": "CN", "Chypre": "CY", "Colombie": "CO",
        "Comores": "KM", "Congo": "CG", "Corée du Nord": "KP", "Corée du Sud": "KR",
        "Costa Rica": "CR", "Croatie": "HR", "Cuba": "CU", "Côte d'Ivoire": "CI",
        "Danemark": "DK", "Djibouti": "DJ", "Dominique": "DM", "El Salvador": "SV",
        "Espagne": "ES", "Estonie": "EE", "Fidji": "FJ", "Finlande": "FI",
        "France": "FR", "Gabon": "GA", "Gambie": "GM", "Ghana": "GH",
        "Gibraltar": "GI", "Grenade": "GD", "Groenland": "GL", "Grèce": "GR",
        "Guadeloupe": "GP", "Guam": "GU", "Guatemala": "GT", "Guernesey": "GG",
        "Guinée": "GN", "Guinée équatoriale": "GQ", "Guinée-Bissau": "GW", "Guyana": "GY",
        "Guyane française": "GF", "Géorgie": "GE", "Haïti": "HT", "Honduras": "HN",
        "Hongrie": "HU", "Inde": "IN", "Indonésie": "ID", "Irak": "IQ",
        "Iran": "IR", "Irlande": "IE", "Islande": "IS", "Israël": "IL",
        "Italie": "IT", "Jamaïque": "JM", "Japon": "JP", "Jersey": "JE",
        "Jordanie": "JO", "Kazakhstan": "KZ", "Kenya": "KE", "Kirghizistan": "KG",
        "Kiribati": "KI", "Kosovo": "XK", "Koweït": "KW", "Laos": "LA",
        "Lesotho": "LS", "Lettonie": "LV", "Liban": "LB", "Libye": "LY",
        "Libéria": "LR", "Liechtenstein": "LI", "Lituanie": "LT", "Luxembourg": "LU",
        "Macédoine": "MK", "Madagascar": "MG", "Malaisie": "MY", "Malawi": "MW",
        "Maldives": "MV", "Mali": "ML", "Malte": "MT", "Maroc": "MA",
        "Martinique": "MQ", "Maurice": "MU", "Mauritanie": "MR", "Mayotte": "YT",
        "Mexique": "MX", "Moldavie": "MD", "Monaco": "MC", "Mongolie": "MN",
        "Montserrat": "MS", "Monténégro": "ME", "Mozambique": "MZ", "Myanmar": "MM",
        "Namibie": "NA", "Nauru": "NR", "Nicaragua": "NI", "Niger": "NE",
        "Nigéria": "NG", "Niue": "NU", "Norvège": "NO", "Nouvelle-Calédonie": "NC",
        "Nouvelle-Zélande": "NZ", "Népal": "NP", "Oman": "OM", "Ouganda": "UG",
        "Ouzbékistan": "UZ", "Pakistan": "PK", "Palaos": "PW", "Panama": "PA",
        "Papouasie-Nouvelle-Guinée": "PG", "Paraguay": "PY", "Pays-Bas": "NL",
        "Philippines": "PH", "Pitcairn": "PN", "Pologne": "PL", "Polynésie française": "PF",
        "Porto Rico": "PR", "Portugal": "PT", "Pérou": "PE", "Qatar": "QA",
        "R.A.S. chinoise de Hong Kong": "HK", "R.A.S. chinoise de Macao": "MO",
        "Roumanie": "RO", "Royaume-Uni": "GB", "Russie": "RU", "Rwanda": "RW",
        "République centrafricaine": "CF", "République dominicaine": "DO",
        "République démocratique du Congo": "CD", "République tchèque": "CZ",
        "Réunion": "RE", "Sahara occidental": "EH", "Saint-Kitts-et-Nevis": "KN",
        "Saint-Marin": "SM", "Saint-Pierre-et-Miquelon": "PM",
        "Saint-Vincent-et-les Grenadines": "VC", "Sainte-Hélène": "SH",
        "Sainte-Lucie": "LC", "Samoa": "WS", "Samoa américaines": "AS",
        "Sao Tomé-et-Principe": "ST", "Serbie": "RS", "Seychelles": "SC",
        "Sierra Leone": "SL", "Singapour": "SG", "Slovaquie": "SK", "Slovénie": "SI",
        "Somalie": "SO", "Soudan": "SD", "Sri Lanka": "LK", "Suisse": "CH",
        "Suriname": "SR", "Suède": "SE", "Swaziland": "SZ", "Syrie": "SY",
        "Sénégal": "SN", "Tadjikistan": "TJ", "Tanzanie": "TZ", "Taïwan": "TW",
        "Tchad": "TD", "Terres australes françaises": "TF",
        "Territoire britannique de l'océan Indien": "IO", "Territoire palestinien": "PS",
        "Thaïlande": "TH", "Timor oriental": "TL", "Togo": "TG", "Tokelau": "TK",
        "Tonga": "TO", "Trinité-et-Tobago": "TT", "Tunisie": "TN", "Turkménistan": "TM",
        "Turquie": "TR", "Tuvalu": "TV", "Ukraine": "UA", "Uruguay": "UY",
        "Vanuatu": "VU", "Venezuela": "VE", "Viêt Nam": "VN", "Wallis-et-Futuna": "WF",
        "Yémen": "YE", "Zambie": "ZM", "Zimbabwe": "ZW", "Égypte": "EG",
        "Émirats arabes unis": "AE", "Équateur": "EC", "Érythrée": "ER",
        "État de la Cité du Vatican": "VA", "États fédérés de Micronésie": "FM",
        "États-Unis": "US", "Éthiopie": "ET", "Île Bouvet": "BV", "Île Norfolk": "NF",
        "Îles Caïmans": "KY", "Îles Cook": "CK", "Îles Féroé": "FO",
        "Îles Heard et MacDonald": "HM", "Îles Malouines": "FK",
        "Îles Mariannes du Nord": "MP", "Îles Marshall": "MH",
        "Îles Mineures Éloignées des États-Unis": "UM", "Îles Salomon": "SB",
        "Îles Turks et Caïques": "TC", "Îles Vierges britanniques": "VG",
        "Îles Vierges des États-Unis": "VI"
    }
    
    # Créer le dictionnaire inverse (code vers pays)
    code_vers_pays = {code: pays for pays, code in pays_vers_code.items()}
    
    # Créer un dictionnaire normalisé pour la recherche insensible à la casse
    pays_normalises = {normaliser_texte(pays): pays for pays in pays_vers_code.keys()}
    
    return pays_vers_code, code_vers_pays, pays_normalises


def normaliser_texte(texte):
    """
    Normalise le texte en le mettant en minuscules et en retirant les accents
    Args:
        texte (str): Texte à normaliser
    Returns:
        str: Texte normalisé
    """
    
    # Convertir en minuscules
    texte = texte.lower()
    
    # Retirer les accents
    texte = ''.join(c for c in unicodedata.normalize('NFD', texte) if unicodedata.category(c) != 'Mn')
    
    return texte


def traduire_pays(entree, mode='pays_vers_code'):
    """
    Traduit un pays en code ISO ou vice-versa.
    
    Args:
        entree (str): Le pays ou le code à traduire
        mode (str): 'pays_vers_code' ou 'code_vers_pays'
    
    Returns:
        str: La traduction correspondante ou None si non trouvée
    """
    pays_vers_code, code_vers_pays, pays_normalises = _getCountryMap()
    
    if mode == 'pays_vers_code':
        # Normaliser l'entrée
        entree_normalisee = normaliser_texte(entree)
        
        # Chercher le pays normalisé correspondant
        pays_original = pays_normalises.get(entree_normalisee)
        
        # Si trouvé, retourner le code correspondant
        if pays_original:
            return pays_vers_code[pays_original]
        return None
        
    elif mode == 'code_vers_pays':
        # Pour les codes, on met en majuscules pour la standardisation
        return code_vers_pays.get(entree.upper())
    else:
        raise ValueError("Mode invalide. Utilisez 'pays_vers_code' ou 'code_vers_pays'")

# size=12 car utilisé principalement pour compter les mois de l'année dans un entier
def integerToBitArray(code:int,size:int=12):
    return [False if code == 0 else code & (1 << n) == 0 for n in range(size)]

def base64ToCsv(base64Str:str) -> dict[str,list]:
    decoded_bytes = base64.b64decode(base64Str)
    csv_data = decoded_bytes.decode('latin-1')
    rows = csv.reader(csv_data.splitlines(), delimiter=';')
    data_dict = defaultdict(list)
    headers = next(rows)
    for row in rows:
        for i, value in enumerate(row):
            header = headers[i].strip()
            if header == "" or (header == "Matricule" and value == ""):
                break
            data_dict[header].append(value.strip())
    
    return data_dict

def CsvToMap(csv:dict[str,list]) -> list[dict[str,any]]:
    return [ { col: csv[col][i] for col in csv } for i in range(len(next(iter(csv.values()))))]

def dict_to_csv(data_dict, output_file):
    with open(output_file, 'w', newline='', encoding='latin-1') as csvfile:
        writer = csv.writer(csvfile,delimiter=";")
        writer.writerow(data_dict.keys())
        writer.writerows(zip(*data_dict.values()))
    return data_dict
        
def LastDayOfPreviousMonth():
    today = date.today()
    lastDayPreviousMonth = today.replace(day=1) - timedelta(days=1)
    return lastDayPreviousMonth