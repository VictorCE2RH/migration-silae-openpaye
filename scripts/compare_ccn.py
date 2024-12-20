import pandas as pd
from typing import List, Set

import sys
import os
# Ajoute le dossier parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logger

def pad_lists_to_equal_length(lists: List[List]) -> List[List]:
    """
    Égalise la longueur des listes en ajoutant des valeurs None.
    """
    max_length = max(len(lst) for lst in lists)
    return [lst + [None] * (max_length - len(lst)) for lst in lists]

def compare_excel_columns(file_path: str, col_a: str, col_b: str):
    """
    Compare les valeurs entre deux colonnes d'un fichier Excel.
    
    Args:
        file_path (str): Chemin vers le fichier Excel
        col_a (str): Nom de la première colonne
        col_b (str): Nom de la deuxième colonne
    
    Returns:
        dict: Dictionnaire contenant les résultats de la comparaison
    """
    try:
        # Lecture du fichier Excel
        df = pd.read_excel(file_path)
        
        # Vérifier si les colonnes existent
        if col_a not in df.columns or col_b not in df.columns:
            raise ValueError(f"Les colonnes {col_a} et/ou {col_b} n'existent pas dans le fichier")
        
        # Convertir les colonnes en string et remplacer les NaN par des strings vides
        df[col_a] = df[col_a].fillna('').astype(str)
        df[col_b] = df[col_b].fillna('').astype(str)
        
        # Trouver les valeurs qui existent dans A et qui sont dans B
        values_in_a = set(df[col_a][df[col_a].str.strip() != ''])
        values_in_b = set(df[col_b][df[col_b].str.strip() != ''])
        
        # Calculer les différentes comparaisons
        matching_values = sorted(list(values_in_a.intersection(values_in_b)))
        only_in_a = sorted(list(values_in_a - values_in_b))
        
        # Préparer les listes pour le DataFrame
        data_dict = {}
        
        # Ajouter les valeurs correspondantes si elles existent
        if matching_values:
            data_dict['Valeurs présentes dans les deux colonnes'] = matching_values
            
        # Ajouter les valeurs uniquement dans A si elles existent
        if only_in_a:
            data_dict['Valeurs uniquement dans ' + col_a] = only_in_a
            
        if data_dict:
            # Égaliser la longueur des listes
            padded_lists = pad_lists_to_equal_length(list(data_dict.values()))
            # Recréer le dictionnaire avec les listes égalisées
            data_dict = dict(zip(data_dict.keys(), padded_lists))
            
            # Créer le DataFrame
            results_df = pd.DataFrame(data_dict)
        else:
            # Créer un DataFrame vide avec les colonnes appropriées
            results_df = pd.DataFrame(columns=['Valeurs présentes dans les deux colonnes', 'Valeurs uniquement dans ' + col_a])
        
        # Sauvegarder les résultats
        output_file = '.\\data\\out\\resultats_comparaison.xlsx'
        results_df.to_excel(output_file, index=False)
        
        return {
            'matching_count': len(matching_values),
            'only_in_a_count': len(only_in_a),
            'matching_values': matching_values,
            'only_in_a': only_in_a,
            'output_file': output_file
        }
        
    except Exception as e:
        logger.log(f"Une erreur s'est produite: {str(e)}")
        return None

# Exemple d'utilisation
if __name__ == "__main__":
    file_path = r"C:\Users\e2rh0\Victor_E2RH\workspace\open-paye-migration\data\out\traduction_emploi_ordonnee.xlsx"  # Remplacer par le chemin de votre fichier
    col_a = "codePAME"  # Remplacer par le nom de votre première colonne
    col_b = "code"  # Remplacer par le nom de votre deuxième colonne
    
    results = compare_excel_columns(file_path, col_a, col_b)
    
    if results:
        logger.log(f"\nRésultats de la comparaison:")
        logger.log(f"Nombre de valeurs communes: {results['matching_count']}")
        logger.log(f"Nombre de valeurs uniquement dans {col_a}: {results['only_in_a_count']}")
        logger.log(f"\nLes résultats détaillés ont été sauvegardés dans: {results['output_file']}")