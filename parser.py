from silae import Dossier
import utils
import role
import extract
import statut_pro as sp
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
        logger.log(f"PAYS NON RECONNU : {paysSilae}")
    return res

def parseDossiers(domain:str, dossierMap: dict[str, Dossier], dossiersDetails: JSON, defaultContact: dict = emptyContact) -> tuple[list[dict],list[dict]]:
    openpaye_dossiers: list[dict] = []
    keys_to_delete:list[str] = []
    for numero, dossier in dossierMap.items():
        dossDetails = dossiersDetails[numero]
        logger.log(f"Parsing Dossier : {dossier.numero}")
        numero = dossier.numero
        raisonSociale = dossier.raisonSociale
        
        #TODO: sketchy signataire mail placeholder, mais nécessaire si on veut pousser les dossiers
        email = dossDetails["CLI_PersonneAContacterMel"] 
        email = getPlaceholderMail(domain) if not email or email == '' else email.split(";")[0]
        
        tel = dossDetails["CLI_PersonneAContacterTel"]
        tel = tel.replace(" ","").replace(".","") if tel != '' else None
        
        nom_contact = (dossDetails["CLI_EmployeurPrenom"] + " " + dossDetails["CLI_EmployeurNom"])
        qualSilae = extract.qualite(dossDetails["CLI_EmployeurQualite"],dossDetails["CLI_EmployeurQualiteAutre"])
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
        if not openpaye_dossier["adresse_email"]:
            logger.warning(f"Informations incompletes Dossier {numero}: {openpaye_dossier}")
            keys_to_delete.append(numero)
            continue
        openpaye_dossiers.append(dataWithParams(openpaye_dossier))
    for numero in keys_to_delete:
        del dossierMap[numero]
    return openpaye_dossiers

def parseEtablissements(etabMap: JSON, etabDetails: dict, codeDict: dict[str, str]) -> list[dict]:
    res = []
    for numero, etabs in etabMap.items():
        dossierId = codeDict[numero]
        for _, etab in enumerate(etabs["informationsEtablissements"]):
            nomInterne = etab.get("nomInterne")
            if nomInterne == "":
                logger.warning(f"Dossier {numero} : Nom interne établissement vide. IGNORÉ")
                continue
            details = etabDetails[numero][nomInterne]
            logger.log(f"Parsing Dossier {numero} Etablissement {nomInterne} Raison Sociale : {details["INT_RaisonSociale"]}")

            ccn  = extract.translateToOpcc(etab["ccn"], etab["idcc"],userInput=True)
            ccn2 = extract.translateToOpcc(etab["ccn2"],etab["idcc2"],userInput=True)
            ccn3 = extract.translateToOpcc(etab["ccn3"],etab["idcc3"],userInput=True)
            ccn4 = extract.translateToOpcc(etab["ccn4"],etab["idcc4"],userInput=True)
            ccn5 = extract.translateToOpcc(etab["ccn5"],etab["idcc5"],userInput=True)

            civ = extract.civilite(int(details["INT_Civilite"]))
            
            virement = etab.get("b_virement", False)
            bic = etab["code_bic"]
            iban = etab["iban"]
            banque = None
            if bic != '' and iban != '':
                if utils.validIban(iban):
                    banque = Banque(
                        code_bic=bic,
                        iban=iban,
                        virement=True,
                    )
                else:
                    logger.error(f"Dossier {numero} - etab {nomInterne} : invalid IBAN {iban}")
            else:
                logger.error(f"Dossier {numero} - etab {nomInterne} : donnée de banque vide iban {iban} bic {bic}")
            tauxAT = details["ETA_S41_G01_00_028_1"]
            if tauxAT == 0:
                tauxAT = extract.getTauxAT(details["ETA_S41_G01_00_026_1"],datetime.now().year)
            siret = etab["siret"]
            if len(siret) not in [13,14]:
                logger.error(f"Dossier {numero} : siret '{siret}' invalide, doit faire 13 ou 14 charactères de long ")
                siret = None
            etabObj = Etablissment(
                code=nomInterne,  # limite de 5 caractères pour le code de l'établissement
                raison_sociale= details["INT_RaisonSociale"],
                main= etab["etablissement_principal"],
                siret=siret,
                adresse=Adresse(
                    adress_postale= details["INT_NumVoie"] + " " + details["INT_NomVoie"],
                    adress_postale2="",
                    complement_adress= details["INT_ComplementAdresse"],
                    code_postal= details["INT_CodePostal"],
                    ville= details["INT_NomVille"],
                    code_insee= details["INT_CommuneINSEE"],
                    code_distribution_etranger="",
                    pays= details["INT_NomPays"],
                ),
                forme_juridique=extract.formeJuridique(details["INT_FormeJuridique"]),  # Forme juridique, voir correspondance silae<>openpaye
                activite=etab.get("activite", ""),
                civilite=civ,
                ape= details["INT_NAF"],
                libelle_ape= details["INT_NAFPrecision"],
                ccn= ccn,
                ccn2= ccn2,
                ccn3= ccn3,
                ccn4= ccn4,
                ccn5= ccn5,
                avenant= etab["application_avenants"],
                numero_cotisant= etab.get("num_cotisant",None),
                date_radiation=etab.get("date_radiation_at", None),
                code_risque_at= details["ETA_S41_G01_00_026_1"],
                taux_at=tauxAT,
                is_taux_versement_transport=etab.get(
                    "b_versement_transport", False
                ),
                taux_versement_transport=etab.get("taux_versement_transport", 0.0),
                banque=banque,
                gestion_conges_payes=GestionCongesPayes(
                    mois_cloture_droits_cp= details["ETA_MoisClotureCP"],
                    report_automatique_conges_payes= details["ETA_ClotureCPReport"],
                    gestion_absences_conges_heures_sur_bulletins=etab.get(
                        "b_abs_cp_heures_bulletins", False
                    ),
                    decompte_conges_payes=etab.get("decompte_cp", ""),
                    valorisation_conges_payes=etab.get("valorisation_cp", ""),
                    bloquer_gestion_conges_payes=etab.get("bloquer_gest_cp", True),
                    etablissement_affilie_caisse_conges_payes=etab.get(
                        "affilie_caisse_cp", False
                    ),
                ),
            )
            if etabObj.banque and (etabObj.banque.iban == '' or etabObj.banque.code_bic == ''):
                etabObj.banque = None
            etabJson = asdict(etabObj)
            etabJson = utils.del_none(dataWithParams(etabJson, {"dossierId": dossierId}))
            if etabObj.main:
                res.insert(0, etabJson)
                # les établissements principaux sont poussé au début de la file de création, 
                # dans le cas contraire un etablissement secondaire pourrait être poussé en premier sur un dossier 
                # et prendre le statut d'établissement principal
            else:
                res.append(etabJson)
    res = filterEmptyResData(res)
    return res

