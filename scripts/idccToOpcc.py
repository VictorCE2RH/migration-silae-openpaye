from bs4 import BeautifulSoup
import pandas as pd
import requests
import sys
import os
import re
from pathlib import Path
# Ajoute le dossier parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logger
from utils import jaccard_similarity,isSimilarText,findSimilarText
from silae import getCCNListFromIDCC

def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Erreur lors de la récupération de la page: {e}")
        return None
    
def load_ccns():
    try:
        pathStr = "C:/Users/e2rh0/Victor_E2RH/E2RH/OPENPAYE/classifications/Liste_traduction_classification_Silae_vers_OP_v3.xlsx"
        path = Path(pathStr)
        df_class = pd.read_excel(path,skiprows=1)
        return dict(zip(df_class['OPCC'], df_class['Code CCN Silae']))
    except Exception as e:
        logger.error(f"Erreur lors du chargement des ccns: {e}")
        return {}
    
def parse_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    data = []
    opcc_map = {}
    doublons = []

    # Création DataFrame avec codes combinés pour les doublons
    for span in soup.find_all('span'):
        strong = span.find('strong')
        if strong and '/' in strong.text:
            opcc, idcc = strong.text.split('/')
            libelle = ''.join(span.text.split(':')[1:]).strip() if ':' in span.text else ''
            if libelle != '':
                x = re.search(r"remplacé par.+?IDCC\s(\d{1,4})",libelle)
                if x: 
                    logger.warning(f"opcc {opcc} à remplacer par {x.group(1)}. SKIP")
                    continue
            if libelle.find("doublons") != -1:
                logger.log(f"doublon {idcc} {opcc} {libelle}. SKIP")
                doublons.append((opcc,libelle.replace("(doublons ne pas utiliser)", "").replace("\\t","").strip()))
                continue
                
            final_opcc = opcc
            # Si CCN pas dans le classeur EmploiCCN
            codesSilae = getCCNListFromIDCC(idcc)
            if len(codesSilae) == 0: 
                ccn = ''
            elif len(codesSilae) == 1:
                ccn = codesSilae[0]["codeCCN"]
            else:
                ccnMaxJacard:tuple[str,float] = ('',-1)
                choixMult = len(codesSilae) == 1
                if choixMult: 
                    logger.statistic(f"IDCC = {idcc} : {libelle}")
                for code in codesSilae:
                    ccn = code["codeCCN"]
                    score = jaccard_similarity(libelle,code["libelleCCN"])
                    logger.progress(f"- ccn {ccn} - score = {score:.5f} - libelleCCN = {code["libelleCCN"]}")
                    if score > ccnMaxJacard[1]:
                        ccnMaxJacard = (ccn, score)
                ccn = ccnMaxJacard[0]
                if choixMult: logger.success(f"- CCN = {ccn}")
                if choixMult: print()
            
            if idcc == '7002':
                print(f"7002 {ccn} {final_opcc}")
            data.append({
                'ccn': ccn,
                'idcc': idcc,
                'opcc': final_opcc,
                'libelle': libelle
            })
        
    # if len(doublons) > 0:
    #     for doublon in doublons:
    #         lines = findIdcc(data,doublon)
            
    return pd.DataFrame(data)

def findIdcc(datas:list, doublon) -> list:
    found = []
    reslist = findSimilarText(doublon[1],[data["libelle"] for data in datas])
    if len(reslist) != 1:
        return found
    datas = [data for data in datas if data["libelle"] in [res[0] for res in reslist]]
    for data in datas:
        if data["opcc"] != doublon[0]:
            logger.progress(f"doublon : {doublon} : {reslist}")
            logger.log(f"Remplacer l'opcc : {doublon[0]} par {data["opcc"]}")
            found.append(data)
    return found

def main():
    url = "https://api.openpaye.co/Listes?type=CCN"

    # Chargement des ccns
    logger.progress("Loading ccns")
    # ccns = load_ccns()
    
    logger.progress(f"Requesting {url}")
    html_content = get_page_content(url)
    if not html_content:
        return
    
    logger.progress("Parsing content")
    df = parse_html_content(html_content)
    
    outpath = Path("data/in/idcc_opcc_mapping.xlsx")
    try: 
        df.to_excel(outpath,index=False)
    except PermissionError as e:
        raise PermissionError("FERME LE FICHIER DUCON")
    logger.success(f"Created file at {outpath}")

if __name__ == "__main__":
    main()