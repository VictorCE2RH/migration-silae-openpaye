from silae import Dossier
import utils
import role
import extract
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

def codePays(paysSilae: int):
    res = utils.traduire_pays(paysSilae)
    if res != None:
        return res

    res = utils.traduire_pays(paysSilae, mode="code_vers_pays")
    if res == None:
        print(f"INFOS PAYS NON RECONNU : {paysSilae}, renvoi de None")

    return res


def parseDossiers(
    dossierMap: dict[str, Dossier],
    contactMap: JSON,
    max: int,
    defaultContact: dict = emptyContact,
) -> list[dict]:
    openpaye_dossiers: list[dict] = []
    i = 1  # compte le nombre de dossiers créés
    for numero, dossier in dossierMap.items():
        contact = contactMap[numero]
        print(f"Parsing Dossier : {dossier.numero}")
        numero = dossier.numero
        raisonSociale = contact.get("Raison sociale", dossier.raisonSociale)
        email = contact.get("E-mail")
        tel = contact.get("Téléphone")
        nom_contact = (
            contact.get("Employeur").removeprefix("Mr").removeprefix("Mme").strip()
        )
        qualite = role.associer_role(contact.get("Qualité")).value
        openpaye_dossier: dict = {
            "code": numero,
            "nom_dossier": raisonSociale,
            "adresse_email": email,
            "telephone": tel,
            "nom_contact": nom_contact,
            "qualite": qualite,
            "annee": "2024",
        }
        openpaye_dossiers.append(dataWithParams(openpaye_dossier))
        if max > 0 and i == max:
            print("Limite max de dossiers créés atteint, arret de la boucle")
            break
        else:
            i += 1

    return openpaye_dossiers


def parseEtablissements(
    etabMap: JSON, etabDetails: dict, codeDict: dict[str, str]
) -> list[dict]:
    """
    construction via les arguments en entrée des jsons qui permettent de créer un etablissement.
    Chaque json sont composés de l'element "data" qui contient le json a envoyé à l'api
    et "params" qui sont les eventuels parametres qui accompagne l'appel

    Args:
        etabMap (JSON): dictionnaire des infos de l'etablissement avec comme clé le numero du dossier
        contactMap (JSON): dictionnaire des infos contact avec comme clé le numéro du dossier
        codeDict (dict[str, str]): dictionnaire liant le numero de dossier à son ID interne openpaye

    Returns:
        list[dict]: renvoi la liste des jsons à transmettre pour la création des etablissements
    """
    res: dict = []
    for numero, etabsJson in etabMap.items():
        dossierId = codeDict[numero]

        for etabJson in etabsJson.get("informationsEtablissements"):
            print(f"Parsing Dossier {numero} Etablissement {etabJson["nomInterne"]} ")
            nomInterne = etabJson.get("nomInterne", "")
            details = etabDetails[nomInterne]["reponsesInfosPaie"]

            ccn = extract.idccToOpcc(etabJson.get("idcc"))
            ccn2 = extract.idccToOpcc(etabJson.get("idcc2"))
            ccn3 = extract.idccToOpcc(etabJson.get("idcc3"))
            ccn4 = extract.idccToOpcc(etabJson.get("idcc4"))
            ccn5 = extract.idccToOpcc(etabJson.get("idcc5"))
            civ = f"{int(details.get("INT_Civilite","0"))+1}"
            
            newEtablissement = Etablissment(
                code=nomInterne[
                    :5
                ],  # limite de 5 caractères pour le code de l'établissement
                raison_sociale=details["INT_RaisonSociale"],
                etablissement_principal=etabJson.get("etablissement_principal", True),
                siret=etabJson.get("siret"),
                adresse=Adresse(
                    adress_postale=details["INT_NumVoie"]
                    + " "
                    + details["INT_NomVoie"],
                    adress_postale2="",
                    complement_adress=details["INT_ComplementAdresse"],
                    code_postal=details["INT_CodePostal"],
                    ville=details["INT_NomVille"],
                    code_insee=details["INT_CommuneINSEE"],
                    code_distribution_etranger="",
                    pays=details["INT_NomPays"],
                ),
                forme_juridique=1,  # Forme juridique, voir correspondance silae<>openpaye
                activite=etabJson.get("activite", ""),
                civilite=civ,
                ape=details["INT_NAF"],
                libelle_ape=etabJson.get("libAPE", ""),
                ccn=ccn,
                ccn2=ccn2,
                ccn3=ccn3,
                ccn4=ccn4,
                ccn5=ccn5,
                avenant=etabJson.get("avenant", False),
                numero_cotisant=etabJson.get("num_cotisant", ""),
                date_radiation=etabJson.get("date_radiation_at", ""),
                code_risque_at=details["ETA_S41_G01_00_026_1"],
                taux_at=details["ETA_S41_G01_00_028_1"],
                is_taux_versement_transport=etabJson.get(
                    "b_versement_transport", False
                ),
                taux_versement_transport=etabJson.get("taux_versement_transport", 0.0),
                banque=Banque(
                    virement=etabJson.get("b_virement", False),
                    code_bic=etabJson.get("code_bic", ""),
                    iban=etabJson.get("iban", ""),
                ),
                gestion_conges_payes=GestionCongesPayes(
                    mois_cloture_droits_cp=details["ETA_MoisClotureCP"],
                    report_automatique_conges_payes=details["ETA_ClotureCPReport"],
                    gestion_absences_conges_heures_sur_bulletins=etabJson.get(
                        "b_abs_cp_heures_bulletins", False
                    ),
                    decompte_conges_payes=etabJson.get("decompte_cp", ""),
                    valorisation_conges_payes=etabJson.get("valorisation_cp", ""),
                    bloquer_gestion_conges_payes=etabJson.get("bloquer_gest_cp", True),
                    etablissement_affilie_caisse_conges_payes=etabJson.get(
                        "affilie_caisse_cp", False
                    ),
                ),
            )
            etabJson = asdict(newEtablissement)
            res.append(
                utils.del_none(dataWithParams(etabJson, {"dossierId": dossierId}))
            )

    return res