def parseOrganismes(organismesMap: dict[str,list],etabDict: dict[str,int]) -> list[dict]:
    # nom_caisse				string      Le Nom de la caisse
    # code_dsn	 				string      Le Code de la caisse
    # adresse_caisse	 		string      L'Adresse de la caisse
    # etablissement_id	 		integer     L'ID de l'établissement associé.
    # type_cotisation  required string      Le type de cotisation.
    # exclus_de_calcul_dsn	 	boolean     Indique si la caisse est exclue du calcul DSN.
    # numero_affiliation	 	string      [ 0 .. 20 ] characters Le numéro d'affiliation.
    # type_paiement	 		    string      Le type de paiement.
    # periodicite_paiement	    string 	    La périodicité de paiement.
    # date_paiement	 	        string 		La date de paiement.
    # iban	 				    string 		Le code IBAN.
    # bic	 				    string 		[ 8 .. 11 ] characters ^([A-Z]{6}[A-Z2-9][A-NP-Z1-9])(X{3}|[A-WY-Z0-...Show pattern Le code BIC.
    res:list[dict] = []
    for numero, organismes in organismesMap.items():
        for organisme in organismes:
            orgaJson: dict = {}
            nomInterne = organisme["nomInterneEtablissement"]
            codeEtabId = f"{numero}/{nomInterne}"
            idEtab = etabDict[codeEtabId]
            orgaJson["code_dsn"] = organisme["codeOrganisme"]
            # orgaJson["nom_caisse"] = extract.nomNatureCotisation(organisme["codeNature"])
            orgaJson["type_cotisation"] = organisme["codeNature"]
            orgaJson["etablissement_id"] = idEtab
            orgaJson["numero_affiliation"] = organisme["numeroAffiliation"]
            orgaJson["periodicite_paiement"] = extract.paiementPeriodicite(organisme["periodicite"])
            orgaJson["date_paiement"] = str(organisme["jourPaiement"])
            orgaJson["type_paiement"] = extract.typePrelevement(organisme["ediModePaiement"])

            # orgaJson:[""] = organisme["edi"]
            # orgaJson[""] = organisme["codeInterne"]
            # orgaJson[""] = organisme["filtreSalaries"]
            # orgaJson[""] = organisme["filtreCodesLibelles"]
            # orgaJson[""] = organisme["numeroRattachement"]
            # orgaJson[""] = organisme["codePopulation"]
            # orgaJson[""] = organisme["codeOption"]
            # orgaJson[""] = organisme["codeDelegataireDeGestion"]
            
            res.append(dataWithParams(utils.del_none(orgaJson)))
    res = utils.filterEmptyResData(res)
    return res

