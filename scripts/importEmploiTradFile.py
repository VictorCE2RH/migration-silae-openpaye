import pandas as pd
import numpy as np
from typing import Optional, Tuple
from pathlib import Path
import sys
import os
# Ajoute le dossier parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logger

import argparse

def setup_argparser():
    parser = argparse.ArgumentParser(description='Compare deux fichiers Excel')
    parser.add_argument('--ignoreCCN',nargs='+', help='Codes CCNs à ignorer (séparés par un espace)')
    return parser

def reorder_excel_columns(input_file: Path, output_file: Path, column_order: list, ignored_ccns:list[str]) -> pd.DataFrame:
    """
    Réorganise les colonnes d'un fichier Excel selon l'ordre spécifié.
    """
    try:
        df = pd.read_excel(input_file, header=1,dtype=str)
        df = df[df['code silae'].apply(lambda x: is_valid_code(x, ignored_ccns))]
        df_reordered = df[column_order]
        df_reordered.to_excel(output_file, index=False)
        print(f"Fichier sauvegardé avec succès: {output_file}")
        return df_reordered
    except Exception as e:
        print(f"Erreur lors de la réorganisation: {str(e)}")
        return None

def is_valid_code(code,ignored_ccns) -> bool:
    """Vérifie si un code silae est valide et n'est pas dans les CCN ignorées."""
    if not (pd.notna(code) and str(code).strip()):
        return False
    return not any(str(code).startswith(ccn) for ccn in (ignored_ccns or []))

def get_composite_key(row):
    """
    Crée une clé composite à partir du code silae et du statut professionnel.
    """
    code = str(row['code silae']).strip() if is_valid_code(row['code silae']) else ''
    statut = str(row['Statut Professionnel']).strip() if pd.notna(row['Statut Professionnel']) else ''
    return f"{code}_{statut}"

def format_row(row: pd.Series) -> str:
    """
    Formate une ligne de données en chaîne de caractères.
    """
    return " | ".join(f"{str(val):<20}" for val in row)

def rows_equal(row1, row2):
    """Compare deux lignes en gérant correctement les NaN."""
    for val1, val2 in zip(row1, row2):
        if pd.isna(val1) and pd.isna(val2):
            continue
        elif pd.isna(val1) or pd.isna(val2):
            return False
        elif str(val1).strip() != str(val2).strip():
            return False
    return True

def compare_excel_files(file1: str, file2: str,ignored_ccns: list[str] = []) -> None:
    """
    Compare deux fichiers Excel en utilisant une clé composite (code silae + Statut Professionnel).
    """
    # Lecture des fichiers
    df1_raw = pd.read_excel(file1,sheet_name="emploiCCN",dtype=str)
    df2_raw = pd.read_excel(file2,dtype=str)
    
    df1 = df1_raw[df1_raw['code silae'].apply(lambda x: is_valid_code(x, ignored_ccns))].reset_index(drop=True)
    df2 = df2_raw[df2_raw['code silae'].apply(lambda x: is_valid_code(x, ignored_ccns))].reset_index(drop=True)

    
    print("\n=== COMPARAISON GIT DIFF STYLE ===")
    print(f"--- {file1}")
    print(f"+++ {file2}")
    print("=" * 100)

    # Affichage de l'en-tête
    header = " | ".join(f"{col:<20}" for col in df1.columns)
    print("\n" + header)
    print("-" * len(header))
    
    # Comparaison ligne par ligne
    max_rows = max(len(df1), len(df2))
    lignes_modifiees = 0
    
    for i in range(max_rows):
        # Si la ligne existe dans df1
        if i < len(df1):
            row1 = df1.iloc[i]
            # Si la ligne existe aussi dans df2
            if i < len(df2):
                row2 = df2.iloc[i]
                # Comparaison des lignes
                if not rows_equal(row1,row2):
                    logger.printWarn(f"local: {format_row(row1)}")
                    logger.printWarn(f"new:   {format_row(row2)}")
                    lignes_modifiees += 1
            else:
                # Ligne supprimée
                logger.printErr(f"- {format_row(row1)}")
        # Si la ligne n'existe que dans df2
        elif i < len(df2):
            row2 = df2.iloc[i]
            logger.printSuccess(f"+ {format_row(row2)}")
    
    # Résumé des modifications
    print("\n=== RÉSUMÉ DES MODIFICATIONS ===")
    lignes_df1 = len(df1)
    lignes_df2 = len(df2)
    print(f"Nombre de lignes fichier 1: {lignes_df1}")
    print(f"Nombre de lignes fichier 2: {lignes_df2}")
    
    if lignes_df1 > lignes_df2:
        logger.printErr(f"- {lignes_df1 - lignes_df2} ligne(s) supprimée(s)")
    elif lignes_df2 > lignes_df1:
        logger.printSuccess(f"+ {lignes_df2 - lignes_df1} ligne(s) ajoutée(s)")
    logger.printWarn(f"~ {lignes_modifiees} ligne(s) modifiée(s)")


if __name__ == "__main__":
    parser = setup_argparser()
    args = parser.parse_args()
    # Configuration des chemins de fichiers
    fichier_entree = Path("C:/Users/e2rh0/Victor_E2RH/E2RH/OPENPAYE/classifications/Liste_traduction_classification_Silae_vers_OP_v3.xlsx")
    fichier_sortie = Path("C:/Users/e2rh0/Victor_E2RH/workspace/open-paye-migration/data/out/traduction_emploi_ordonnee.xlsx")
    fichier_test = Path("C:/Users/e2rh0/Victor_E2RH/workspace/open-paye-migration/data/in/traduction_code_silae_openpaye.xlsx")

    # Nouvel ordre des colonnes
    nouvel_ordre = [
        "code silae",
        "Statut Professionnel",
        "OPCC",
        "Code",
        "Statut",
        "Libellé"
    ]

    df_reordonne = reorder_excel_columns(fichier_entree, fichier_sortie, nouvel_ordre, args.ignoreCCN)
    if df_reordonne is not None:
        compare_excel_files(fichier_test, fichier_sortie, args.ignoreCCN)