def parseSalaries(salDetails: dict, codeDict: dict[str, str]) -> list[dict]:

    res: list[dict] = []
    for numero, salaries in salDetails.items():
        dossierId = codeDict[numero]
        for matricule, salarieInfos in salaries.items():
            print(f"Parsing salarié {matricule} Dossier {numero} ")

            salarie = salarieInfos["reponsesInfosPaie"]
            situationFamilliale = extract.situationFamiliale(salarie["INT_SituationFamiliale"])
            adresse = salarie["INT_BTQC"] + " " + salarie["INT_NomVoie"]
            complement = salarie["INT_ComplementAdresse"]

            salJson: dict = {}
            salJson["matricule_salarie"] = matricule
            salJson["nbr_enfants_charge"] = salarie["SAL_NbPersACharge"]
            salJson["iban"] = salarie["SAL_Iban1"]
            salJson["code_bic"] = salarie["SAL_Bic1"]
            salJson["virement"] = salarie["SAL_Iban1"] != ""
            salJson["civilite"] = salarie["INT_Civilite"]
            salJson["nom"] = salarie["INT_NomUsuel"]
            salJson["prenom"] = salarie["INT_Prenom"]
            salJson["email"] = salarie["INT_Mel"]
            salJson["nom_naissance"] = salarie["INT_NomNaissance"]
            salJson["situation_familiale"] = situationFamilliale
            salJson["numero_ss_cle"] = salarie["INT_NumeroSS"]
            salJson["date_naissance"] = salarie["INT_DateNaissance"]
            salJson["departement"] = salarie["INT_DepartementNaissance"]
            salJson["commune_naissance"] = salarie["INT_CommuneNaissance"]
            salJson["pays_naissance"] = codePays(salarie["INT_PaysNaissance"])
            salJson["numero_voie"] = salarie["INT_NumVoie"]
            salJson["complement"] = adresse
            salJson["pays"] = salarie["INT_NomPays"]
            salJson["nationalite"] = codePays(salarie["INT_PaysNationalite"])
            salJson["frontalier"] = salarie["SAL_Frontalier"]
            salJson["code_postal"] = salarie["INT_CodePostal"]
            salJson["ville"] = salarie["INT_NomVille"]
            salJson["code_insee"] = salarie["INT_CommuneINSEE"]
            salJson["telephone"] = salarie["INT_TelPortablePro"]

            res.append(dataWithParams(salJson, {"dossierId": dossierId}))
    return res

