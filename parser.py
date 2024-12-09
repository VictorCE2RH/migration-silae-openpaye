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

def parseDossiers(dossierMap: dict[str, Dossier], dossiersDetails: JSON, defaultContact: dict = emptyContact) -> list[dict]:
    openpaye_dossiers: list[dict] = []
    keys_to_delete:list[str] = []
    for numero, dossier in dossierMap.items():
        dossDetails = dossiersDetails[numero]
        print(f"Parsing Dossier : {dossier.numero}")
        numero = dossier.numero
        raisonSociale = dossier.raisonSociale
        email:str = dossDetails["CLI_PersonneAContacterMel"]
        tel = str(dossDetails["CLI_PersonneAContacterTel"]).replace(" ","").replace(".","")
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
            "adresse_email": email.split(";")[0] if email != '' else None,
            "telephone": tel if tel != '' else None,
            "nom_contact": nom_contact,
            "qualite": qualite,
            "annee": str(datetime.now().year),
        }
        if not openpaye_dossier["adresse_email"]:
            logger.printWarn(f"Informations incompletes Dossier {numero}: {openpaye_dossier}")
            keys_to_delete.append(numero)
            continue
        openpaye_dossiers.append(dataWithParams(openpaye_dossier))
    for numero in keys_to_delete:
        del dossierMap[numero]
    return openpaye_dossiers

