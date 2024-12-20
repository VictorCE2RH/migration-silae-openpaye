import sys
import os
import base64
# Ajoute le dossier parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import extract
import utils
import silae
import logger
import parser
import statut_pro as sp
from opapi import __VARIABLESREPRISEDOSSIER__
from typerscript import creerMultiples

def testFunc(context,res, condition):
    logger.log(f"{context} {logger.SuccessStatement("OK") if res == condition else logger.ErrorStatement("KO")} {f"'{res}'" if res != condition else ''}")

def testCodeTravail(code,motif=None,typeContrat=None, emploiPart=None,expected=None, default=None):
    testFunc(f"Résultat Code travail ({code} {motif} {typeContrat} {emploiPart}) == '{expected}'",
            extract.codeTravail(code,motif,typeContrat,emploiPart,default),
            expected)

def testStatutProf(code, expected):
    testFunc(f"Résultat Statut professionnel {code} == {expected}", 
            extract.statutProf(code),
            expected)

def testEmploiCCN(sCode, statutCode, opcc, empCode, statut=sp.PAS_STATUT):
    testFunc(f"Résultat emploiCCN {sCode} {statutCode} = {opcc} {empCode} {statut}", 
            extract.emploiCCN(sCode, statutCode, opcc),
            [opcc, empCode, statut])

def testTranslateOpcc(ccn,idcc,expected):
    if idcc=="7002":
        print("baba")
    testFunc(f"Résultat IDCC to OPCC {ccn} {idcc} == {expected}", 
            extract.translateToOpcc(ccn, idcc,userInput=False),
            expected)
    
def testOpccToIdcc(idcc,opcc):
    testFunc(f"Résultat OPCC to IDCC {opcc} == {idcc}", 
            extract.opccToIdcc(opcc),
            idcc)
    

def testCivilite(civilite, expected):
    testFunc(f"Résultat Civilite {civilite} = {expected}",
            extract.civilite(civilite),
            expected)

def testTauxAT(codeRisque,annee,expected):
    testFunc(f"Résultat Taux AT {codeRisque} {annee} == {expected}",
            extract.getTauxAT(codeRisque,annee),
            expected)

def testNomCotisation(codeNature, expected):
    testFunc(f"Résultat Nom cotisation {codeNature} == {expected}", 
            extract.nomNatureCotisation(codeNature),
            expected)

