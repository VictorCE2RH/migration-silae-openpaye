from silae import Dossier
import utils
import role
from utils import *
from etablissement import *


# TODO: request default manager from API
emptyContact = {
    "identifiant": "",
    "codeCollaborateur": "",
    "nomNaissance": "",
    "nomUsuel": "",
    "prenom": "",
    "email": "",
    "telephoneBureau": "",
    "telephonePortable": "",
    "storedSince": "",
}


def parseDossiers(
    dossierMap: dict[str, Dossier],
    contactMap: NumToJson,
    max: int,
    defaultContact: JSON = emptyContact,
) -> list[JSON]:
    openpaye_dossiers: list[JSON] = []
    i = 1  # compte le nombre de dossiers créés
    for numero, dossier in dossierMap.items():
        contact = contactMap[numero]
        print(f"Parsing Dossier : {dossier.numero}")
        numero = dossier.numero
        raisonSociale = dossier.raisonSociale
        email = contact.get("E-mail")
        tel = contact.get("Téléphone")
        nom_contact = (
            contact.get("Employeur").removeprefix("Mr").removeprefix("Mme").strip()
        )
        qualite = role.associer_role(contact.get("Qualité")).value
        openpaye_dossier: JSON = {
            "code": numero,
            "nom_dossier": raisonSociale,
            "adresse_email": email,
            "telephone": tel,
            "nom_contact": nom_contact,
            "qualite": qualite,
            "annee": "2024",
        }
        openpaye_dossiers.append(openpaye_dossier)
        print(f"[{i}] Dossier {dossier.numero} ajouté à la liste de création")
        if max > 0 and i == max:
            print("Limite max de dossiers créés atteint, arret de la boucle")
            break
        else:
            i += 1
    
    return openpaye_dossiers

def parseEtablissements(domain:str, etabMap: NumToJson, contactMap: NumToJson) -> list[JSON]:
    print(f"Parsing Etablissements Silae -> Openpaye")
    res:list[JSON] = []
    for numero, etabsJson in etabMap.items():
        print(f"Parsing {numero} ")
        contact = contactMap[numero]
        for etabJson in etabsJson.get("informationsEtablissements"):
            newEtablissement = Etablissment(
                None,# id, non renseigné dans l'export
                etabJson.get("nomInterne",""),
                contact.get("Raison sociale",""),
                etabJson.get("etablissementPrincipal",True),
                etabJson.get("siret",""),
                Adresse(
                    etabJson.get("adresse_postale",""),
                    etabJson.get("adresse_postale2",""), # adresse 2 
                    etabJson.get("adresse_complement",""), # complement adresse
                    contact.get("Code postal",""),
                    contact.get("Ville",""),
                    etabJson.get("insee",""), # insee
                    etabJson.get("code_distribution",""), # ditribution etranger 
                    etabJson.get("pays","France"),
                ),
                etabJson.get("juridique",""), # juridique
                etabJson.get("civilite",""), # civilité
                etabJson.get("civilite"), # activité
                contact.get("Code NAF",""),
                etabJson.get("libAPE",""), # libelle APE 
                etabJson.get("idcc",""), # ccn
                etabJson.get("idcc2",""), # ccn2
                etabJson.get("idcc3",""), # ccn3
                etabJson.get("idcc4",""), # ccn4
                etabJson.get("idcc5",""), # ccn5
                etabJson.get("avenant", False),  # avenent
                etabJson.get("num_cotisant",""), # num cotisant
                etabJson.get("date_radiation_at",""), # date radiation at
                etabJson.get("code_radiation_at",""), # code at
                etabJson.get("taux_radiation_at",0.0),    # taux at
                etabJson.get("b_versement_transport",False),  # is versement transport
                etabJson.get("taux_versement_transport",0.0), # taux versement transport
                Banque(
                    virement=etabJson.get("b_virement",False),
                    code_bic=etabJson.get("code_bic",""),
                    iban=etabJson.get("iban","")
                ),
                GestionCongesPayes(
                    mois_cloture_droits_cp=etabJson.get("mois_cp_cloture",5),
                    report_automatique_conges_payes=etabJson.get("b_repport_auto_cp",False),
                    gestion_absences_conges_heures_sur_bulletins=etabJson.get("b_abs_cp_heures_bulletins",False),
                    decompte_conges_payes=etabJson.get("decompte_cp",""),
                    valorisation_conges_payes=etabJson.get("valorisation_cp",""),
                    bloquer_gestion_conges_payes=etabJson.get("bloquer_gest_cp",True),
                    etablissement_affilie_caisse_conges_payes=etabJson.get("affilie_caisse_cp",False)
                )
            )
            etabJson = utils.objectEncoderJson(newEtablissement)
            res.append(etabJson)
        
    return res