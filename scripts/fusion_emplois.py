import pandas as pd

input_file = r'.\data\in\emplois_ccn_original.xlsx'
output_file = r'.\data\in\emploi_ccn.xlsx'

def get_distinct_statuts_all_sheets(fichier):
    # Lire le fichier Excel
    excel_file = pd.ExcelFile(fichier)
    
    # Set pour stocker tous les statuts uniques
    # On utilise un set car il élimine automatiquement les doublons
    tous_statuts = set()
    
    # Parcourir chaque feuille
    for sheet_name in excel_file.sheet_names:
        try:
            # Lire la feuille en ignorant les deux premières lignes
            df = pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=2)
            
            # Récupérer les statuts de cette feuille
            statuts_feuille = df['Statut'].dropna().unique()
            
            # Ajouter les statuts au set global
            tous_statuts.update(statuts_feuille)
            
            print(f"Feuille '{sheet_name}' traitée avec succès")
            
        except Exception as e:
            print(f"Erreur lors du traitement de la feuille '{sheet_name}': {str(e)}")
            continue
    
    # Convertir le set en liste triée
    statuts_distincts = sorted(tous_statuts)
    
    # Afficher les résultats
    print("\nStatuts distincts trouvés dans toutes les feuilles :")
    for statut in statuts_distincts:
        print(f"- {statut}")
    
    return statuts_distincts

def process_excel_file(input_file, output_file):
    # Lire le fichier Excel
    excel_file = pd.ExcelFile(input_file)
    
    # Liste pour stocker les DataFrames de chaque feuille
    all_sheets_data = []
    
    # Parcourir chaque feuille
    for sheet_name in excel_file.sheet_names:
        try:
            # Extraire l'IDCC depuis le nom de la feuille (4 premiers caractères)
            sheet_idcc = sheet_name[:4]
            
            # Vérifier si l'IDCC extrait est valide (4 chiffres)
            if not sheet_idcc.isdigit() or len(sheet_idcc) != 4:
                print(f"Feuille '{sheet_name}' ignorée : IDCC invalide")
                continue
                
            # Lire la feuille en ignorant les deux premières lignes
            df = pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=2)
            
            # Sélectionner uniquement les colonnes qui nous intéressent
            selected_columns = df[['Code', 'Libellé']]
            
            # Supprimer les lignes où Code est vide
            selected_columns = selected_columns.dropna(subset=['Code'])
            
            # Ajouter l'IDCC extrait du nom de la feuille
            selected_columns['IDCC'] = sheet_idcc
            
            # Ajouter une colonne pour identifier la feuille d'origine
            selected_columns['Source'] = sheet_name
            
            # Ajouter à notre liste
            all_sheets_data.append(selected_columns)
            
            print(f"Feuille '{sheet_name}' traitée avec succès (IDCC: {sheet_idcc})")
            
        except Exception as e:
            print(f"Erreur lors du traitement de la feuille '{sheet_name}': {str(e)}")
            continue
    
    # Combiner tous les DataFrames
    if all_sheets_data:
        combined_df = pd.concat(all_sheets_data, ignore_index=True)
            
        # Créer un nouveau DataFrame avec les colonnes dans l'ordre souhaité
        new_df = pd.DataFrame({
            'A': ["" for _ in range(len(all_sheets_data))],
            'B': combined_df['IDCC'],
            'C': combined_df['Code'],
            'D': combined_df['Libellé'],
            'E': combined_df['Source']  # Colonne supplémentaire pour tracer l'origine
        })
        
        # Créer un nouveau fichier Excel
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            new_df.to_excel(writer, sheet_name='Résultat', index=False)
        
        print(f"\nNouveau fichier Excel créé avec succès : '{output_file}'")
        print(f"Nombre total de lignes : {len(new_df)}")
    else:
        print("Aucune donnée n'a été trouvée dans les feuilles")


statuts = get_distinct_statuts_all_sheets(input_file)
print(statuts)
# process_excel_file(input_file, output_file)