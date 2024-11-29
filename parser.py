from silae import Dossier
import utils
import role
import extract
import statut_pro
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
    if not paysSilae:
        return None
    res = utils.traduire_pays(paysSilae)
    if res != None:
        return res
    res = utils.traduire_pays(paysSilae, mode="code_vers_pays")
    if res and res != "":
        print(f"PAYS NON RECONNU : {paysSilae}")

    return res

def parseDossiers(
    dossierMap: dict[str, Dossier],
    dossiersDetails: JSON,
    max: int,
    defaultContact: dict = emptyContact,
) -> list[dict]:
    openpaye_dossiers: list[dict] = []

    i = 1  # compte le nombre de dossiers créés
    for numero, dossier in dossierMap.items():
        dossDetails = dossiersDetails[numero]
        print(f"Parsing Dossier : {dossier.numero}")
        numero = dossier.numero
        raisonSociale = dossier.raisonSociale
        email = dossDetails["CLI_PersonneAContacterMel"]
        tel = str(dossDetails["CLI_PersonneAContacterTel"]).replace(" ", "")
        nom_contact = (
            dossDetails["CLI_EmployeurPrenom"] + " " + dossDetails["CLI_EmployeurNom"]
        )
        qualSilae = extract.qualite(
            dossDetails["CLI_EmployeurQualite"],
            dossDetails["CLI_EmployeurQualiteAutre"],
        )
        qualite = role.associer_role(str(qualSilae)).value
        openpaye_dossier: dict = {
            "code": numero,
            "nom_dossier": raisonSociale,
            "adresse_email": email,
            "telephone": tel,
            "nom_contact": nom_contact,
            "qualite": qualite,
            "annee": str(datetime.now().year),
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
    res = []
    for numero, etabsJson in etabMap.items():
        dossierId = codeDict[numero]

        for etabJson in etabsJson.get("informationsEtablissements"):
            print(f"Parsing Dossier {numero} Etablissement {etabJson["nomInterne"]} ")
            nomInterne = etabJson.get("nomInterne", "")
            details = etabDetails[nomInterne]

            ccn = extract.idccToOpcc(etabJson.get("idcc"))
            ccn2 = extract.idccToOpcc(etabJson.get("idcc2"))
            ccn3 = extract.idccToOpcc(etabJson.get("idcc3"))
            ccn4 = extract.idccToOpcc(etabJson.get("idcc4"))
            ccn5 = extract.idccToOpcc(etabJson.get("idcc5"))
            civ = f"{int(details.get("INT_Civilite","0"))+1}"

            newEtablissement = Etablissment(
                code=nomInterne[:5],  # limite de 5 caractères pour le code de l'établissement
                raison_sociale=details["INT_RaisonSociale"],
                etablissement_principal=etabJson.get("etablissement_principal", True),
                siret=etabJson.get("siret"),
                adresse=Adresse(
                    adress_postale=details["INT_NumVoie"] + " " + details["INT_NomVoie"],
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
                libelle_ape=details["INT_NAFPrecision"],
                ccn=ccn,
                ccn2=ccn2,
                ccn3=ccn3,
                ccn4=ccn4,
                ccn5=ccn5,
                avenant=etabJson.get("application_avenants", False),
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
            situationFamilliale = extract.situationFamiliale(
                salarie["INT_SituationFamiliale"]
            )
            adresse = salarie["INT_NumVoie"] + " " + salarie["INT_BTQC"] + " " + salarie["INT_NomVoie"]
            complement = salarie["INT_ComplementAdresse"]

            salJson: dict = {}
            adresseDTO: dict = {}
            banqueDTO: dict = {}
            salJson["matricule_salarie"] = matricule
            salJson["nbr_enfants_charge"] = salarie["SAL_NbPersACharge"]
            banqueDTO["iban"] = salarie["SAL_Iban1"]
            banqueDTO["code_bic"] = salarie["SAL_Bic1"]
            banqueDTO["virement"] = salarie["SAL_Iban1"] != "" and salarie["SAL_Bic1"] != ""
            salJson["civilite"] = salarie["INT_Civilite"]
            salJson["nom"] = salarie["INT_NomUsuel"]
            salJson["prenom"] = salarie["INT_Prenom"]
            salJson["email"] = salarie["INT_MelPerso"]
            salJson["nom_naissance"] = salarie["INT_NomNaissance"]
            salJson["situation_familiale"] = situationFamilliale
            salJson["numero_ss_cle"] = salarie["INT_NumeroSS"]
            salJson["date_naissance"] = salarie["INT_DateNaissance"]
            salJson["departement"] = salarie["INT_DepartementNaissance"]
            salJson["commune_naissance"] = salarie["INT_CommuneNaissance"]
            salJson["pays_naissance"] = codePays(salarie["INT_PaysNaissance"])
            salJson["nationalite"] = codePays(salarie["INT_PaysNationalite"])
            salJson["telephone"] = salarie["INT_TelPortable"].replace(" ","").replace(".","")
            # if salJson["telephone"].startswith("0"):
            #     salJson["telephone"] = salJson["telephone"][1:]
            adresseDTO["numero_voie"] = adresse
            adresseDTO["complement"] = complement
            adresseDTO["pays"] = codePays(salarie["INT_NomPays"])
            adresseDTO["frontalier"] = salarie["SAL_Frontalier"]
            adresseDTO["code_postal"] = salarie["INT_CodePostal"]
            adresseDTO["ville"] = salarie["INT_NomVille"]
            adresseDTO["code_insee"] = salarie["INT_CommuneINSEE"]

            salJson["adresse"] = adresseDTO
            salJson["banque"] = banqueDTO

            res.append(dataWithParams(salJson, {"dossierId": dossierId}))
    res = utils.filterEmptyResData(res)
    return res


def parseEmplois(emp_detailsMap: dict, codeDict: dict):
    res = []
    for numero, emplois in emp_detailsMap.items():
        dossierId = codeDict[numero]
        numContrat = -1
        for matricule, emploiInfo in emplois.items():
            empJson: dict = {}
            moisAExclure: dict = {}
            joursHebdo: dict = {}
            horaires: dict = {}
            emploi = emploiInfo["reponsesInfosPaie"]
            print(f"Parsing emplois {matricule} Dossier {numero} ")
            numContrat += 1
            # Extracting type_contrat_travail
            cCode = (
                emploi["SEM_S41_G01_00_012_001"]
                if emploi["SEM_S41_G01_00_012_001"] != ""
                else None
            )
            motif = emploi["SEM_CDDMotif"] if emploi["SEM_CDDMotif"] != "" else None
            tContrat = (
                emploi["SEM_TypeContratParticulier"]
                if emploi["SEM_TypeContratParticulier"] != ""
                else None
            )
            emploiPart = (
                emploi["SEM_EmpCasPart"] if emploi["SEM_EmpCasPart"] != "" else None
            )
            codeTravail = extract.codeTravail(code=cCode, motif=motif, typeContrat=tContrat, emploiPart=emploiPart, default_value=90)
            
            opcc = extract.idccToOpcc(emploi["SEM_CodeCCN"])
            ccnEmploi = extract.emploiCCN(emploi["SEM_CLM_Code"], emploi["SEM_S41_G01_00_014"], ccn=opcc)
            statutPro = extract.statutProf(ccnEmploi[2])
            # verif si code document != code opcc traduction
            if ccnEmploi[0] != opcc:
                code = extract.idccToOpcc(ccnEmploi[0])
                opcc = code if code != None else opcc
                    
            empJson["ccn"] = opcc if opcc == 4578 else None
            empJson["code_etablissement"] = emploi["EMP_NomInterneEta"][:5]  # TODO: change when codeETA can be >5 chars long
            empJson["matricule_salarie"] = matricule
            empJson["numero_contrat"] = f"{numContrat:05}"
            # empJson["ancien_numero_contrat_dsn"] = emploi[""]
            empJson["emploi_conventionnel"] = ccnEmploi[1]
            empJson["emploi"] = emploi["EMP_libEmploi"]
            empJson["type_contrat_travail"] = codeTravail
            # empJson["type_contrat_temps_partiel"] = emploi[""]
            empJson["statut_professionnel"] = statutPro
            empJson["regime_retraite"] = emploi["SEM_S41_G01_01_001"]
            # empJson["cas_particuliers"] = extract
            dateAnc = emploi["SEM_DtDebAncGrade"]
            empJson["date_anciennete"] = dateAnc if dateAnc and dateAnc != "" else emploi["EMP_DateDebut"]
            dtFin = emploi["EMP_DateFin"]
            if dtFin and dtFin != "":
                empJson["date_fin_previsionnelle_contrat"] = dtFin
            empJson["date_debut_contrat"] = emploi["EMP_DateDebut"]
            # empJson["salarie_temps_partiel"] = emploi[""]

            empJson["forfait_jour"] = emploi["SEM_S41_G01_00_013"] == "10"
            typeSal = emploi["SEM_TypeSalaireDeBase"]
            if typeSal == 0:
                empJson["type_salaire"] = "Mensuel"
                empJson["salaire_mensuel"] = emploi["SEM_SalaireDeBase"]
            elif typeSal == 1:
                empJson["type_salaire"] = "Horaire"
                empJson["salaire_horaire"] = emploi["SEM_SalaireDeBase"]

            if empJson["forfait_jour"]:
                empJson["nbr_jour_annuels_prevus"] = emploi["SEM_FJNbJAn"]
                
                # Vaut 8 si c'est un jour travaillé (case correspondante cochée, 0 si ce n'est pas le cas)
                joursHebdo["jour_lundi"] = emploi["SEM_HTLun"] == 8
                joursHebdo["jour_mardi"] = emploi["SEM_HTMar"] == 8
                joursHebdo["jour_mercredi"] = emploi["SEM_HTMer"] == 8
                joursHebdo["jour_jeudi"] = emploi["SEM_HTJeu"] == 8
                joursHebdo["jour_vendredi"] = emploi["SEM_HTVen"] == 8
                joursHebdo["jour_samedi"] = emploi["SEM_HTSam"] == 8
                joursHebdo["jour_dimanche"] = emploi["SEM_HTDim"] == 8
                empJson["jours_hebdomadaires"] = joursHebdo
            else:
                empJson["nbr_heures_travail_mensuel_majorees"] = emploi[
                    "SEM_HoraireMensuelHeuresMajorees"
                ]
                # empJson["horaire_travail"] = emploi["SEM_TotalHeures"] NOTWORK
                # empJson["horaire_hebdo"] = emploi["SEM_MTH"] NOTWORK
                horaires["horaire_lundi"] = emploi["SEM_HTLun"]
                horaires["horaire_mardi"] = emploi["SEM_HTMar"]
                horaires["horaire_mercredi"] = emploi["SEM_HTMer"]
                horaires["horaire_jeudi"] = emploi["SEM_HTJeu"]
                horaires["horaire_vendredi"] = emploi["SEM_HTVen"]
                horaires["horaire_samedi"] = emploi["SEM_HTSam"]
                horaires["horaire_dimanche"] = emploi["SEM_HTDim"]
                empJson["horaires"] = horaires
            # empJson["ne_pas_calculer_premier_bulletin"] = emploi[""]
            moisCompris = emploi["SEM_BulletinsMoisBits"]
            if moisCompris != None:
                bullArray = integerToBitArray(moisCompris)
                moisAExclure["exclure_janvier"] = bullArray[0]
                moisAExclure["exclure_fevrier"] = bullArray[1]
                moisAExclure["exclure_mars"] = bullArray[2]
                moisAExclure["exclure_avril"] = bullArray[3]
                moisAExclure["exclure_mai"] = bullArray[4]
                moisAExclure["exclure_juin"] = bullArray[5]
                moisAExclure["exclure_juillet"] = bullArray[6]
                moisAExclure["exclure_aout"] = bullArray[7]
                moisAExclure["exclure_septembre"] = bullArray[8]
                moisAExclure["exclure_octobre"] = bullArray[9]
                moisAExclure["exclure_novembre"] = bullArray[10]
                moisAExclure["exclure_decembre"] = bullArray[11]
                empJson["mois_a_exclure"] = moisAExclure
            # empJson["tags"] = emploi[""]

            res.append(dataWithParams(empJson, {"dossierId": dossierId}))
    res = utils.filterEmptyResData(res)
    return res


def updateContrats(contratsCrees, op_contratsIdToDSN):
    contratsToUpdate = []
    for contrat in contratsCrees:
        oldNumDSN = op_contratsIdToDSN[contrat["matricule_salarie"]][1]
        if not oldNumDSN or oldNumDSN == "":
            continue
        contrat["numero_contrat"] = oldNumDSN
        contratsToUpdate.append(dataWithParams(contrat, None))
    return contratsToUpdate


def parseCumuls(cumul_detailsMap: dict, matriculeContratId: dict[str, dict]):
    res: list = []
    matMapDSNToContratID = {}
    for _, encodedCumuls in cumul_detailsMap.items():
        cumulCsv = utils.base64ToCsv(encodedCumuls["Cumul"])
        col = extract.editionCumulColonnes()
        cumulMap = utils.CsvToMap(cumulCsv)
        varval: dict[str,str] = {}
        for i in range(len(cumulMap)):
            for code, titre in col.items():
                varval[code] = cumulMap[i][titre]
            matricule = cumulMap[i]["Matricule"]
            contratID = matriculeContratId[matricule]["id"]
            datereprise = dict()
            datereprise["contratId"] = contratID
            datereprise["nomVariable"] = "$DOS.DATEREPRISE"
            datereprise["valeur"] = encodedCumuls["DateReprise"]
            res.append(dataWithParams(None,datereprise))
            for var, val in varval.items():
                if float(val) == 0.0:
                    print(f"Skip 0: {var} {val}")
                    continue # passe l'ajout de cette valeur, 0 est la valeur par défaut dans des variables de cumuls
                params = dict()
                params["contratId"] = contratID
                params["nomVariable"] = var
                params["valeur"] = str(float(val))
                res.append(dataWithParams(None, params))
                if (
                    matriculeContratId[matricule]["date_debut_contrat"]
                    == cumulMap[i]["Datededébutdecontrat"]
                ):
                    matMapDSNToContratID[matricule] = (
                        matriculeContratId[matricule]["id"],
                        cumulMap[i]["Numérodecontrat"],
                    )
    return (res, matMapDSNToContratID)


def dataWithParams(data: dict, params: dict = None):
    jsonWithParam: dict = {}
    jsonWithParam["data"] = data
    jsonWithParam["params"] = params
    return jsonWithParam

    # $SAL.CUMULANT_HRS" : "Heures",
    # $SAL.CUMULANT_HRSSUP" : "HeuresSupp",
    # $SAL.CUMULANT_BRUT" : "Brut",
    # $SAL.CUMULANT_NET" : "Netàpayer",
    # $SAL.CUMULANT_NETIMPO" : "Netimposable",
    # $SAL.CUMULANT_ABAT" : "Abattement",
    # $SAL.CUMULANT_PMSS" : "PMSS",
    # $SAL.CUMULANT_TA" : "TrancheA",
    # $SAL.CUMULANT_TB" : "TrancheB",
    # $SAL.CUMULANT_TC" : "TrancheC",
    # $SAL.CUMULANT_T2" : "Tranche2AFIRCARRCO",
    # $SAL.CUMULANT_SMICFILLON" : "SMICFILLOn",
    # $SAL.CUMULANT_RNF" : "MontantnetfiscaléxonérationsurHSHC",
    # $SAL.CUMULANT_CP" : "ChargesPatronales",
    # $SAL.CUMULANT_MTPAS" : "RetenueAlasource",
    # $SAL.CUMULANT_BASECPN1" : "BaseCPN1",
    # $SAL.CUMULANT_BASECPPRISN1" : "BaseCPPrisN1",
    # $SAL.CUMULANT_CPN1" : "JoursAcquisN1",
    # $SAL.CUMULANT_CPPRISN1" : "JoursPrisN1",
    # $SAL.CUMULANT_BASECPN" : "BaseCPN",
    # $SAL.CUMULANT_BASECPPRISN" : "BaseCPPrisN",
    # $SAL.CUMULANT_CPN" : "JoursAcquisN",
    # $SAL.CUMULANT_CPPRISN" : "JoursPrisN",
    # $SAL.RTTACQUIS" : "RTTACQUIS",
    # $SAL.RTTPRIS" : "RTTPRIS",