def parseSalaries(salDetails: dict, codeDict: dict[str, str]) -> list[dict]:
    res: list[dict] = []
    for numero, salaries in salDetails.items():
        dossierId = codeDict[numero]
        for matricule, salarieInfos in salaries.items():
            logger.log(f"Parsing salarié {matricule} Dossier {numero} ")
            
            salarie = salarieInfos["reponsesInfosPaie"]
            situationFamilliale = extract.situationFamiliale(salarie["INT_SituationFamiliale"])
            adresse = f"{salarie["INT_NumVoie"]}{salarie["INT_BTQC"]} {salarie["INT_NomVoie"]}"
            complement = salarie["INT_ComplementAdresse"]

            salJson: dict = {}
            adresseDTO: dict = {}            
            banqueDTO: dict = {}
            salJson["banque"] = None
            banqueDTO["iban"] = salarie["SAL_Iban1"]
            banqueDTO["code_bic"] = salarie["SAL_Bic1"]
            banqueDTO["virement"] = True
            
            if banqueDTO["iban"] != "" and banqueDTO["code_bic"] != "":
                salJson["banque"] = banqueDTO
            
            salJson["matricule_salarie"] = matricule
            salJson["nbr_enfants_charge"] = salarie["SAL_NbPersACharge"]
            salJson["civilite"] = extract.civilite(salarie["INT_Civilite"]) 
            salJson["nom"] = salarie["INT_NomUsuel"]
            salJson["prenom"] = salarie["INT_Prenom"]
            salJson["email"] = salarie["INT_MelPerso"]
            salJson["nom_naissance"] = salarie["INT_NomNaissance"]
            salJson["situation_familiale"] = situationFamilliale
            salJson["numero_ss_cle"] = salarie["INT_NumeroSS"]
            if len(salarie["INT_NumeroSS"]) not in [14,15]:
                logger.error(f"Parsing Salarié {matricule} : Numéro de sécurité sociale invalide (Doit être entre 14 et 15 caractères) : '{salarie["INT_NumeroSS"]}'")
                salJson["numero_ss_cle"] = None
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

            res.append(dataWithParams(salJson, {"dossierId": dossierId}))
    res = utils.filterEmptyResData(res)
    return res