def parseEtablissements(etabMap: JSON, etabDetails: dict, codeDict: dict[str, str]) -> list[dict]:
    res = []
    for numero, etabsJson in etabMap.items():
        dossierId = codeDict[numero]

        for etabJson in etabsJson.get("informationsEtablissements"):
            print(f"Parsing Dossier {numero} Etablissement {etabJson["nomInterne"]} ")
            nomInterne = etabJson.get("nomInterne", "")
            details = etabDetails[nomInterne]

            ccn = next(iter(extract.idccToOpcc(etabJson.get("idcc")) or []), None) 
            ccn2 = next(iter(extract.idccToOpcc(etabJson.get("idcc2")) or []), None)
            ccn3 = next(iter(extract.idccToOpcc(etabJson.get("idcc3")) or []), None)
            ccn4 = next(iter(extract.idccToOpcc(etabJson.get("idcc4")) or []), None)
            ccn5 = next(iter(extract.idccToOpcc(etabJson.get("idcc5")) or []), None)

            civ = extract.civilite(int(details["INT_Civilite"]))
            
            virement = etabJson.get("b_virement", False)
            bic = etabJson["code_bic"] if etabJson["code_bic"] != '' else None
            iban = etabJson["iban"] if etabJson["iban"] != '' else None
            
            tauxAT = details["ETA_S41_G01_00_028_1"]
            if tauxAT == 0:
                tauxAT = extract.getTauxAT(details["ETA_S41_G01_00_026_1"],datetime.now().year)

            newEtablissement = Etablissment(
                code=nomInterne,  # limite de 5 caractères pour le code de l'établissement
                raison_sociale=details["INT_RaisonSociale"],
                etablissement_principal=etabJson.get("etablissementPrincipal", False),
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
                taux_at=tauxAT,
                is_taux_versement_transport=etabJson.get(
                    "b_versement_transport", False
                ),
                taux_versement_transport=etabJson.get("taux_versement_transport", 0.0),
                banque=Banque(
                    virement=virement,
                    code_bic=bic,
                    iban=iban,
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
            res.append(utils.del_none(dataWithParams(etabJson, {"dossierId": dossierId})))
    res = filterEmptyResData(res)
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
            salJson["civilite"] = extract.civilite(salarie["INT_Civilite"]) 
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

def parseEmplois(emp_detailsMap: dict,etab_detailsMap:dict, codeDict: dict):
    res = []
    for numero, emplois in emp_detailsMap.items():
        dossierId = codeDict[numero]
        for matricule, emploiInfo in emplois.items():
            empJson: dict = {}
            moisAExclure: dict = {}
            joursHebdo: dict = {}
            horaires: dict = {}
            emploi = emploiInfo["reponsesInfosPaie"]
            etabDetails = etab_detailsMap[emploi["EMP_NomInterneEta"]]
            print(f"Parsing emplois {matricule} Dossier {numero} ")
            # Extracting type_contrat_travail
            cCode = (emploi["SEM_S41_G01_00_012_001"] if emploi["SEM_S41_G01_00_012_001"] != "" else None)
            motif = emploi["SEM_CDDMotif"] if emploi["SEM_CDDMotif"] != "" else None
            tContrat = (emploi["SEM_TypeContratParticulier"] if emploi["SEM_TypeContratParticulier"] != "" else None)
            emploiPart = (emploi["SEM_EmpCasPart"] if emploi["SEM_EmpCasPart"] != "" else None)
            codeTravail = extract.codeTravail(code=cCode, motif=motif, typeContrat=tContrat, emploiPart=emploiPart, default_value=90)
            
            opcc = extract.idccToOpcc(emploi["SEM_CodeCCN"])
            ccnEmploi = extract.emploiCCN(emploi["SEM_CLM_Code"], emploi["SEM_S41_G01_00_014"], ccns=opcc)
            logger.printStat(f"ccn Emploi : {emploi["SEM_CLM_Code"]} {emploi["SEM_S41_G01_00_014"]} {opcc} = {ccnEmploi}")
            statutPro = extract.statutProf(ccnEmploi[2])
            # verif si code document != code opcc traduction
            if ccnEmploi[0] != opcc:
                code = next(iter(extract.idccToOpcc(ccnEmploi[0]) or []), None)
                opcc = code if code != None else opcc[0]
                    
            empJson["ccn"] = opcc
            empJson["code_etablissement"] = emploi["EMP_NomInterneEta"]
            empJson["matricule_salarie"] = matricule
            empJson["numero_contrat"] = f"{1:05}"
            # empJson["ancien_numero_contrat_dsn"] = emploi[""]
            empJson["emploi_conventionnel"] = ccnEmploi[1]
            empJson["emploi"] = emploi["EMP_libEmploi"]
            empJson["type_contrat_travail"] = codeTravail
            empJson["statut_professionnel"] = statutPro
            empJson["regime_retraite"] = extract.regimeRetraite(emploi["SEM_S41_G01_00_015_002"])
            # empJson["cas_particuliers"] = extract
            dateAnc = emploi["SEM_DtDebAncGrade"]
            empJson["date_debut_contrat"] = emploi["EMP_DateDebut"]
            empJson["date_debut_emploi"] = emploi["EMP_DateDebut"]
            empJson["date_anciennete"] = dateAnc if dateAnc and dateAnc != "" else emploi["EMP_DateDebut"]
            dtFin = emploi["EMP_DateFin"]
            if dtFin and dtFin != "":
                empJson["date_fin_previsionnelle_contrat"] = dtFin
            
            empJson["forfait_jour"] = emploi["SEM_S41_G01_00_013"] == "10"
            typeSal = emploi["SEM_TypeSalaireDeBase"]
            salBase = utils.extract_decimal(emploi["SEM_SalaireDeBase"]) 
            salBase = salBase if salBase != 0 else None
            
            if typeSal == 0:
                empJson["type_salaire"] = "Mensuel"
                empJson["salaire_mensuel"] = salBase
            elif typeSal == 1:
                empJson["type_salaire"] = "Horaire"
                empJson["salaire_horaire"] = salBase

            if empJson["forfait_jour"]:
                empJson["nbr_jour_annuels_prevus"] = emploi["SEM_FJNbJAn"]
                
                # Vaut 8 si c'est un jour travaillé (case correspondante cochée, 0 si ce n'est pas le cas)
                joursHebdo["jour_lundi"] = utils.calculateJour(emploi["SEM_HTLun"])
                joursHebdo["jour_mardi"] = utils.calculateJour(emploi["SEM_HTMar"])
                joursHebdo["jour_mercredi"] = utils.calculateJour(emploi["SEM_HTMer"])
                joursHebdo["jour_jeudi"] = utils.calculateJour(emploi["SEM_HTJeu"])
                joursHebdo["jour_vendredi"] = utils.calculateJour(emploi["SEM_HTVen"])
                joursHebdo["jour_samedi"] = utils.calculateJour(emploi["SEM_HTSam"])
                joursHebdo["jour_dimanche"] = utils.calculateJour(emploi["SEM_HTDim"])
                empJson["jours_hebdomadaires"] = joursHebdo
            else:
                hMMensuel = emploi["SEM_HoraireMensuelHeuresMajorees"]
                empJson["nbr_heures_travail_mensuel_majorees"] = hMMensuel if hMMensuel > 0 else etabDetails["ETA_HMHoraireMensuel"]
                totalHebdoSalarie = emploi["SEM_HTLun"] + emploi["SEM_HTMar"] + emploi["SEM_HTMer"] + emploi["SEM_HTJeu"] + emploi["SEM_HTVen"] + emploi["SEM_HTSam"] + emploi["SEM_HTDim"]
                if totalHebdoSalarie == 0:
                    horaires["horaire_lundi"] = float(etabDetails["ETA_HTLun"]) + float(etabDetails["ETA_HMLun"])
                    horaires["horaire_mardi"] = float(etabDetails["ETA_HTMar"]) + float(etabDetails["ETA_HMMar"])
                    horaires["horaire_mercredi"] = float(etabDetails["ETA_HTMer"]) + float(etabDetails["ETA_HMMer"])
                    horaires["horaire_jeudi"] = float(etabDetails["ETA_HTJeu"]) + float(etabDetails["ETA_HMJeu"])
                    horaires["horaire_vendredi"] = float(etabDetails["ETA_HTVen"]) + float(etabDetails["ETA_HMVen"])
                    horaires["horaire_samedi"] = float(etabDetails["ETA_HTSam"]) + float(etabDetails["ETA_HMSam"])
                    horaires["horaire_dimanche"] = float(etabDetails["ETA_HTDim"]) + float(etabDetails["ETA_HMDim"])
                else: 
                    horaires["horaire_lundi"] = float(emploi["SEM_HTLun"]) + float(emploi["SEM_HMLun"])  
                    horaires["horaire_mardi"] = float(emploi["SEM_HTMar"]) + float(emploi["SEM_HMMar"])  
                    horaires["horaire_mercredi"] = float(emploi["SEM_HTMer"]) + float(emploi["SEM_HMMer"])
                    horaires["horaire_jeudi"] = float(emploi["SEM_HTJeu"]) + float(emploi["SEM_HMJeu"])
                    horaires["horaire_vendredi"] = float(emploi["SEM_HTVen"]) + float(emploi["SEM_HMVen"])
                    horaires["horaire_samedi"] = float(emploi["SEM_HTSam"]) + float(emploi["SEM_HMSam"]) 
                    horaires["horaire_dimanche"] = float(emploi["SEM_HTDim"]) + float(emploi["SEM_HMDim"])
                horaires["horaire_hebdo"] = horaires["horaire_lundi"] + horaires["horaire_mardi"] + horaires["horaire_mercredi"] + horaires["horaire_jeudi"] + horaires["horaire_vendredi"] + horaires["horaire_samedi"] + horaires["horaire_dimanche"]
                horaires["horaire_travail"] = emploi['SEM_HoraireMensuel'] if emploi['SEM_HoraireMensuel'] > 0 else float(etabDetails["ETA_HNHoraireMensuel"]) + float(etabDetails["ETA_HMHoraireMensuel"])
                
                empJson["horaires"] = horaires
                empJson["salarie_temps_partiel"] = horaires["horaire_hebdo"] < 35
                # empJson["type_contrat_temps_partiel"] = emploi[""]
            # empJson["ne_pas_calculer_premier_bulletin"]
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
        newContrat = {}
        contratToDSN = op_contratsIdToDSN.get(contrat["matricule_salarie"],None)
        if not contratToDSN or contratToDSN == () or contratToDSN[1] == "":
            continue
        contrat["numero_contrat"] = contratToDSN[1]
        contratsToUpdate.append(dataWithParams(contrat, None))
    return contratsToUpdate

def parseCumuls(cumul_detailsMap: dict, matriculeContratId: dict[str, dict]):
    res: list = []
    nbSkips = 0
    matMapDSNToContratID = {}
    for _, encodedCumuls in cumul_detailsMap.items():
        cumulCsv = utils.base64CSVToDict(encodedCumuls["Cumul"])
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
                    nbSkips += 1
                    continue # passe l'ajout de cette valeur, 0 est la valeur par défaut dans des variables de cumuls
                params = dict()
                params["contratId"] = contratID
                params["nomVariable"] = var
                params["valeur"] = str(float(val))
                res.append(dataWithParams(None, params))
                if (matriculeContratId[matricule]["date_debut_contrat"] == cumulMap[i]["Datededébutdecontrat"]):
                    matMapDSNToContratID[matricule] = (matriculeContratId[matricule]["id"], cumulMap[i]["Numérodecontrat"])
    logger.printStat(f"{nbSkips} Skips de variables valeurs = 0.0")
    return (res, matMapDSNToContratID)

def updateSpecificsCcns(etabCrees:list[dict], emp_detailsMap: dict):
    specificCCNS = ["16"]
    for etab in etabCrees:
        if etab["data"]["ccn"] not in specificCCNS:
            continue
        # for numero, emplois in emp_detailsMap.items():
        #     emploi = extract.idccToOpcc

def dataWithParams(data: dict, params: dict = None):
    jsonWithParam: dict = {}
    jsonWithParam["data"] = data
    jsonWithParam["params"] = params
    return jsonWithParam
