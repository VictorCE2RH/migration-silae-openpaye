from enum import Enum
import pandas as pd


# Enum des rôles définis
class RoleOP(Enum):
    GestionPaie = "1"
    Direction = "2"
    Compta = "3"
    CtrlGestion = "4"
    RH = "5"
    Autre = "6"
    ChefEntreprise = "7"
    Directeur = "8"
    Comptable = "9"
    MandataireLiquidateur = "9"
    Gerant = "10"
    ChefPersonnel = "11"
    AdminJudiciaire = "12"
    DG = "13"
    President = "14"

# Dictionnaire dynamique pour correspondre les textes aux rôles
role_mapping = {
    "chef d'entreprise": RoleOP.ChefEntreprise,
    "présidente": RoleOP.President,
    "président": RoleOP.President,
    "gérante": RoleOP.Gerant,
    "gérant": RoleOP.Gerant,
    "directeur général": RoleOP.DG,
    "directrice général": RoleOP.DG,
    "DG": RoleOP.DG,
    "directeur": RoleOP.Directeur,
    "directrice": RoleOP.Directeur,
    "comptable": RoleOP.Comptable,
    "chef du personnel": RoleOP.ChefPersonnel,
    "responsable ressources humaines": RoleOP.RH,
    "responsable RH": RoleOP.RH,
    "RH": RoleOP.RH,
    "DRH": RoleOP.RH,
    "Directeur RH": RoleOP.RH,
    "Directrice RH": RoleOP.RH,
    "mandataire liquidateur": RoleOP.MandataireLiquidateur
}


# Fonction qui associe un texte de qualité à un rôle
def associer_role(qualite_texte: str, mapping: dict[str, RoleOP] = role_mapping):

    qualite_texte = qualite_texte.strip().lower()

    # Recherche dans le dictionnaire avec un retour par défaut sur RoleOP.Autre
    for key in mapping:
        if key in qualite_texte:
            return mapping[key]

    print(f"QUALITEE : AUCUNE CORRESPONDANCE, attribution du role AUTRE\n {qualite_texte} (clé={key}). ajoutez une correspondance si nécessaire dans role.py")
    # Si aucune correspondance n'a été trouvée, renvoyer RoleOP.Autre
    return RoleOP.Autre