def parseEmplois(emp_detailsMap: dict, sal_DetailsMap: dict,etab_detailsMap:dict, codeDict: dict):
    res = []
    for numero, emplois in emp_detailsMap.items():
        empMatRes = {}
        dossierId = codeDict[numero]
        for matricule, emplois in emplois.items():
            empMatRes[matricule] = list()
            for i, emploi in enumerate(emplois):
                # Initialisation des variables utile à l'emploi
                empJson: dict = {}
                moisAExclure: dict = {}
                joursHebdo: dict = {}
                horaires: dict = {}
                departSalarie: dict = None
                salarie = sal_DetailsMap[numero][matricule]["reponsesInfosPaie"]
                etabDetails = etab_detailsMap[numero][emploi["EMP_NomInterneEta"]]
                
                # Gestion numero contrat
                numeroContrat = emploi["SEM_DSNNumeroContrat"] if emploi["SEM_DSNNumeroContrat"] != "" else "vide" 
                logger.log(f"Parsing matricule(emploi) {matricule}({numeroContrat}) Dossier {numero} ")
                empJson["numero_contrat"] = numeroContrat
                
                # Gestion des dates
                empDtDeb = emploi["SEM_DtDeb"]
                empDtDebContrat = emploi["SEM_DtDebContrat"]
                empJson["date_debut_contrat"] = empDtDebContrat
                if empDtDebContrat in [None,""]:
                    empJson["date_debut_contrat"] = empDtDeb
                    
                dateAnc = salarie["SAL_DateAnciennete"]
                if dateAnc in [None,""]:
                    dateAnc = salarie["SAL_DateEntree"]
                if dateAnc in [None,""]:
                    dateAnc = empJson["date_debut_contrat"]
                
                empJson["date_anciennete"] = dateAnc 
                if emploi["SEM_DtFin"] not in [None,""]:
                    empJson["date_fin_previsionnelle_contrat"] = emploi["SEM_DtFin"]
                elif emploi["SEM_CDDDateFinPrev"] != "":
                    empJson["date_fin_previsionnelle_contrat"] = emploi["SEM_CDDDateFinPrev"]
                
                # Gestion de la qualification de l'emploi
                cCode = (emploi["SEM_S41_G01_00_012_001"] if emploi["SEM_S41_G01_00_012_001"] != "" else None)
                motif = emploi["SEM_CDDMotif"] if emploi["SEM_CDDMotif"] != "" else None
                tContrat = (emploi["SEM_TypeContratParticulier"] if emploi["SEM_TypeContratParticulier"] != "" else None)
                emploiPart = (emploi["SEM_EmpCasPart"] if emploi["SEM_EmpCasPart"] != "" else None)
                codeTravail = extract.codeTravail(code=cCode, motif=motif, typeContrat=tContrat, emploiPart=emploiPart, default_value=90)
                strTravail = sp.PAS_STATUT
                
                # Gestion de l'emploi Conventionnel
                opcc:int = 0
                if emploi["SEM_CodeCCN"] == "null":
                    logger.warning(f"Aucune ccn lié à l'emploi du salarié {matricule}")
                else:
                    idcc = emploi["SEM_CodeIDCC"]
                    classification = emploi["SEM_CodeCCN"]
                    opcc = extract.translateToOpcc(classification,idcc)
                    if not opcc:
                        logger.warning(f"IDCC {idcc} not supported (classification: '{emploi["SEM_CLM_Code"]}')")
                    else:
                        ccnEmploi = extract.emploiCCN(emploi["SEM_CLM_Code"], emploi["SEM_S41_G01_00_014"], ccn=opcc)
                        logger.progress(f"ccn Emploi - matricule {matricule} : {emploi["SEM_CLM_Code"]} {emploi["SEM_S41_G01_00_014"]} {opcc} = '{ccnEmploi}'")
                        if ccnEmploi:
                            empJson["ccn"] = ccnEmploi[0]
                            empJson["IDCC"] = idcc # permet de distinguer les codes 'ccn' identiques
                            empJson["emploi_conventionnel"] = ccnEmploi[1]
                            strTravail = ccnEmploi[2]
                            # if ccnEmploi[0] != int(opcc):
                            #     logger.warning(f"DIFF translateToOpcc={opcc} <=> emploiCCN={ccnEmploi[0]}")

                empJson["statut_professionnel"] = extract.statutProf(strTravail)
                
                empJson["code_etablissement"] = emploi["EMP_NomInterneEta"]
                empJson["matricule_salarie"] = matricule
                # empJson["ancien_numero_contrat_dsn"] = emploi[""]
                empJson["emploi"] = emploi["EMP_libEmploi"]
                empJson["type_contrat_travail"] = codeTravail
                empJson["regime_retraite"] = extract.regimeRetraite(emploi["SEM_S41_G01_00_015_002"])
                # empJson["cas_particuliers"] = extract


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
                    joursHebdo["jour_lundi"] = utils.calculateJour(emploi["SEM_HNLun"])
                    joursHebdo["jour_mardi"] = utils.calculateJour(emploi["SEM_HNMar"])
                    joursHebdo["jour_mercredi"] = utils.calculateJour(emploi["SEM_HNMer"])
                    joursHebdo["jour_jeudi"] = utils.calculateJour(emploi["SEM_HNJeu"])
                    joursHebdo["jour_vendredi"] = utils.calculateJour(emploi["SEM_HNVen"])
                    joursHebdo["jour_samedi"] = utils.calculateJour(emploi["SEM_HNSam"])
                    joursHebdo["jour_dimanche"] = utils.calculateJour(emploi["SEM_HNDim"])
                    empJson["jours_hebdomadaires"] = joursHebdo
                else:
                    hMMensuel = emploi["SEM_HoraireMensuelHeuresMajorees"]
                    empJson["nbr_heures_travail_mensuel_majorees"] = hMMensuel if hMMensuel > 0 else etabDetails["ETA_HMHoraireMensuel"]
                    totalHebdoSalarie = emploi["SEM_HNLun"] + emploi["SEM_HNMar"] + emploi["SEM_HNMer"] + emploi["SEM_HNJeu"] + emploi["SEM_HNVen"] + emploi["SEM_HNSam"] + emploi["SEM_HNDim"]
                    if totalHebdoSalarie == 0:
                        horaires["horaire_lundi"] = float(etabDetails["ETA_HNLun"]) + float(etabDetails["ETA_HMLun"])
                        horaires["horaire_mardi"] = float(etabDetails["ETA_HNMar"]) + float(etabDetails["ETA_HMMar"])
                        horaires["horaire_mercredi"] = float(etabDetails["ETA_HNMer"]) + float(etabDetails["ETA_HMMer"])
                        horaires["horaire_jeudi"] = float(etabDetails["ETA_HNJeu"]) + float(etabDetails["ETA_HMJeu"])
                        horaires["horaire_vendredi"] = float(etabDetails["ETA_HNVen"]) + float(etabDetails["ETA_HMVen"])
                        horaires["horaire_samedi"] = float(etabDetails["ETA_HNSam"]) + float(etabDetails["ETA_HMSam"])
                        horaires["horaire_dimanche"] = float(etabDetails["ETA_HNDim"]) + float(etabDetails["ETA_HMDim"])
                    else: 
                        horaires["horaire_lundi"] = float(emploi["SEM_HNLun"]) + float(emploi["SEM_HMLun"])  
                        horaires["horaire_mardi"] = float(emploi["SEM_HNMar"]) + float(emploi["SEM_HMMar"])  
                        horaires["horaire_mercredi"] = float(emploi["SEM_HNMer"]) + float(emploi["SEM_HMMer"])
                        horaires["horaire_jeudi"] = float(emploi["SEM_HNJeu"]) + float(emploi["SEM_HMJeu"])
                        horaires["horaire_vendredi"] = float(emploi["SEM_HNVen"]) + float(emploi["SEM_HMVen"])
                        horaires["horaire_samedi"] = float(emploi["SEM_HNSam"]) + float(emploi["SEM_HMSam"]) 
                        horaires["horaire_dimanche"] = float(emploi["SEM_HNDim"]) + float(emploi["SEM_HMDim"])
                    horaires["horaire_hebdo"] = horaires["horaire_lundi"] + horaires["horaire_mardi"] + horaires["horaire_mercredi"] + horaires["horaire_jeudi"] + horaires["horaire_vendredi"] + horaires["horaire_samedi"] + horaires["horaire_dimanche"]
                    horaires["horaire_travail"] = emploi['SEM_HoraireMensuel']+emploi["SEM_HoraireMensuelHeuresMajorees"] if emploi['SEM_HoraireMensuel'] > 0 else float(etabDetails["ETA_HNHoraireMensuel"]) + float(etabDetails["ETA_HMHoraireMensuel"])
                    
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
                
                empJson["depart_salarie"] = departSalarie
                
                # Gestion des emplois multiples
                if numeroContrat not in [savedEmp["numero_contrat"] for savedEmp in empMatRes[matricule]]:
                    # first contract added or different contract for this employee
                    empMatRes[matricule].append(empJson)
                else:
                    # same contract, chose the most recent one
                    for i, savedEmp in enumerate(empMatRes[matricule]):
                        dtDebContrat = "date_debut_contrat"
                        if savedEmp[dtDebContrat] and empJson[dtDebContrat]:
                            dtEmpSaved = datetime.strptime(savedEmp[dtDebContrat],"%d/%m/%Y")
                            dtEmpCurrent = datetime.strptime(empJson[dtDebContrat],"%d/%m/%Y")
                        else:
                            logger.warning(f"parse emploi : {matricule} même numéro contrat mais pas de date_debut_emploi. Skip")
                            continue
                        logger.warning(f"Parse Emploi : current = {dtEmpCurrent} saved = {dtEmpSaved}")
                        if dtEmpCurrent and dtEmpSaved and dtEmpCurrent > dtEmpSaved:
                            logger.warning(f"Numero contrat identitique: Current is the most recent !")
                            empMatRes[matricule][i] = empJson
            
            for empJson in empMatRes[matricule]:
                res.append(dataWithParams(empJson, {"dossierId": dossierId}))
    res = utils.filterEmptyResData(res)
    return res

