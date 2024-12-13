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
    print(f"{context} {logger.SuccessStatement("OK") if res == condition else logger.ErrorStatement("KO")} {f"'{res}'" if res != condition else ''}")

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
    testFunc(f"Résultat IDCC to OPCC {ccn} {idcc} == {expected}", 
            extract.translateToOpcc(ccn, idcc),
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
    # print()
    # print()
    # print()
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
    # # print()
    # # print()
    # # print()
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
    # print()
    # print()
    # print()
    # testCivilite(1,1)
    # testCivilite(0,None)
    # testCivilite(2,2)
    # testCivilite(3,2)
    # testCivilite(512,None)
    # testCivilite(-5165,None)
    print()
    print()
    print()
    testTranslateOpcc(ccn='V001', idcc='2198',expected=83)
    testTranslateOpcc(ccn='R003', idcc='0706',expected=870)
    testTranslateOpcc(ccn='R003', idcc='0706',expected=8163)
    testTranslateOpcc(ccn='V002', idcc='1821',expected=1821)
    testTranslateOpcc(ccn='V001', idcc='1543',expected=1543)
    testTranslateOpcc(ccn='H019', idcc='1979',expected=7500)
    testTranslateOpcc(ccn='H019', idcc='1979',expected=2369)
    testTranslateOpcc(ccn='H019', idcc='1979',expected=1979)
    testTranslateOpcc(ccn='V001', idcc='2198',expected=7779)
    testTranslateOpcc(ccn='V002', idcc='1821',expected=2306)
    testTranslateOpcc(ccn='T026', idcc='0016',expected=7001)
    testTranslateOpcc(ccn='T026', idcc='0016',expected=7002)
    testTranslateOpcc(ccn='T026', idcc='7002',expected=7002)
    testTranslateOpcc(ccn='T026', idcc='0016',expected=7003)
    testTranslateOpcc(ccn='T026', idcc='0016',expected=7004)
    testTranslateOpcc(ccn='T026', idcc='0016',expected=7005)
    testTranslateOpcc(ccn='E212', idcc='7024',expected=7024)
    testTranslateOpcc(ccn='E212', idcc='7024',expected=7026)
    
    print()
    print()
    print()
    # print()
    # print()
    # print()
    # # print(f"0xFFF \n{utils.integerToBitArray(0xFFF)}")
    # # print(f"0x0FF \n{utils.integerToBitArray(0x0FF)}")
    # # print(f"0     \n{utils.integerToBitArray(0)}")
    # # print(f"0xDA3 \n{utils.integerToBitArray(0xDA3)}")
    # # print(f"0x3   \n{utils.integerToBitArray(0x3)}")
    # # print(f"0x20F \n{utils.integerToBitArray(0x20F)}")
    # print()
    # print()
    # print()
    # FROMSILAE_OR09820 = "TWF0cmljdWxlO1NhbGFyaek7Tm9tO051belyb2RlY29udHJhdDtEYXRlZGVk6WJ1dGRlY29udHJhdDtEYXRlZGVk6WJ1dGRlbXBsb2k7Sm91cnNBY3F1aXNOMTtKb3Vyc1ByaXNOMTtKb3Vyc1NvbGRlTjE7QmFzZUNQTjE7QmFzZUNQUHJpc04xO0Jhc2VDUFNvbGRlTjE7Sm91cnNBY3F1aXNOO0pvdXJzUHJpc047Sm91cnNTb2xkTjtCYXNlQ1BOO0Jhc2VDUFByaXNOO0Jhc2VDUFNvbGRlTjtSVFRBQ1FVSVM7UlRUUFJJUztSVFRTT0xERTtIZXVyZXM7SGV1cmVzU3VwcDtCcnV0O05ldOBwYXllcjtOZXRpbXBvc2FibGU7QWJhdHRlbWVudDtQTVNTO1RyYW5jaGVBO1RyYW5jaGVCO1RyYW5jaGVDO1RyYW5jaGUyQUZJUkNBUlJDTztTTUlDaGV1cmVzdHJhdmFpbGzpZXM7U01JQ0ZJTExPbjtUb3RhbFJlZHVjdGlvbkfpbulyYWxlVXJzc2FmO1RvdGFsUmVkdWN0aW9uR+lu6XJhbGVSZXRyYWl0ZTtNb250YW50bmV0ZmlzY2Fs6XhvbulyYXRpb25zdXJIU0hDO0NoYXJnZXNQYXRyb25hbGVzO1JldGVudWVBbGFzb3VyY2U7RGF0ZVJlcHJpc2U7DQowMDAwMTtEVVJFVVggR2VvZmZyZXk7RFVSRVVYOzAwMDAxOzAxLzA4LzIwMjI7MDEvMDgvMjAyMjswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7NDQwMDAuMDA7MzM5ODIuNzM7MzY0ODAuMjk7MC4wMDs0MjUwNC4wMDs0MjUwNC4wMDsxNDk2LjAwOzAuMDA7MTQ5Ni4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MTc0ODYuNzk7Njc2LjczOzExLzIwMjQ7DQo7VG90YWwgZ+lu6XJhbDs7Ozs7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzQ0MDAwLjAwOzMzOTgyLjczOzM2NDgwLjI5OzAuMDA7NDI1MDQuMDA7NDI1MDQuMDA7MTQ5Ni4wMDswLjAwOzE0OTYuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzE3NDg2Ljc5OzY3Ni43Mzs7DQo="
    # cumulMap = parser.parseEncodedCumul(FROMSILAE_OR09820)
    
    # OR10420 = "TWF0cmljdWxlO1NhbGFyaek7Tm9tO051belyb2RlY29udHJhdDtEYXRlZGVk6WJ1dGRlY29udHJhdDtEYXRlZGVk6WJ1dGRlbXBsb2k7Sm91cnNBY3F1aXNOMTtKb3Vyc1ByaXNOMTtKb3Vyc1NvbGRlTjE7QmFzZUNQTjE7QmFzZUNQUHJpc04xO0Jhc2VDUFNvbGRlTjE7Sm91cnNBY3F1aXNOO0pvdXJzUHJpc047Sm91cnNTb2xkTjtCYXNlQ1BOO0Jhc2VDUFByaXNOO0Jhc2VDUFNvbGRlTjtSVFRBQ1FVSVM7UlRUUFJJUztSVFRTT0xERTtIZXVyZXM7SGV1cmVzU3VwcDtCcnV0O05ldOBwYXllcjtOZXRpbXBvc2FibGU7QWJhdHRlbWVudDtQTVNTO1RyYW5jaGVBO1RyYW5jaGVCO1RyYW5jaGVDO1RyYW5jaGUyQUZJUkNBUlJDTztTTUlDaGV1cmVzdHJhdmFpbGzpZXM7U01JQ0ZJTExPbjtUb3RhbFJlZHVjdGlvbkfpbulyYWxlVXJzc2FmO1RvdGFsUmVkdWN0aW9uR+lu6XJhbGVSZXRyYWl0ZTtNb250YW50bmV0ZmlzY2Fs6XhvbulyYXRpb25zdXJIU0hDO0NoYXJnZXNQYXRyb25hbGVzO1JldGVudWVBbGFzb3VyY2U7RGF0ZVJlcHJpc2U7DQowMDAwNztBQlJZIFZhbOlyaWU7QUJSWTtDVDAwMDAwMTswMy8wNS8yMDIyOzAzLzA1LzIwMjI7MzAwLjAwOzIwMS4wMDs5OS4wMDs0OTk2NS4wMDs1MzcyMy4xMDs1MTc1NS40MDsxNjIuNTA7MC4wMDsxNjIuNTA7NTg2OTIuMDA7MC4wMDs5NjI5Ny44MDswLjAwOzAuMDA7MC4wMDs4MzQxLjg1OzAuMDA7MTA4NjU3LjAwOzg0MDQ1Ljk4Ozg4MTczLjY2OzAuMDA7MjEyNTIwLjAwOzEwODY1Ny4wMDswLjAwOzAuMDA7MC4wMDs5NzE4Mi41NTs5NzE4Mi44MDsyMDI0MC44MDs0NjkxLjQ5OzAuMDA7MTQ0OTQuMjI7MjA1NC4wNDs7DQowMDAwOTtDSEVWUk9UIEFsZXhhbmRyZTtDSEVWUk9UO0NUMDAwMDAzOzAyLzAxLzIwMjQ7MDIvMDEvMjAyNDs2NS4wMDs2LjAwOzU5LjAwOzQ3MjQwLjAwOzQzNjAuNTA7NDI4ODAuNDA7NzUuNTA7MC4wMDs3NS41MDs1NzQ5NC4yMDswLjAwOzU3NDk0LjIwOzAuMDA7MC4wMDswLjAwOzgzNDEuODU7MC4wMDsxMDQ3MzQuMjk7Nzk1MzQuNzc7ODUzMTMuNzM7MC4wMDsyMTEyNzMuNTA7MTA0NzM0LjI5OzAuMDA7MC4wMDswLjAwOzk3MTgyLjU1Ozk3MTgyLjgwOzIxOTM2LjA4OzUwODQuMzQ7MC4wMDsxMTg5OC4wMjsxMjM3LjIzOzsNCjAwMDAyO0RVQlVDIE3pbGlzc2E7RFVCVUM7OzAxLzEyLzIwMTE7MDEvMTIvMjAxMTsxODAuMDA7NDAuMDA7MTQwLjAwOzAuMDA7MTg2ODEuNjA7MjE5NDUuMDA7MTM1LjAwOzAuMDA7MTM1LjAwOzI5MTQ4LjQwOzAuMDA7MjExNjEuMzA7MC4wMDswLjAwOzAuMDA7Mjc2Ny40MDswLjAwOzUyOTk2LjA0OzU2Nzc0LjQ4OzQzMTYzLjc4OzAuMDA7NTQ1NTkuMTg7NDY2MTMuMjI7NjM4Mi44MjswLjAwOzYzODIuODI7MzIyNDAuMjE7MzAwNjYuNzA7MjA2My42ODs0NzguMzI7MC4wMDsyMTY4My4xODswLjAwOzsNCjAwMDA0O0xFQ0xFUkMgU3TpcGhhbmU7TEVDTEVSQztDVDAwMDI1OzI5LzA4LzIwMTY7MjkvMDgvMjAxNjszMjAuMDA7MTkyLjAwOzEyOC4wMDs3OTk0NS4wMDs5NTI5OS43MDsxNDg3MzYuMDA7MTYyLjUwOzAuMDA7MTYyLjUwOzk1Njg3LjUwOzAuMDA7MTkyODU4LjUwOzAuMDA7MC4wMDswLjAwOzc4OTMuODU7NDE2LjMyOzE2OTEzNi4yMjsxMzcxMjMuMjY7MTI5Nzg3LjM2OzAuMDA7MjA5NTI4LjQ4OzE2OTEzNi4yMjswLjAwOzAuMDA7MC4wMDs5NjgxMy40ODs5ODQ4MC41NjswLjAwOzAuMDA7ODg2MS45Mjs2MTUxMi41OTs2MTAxLjYyOzsNCjAwMDAzO1JPVUlMTEVUIE1vcmdhbjtST1VJTExFVDtDVDAwMDIzOzE0LzAzLzIwMTY7MTQvMDMvMjAxNjszNDIuNTA7MTY1LjUwOzE3Ny4wMDs2MTk2My41MDs1NTcxOC4yMDsxNTY1MzMuMDA7MTYyLjUwOzAuMDA7MTYyLjUwOzc0MTM5LjIwOzAuMDA7MTQ3NDQ3LjUwOzAuMDA7MC4wMDswLjAwOzc1MzYuODU7MC4wMDsxMjM4MTguNDQ7MTAyNjQxLjE4OzEwMDgwMC40MTswLjAwOzE5MzY2OS41MjsxMjM4MTguNDQ7MC4wMDswLjAwOzAuMDA7ODc4MDQuMzA7ODgyNTAuODE7NzUxMi41MjsxNzQxLjEwOzAuMDA7MzY1MzUuMDE7MzQ1My40Njs7DQowMDAwODtaQVJGQU5JIFRsYXl0bWFzc2U7WkFSRkFOSTtDVDAwMDAwMjswMS8wNi8yMDIyOzAxLzA2LzIwMjI7MzAwLjAwOzE2Mi4wMDsxMzguMDA7NTE2ODkuMDA7NjgxOTIuMzA7ODM4NDIuMTA7MTYyLjUwOzAuMDA7MTYyLjUwOzYwOTQ3LjAwOzAuMDA7MTAzMzI4LjYwOzAuMDA7MC4wMDswLjAwOzgzNDEuODU7MC4wMDsxMTI2MzYuNDA7ODU0ODguNTY7OTE3MjYuMzY7MC4wMDsyMTI1MjAuMDA7MTEyNjM2LjQwOzAuMDA7MC4wMDswLjAwOzk3MTgyLjU1Ozk3MTgyLjgwOzE4NTIxLjY5OzQyOTIuOTU7MC4wMDsxODk0Ni42MzsxMzI0LjU0OzsNCjtUb3RhbCBn6W7pcmFsOzs7OzsxNTA3LjUwOzc2Ni41MDs3NDEuMDA7MjkwODAyLjUwOzI5NTk3NS40MDs1MDU2OTEuOTA7ODYwLjUwOzAuMDA7ODYwLjUwOzM3NjEwOC4zMDswLjAwOzYxODU4Ny45MDswLjAwOzAuMDA7MC4wMDs0MzIyMy42NTs0MTYuMzI7NjcxOTc4LjM5OzU0NTYwOC4yMzs1Mzg5NjUuMzA7MC4wMDsxMDk0MDcwLjY4OzY2NTU5NS41Nzs2MzgyLjgyOzAuMDA7NjM4Mi44Mjs1MDg0MDUuNjU7NTA4MzQ2LjQ3OzcwMjc0Ljc3OzE2Mjg4LjIwOzg4NjEuOTI7MTY1MDY5LjY1OzE0MTcwLjg5OzsNCg=="
    # D4KOR0022   = "TWF0cmljdWxlO1NhbGFyaek7Tm9tO051belyb2RlY29udHJhdDtEYXRlZGVk6WJ1dGRlY29udHJhdDtEYXRlZGVk6WJ1dGRlbXBsb2k7Sm91cnNBY3F1aXNOMTtKb3Vyc1ByaXNOMTtKb3Vyc1NvbGRlTjE7QmFzZUNQTjE7QmFzZUNQUHJpc04xO0Jhc2VDUFNvbGRlTjE7Sm91cnNBY3F1aXNOO0pvdXJzUHJpc047Sm91cnNTb2xkTjtCYXNlQ1BOO0Jhc2VDUFByaXNOO0Jhc2VDUFNvbGRlTjtSVFRBQ1FVSVM7UlRUUFJJUztSVFRTT0xERTtIZXVyZXM7SGV1cmVzU3VwcDtCcnV0O05ldOBwYXllcjtOZXRpbXBvc2FibGU7QWJhdHRlbWVudDtQTVNTO1RyYW5jaGVBO1RyYW5jaGVCO1RyYW5jaGVDO1RyYW5jaGUyQUZJUkNBUlJDTztTTUlDaGV1cmVzdHJhdmFpbGzpZXM7U01JQ0ZJTExPbjtUb3RhbFJlZHVjdGlvbkfpbulyYWxlVXJzc2FmO1RvdGFsUmVkdWN0aW9uR+lu6XJhbGVSZXRyYWl0ZTtNb250YW50bmV0ZmlzY2Fs6XhvbulyYXRpb25zdXJIU0hDO0NoYXJnZXNQYXRyb25hbGVzO1JldGVudWVBbGFzb3VyY2U7RGF0ZVJlcHJpc2U7DQowMDAyNjtCRUxMRVMgQ2hyaXN0b3BoZXI7QkVMTEVTOzsxNC8xMC8yMDI0OzE0LzEwLzIwMjQ7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7NC4wMDswLjAwOzQuMDA7MjU4Ny4zMDswLjAwOzI1ODcuMzA7MC4wMDswLjAwOzAuMDA7MjE0LjAwOzAuMDA7MjU4Ny4yNjsyNzQyLjIyOzIwODQuMzk7MC4wMDs1MjM0Ljk5OzI1ODcuMjY7MC4wMDswLjAwOzAuMDA7MjU0Mi4zMjsyNTIzLjAwOzYyNi41MjsxMjYuMzc7MC4wMDsyMzcuNTI7MC4wMDsxMS8yMDI0Ow0KMDAwMjg7QkVOTkVUT1QgQ2hhcmxlcztCRU5ORVRPVDswMDAwMTsxNC8xMC8yMDI0OzE0LzEwLzIwMjQ7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7NC4wMDswLjAwOzQuMDA7MzM3MC42MDswLjAwOzMzNzAuNjA7MC4wMDswLjAwOzAuMDA7MjQ5LjY3OzAuMDA7MzM3MC41NTszMjYyLjc2OzI3MTMuMDI7MC4wMDs2MTA3LjYxOzMzNzAuNTU7MC4wMDswLjAwOzAuMDA7Mjk2Ni4wODsyOTQzLjU0OzU3OC42MzsxMTYuNzE7MC4wMDs1OTYuNDE7NDkuNDU7MTEvMjAyNDsNCjAwMDMzO0NIQU1QT1RSQVkgTm/pbWllO0NIQU1QT1RSQVk7OzE4LzExLzIwMjQ7MTgvMTEvMjAyNDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDsxLjA4OzAuMDA7MS4wODs4NDYuMzA7MC4wMDs4NDYuMzA7MC4wMDswLjAwOzAuMDA7NzAuMDA7MC4wMDs4NDYuMzA7MTA5Ni43NDs2ODEuODA7MC4wMDsxNjc0LjQwOzg0Ni4zMDswLjAwOzAuMDA7MC4wMDs4MzEuNjA7ODMxLjYwOzIwOS4zMDs0Mi4yMjswLjAwOzcyLjQ2OzAuMDA7MTEvMjAyNDsNCjAwMDMwO0NPVFRJTEFSRCBFdmFuO0NPVFRJTEFSRDs7MTgvMTEvMjAyNDsxOC8xMS8yMDI0OzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzEuMDg7MC4wMDsxLjA4Ozg0Ni4zMDswLjAwOzg0Ni4zMDswLjAwOzAuMDA7MC4wMDs3MC4wMDswLjAwOzg0Ni4zMDsxMDc2Ljc0OzY4MS44MDswLjAwOzE2NzQuNDA7ODQ2LjMwOzAuMDA7MC4wMDswLjAwOzgzMS42MDs4MzEuNjA7MjA5LjMwOzQyLjIyOzAuMDA7NzIuNDY7MC4wMDsxMS8yMDI0Ow0KMDAwMDI7RE9VQkxFVCBCZW5v7nQ7RE9VQkxFVDswMDAwMTAwMDA2MTUxMzE7MTEvMDUvMjAxNTsxMS8wNS8yMDE1OzMwLjAwOzE5LjAwOzExLjAwOzIyMjYyLjYwOzE0MDkxLjAwOzgxNjMuMTA7MTUuMDA7MC4wMDsxNS4wMDsxMTQ1Ny41MDswLjAwOzExNDU3LjUwOzAuMDA7MC4wMDswLjAwOzE2NjguMzc7MC4wMDsyMDk5Mi45MzsyMDYwNC45MzsxNjkxMi40NDswLjAwOzQyNTA0LjAwOzIwOTkyLjkzOzAuMDA7MC4wMDswLjAwOzE5ODIwLjI0OzE5NDcxLjQ0OzQzOTEuODQ7ODg1Ljc4OzAuMDA7MjU0My4xODswLjAwOzExLzIwMjQ7DQowMDAzMTtEVU1FTklMIFpv6TtEVU1FTklMOzsxOC8xMS8yMDI0OzE4LzExLzIwMjQ7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MS4wODswLjAwOzEuMDg7ODQ2LjMwOzAuMDA7ODQ2LjMwOzAuMDA7MC4wMDswLjAwOzQ5LjAwOzAuMDA7NTkyLjQxOzc3OS40OTs0NzcuMjc7MC4wMDsxMjg4LjAwOzU5Mi40MTswLjAwOzAuMDA7MC4wMDs1ODIuMTI7NTgyLjEyOzE0Ni41MTsyOS41NTswLjAwOzUwLjcxOzAuMDA7MTEvMjAyNDsNCjAwMDI3O0ZMRVVUUlkgQWxleGlzO0ZMRVVUUlk7MDAwMDE7MTQvMTAvMjAyNDsxNC8xMC8yMDI0OzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzQuMDA7MC4wMDs0LjAwOzMwMTguNTA7MC4wMDszMDE4LjUwOzAuMDA7MC4wMDswLjAwOzI0OS42NzswLjAwOzMwMTguNTE7MzEzOC43MjsyNDI5LjQzOzAuMDA7NjEwNy42MTszMDE4LjUxOzAuMDA7MC4wMDswLjAwOzI5NjYuMDg7Mjk0My41NDs3MzAuOTY7MTQ3LjQzOzAuMDA7MjgyLjA4OzAuMDA7MTEvMjAyNDsNCjAwMDA1O0dBTExJT1ogTG9pcztHQUxMSU9aOzAwMDAxMDAwMjAxOTE3MTsyMC8wNi8yMDE5OzIwLzA2LzIwMTk7NjAuMDA7MC4wMDs2MC4wMDs0MTg3Ny4xMDswLjAwOzQ0MDEwLjAwOzE1LjAwOzAuMDA7MTUuMDA7MTE0MDUuNDA7MC4wMDsxMTQwNS40MDswLjAwOzAuMDA7MC4wMDsxNjY4LjM3OzAuMDA7MjA3NTcuMzY7MjE0NTIuNzE7MTY3MDkuNTc7MC4wMDs0MjUwNC4wMDsyMDc1Ny4zNjswLjAwOzAuMDA7MC4wMDsxOTgyMC4yNDsxOTQ3MS40NDs0NDkyLjgwOzkwNi4xOTswLjAwOzI1MjcuNTE7MC4wMDsxMS8yMDI0Ow0KMDAwMDc7R0lNRVIgTGF1cmVudDtHSU1FUjswMDAwMTAwMDIzMTkyMTg7MDYvMDgvMjAxOTswNi8wOC8yMDE5OzMwLjAwOzI2LjAwOzQuMDA7MjE4MzUuNzA7MTg3MDMuNjA7MjkzNC4wMDsxNS4wMDswLjAwOzE1LjAwOzExMzMyLjIwOzAuMDA7MTEzMzIuMjA7MC4wMDswLjAwOzAuMDA7MTY2OC4zNzswLjAwOzIwNjg0LjAwOzIwNDQzLjI0OzE2NjUwLjQ3OzAuMDA7NDI1MDQuMDA7MjA2ODQuMDA7MC4wMDswLjAwOzAuMDA7MTk4MjAuMjQ7MTk0NzEuNDQ7NDUyNS4xMzs5MTIuNjk7MC4wMDsyNDYxLjM0OzAuMDA7MTEvMjAyNDsNCjAwMDMyO0xFQkFTIENocmlzdG9waGU7TEVCQVM7OzE4LzExLzIwMjQ7MTgvMTEvMjAyNDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDsxLjA4OzAuMDA7MS4wODs4NDYuMzA7MC4wMDs4NDYuMzA7MC4wMDswLjAwOzAuMDA7NzAuMDA7MC4wMDs4NDYuMzA7MTI3Ni43NDs2ODEuODA7MC4wMDsxNjc0LjQwOzg0Ni4zMDswLjAwOzAuMDA7MC4wMDs4MzEuNjA7ODMxLjYwOzIwOS4zMDs0Mi4yMjswLjAwOzcyLjQ2OzAuMDA7MTEvMjAyNDsNCjAwMDI1O0xFTE9VQVJEIE1heGltZTtMRUxPVUFSRDswMDAwMTsxMS8xMC8yMDI0OzExLzEwLzIwMjQ7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7NC4yNTswLjAwOzQuMjU7MjY1OS44MDswLjAwOzI2NTkuODA7MC4wMDswLjAwOzAuMDA7MjIwLjAwOzAuMDA7MjY1OS44MDsyODEzLjc2OzIxNDIuODE7MC4wMDs1NTU1LjUwOzI2NTkuODA7MC4wMDswLjAwOzAuMDA7MjYxMy42MDsyNTkyLjkwOzY0My40MzsxMjkuNzc7MC4wMDsyNDQuOTc7MC4wMDsxMS8yMDI0Ow0KMDAwMjk7TEVURUxMSUVSIE1hdHRoaWV1O0xFVEVMTElFUjs7MTgvMTEvMjAyNDsxOC8xMS8yMDI0OzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzEuMDg7MC4wMDsxLjA4Ozg0Ni4zMDswLjAwOzg0Ni4zMDswLjAwOzAuMDA7MC4wMDs3MC4wMDswLjAwOzg0Ni4zMDs5NzYuNzQ7NjgxLjgwOzAuMDA7MTY3NC40MDs4NDYuMzA7MC4wMDswLjAwOzAuMDA7ODMxLjYwOzgzMS42MDsyMDkuMzA7NDIuMjI7MC4wMDs3Mi40NjswLjAwOzExLzIwMjQ7DQowMDAyMjtQSUVSUkVUIENocnlzdGVsbGU7UElFUlJFVDswMDAwMTswOC8wNy8yMDI0OzA4LzA3LzIwMjQ7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MTIuMDA7MC4wMDsxMi4wMDs1MDYxLjcwOzAuMDA7NTA2MS43MDswLjAwOzAuMDA7MC4wMDs0MTguNjg7MC4wMDs1MDYxLjg0OzU3ODMuMzA7NDA3OC4wMTswLjAwOzEwNTQxLjYxOzUwNjEuODQ7MC4wMDswLjAwOzAuMDA7NDk3My45Mjs0ODk3LjU3OzExOTguODE7MjQxLjc5OzAuMDA7NDk3LjEwOzAuMDA7MTEvMjAyNDsNCjAwMDI0O1NPQVJFUyBIdWdvO1NPQVJFUzs7MTAvMTAvMjAyNDsxMC8xMC8yMDI0OzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzQuMzM7MC4wMDs0LjMzOzI3MzIuMzA7MC4wMDsyNzMyLjMwOzAuMDA7MC4wMDswLjAwOzIyNi4wMDswLjAwOzI3MzIuMzQ7Mjg4NS4zNDsyMjAxLjI3OzAuMDA7NTY2Mi4zMzsyNzMyLjM0OzAuMDA7MC4wMDswLjAwOzI2ODQuODg7MjY2Mi44MDs2NjAuNTE7MTMzLjIzOzAuMDA7MjUyLjE4OzAuMDA7MTEvMjAyNDsNCjtUb3RhbCBn6W7pcmFsOzs7OzsxMjAuMDA7NDUuMDA7NzUuMDA7ODU5NzUuNDA7MzI3OTQuNjA7NTUxMDcuMTA7ODIuOTg7MC4wMDs4Mi45ODs1Nzg1Ni44MDswLjAwOzU3ODU2LjgwOzAuMDA7MC4wMDswLjAwOzY5MTIuMTM7MC4wMDs4NTg0Mi4yMDs4ODMzMy40Mzs2OTEyNS44ODswLjAwOzE3NDcwNy4yNTs4NTg0Mi4yMDswLjAwOzAuMDA7MC4wMDs4MjExNi4xMDs4MDg4Ni4xOTsxODgzMi4zNDszNzk4LjM5OzAuMDA7OTk4Mi44NDs0OS40NTs7DQo="
    # OR07720     = "TWF0cmljdWxlO1NhbGFyaek7Tm9tO051belyb2RlY29udHJhdDtEYXRlZGVk6WJ1dGRlY29udHJhdDtEYXRlZGVk6WJ1dGRlbXBsb2k7Sm91cnNBY3F1aXNOMTtKb3Vyc1ByaXNOMTtKb3Vyc1NvbGRlTjE7QmFzZUNQTjE7QmFzZUNQUHJpc04xO0Jhc2VDUFNvbGRlTjE7Sm91cnNBY3F1aXNOO0pvdXJzUHJpc047Sm91cnNTb2xkTjtCYXNlQ1BOO0Jhc2VDUFByaXNOO0Jhc2VDUFNvbGRlTjtSVFRBQ1FVSVM7UlRUUFJJUztSVFRTT0xERTtIZXVyZXM7SGV1cmVzU3VwcDtCcnV0O05ldOBwYXllcjtOZXRpbXBvc2FibGU7QWJhdHRlbWVudDtQTVNTO1RyYW5jaGVBO1RyYW5jaGVCO1RyYW5jaGVDO1RyYW5jaGUyQUZJUkNBUlJDTztTTUlDaGV1cmVzdHJhdmFpbGzpZXM7U01JQ0ZJTExPbjtUb3RhbFJlZHVjdGlvbkfpbulyYWxlVXJzc2FmO1RvdGFsUmVkdWN0aW9uR+lu6XJhbGVSZXRyYWl0ZTtNb250YW50bmV0ZmlzY2Fs6XhvbulyYXRpb25zdXJIU0hDO0NoYXJnZXNQYXRyb25hbGVzO1JldGVudWVBbGFzb3VyY2U7RGF0ZVJlcHJpc2U7DQowMDAwMTtTVUlOIEdoaXpsYW5lO1NVSU47MDAwMDI7OzAxLzEwLzIwMjI7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzI0NTQ5LjY5OzE4NTY3Ljg2OzIwMDAwLjA0OzAuMDA7NDI1MDQuMDA7MjQ1NDkuNjk7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzExMDk0LjgzOzY3OC41MDsxMS8yMDI0Ow0KO1RvdGFsIGfpbulyYWw7Ozs7OzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDsyNDU0OS42OTsxODU2Ny44NjsyMDAwMC4wNDswLjAwOzQyNTA0LjAwOzI0NTQ5LjY5OzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDsxMTA5NC44Mzs2NzguNTA7Ow0K"
    TESTALLONES = "TWF0cmljdWxlO1NhbGFyaek7Tm9tO051belyb2RlY29udHJhdDtEYXRlZGVk6WJ1dGRlY29udHJhdDtEYXRlZGVk6WJ1dGRlbXBsb2k7Sm91cnNBY3F1aXNOMTtKb3Vyc1ByaXNOMTtKb3Vyc1NvbGRlTjE7QmFzZUNQTjE7QmFzZUNQUHJpc04xO0Jhc2VDUFNvbGRlTjE7Sm91cnNBY3F1aXNOO0pvdXJzUHJpc047Sm91cnNTb2xkTjtCYXNlQ1BOO0Jhc2VDUFByaXNOO0Jhc2VDUFNvbGRlTjtSVFRBQ1FVSVM7UlRUUFJJUztSVFRTT0xERTtIZXVyZXM7SGV1cmVzU3VwcDtCcnV0O05ldOBwYXllcjtOZXRpbXBvc2FibGU7QWJhdHRlbWVudDtQTVNTO1RyYW5jaGVBO1RyYW5jaGVCO1RyYW5jaGVDO1RyYW5jaGUyQUZJUkNBUlJDTztTTUlDaGV1cmVzdHJhdmFpbGzpZXM7U01JQ0ZJTExPbjtUb3RhbFJlZHVjdGlvbkfpbulyYWxlVXJzc2FmO1RvdGFsUmVkdWN0aW9uR+lu6XJhbGVSZXRyYWl0ZTtNb250YW50bmV0ZmlzY2Fs6XhvbulyYXRpb25zdXJIU0hDO0NoYXJnZXNQYXRyb25hbGVzO1JldGVudWVBbGFzb3VyY2U7RGF0ZVJlcHJpc2UNCjAwMDAyO1RFU1QgVEVTVDtURVNUOzAwMDAxOzAxLzAxLzIwMTk7MDEvMDEvMjAxOTsyOzE7MTsyOzE7MTsyOzE7MTsyOzE7MTsyOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTtub3YtMjQNCg=="
    cumulmap = {"SEA OI":{"DateReprise":"01/12/2024","Cumul":TESTALLONES}}
    matContrID = {"00002":{"id": 263033, "date_debut_contrat":"01/01/2019"}}
    op_cumuls, contrat = parser.parseCumuls(cumulmap,matriculeContratId=matContrID)
    creerMultiples("E2RH",__VARIABLESREPRISEDOSSIER__, op_cumuls)
    
    # # print()
    # # print()
    # # print()
    # testTauxAT("271ZF",2025,7.38)
    # testTauxAT("271ZF",2024,7.38)
    # testTauxAT("271ZF",2023,8.83)
    # testTauxAT("27.1ZF",2024,7.38)
    # testTauxAT("unknown",2024,None)
    print()
    print()
    print()
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
    print()
    print()
    print()