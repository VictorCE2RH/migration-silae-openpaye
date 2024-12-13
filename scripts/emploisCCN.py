from bs4 import BeautifulSoup
import pandas as pd
import requests
import sys
import os
from datetime import datetime

# Ajoute le dossier parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils
import logger

def get_page_content(url):
    """Récupère le contenu de la page web"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lève une exception si la requête échoue
        return response.text
    except requests.RequestException as e:
        logger.printErr(f"Erreur lors de la récupération de la page: {e}")
        return None

def parse_html_content(html_content):
    """Parse le ²contenu HTML et extrait les données des spans"""
    soup = BeautifulSoup(html_content, 'html.parser')
    data = []
    
    # Trouve tous les spans
    spans = soup.find_all('span')
    
    for span in spans:
        # Divise le texte du span par ':'
        parts = [part.strip() for part in span.text.split(':')]
        if len(parts) == 3:  # Vérifie qu'on a bien 3 parties
            data.append({
                'CCN': parts[0],
                'Code': parts[1],
                'Libellé': parts[2]
            })
    
    return data
    

def main():
    # URL de la page
    url = "https://api.openpaye.co/Listes?type=Emploi%20Conventionnel"
    
    logger.printProgress(f"Requesting {url}")
    # Récupère le contenu de la page
    html_content = get_page_content(url)
    if html_content is None:
        logger.printWarn("html content null")
        return
    
    logger.printProgress(f"Parsing {url}")
    
    # Parse le contenu HTML
    data = parse_html_content(html_content)
    
    # Vérifie si des données ont été trouvées
    if not data:
        logger.WarningStatement("Aucune donnée trouvée dans la page")
        return
    
    logger.printStat(f"Collected {len(data)} elements")
    # Crée le fichier Excel
    logger.printProgress("Creating excel file")
    timestamp = datetime.now().strftime("%Y-%m-%d")
    outpath = r'.\data\out'
    outpath = f"{outpath}\\{timestamp}_emplois_conventionnels.xlsx"
    utils.create_excel_file(data,outpath)
    logger.printProgress(f"Created File at {outpath} ")

if __name__ == "__main__":
    main()
    logger.printSuccess("FIN")