def updateSpecificsIDCC(etabCrees:list[dict], emp_detailsMap: dict):
    specificIDCC = ["0016"]
    for etab in etabCrees:
        if etab["data"]["ccn"] not in specificIDCC:
            continue
        # for numero, emplois in emp_detailsMap.items():
        #     emploi = extract.idccToOpcc

def updateContrats(contratList:dict, numeroContratDict):
    contratsToUpdate = []
    for numero, matricules in numeroContratDict.items():
        for matricule, contratsNum in matricules.items():
            for _, contratIdReelNum in contratsNum.items():
                contratToUpdate = None
                try:
                    contratToUpdate = [contrat for _,contrats in contratList.items() for contrat in contrats if contrat["id"] == contratIdReelNum[0]][0]
                except Exception as e: 
                    logger.warning(f"Contrat not found {contratIdReelNum}")
                if contratToUpdate and contratToUpdate["matricule_salarie"] == matricule:
                    logger.progress(f"dossier {numero} contrat {contratToUpdate["id"]} : Mise à jour du numero contrat {contratToUpdate["numero_contrat"]}=>{contratIdReelNum[1]}")
                    contratToUpdate["numero_contrat"] = contratIdReelNum[1]
                    contratsToUpdate.append(dataWithParams(contratToUpdate, None))
    return contratsToUpdate