if __name__ == "__main__":
    # testCodeTravail(code="01",expected=1)
    # testCodeTravail(code="2",motif="8",typeContrat=145, expected=60)
    # testCodeTravail(code="1",typeContrat="140", expected=82)
    # testCodeTravail(code="1",motif="8",typeContrat=145,emploiPart="14.3", expected=1)
    # testCodeTravail(code="29",motif="8",typeContrat=10, expected=29)
    # testCodeTravail(code="1",typeContrat="140", expected=82) 
    # testCodeTravail(code="2",typeContrat="10", expected=2) 
    #logger.print()
    #logger.print()
    #logger.print()
    # testStatutProf(code="Stagiaire", expected=5)
    # testStatutProf(code="Apprenti", expected=6)
    # testStatutProf(code="Employé d'immeuble", expected=7)
    # testStatutProf(code="Employés qualifiés", expected=8)
    # testStatutProf(code="Intermittent", expected=9)
    # testStatutProf(code="Ouvrier", expected=10)
    # testStatutProf(code="Employé", expected=11)
    # testStatutProf(code="Technicien", expected=12)
    # testStatutProf(code="Etam", expected=13)
    # testStatutProf(code="TAM", expected=13)
    # testStatutProf(code="Agent de maîtrise", expected=21)
    # testStatutProf(code="Cadre", expected=22)
    # testStatutProf(code="Cadre supérieur", expected=23)
    # testStatutProf(code="Cadre dirigeant", expected=25)
    # testStatutProf(code="Gérant minoritaire", expected=26)
    # testStatutProf(code="Gérant égalitaire", expected=27)
    # testStatutProf(code="Mandataire", expected=28)
    # testStatutProf(code="Agent de maitrise assimilé cadre", expected=29)
    # testStatutProf(code="Pas de statut professionnel", expected=90)
    # #logger.print()
    # #logger.print()
    # #logger.print()
    testEmploiCCN(sCode='A018.01.001', statutCode='01',opcc=1880, empCode=10, statut=sp.OUVRIER)
    testEmploiCCN(sCode='A018.02.005', statutCode='02',opcc=1880, empCode=80, statut=sp.EMPLOYE)
    testEmploiCCN(sCode='A018.02.005', statutCode='02',opcc=1880, empCode=90, statut=sp.EMPLOYE)
    testEmploiCCN(sCode='A018.03.019', statutCode='02',opcc=1880, empCode=400, statut=sp.EMPLOYE)
    testEmploiCCN(sCode='A018.03.019', statutCode='02',opcc=1880, empCode=410, statut=sp.EMPLOYE)
    testEmploiCCN(sCode='A018.03.021', statutCode='02',opcc=1880, empCode=430, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='A018.04.001', statutCode='03',opcc=1880, empCode=440, statut=sp.TECHNICIEN)
    # testEmploiCCN(sCode='A018.04.002', statutCode='03',opcc=1880, empCode=450, statut=sp.TECHNICIEN)
    # testEmploiCCN(sCode='A018.04.003', statutCode='03',opcc=1880, empCode=460, statut=sp.TECHNICIEN)
    # testEmploiCCN(sCode='A018.04.008', statutCode='03',opcc=1880, empCode=510, statut=sp.TECHNICIEN)
    testEmploiCCN(sCode='A018.04.009', statutCode='03',opcc=1880, empCode=520, statut=sp.TECHNICIEN)
    testEmploiCCN(sCode='A018.05.001', statutCode='04',opcc=1880, empCode=530, statut= sp.AGENT_MAITRISE)
    testEmploiCCN(sCode='A018.05.002', statutCode='04',opcc=1880, empCode=540, statut= sp.AGENT_MAITRISE)
    # testEmploiCCN(sCode='A018.05.005', statutCode='04',opcc=1880, empCode=590, statut= sp.AGENT_MAITRISE)
    # testEmploiCCN(sCode='A018.05.006', statutCode='04',opcc=1880, empCode=620, statut= sp.AGENT_MAITRISE)
    # testEmploiCCN(sCode='A018.06.001', statutCode='04',opcc=1880, empCode=630, statut= sp.AGENT_MAITRISE)
    # testEmploiCCN(sCode='A018.06.001', statutCode='29',opcc=1880, empCode=640, statut=sp.CADRE)
    # testEmploiCCN(sCode='A018.06.002', statutCode='04',opcc=1880, empCode=650, statut= sp.AGENT_MAITRISE)
    # testEmploiCCN(sCode='A018.06.002', statutCode='29',opcc=1880, empCode=660, statut=sp.CADRE)
    # testEmploiCCN(sCode='A018.06.003', statutCode='04',opcc=1880, empCode=670, statut= sp.AGENT_MAITRISE)
    # testEmploiCCN(sCode='A018.06.003', statutCode='29',opcc=1880, empCode=680, statut=sp.CADRE)
    # testEmploiCCN(sCode='A018.06.004', statutCode='04',opcc=1880, empCode=690, statut= sp.AGENT_MAITRISE)
    # testEmploiCCN(sCode='A018.06.008', statutCode='29',opcc=1880, empCode=780, statut=sp.CADRE)
    # testEmploiCCN(sCode='A018.06.009', statutCode='04',opcc=1880, empCode=790, statut= sp.AGENT_MAITRISE)
    # testEmploiCCN(sCode='A018.06.009', statutCode='29',opcc=1880, empCode=800, statut=sp.CADRE)
    # testEmploiCCN(sCode='A018.07.001', statutCode='04',opcc=1880, empCode=810, statut= sp.AGENT_MAITRISE)
    # testEmploiCCN(sCode='A018.07.001', statutCode='29',opcc=1880, empCode=820, statut=sp.CADRE)
    # testEmploiCCN(sCode='A018.07.002', statutCode='04',opcc=1880, empCode=830, statut= sp.AGENT_MAITRISE)
    # testEmploiCCN(sCode='A018.07.002', statutCode='29',opcc=1880, empCode=840, statut=sp.CADRE)
    # testEmploiCCN(sCode='A018.07.003', statutCode='04',opcc=1880, empCode=850, statut= sp.AGENT_MAITRISE)
    # testEmploiCCN(sCode='A018.07.003', statutCode='29',opcc=1880, empCode=860, statut=sp.CADRE)
    testEmploiCCN(sCode='A018.08.001', statutCode='29',opcc=1880, empCode=870, statut=sp.CADRE)
    testEmploiCCN(sCode='A018.09.002', statutCode='12',opcc=1880, empCode=900, statut=sp.CADRE_SUP)
    testEmploiCCN(sCode='A018.09.002', statutCode='13',opcc=1880, empCode=910, statut=sp.CADRE_DIRIGEANT)
    testEmploiCCN(sCode='A018.09.002', statutCode='29',opcc=1880, empCode=920, statut=sp.CADRE)
    # testEmploiCCN(sCode='A018.10.001', statutCode='90',opcc=1880, empCode=930, statut= sp.PAS_STATUT)
    # testEmploiCCN(sCode='A018.10.002', statutCode='90',opcc=1880, empCode=940, statut= sp.PAS_STATUT)
    # testEmploiCCN(sCode='E161.01.001', statutCode='01',opcc=7023, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='E161.01.001', statutCode='02',opcc=7023, empCode=20, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='E161.01.003', statutCode='02',opcc=7023, empCode=60, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='E161.01.004', statutCode='01',opcc=7023, empCode=70, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='E161.01.004', statutCode='02',opcc=7023, empCode=80, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='E161.01.005', statutCode='01',opcc=7023, empCode=90, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='E161.01.007', statutCode='02',opcc=7023, empCode=140, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='E161.01.008', statutCode='01',opcc=7023, empCode=150, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='E161.01.008', statutCode='02',opcc=7023, empCode=160, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='E161.01.009', statutCode='01',opcc=7023, empCode=170, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='E161.01.032', statutCode='01',opcc=7023, empCode=630, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='E161.01.032', statutCode='02',opcc=7023, empCode=640, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='E161.01.033', statutCode='01',opcc=7023, empCode=650, statut=sp.OUVRIER)
    testEmploiCCN(sCode='E161.01.033', statutCode='02',opcc=7023, empCode=660, statut=sp.EMPLOYE)
    testEmploiCCN(sCode='E161.02.013', statutCode='04',opcc=7023, empCode=790, statut= sp.AGENT_MAITRISE)
    testEmploiCCN(sCode='E161.02.014', statutCode='04',opcc=7023, empCode=800, statut= sp.AGENT_MAITRISE)
    testEmploiCCN(sCode='E161.02.018', statutCode='04',opcc=7023, empCode=840, statut= sp.AGENT_MAITRISE)
    testEmploiCCN(sCode='E161.03.001', statutCode='29',opcc=7023, empCode=850, statut=sp.CADRE)
    # testEmploiCCN(sCode='E161.03.002', statutCode='29',opcc=7023, empCode=860, statut=sp.CADRE)
    # testEmploiCCN(sCode='E161.03.005', statutCode='29',opcc=7023, empCode=890, statut=sp.CADRE)
    testEmploiCCN(sCode='A023.07', statutCode='',opcc=9578, empCode=9999, statut= sp.PAS_STATUT)
    testEmploiCCN(sCode='A023.07.001', statutCode='',opcc=9578, empCode=9999, statut= sp.PAS_STATUT)
    testEmploiCCN(sCode='A023.07.002', statutCode='',opcc=9578, empCode=9999, statut= sp.PAS_STATUT)
    testEmploiCCN(sCode='A023.07.005', statutCode='',opcc=9578, empCode=9999, statut= sp.PAS_STATUT)
    testEmploiCCN(sCode='A023.08', statutCode='',opcc=9578, empCode=9999, statut= sp.PAS_STATUT)
    # testEmploiCCN(sCode='A023.08.01.001', statutCode='02',opcc=9578, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='A023.08.02.001', statutCode='03',opcc=9578, empCode=40, statut=sp.TECHNICIEN)
    # testEmploiCCN(sCode='A023.08.02.005', statutCode='03',opcc=9578, empCode=120, statut=sp.TECHNICIEN)
    # testEmploiCCN(sCode='A023.08.02.006', statutCode='03',opcc=9578, empCode=140, statut=sp.TECHNICIEN)
    # testEmploiCCN(sCode='A023.08.03.001', statutCode='29',opcc=9578, empCode=150, statut=sp.CADRE)
    # testEmploiCCN(sCode='A023.08.04.006', statutCode='29',opcc=9578, empCode=260, statut=sp.CADRE)
    testEmploiCCN(sCode='A032.01.001', statutCode='02',opcc=2571, empCode=10, statut=sp.EMPLOYE)
    testEmploiCCN(sCode='A032.01.001', statutCode='03',opcc=2571, empCode=20, statut=sp.TECHNICIEN)
    testEmploiCCN(sCode='A032.01.001', statutCode='04',opcc=2571, empCode=30, statut= sp.AGENT_MAITRISE)
    #logger.print()
    #logger.print()
    #logger.print()
    # testCivilite(1,1)
    # testCivilite(0,None)
    # testCivilite(2,2)
    # testCivilite(3,2)
    # testCivilite(512,None)
    # testCivilite(-5165,None)
    logger.log("")
    logger.log("")
    logger.log("")
    testTranslateOpcc(ccn='V001', idcc='2198',expected=83)
    testTranslateOpcc(ccn='V001', idcc='2198',expected=7779)
    testTranslateOpcc(ccn='V001', idcc='1543',expected=1543)
    testTranslateOpcc(ccn='R003', idcc='0706',expected=870)
    testTranslateOpcc(ccn='R003', idcc='0706',expected=8163)
    testTranslateOpcc(ccn='V002', idcc='1821',expected=1821)
    testTranslateOpcc(ccn='V002', idcc='1821',expected=2306)
    testTranslateOpcc(ccn='H019', idcc='1979',expected=7500)
    testTranslateOpcc(ccn='H019', idcc='1979',expected=2369)
    testTranslateOpcc(ccn='H019', idcc='1979',expected=1979)
    testTranslateOpcc(ccn='T026', idcc='0016',expected=7001)
    testTranslateOpcc(ccn='T026', idcc='0016',expected=7002)
    testTranslateOpcc(ccn='T026', idcc='7002',expected=7002)
    testTranslateOpcc(ccn='T026', idcc='0016',expected=7003)
    testTranslateOpcc(ccn='T026', idcc='0016',expected=7004)
    testTranslateOpcc(ccn='T026', idcc='0016',expected=7005)
    testTranslateOpcc(ccn='E212', idcc='7024',expected=7024)
    testTranslateOpcc(ccn='E212', idcc='7024',expected=7026)
    
    logger.log("")
    logger.log("")
    logger.log("")
    #logger.print()
    #logger.print()
    #logger.print()
    # #logger.print(f"0xFFF \n{utils.integerToBitArray(0xFFF)}")
    # #logger.print(f"0x0FF \n{utils.integerToBitArray(0x0FF)}")
    # #logger.print(f"0     \n{utils.integerToBitArray(0)}")
    # #logger.print(f"0xDA3 \n{utils.integerToBitArray(0xDA3)}")
    # #logger.print(f"0x3   \n{utils.integerToBitArray(0x3)}")
    # #logger.print(f"0x20F \n{utils.integerToBitArray(0x20F)}")
    #logger.print()
    #logger.print()
    #logger.print()
    PAME05ACDEM="TWF0cmljdWxlO1NhbGFyaek7Tm9tO051belyb2RlY29udHJhdDtEYXRlZGVk6WJ1dGRlY29udHJhdDtEYXRlZGVk6WJ1dGRlbXBsb2k7Sm91cnNBY3F1aXNOMTtKb3Vyc1ByaXNOMTtKb3Vyc1NvbGRlTjE7QmFzZUNQTjE7QmFzZUNQUHJpc04xO0Jhc2VDUFNvbGRlTjE7Sm91cnNBY3F1aXNOO0pvdXJzUHJpc047Sm91cnNTb2xkTjtCYXNlQ1BOO0Jhc2VDUFByaXNOO0Jhc2VDUFNvbGRlTjtSVFRBQ1FVSVM7UlRUUFJJUztSVFRTT0xERTtIZXVyZXM7SGV1cmVzU3VwcDtCcnV0O05ldOBwYXllcjtOZXRpbXBvc2FibGU7QWJhdHRlbWVudDtQTVNTO1RyYW5jaGVBO1RyYW5jaGVCO1RyYW5jaGVDO1RyYW5jaGUyQUZJUkNBUlJDTztTTUlDaGV1cmVzdHJhdmFpbGzpZXM7U01JQ0ZJTExPbjtUb3RhbFJlZHVjdGlvbkfpbulyYWxlVXJzc2FmO1RvdGFsUmVkdWN0aW9uR+lu6XJhbGVSZXRyYWl0ZTtNb250YW50bmV0ZmlzY2Fs6XhvbulyYXRpb25zdXJIU0hDO0NoYXJnZXNQYXRyb25hbGVzO1JldGVudWVBbGFzb3VyY2U7RGF0ZVJlcHJpc2U7DQowMDAwMTtDT1JURVMgU0FORFJJTkU7Q09SVEVTOzAwMDAxOzEyLzAzLzIwMTg7MTIvMDMvMjAxODszMDAuMDA7Mjg0LjUwOzE1LjUwOzM2Njg1NC4zMDsyODYzODUuODA7MTkxOTMuODA7MTYyLjUwOzEwOS41MDs1My4wMDsyMDA5MTMuODA7MTIyNDk2LjgwOzY1MzE1LjYwOzAuMDA7MC4wMDswLjAwOzExODMwLjI2OzEzNTEuNzQ7MjAzMzMwLjk4OzE4MTI1OC4xOTsxNDQyMDkuMDk7MC4wMDszMDEzOTIuMDA7MjAzMzMwLjk4OzAuMDA7MC4wMDswLjAwOzE1NDQ2NC4zMTsxNTM2ODYuOTE7LTE4Mzk2LjM2Oy0zNzEwLjUyOzIyODA1LjQwOzQ2MDg0LjAwOzI0MzcuNjI7Ow0KMDAwMTA7TUFHTklFUiBNQVJUSU5FIG7pZSBNRUhVTDtNQUdOSUVSOzsyOC8wOC8yMDE3OzI4LzA4LzIwMTc7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzMxMjQzOC43NTsxOTUwNzAuMzM7MjUzMzQ0LjM2OzAuMDA7MzAxMzkyLjAwOzMwMTM5Mi4wMDsxMTA0Ni43NTswLjAwOzExMDQ2Ljc1OzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDsxMjE0MDQuMDM7NDYyNjQuMDc7Ow0KMDAwMDc7TUFHTklFUiBWSU5DRU5UO01BR05JRVI7MDAwMDE7MDUvMDUvMjAxNDswNS8wNS8yMDE0OzMwMC4wMDsyOTguMDA7Mi4wMDs2NTc0MTIuNTA7MjkxNDkyLjcwOzQyOTIuODA7MTYyLjUwOzEwOS4wMDs1My41MDszMzkwNDguMjA7NjEwNDIuNTA7MTA4OTQ5LjQwOzAuMDA7MC4wMDswLjAwOzExNjkwLjI2OzEzMzcuNzQ7MzU2NTM0LjQ0OzI0OTM2Mi42MzsyNTM0MTUuMTk7MC4wMDsyOTg4NDAuOTA7Mjk4ODQwLjkwOzU3NjkzLjU0OzAuMDA7NTc2OTMuNTQ7MTUyNjU5LjYzOzE1MTg5Ny45MTswLjAwOzAuMDA7MzU4NTUuMTY7MTI3MjU4LjE3OzMxNDcyLjY5OzsNCjtUb3RhbCBn6W7pcmFsOzs7Ozs2MDAuMDA7NTgyLjUwOzE3LjUwOzEwMjQyNjYuODA7NTc3ODc4LjUwOzIzNDg2LjYwOzMyNS4wMDsyMTguNTA7MTA2LjUwOzUzOTk2Mi4wMDsxODM1MzkuMzA7MTc0MjY1LjAwOzAuMDA7MC4wMDswLjAwOzIzNTIwLjUyOzI2ODkuNDg7ODcyMzA0LjE3OzYyNTY5MS4xNTs2NTA5NjguNjQ7MC4wMDs5MDE2MjQuOTA7ODAzNTYzLjg4OzY4NzQwLjI5OzAuMDA7Njg3NDAuMjk7MzA3MTIzLjk0OzMwNTU4NC44MjstMTgzOTYuMzY7LTM3MTAuNTI7NTg2NjAuNTY7Mjk0NzQ2LjIwOzgwMTc0LjM4OzsNCg=="
    res = utils.base64CSVToDict(PAME05ACDEM)
    utils.dictToCSVFile(res,"pame_05ACDEM_cumul.csv")
    # TESTALLONES = "TWF0cmljdWxlO1NhbGFyaek7Tm9tO051belyb2RlY29udHJhdDtEYXRlZGVk6WJ1dGRlY29udHJhdDtEYXRlZGVk6WJ1dGRlbXBsb2k7Sm91cnNBY3F1aXNOMTtKb3Vyc1ByaXNOMTtKb3Vyc1NvbGRlTjE7QmFzZUNQTjE7QmFzZUNQUHJpc04xO0Jhc2VDUFNvbGRlTjE7Sm91cnNBY3F1aXNOO0pvdXJzUHJpc047Sm91cnNTb2xkTjtCYXNlQ1BOO0Jhc2VDUFByaXNOO0Jhc2VDUFNvbGRlTjtSVFRBQ1FVSVM7UlRUUFJJUztSVFRTT0xERTtIZXVyZXM7SGV1cmVzU3VwcDtCcnV0O05ldOBwYXllcjtOZXRpbXBvc2FibGU7QWJhdHRlbWVudDtQTVNTO1RyYW5jaGVBO1RyYW5jaGVCO1RyYW5jaGVDO1RyYW5jaGUyQUZJUkNBUlJDTztTTUlDaGV1cmVzdHJhdmFpbGzpZXM7U01JQ0ZJTExPbjtUb3RhbFJlZHVjdGlvbkfpbulyYWxlVXJzc2FmO1RvdGFsUmVkdWN0aW9uR+lu6XJhbGVSZXRyYWl0ZTtNb250YW50bmV0ZmlzY2Fs6XhvbulyYXRpb25zdXJIU0hDO0NoYXJnZXNQYXRyb25hbGVzO1JldGVudWVBbGFzb3VyY2U7RGF0ZVJlcHJpc2UNCjAwMDAyO1RFU1QgVEVTVDtURVNUOzAwMDAxOzAxLzAxLzIwMTk7MDEvMDEvMjAxOTsyOzE7MTsyOzE7MTsyOzE7MTsyOzE7MTsyOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTtub3YtMjQNCg=="
    # cumulmap = {"ACTION":{"DateReprise":"01/12/2024","Cumul":PAME05ACDEM}}
    # matContrID = {"00002":{"id": 263033, "date_debut_contrat":"01/01/2019"}}
    # op_cumuls, contrat = parser.parseCumuls(cumulmap,matriculeContratId=matContrID)
    # creerMultiples("E2RH",__VARIABLESREPRISEDOSSIER__, op_cumuls)
    # #logger.print()
    # #logger.print()
    # #logger.print()
    # testTauxAT("271ZF",2025,7.38)
    # testTauxAT("271ZF",2024,7.38)
    # testTauxAT("271ZF",2023,8.83)
    # testTauxAT("27.1ZF",2024,7.38)
    # testTauxAT("unknown",2024,None)
    logger.log("")
    logger.log("")
    logger.log("")
    # JOURNALPAIE=r".\data\in\base64JournalPaie"
    # with open(JOURNALPAIE, encoding="utf-8") as f:
    #     content = base64.b64decode(f.read())
    # with open(r".\data\out\edition_journal_paie.xml",'w',encoding="utf-8") as f:
    #     f.write(str(content))
    
    testNomCotisation("SSOC", "Sécurité sociale")
    testNomCotisation("CH", "Chômage")
    testNomCotisation("ARRCO", "ARRCO")
    testNomCotisation("AGIRC", "AGIRC")
    testNomCotisation("GRS", "Garantie retraite supplémentaire")
    testNomCotisation("RPO", "Régime de Prévoyance Obligatoire")
    testNomCotisation("RPS", "Régime de Prévoyance Supplémentaire")
    testNomCotisation("CCP", "Caisse de Congés Payés")
    testNomCotisation("MT", "Médecine du Travail")
    testNomCotisation("FP", "Formation Professionnelle")
    testNomCotisation("RSPECIAL", "Régime Spécial")
    testNomCotisation("TS", "Taxe sur les Salaires")
    testNomCotisation("ATCS", "Autres Taxes/Contributions sur les Salaires")
    testNomCotisation("DIV", "Divers")
    logger.log("")
    logger.log("")
    logger.log("")