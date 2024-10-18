from dataclasses import dataclass

@dataclass
class Adresse:
    adress_postale: str
    adress_postale2: str
    complement_adress: str
    code_postal: str
    ville: str
    code_insee: str
    code_distribution_etranger: str
    pays: str


@dataclass
class Banque:
    virement: bool
    code_bic: str
    iban: str


@dataclass
class GestionCongesPayes:
    mois_cloture_droits_cp: int
    report_automatique_conges_payes: bool
    gestion_absences_conges_heures_sur_bulletins: bool
    decompte_conges_payes: str
    valorisation_conges_payes: str
    bloquer_gestion_conges_payes: bool
    etablissement_affilie_caisse_conges_payes: bool


@dataclass
class Etablissment:
    id: int | None  # Ignoré pour une création d'établissement
    code: str
    raison_sociale: str
    etablissement_principal: bool
    siret: str
    adresse: Adresse
    forme_juridique: int
    civilite: str
    activite: str
    ape: str
    libelle_ape: str
    ccn: int
    ccn2: int
    ccn3: int
    ccn4: int
    ccn5: int
    avenant: bool
    numero_cotisant: str
    date_radiation: str
    code_risque_at: str
    taux_at: float
    is_taux_versement_transport: bool
    taux_versement_transport: float
    banque: Banque
    gestion_conges_payes: GestionCongesPayes


@dataclass
class Silae_Etablissement:
    nomInterne: str
    siret: str
    principal: bool