def parseCumuls(cumul_detailsMap: dict, emp_detailsMap:dict, dosMatrToContratNum: dict):
    res: list = []
    nbSkips = 0
    matMapDSNToContratID = {}
    for numero, encodedCumul in cumul_detailsMap.items():
        logger.log(f"Dossier {numero} parsing de {len(encodedCumul)} cumuls")

        cumulMap = parseEncodedCumul(encodedCumul["Cumul"])
        col = extract.editionCumulColonnes()
        varval: dict[str,str] = {}
        for i in range(len(cumulMap)):
            for code, titre in col.items():
                varval[code] = cumulMap[i][titre]
            matricule:str = cumulMap[i]["Matricule"]
            dtDebContrat = cumulMap[i]["Datededébutdecontrat"]
            dtDebEmploi = cumulMap[i]["Datededébutdemploi"] 
            if dtDebEmploi == "": dtDebEmploi = None
            if dtDebContrat == "": dtDebContrat = None
            contratID, numeroContrat, empIndex = getContratID(numero,matricule,dtDebContrat,dtDebEmploi,dosMatrToContratNum,emp_detailsMap)
            if not contratID:
                logger.warning(f"skip {matricule} ")
                continue
            datereprise = dict()
            datereprise["contratId"] = contratID
            datereprise["nomVariable"] = "$DOS.DATEREPRISE"
            datereprise["valeur"] = encodedCumul["DateReprise"]
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
                
            contratInfos = dosMatrToContratNum[numero][matricule][numeroContrat][empIndex]
            # logger.log(f"Verif contrat {contratInfos["id"]} {numeroContrat}=>{cumulMap[i]["Numérodecontrat"]}")
            if cumulMap[i]["Numérodecontrat"] != numeroContrat and numeroContrat == "vide":
                logger.progress(f"Added contrat {contratInfos["id"]} {numeroContrat}=>{cumulMap[i]["Numérodecontrat"]}")
                matMapDSNToContratID.setdefault(numero,{}).setdefault(matricule,{})[numeroContrat] = (contratID, cumulMap[i]["Numérodecontrat"])
            
            
        logger.statistic(f"{nbSkips} Skips de variables valeurs = 0.0")
    return (res, matMapDSNToContratID)

def dataWithParams(data: dict, params: dict = None):
    jsonWithParam: dict = {}
    jsonWithParam["data"] = data
    jsonWithParam["params"] = params
    return jsonWithParam

def buildEtabDict(op_etabs:list,etabsCrees:list,codesDict: dict[str,int]) -> dict[str,int]:
    etabDict:dict[str,int] = {}
    for op_etab in op_etabs:
        data = op_etab["data"]
        params = op_etab["params"]
        dossierId = params["dossierId"]
        numero = next(numero for numero, id in codesDict.items() if id == dossierId)
        try:
            etab = next(c_etab for c_etab in etabsCrees if c_etab["code"] == data["code"])
            etabDictCode = f"{numero}/{etab["code"]}"
            etabDict[etabDictCode] = etab["id"]
        except Exception as e:
            logger.warning(f"Next failed Dossier {numero}: etab {data["code"]} ")
            continue
    logger.log(etabDict)
    return etabDict

def parseEncodedCumul(base64: str):
    cumulCsv = utils.base64CSVToDict(base64)
    cumulMap = utils.CsvToMap(cumulCsv)
    return cumulMap