def parseEmplois(emp_detailsMap: dict, codeDict: dict):
    res = []
    for numero, emplois in emp_detailsMap.items():
        dossierId = codeDict[numero]
        numContrat = -1
        for matricule, emploiInfo in emplois.items():
            empJson: dict = {}
            emploi = emploiInfo["reponsesInfosPaie"]
            print(f"Parsing salarié {matricule} Dossier {numero} ")
            numContrat += 1

            # Extracting type_contrat_travail
            cCode = (emploi["SEM_S41_G01_00_012_001"] if emploi["SEM_S41_G01_00_012_001"] != 0 else None)
            motif = emploi["SEM_CDDMotif"] if emploi["SEM_CDDMotif"] != 0 else None
            tContrat = ( emploi["SEM_TypeContratParticulier"] if emploi["SEM_TypeContratParticulier"] != 0 else None)
            emploiPart = (emploi["SEM_EmpCasPart"] if emploi["SEM_EmpCasPart"] != 0 else None)
            
            codeTravail = extract.codeTravail(
                code=cCode,
                motif=motif,
                typeContrat=tContrat,
                emploiPart=emploiPart,
                default_value=90,
            )

            # Extracting statut Pro
            statutPro = extract.statutProf(str(cCode))
            opcc = extract.idccToOpcc(emploi["SEM_CodeCCN"])
            
            ccnEmploi = extract.emploiCCN(emploi["SEM_CLM_Code"], defaultValues=(opcc, 9999))
            
            # verif si code document != code opcc traduction
            if ccnEmploi[0] != opcc:
                code = extract.idccToOpcc(ccnEmploi[0]) 
                opcc = code if code != None else opcc 

            empJson["code_etablissement"] = emploi["EMP_NomInterneEta"][:5]  # TODO: change when codeETA can be >5 chars long
            empJson["matricule_salarie"] = matricule
            empJson["numero_contrat"] = f"{numContrat:05}"
            # empJson["ancien_numero_contrat_dsn"] = emploi[""]
            empJson["emploi_conventionnel"] = ccnEmploi[1]
            empJson["ccn"] = opcc
            empJson["emploi"] =  emploi["EMP_libEmploi"]
            empJson["type_contrat_travail"] = codeTravail
            # empJson["type_contrat_temps_partiel"] = emploi[""]
            empJson["statut_professionnel"] = statutPro
            empJson["regime_retraite"] = emploi["SEM_S41_G01_01_001"]
            # empJson["cas_particuliers"] = extract
            # empJson["salaire_mensuel"] = emploi["SEM_SalaireDeBase"]
            # empJson["date_anciennete"] = emploi["SEM_DtDebAncGrade"]
            # empJson["date_fin_previsionnelle_contrat"] = emploi[""]
            # empJson["date_debut_contrat"] = emploi["EMP_DateDebut"]
            # empJson["nbr_heures_travail_mensuel_majorees"] = emploi[""]
            # empJson["salaire_horaire"] = emploi[""]
            # empJson["salarie_temps_partiel"] = emploi[""]
            # empJson["forfait_jour"] = emploi[""]
            # empJson["jours_hebdo"] = emploi[""]
            # empJson["jour_lundi"] = emploi[""]
            # empJson["jour_mardi"] = emploi[""]
            # empJson["jour_mercredi"] = emploi[""]
            # empJson["jour_jeudi"] = emploi[""]
            # empJson["jour_vendredi"] = emploi[""]
            # empJson["jour_samedi"] = emploi[""]
            # empJson["jour_dimanche"] = emploi[""]
            # empJson["horaire_travail"] = emploi[""]
            # empJson["horaire_hebdo"] = emploi[""]
            # empJson["horaire_lundi"] = emploi[""]
            # empJson["horaire_mardi"] = emploi[""]
            # empJson["horaire_mercredi"] = emploi[""]
            # empJson["horaire_jeudi"] = emploi[""]
            # empJson["horaire_vendredi"] = emploi[""]
            # empJson["horaire_samedi"] = emploi[""]
            # empJson["horaire_dimanche"] = emploi[""]
            # empJson["type_salaire"] = emploi[""]
            # empJson["ne_pas_calculer_premier_bulletin"] = emploi[""]
            # empJson["mois_a_exclure"] = emploi[""]
            # empJson["exclure_janvier"] = emploi[""]
            # empJson["exclure_fevrier"] = emploi[""]
            # empJson["exclure_mars"] = emploi[""]
            # empJson["exclure_avril"] = emploi[""]
            # empJson["exclure_mai"] = emploi[""]
            # empJson["exclure_juin"] = emploi[""]
            # empJson["exclure_juillet"] = emploi[""]
            # empJson["exclure_aout"] = emploi[""]
            # empJson["exclure_septembre"] = emploi[""]
            # empJson["exclure_octobre"] = emploi[""]
            # empJson["exclure_novembre"] = emploi[""]
            # empJson["exclure_decembre"] = emploi[""]
            # empJson["nbr_jour_annuels_prevus"] = emploi[""]
            # empJson["tags"] = emploi[""]

            res.append(dataWithParams(empJson, {"dossierId": dossierId}))
    return res


def dataWithParams(data: dict, params: dict = None):
    jsonWithParam: dict = {}
    jsonWithParam["data"] = data
    jsonWithParam["params"] = params
    return jsonWithParam
