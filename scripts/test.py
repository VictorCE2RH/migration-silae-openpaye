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

def testFunc(context,res, condition):
    print(f"{context} {logger.SuccessStatement(
        "OK") if res == condition else logger.ErrorStatement("KO")}")

def testEmploiCCN(sCode, statutCode, opcc, empCode, statut=sp.PAS_STATUT):
    testFunc(f"Résultat emploiCCN {sCode} {statutCode} = {opcc} {empCode} {statut}", 
            extract.emploiCCN(sCode, statutCode, opcc),
            [opcc, empCode, statut])

def testCivilite(civilite, expected):
    testFunc(f"Résultat Civilite {civilite} = {expected}",
            extract.civilite(civilite),
            expected)

def testTauxAT(codeRisque,annee,expected):
    testFunc(f"Résultat Taux AT {codeRisque} {annee} == {expected}",
            extract.getTauxAT(codeRisque,annee),
            expected)


if __name__ == "__main__":
    # print(f" Résultat codeTravail           '1' = 1  {extract.codeTravail(code="01") == 1 }")
    # print(f" Résultat codeTravail   '2' '8' 145 = 60 {extract.codeTravail(code="2",motif="8",typeContrat=145) == 60}")
    # print(f" Résultat codeTravail  '1' None 140 = 82 {extract.codeTravail(code="1",typeContrat="140") == 82}")
    # print(f" Résultat codeTravail '1' '8' 145 = None {extract.codeTravail(code="1",motif="8",typeContrat=145,emploiPart="14.3") == None}")
    # print(f" Résultat codeTravail  '1' None 140 = 82 {extract.codeTravail(code="1",typeContrat="140") == 82}")
    # print(f" Résultat codeTravail  '1' None 140 = 82 {extract.codeTravail(code="1",typeContrat="140") == 82}")
    # print(f" Résultat codeTravail  '1' None 140 = 82 {extract.codeTravail(code="1",typeContrat="140") == 82}")
    # print(f" Résultat codeTravail  '1' None 140 = 82 {extract.codeTravail(code="1",typeContrat="140") == 82}")

    # print(f"Résultat Statut prof 9  = 5  {extract.statutProf(9) == 5}")
    # print(f"Résultat Statut prof 88 = 28 {extract.statutProf(88) == 28}")
    # print(f"Résultat Statut prof 21 = 27 {extract.statutProf(21) == 27}")
    # print(f"Résultat Statut prof 12 = 23 {extract.statutProf(12) == 23}")
    # print(f"Résultat Statut prof 5  = 90 {extract.statutProf(5) == 90}")
    # print(f"Résultat Statut prof 90 = 90 {extract.statutProf(90) == 90}")

    # testEmploiCCN(sCode='A018.01.001', statutCode='01',opcc=1880, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='E161.01.001', statutCode='01',opcc=7023, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='A023.07', statutCode='',opcc=9578, empCode=None, statut=sp.PAS_STATUT)
    # testEmploiCCN(sCode='A032.01.001', statutCode='02',opcc=2571, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='A034.01.001', statutCode='02',opcc=2247, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='A044.01.001', statutCode='01',opcc=3021, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='B065.01.1', statutCode='31',opcc=1000, empCode=10, statut=sp.ETAM)
    # testEmploiCCN(sCode='C050.02.001', statutCode='02',opcc=2978, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='C051.04.001', statutCode='01',opcc=1408, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='C001.01.001', statutCode='02',opcc=8745, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='D002.001', statutCode='02',opcc=3052, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='F009.01.001', statutCode='02',opcc=9999, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='R007.06.001', statutCode='02',opcc=7510, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='P015.01.001', statutCode='01',opcc=786, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='O002.01.01', statutCode='90',opcc=6661, empCode=10, statut=sp.PAS_STATUT)
    # testEmploiCCN(sCode='P055.01.001', statutCode='02',opcc=3021, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='T002.01.001', statutCode='02',opcc=96, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='E026.01.001', statutCode='29',opcc=2010, empCode=10, statut=sp.CADRE)
    # testEmploiCCN(sCode='C069.01.001', statutCode='02',opcc=5000, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='F005.01.001', statutCode='02',opcc=5454, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='B007.01.001', statutCode='29',opcc=1843, empCode=10, statut=sp.CADRE)
    # testEmploiCCN(sCode='B032.01.1', statutCode='01',opcc=1740, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='B025.01.001', statutCode='90',opcc=9789, empCode=10, statut=sp.PAS_STATUT)
    # testEmploiCCN(sCode='B026.01.001', statutCode='01',opcc=9789, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='B009.01.001', statutCode='02',opcc=9517, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='B006.05.001', statutCode='29',opcc=3874, empCode=10, statut=sp.CADRE)
    # testEmploiCCN(sCode='B033.01.1', statutCode='01',opcc=2827, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='B008.01.001', statutCode='02',opcc=5782, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='B045.01.1', statutCode='01',opcc=8002, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='B053.01.1', statutCode='01',opcc=158, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='M107.01.1', statutCode='01',opcc=3216, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='B056.01.1', statutCode='01',opcc=7531, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='B057.01.001', statutCode='01',opcc=6083, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='C070.01.1', statutCode='02',opcc=2222, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='C078.01.001', statutCode='01',opcc=9988, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='A038.01.1', statutCode='29',opcc=2642, empCode=10, statut=sp.CADRE)
    # testEmploiCCN(sCode='C055.01.1', statutCode='02',opcc=1111, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='C083.01.001', statutCode='01',opcc=1561, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='V001.05.001', statutCode='01',opcc=1543, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='H001.01.01', statutCode='01',opcc=3213, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='E023.01.001', statutCode='01',opcc=1790, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='D005.01.1', statutCode='01',opcc=1605, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='E028.02.01', statutCode='02',opcc=1605, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='H013.04.01', statutCode='01',opcc=1487, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='H019.01.1', statutCode='02',opcc=7500, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='I001.01.01', statutCode='02',opcc=8555, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='I002.01.001', statutCode='02',opcc=3399, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='M009.01.01', statutCode='01',opcc=2528, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='T019.09.01', statutCode='01',opcc=1404, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='M095.05.01', statutCode='01',opcc=1930, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='P018.01.001', statutCode='01',opcc=176, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='P022.01.001', statutCode='01',opcc=8787, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='P050.01.001', statutCode='01',opcc=1396, empCode=5, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='V014.1.001', statutCode='',opcc=3333, empCode=10, statut=sp.PAS_STATUT)
    # testEmploiCCN(sCode='V008.01.001', statutCode='01',opcc=5020, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='T029.009', statutCode='02',opcc=1413, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='T026.1.1', statutCode='01',opcc=7002, empCode=10, statut=sp.OUVRIER)
    # testEmploiCCN(sCode='T013.01.001', statutCode='02',opcc=4759, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='S009.01.001', statutCode='02',opcc=9876, empCode=10, statut=sp.EMPLOYE)
    # testEmploiCCN(sCode='S008.01.1', statutCode='02',opcc=8888, empCode=10, statut=sp.EMPLOYE)
    
    testCivilite(1,1)
    testCivilite(0,None)
    testCivilite(2,2)
    testCivilite(3,2)
    testCivilite(512,None)
    testCivilite(-5165,None)

    # print(f"Résultat IDCC to OPCC 3016 0964 {extract.idccToOpcc("3016") == 964}")
    # print(f"Résultat IDCC to OPCC 1539 3570 {extract.idccToOpcc("1539") == 3570}")
    # print(f"Résultat IDCC to OPCC 0915 9876 {extract.idccToOpcc("0915") == 9876}")
    # print(f"Résultat IDCC to OPCC 0303 6624 {extract.idccToOpcc("0303") == 6624}")
    # print(f"Résultat IDCC to OPCC 1286 9988 {extract.idccToOpcc("1286") == 9988}")
    # print(f"Résultat IDCC to OPCC 2420 3874 {extract.idccToOpcc("2420") == 3874}")
    # print(f"Résultat IDCC to OPCC 2666 9835 {extract.idccToOpcc("2666") == 9835}")
    # print(f"Résultat IDCC to OPCC 1880 4578 {extract.idccToOpcc("1880") == 4578}")

    # print(f"Résultat IDCC to OPCC 1880 4578 {extract.idccToOpcc("1880") == 4578}")
    # print(f"Résultat IDCC to OPCC 1880 4578 {extract.idccToOpcc(1880) == 4578}")
    # print(f"Résultat IDCC to OPCC 1880 4578 {extract.idccToOpcc(1880) == 4578}")
    # print(f"Résultat IDCC to OPCC 1880 4578 {extract.idccToOpcc(1880) == 4578}")
    # print(f"Résultat IDCC to OPCC 1880 4578 {extract.idccToOpcc(1880) == 4578}")
    # print(f"Résultat IDCC to OPCC 1880 4578 {extract.idccToOpcc("1880") == 4578}")
    # print(f"Résultat IDCC to OPCC 1880 4578 {extract.idccToOpcc("1880") == 4578}")
    # print(f"Résultat IDCC to OPCC 2408 8551 {extract.idccToOpcc("2408") == 8551}")
    # print(f"Résultat IDCC to OPCC 2691 8550 {extract.idccToOpcc("2691") == 8550}")
    # print(f"Résultat IDCC to OPCC 2198 0083 {extract.idccToOpcc("2198") == 83}")
    # print(f"Résultat IDCC to OPCC 1686 3125 {extract.idccToOpcc("1686") == 3125}")
    # print(f"Résultat IDCC to OPCC 2543 7100 {extract.idccToOpcc("2543") == 7100}")
    # print(f"Résultat IDCC to OPCC 1518 3333 {extract.idccToOpcc("1518") == 3333}")
    # print(f"Résultat IDCC to OPCC 1740 2827 {extract.idccToOpcc("1740") == 2827}")
    # print(f"Résultat IDCC to OPCC 0993 3333 {extract.idccToOpcc("0993") == 3333}")
    # print(f"Résultat IDCC to OPCC 2332 9578 {extract.idccToOpcc("2332") == 9578}")
    # print(f"Résultat IDCC to OPCC 1000 8527 {extract.idccToOpcc("1000") == 8527}")

    # print(f"0xFFF \n{utils.integerToBitArray(0xFFF)}")
    # print(f"0x0FF \n{utils.integerToBitArray(0x0FF)}")
    # print(f"0     \n{utils.integerToBitArray(0)}")
    # print(f"0xDA3 \n{utils.integerToBitArray(0xDA3)}")
    # print(f"0x3   \n{utils.integerToBitArray(0x3)}")
    # print(f"0x20F \n{utils.integerToBitArray(0x20F)}")

    # OR10420 = "TWF0cmljdWxlO1NhbGFyaek7Tm9tO051belyb2RlY29udHJhdDtEYXRlZGVk6WJ1dGRlY29udHJhdDtEYXRlZGVk6WJ1dGRlbXBsb2k7Sm91cnNBY3F1aXNOMTtKb3Vyc1ByaXNOMTtKb3Vyc1NvbGRlTjE7QmFzZUNQTjE7QmFzZUNQUHJpc04xO0Jhc2VDUFNvbGRlTjE7Sm91cnNBY3F1aXNOO0pvdXJzUHJpc047Sm91cnNTb2xkTjtCYXNlQ1BOO0Jhc2VDUFByaXNOO0Jhc2VDUFNvbGRlTjtSVFRBQ1FVSVM7UlRUUFJJUztSVFRTT0xERTtIZXVyZXM7SGV1cmVzU3VwcDtCcnV0O05ldOBwYXllcjtOZXRpbXBvc2FibGU7QWJhdHRlbWVudDtQTVNTO1RyYW5jaGVBO1RyYW5jaGVCO1RyYW5jaGVDO1RyYW5jaGUyQUZJUkNBUlJDTztTTUlDaGV1cmVzdHJhdmFpbGzpZXM7U01JQ0ZJTExPbjtUb3RhbFJlZHVjdGlvbkfpbulyYWxlVXJzc2FmO1RvdGFsUmVkdWN0aW9uR+lu6XJhbGVSZXRyYWl0ZTtNb250YW50bmV0ZmlzY2Fs6XhvbulyYXRpb25zdXJIU0hDO0NoYXJnZXNQYXRyb25hbGVzO1JldGVudWVBbGFzb3VyY2U7RGF0ZVJlcHJpc2U7DQowMDAwNztBQlJZIFZhbOlyaWU7QUJSWTtDVDAwMDAwMTswMy8wNS8yMDIyOzAzLzA1LzIwMjI7MzAwLjAwOzIwMS4wMDs5OS4wMDs0OTk2NS4wMDs1MzcyMy4xMDs1MTc1NS40MDsxNjIuNTA7MC4wMDsxNjIuNTA7NTg2OTIuMDA7MC4wMDs5NjI5Ny44MDswLjAwOzAuMDA7MC4wMDs4MzQxLjg1OzAuMDA7MTA4NjU3LjAwOzg0MDQ1Ljk4Ozg4MTczLjY2OzAuMDA7MjEyNTIwLjAwOzEwODY1Ny4wMDswLjAwOzAuMDA7MC4wMDs5NzE4Mi41NTs5NzE4Mi44MDsyMDI0MC44MDs0NjkxLjQ5OzAuMDA7MTQ0OTQuMjI7MjA1NC4wNDs7DQowMDAwOTtDSEVWUk9UIEFsZXhhbmRyZTtDSEVWUk9UO0NUMDAwMDAzOzAyLzAxLzIwMjQ7MDIvMDEvMjAyNDs2NS4wMDs2LjAwOzU5LjAwOzQ3MjQwLjAwOzQzNjAuNTA7NDI4ODAuNDA7NzUuNTA7MC4wMDs3NS41MDs1NzQ5NC4yMDswLjAwOzU3NDk0LjIwOzAuMDA7MC4wMDswLjAwOzgzNDEuODU7MC4wMDsxMDQ3MzQuMjk7Nzk1MzQuNzc7ODUzMTMuNzM7MC4wMDsyMTEyNzMuNTA7MTA0NzM0LjI5OzAuMDA7MC4wMDswLjAwOzk3MTgyLjU1Ozk3MTgyLjgwOzIxOTM2LjA4OzUwODQuMzQ7MC4wMDsxMTg5OC4wMjsxMjM3LjIzOzsNCjAwMDAyO0RVQlVDIE3pbGlzc2E7RFVCVUM7OzAxLzEyLzIwMTE7MDEvMTIvMjAxMTsxODAuMDA7NDAuMDA7MTQwLjAwOzAuMDA7MTg2ODEuNjA7MjE5NDUuMDA7MTM1LjAwOzAuMDA7MTM1LjAwOzI5MTQ4LjQwOzAuMDA7MjExNjEuMzA7MC4wMDswLjAwOzAuMDA7Mjc2Ny40MDswLjAwOzUyOTk2LjA0OzU2Nzc0LjQ4OzQzMTYzLjc4OzAuMDA7NTQ1NTkuMTg7NDY2MTMuMjI7NjM4Mi44MjswLjAwOzYzODIuODI7MzIyNDAuMjE7MzAwNjYuNzA7MjA2My42ODs0NzguMzI7MC4wMDsyMTY4My4xODswLjAwOzsNCjAwMDA0O0xFQ0xFUkMgU3TpcGhhbmU7TEVDTEVSQztDVDAwMDI1OzI5LzA4LzIwMTY7MjkvMDgvMjAxNjszMjAuMDA7MTkyLjAwOzEyOC4wMDs3OTk0NS4wMDs5NTI5OS43MDsxNDg3MzYuMDA7MTYyLjUwOzAuMDA7MTYyLjUwOzk1Njg3LjUwOzAuMDA7MTkyODU4LjUwOzAuMDA7MC4wMDswLjAwOzc4OTMuODU7NDE2LjMyOzE2OTEzNi4yMjsxMzcxMjMuMjY7MTI5Nzg3LjM2OzAuMDA7MjA5NTI4LjQ4OzE2OTEzNi4yMjswLjAwOzAuMDA7MC4wMDs5NjgxMy40ODs5ODQ4MC41NjswLjAwOzAuMDA7ODg2MS45Mjs2MTUxMi41OTs2MTAxLjYyOzsNCjAwMDAzO1JPVUlMTEVUIE1vcmdhbjtST1VJTExFVDtDVDAwMDIzOzE0LzAzLzIwMTY7MTQvMDMvMjAxNjszNDIuNTA7MTY1LjUwOzE3Ny4wMDs2MTk2My41MDs1NTcxOC4yMDsxNTY1MzMuMDA7MTYyLjUwOzAuMDA7MTYyLjUwOzc0MTM5LjIwOzAuMDA7MTQ3NDQ3LjUwOzAuMDA7MC4wMDswLjAwOzc1MzYuODU7MC4wMDsxMjM4MTguNDQ7MTAyNjQxLjE4OzEwMDgwMC40MTswLjAwOzE5MzY2OS41MjsxMjM4MTguNDQ7MC4wMDswLjAwOzAuMDA7ODc4MDQuMzA7ODgyNTAuODE7NzUxMi41MjsxNzQxLjEwOzAuMDA7MzY1MzUuMDE7MzQ1My40Njs7DQowMDAwODtaQVJGQU5JIFRsYXl0bWFzc2U7WkFSRkFOSTtDVDAwMDAwMjswMS8wNi8yMDIyOzAxLzA2LzIwMjI7MzAwLjAwOzE2Mi4wMDsxMzguMDA7NTE2ODkuMDA7NjgxOTIuMzA7ODM4NDIuMTA7MTYyLjUwOzAuMDA7MTYyLjUwOzYwOTQ3LjAwOzAuMDA7MTAzMzI4LjYwOzAuMDA7MC4wMDswLjAwOzgzNDEuODU7MC4wMDsxMTI2MzYuNDA7ODU0ODguNTY7OTE3MjYuMzY7MC4wMDsyMTI1MjAuMDA7MTEyNjM2LjQwOzAuMDA7MC4wMDswLjAwOzk3MTgyLjU1Ozk3MTgyLjgwOzE4NTIxLjY5OzQyOTIuOTU7MC4wMDsxODk0Ni42MzsxMzI0LjU0OzsNCjtUb3RhbCBn6W7pcmFsOzs7OzsxNTA3LjUwOzc2Ni41MDs3NDEuMDA7MjkwODAyLjUwOzI5NTk3NS40MDs1MDU2OTEuOTA7ODYwLjUwOzAuMDA7ODYwLjUwOzM3NjEwOC4zMDswLjAwOzYxODU4Ny45MDswLjAwOzAuMDA7MC4wMDs0MzIyMy42NTs0MTYuMzI7NjcxOTc4LjM5OzU0NTYwOC4yMzs1Mzg5NjUuMzA7MC4wMDsxMDk0MDcwLjY4OzY2NTU5NS41Nzs2MzgyLjgyOzAuMDA7NjM4Mi44Mjs1MDg0MDUuNjU7NTA4MzQ2LjQ3OzcwMjc0Ljc3OzE2Mjg4LjIwOzg4NjEuOTI7MTY1MDY5LjY1OzE0MTcwLjg5OzsNCg=="
    D4KOR0022 = "TWF0cmljdWxlO1NhbGFyaek7Tm9tO051belyb2RlY29udHJhdDtEYXRlZGVk6WJ1dGRlY29udHJhdDtEYXRlZGVk6WJ1dGRlbXBsb2k7Sm91cnNBY3F1aXNOMTtKb3Vyc1ByaXNOMTtKb3Vyc1NvbGRlTjE7QmFzZUNQTjE7QmFzZUNQUHJpc04xO0Jhc2VDUFNvbGRlTjE7Sm91cnNBY3F1aXNOO0pvdXJzUHJpc047Sm91cnNTb2xkTjtCYXNlQ1BOO0Jhc2VDUFByaXNOO0Jhc2VDUFNvbGRlTjtSVFRBQ1FVSVM7UlRUUFJJUztSVFRTT0xERTtIZXVyZXM7SGV1cmVzU3VwcDtCcnV0O05ldOBwYXllcjtOZXRpbXBvc2FibGU7QWJhdHRlbWVudDtQTVNTO1RyYW5jaGVBO1RyYW5jaGVCO1RyYW5jaGVDO1RyYW5jaGUyQUZJUkNBUlJDTztTTUlDaGV1cmVzdHJhdmFpbGzpZXM7U01JQ0ZJTExPbjtUb3RhbFJlZHVjdGlvbkfpbulyYWxlVXJzc2FmO1RvdGFsUmVkdWN0aW9uR+lu6XJhbGVSZXRyYWl0ZTtNb250YW50bmV0ZmlzY2Fs6XhvbulyYXRpb25zdXJIU0hDO0NoYXJnZXNQYXRyb25hbGVzO1JldGVudWVBbGFzb3VyY2U7RGF0ZVJlcHJpc2U7DQowMDAyNjtCRUxMRVMgQ2hyaXN0b3BoZXI7QkVMTEVTOzsxNC8xMC8yMDI0OzE0LzEwLzIwMjQ7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7NC4wMDswLjAwOzQuMDA7MjU4Ny4zMDswLjAwOzI1ODcuMzA7MC4wMDswLjAwOzAuMDA7MjE0LjAwOzAuMDA7MjU4Ny4yNjsyNzQyLjIyOzIwODQuMzk7MC4wMDs1MjM0Ljk5OzI1ODcuMjY7MC4wMDswLjAwOzAuMDA7MjU0Mi4zMjsyNTIzLjAwOzYyNi41MjsxMjYuMzc7MC4wMDsyMzcuNTI7MC4wMDsxMS8yMDI0Ow0KMDAwMjg7QkVOTkVUT1QgQ2hhcmxlcztCRU5ORVRPVDswMDAwMTsxNC8xMC8yMDI0OzE0LzEwLzIwMjQ7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7NC4wMDswLjAwOzQuMDA7MzM3MC42MDswLjAwOzMzNzAuNjA7MC4wMDswLjAwOzAuMDA7MjQ5LjY3OzAuMDA7MzM3MC41NTszMjYyLjc2OzI3MTMuMDI7MC4wMDs2MTA3LjYxOzMzNzAuNTU7MC4wMDswLjAwOzAuMDA7Mjk2Ni4wODsyOTQzLjU0OzU3OC42MzsxMTYuNzE7MC4wMDs1OTYuNDE7NDkuNDU7MTEvMjAyNDsNCjAwMDMzO0NIQU1QT1RSQVkgTm/pbWllO0NIQU1QT1RSQVk7OzE4LzExLzIwMjQ7MTgvMTEvMjAyNDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDsxLjA4OzAuMDA7MS4wODs4NDYuMzA7MC4wMDs4NDYuMzA7MC4wMDswLjAwOzAuMDA7NzAuMDA7MC4wMDs4NDYuMzA7MTA5Ni43NDs2ODEuODA7MC4wMDsxNjc0LjQwOzg0Ni4zMDswLjAwOzAuMDA7MC4wMDs4MzEuNjA7ODMxLjYwOzIwOS4zMDs0Mi4yMjswLjAwOzcyLjQ2OzAuMDA7MTEvMjAyNDsNCjAwMDMwO0NPVFRJTEFSRCBFdmFuO0NPVFRJTEFSRDs7MTgvMTEvMjAyNDsxOC8xMS8yMDI0OzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzEuMDg7MC4wMDsxLjA4Ozg0Ni4zMDswLjAwOzg0Ni4zMDswLjAwOzAuMDA7MC4wMDs3MC4wMDswLjAwOzg0Ni4zMDsxMDc2Ljc0OzY4MS44MDswLjAwOzE2NzQuNDA7ODQ2LjMwOzAuMDA7MC4wMDswLjAwOzgzMS42MDs4MzEuNjA7MjA5LjMwOzQyLjIyOzAuMDA7NzIuNDY7MC4wMDsxMS8yMDI0Ow0KMDAwMDI7RE9VQkxFVCBCZW5v7nQ7RE9VQkxFVDswMDAwMTAwMDA2MTUxMzE7MTEvMDUvMjAxNTsxMS8wNS8yMDE1OzMwLjAwOzE5LjAwOzExLjAwOzIyMjYyLjYwOzE0MDkxLjAwOzgxNjMuMTA7MTUuMDA7MC4wMDsxNS4wMDsxMTQ1Ny41MDswLjAwOzExNDU3LjUwOzAuMDA7MC4wMDswLjAwOzE2NjguMzc7MC4wMDsyMDk5Mi45MzsyMDYwNC45MzsxNjkxMi40NDswLjAwOzQyNTA0LjAwOzIwOTkyLjkzOzAuMDA7MC4wMDswLjAwOzE5ODIwLjI0OzE5NDcxLjQ0OzQzOTEuODQ7ODg1Ljc4OzAuMDA7MjU0My4xODswLjAwOzExLzIwMjQ7DQowMDAzMTtEVU1FTklMIFpv6TtEVU1FTklMOzsxOC8xMS8yMDI0OzE4LzExLzIwMjQ7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MS4wODswLjAwOzEuMDg7ODQ2LjMwOzAuMDA7ODQ2LjMwOzAuMDA7MC4wMDswLjAwOzQ5LjAwOzAuMDA7NTkyLjQxOzc3OS40OTs0NzcuMjc7MC4wMDsxMjg4LjAwOzU5Mi40MTswLjAwOzAuMDA7MC4wMDs1ODIuMTI7NTgyLjEyOzE0Ni41MTsyOS41NTswLjAwOzUwLjcxOzAuMDA7MTEvMjAyNDsNCjAwMDI3O0ZMRVVUUlkgQWxleGlzO0ZMRVVUUlk7MDAwMDE7MTQvMTAvMjAyNDsxNC8xMC8yMDI0OzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzQuMDA7MC4wMDs0LjAwOzMwMTguNTA7MC4wMDszMDE4LjUwOzAuMDA7MC4wMDswLjAwOzI0OS42NzswLjAwOzMwMTguNTE7MzEzOC43MjsyNDI5LjQzOzAuMDA7NjEwNy42MTszMDE4LjUxOzAuMDA7MC4wMDswLjAwOzI5NjYuMDg7Mjk0My41NDs3MzAuOTY7MTQ3LjQzOzAuMDA7MjgyLjA4OzAuMDA7MTEvMjAyNDsNCjAwMDA1O0dBTExJT1ogTG9pcztHQUxMSU9aOzAwMDAxMDAwMjAxOTE3MTsyMC8wNi8yMDE5OzIwLzA2LzIwMTk7NjAuMDA7MC4wMDs2MC4wMDs0MTg3Ny4xMDswLjAwOzQ0MDEwLjAwOzE1LjAwOzAuMDA7MTUuMDA7MTE0MDUuNDA7MC4wMDsxMTQwNS40MDswLjAwOzAuMDA7MC4wMDsxNjY4LjM3OzAuMDA7MjA3NTcuMzY7MjE0NTIuNzE7MTY3MDkuNTc7MC4wMDs0MjUwNC4wMDsyMDc1Ny4zNjswLjAwOzAuMDA7MC4wMDsxOTgyMC4yNDsxOTQ3MS40NDs0NDkyLjgwOzkwNi4xOTswLjAwOzI1MjcuNTE7MC4wMDsxMS8yMDI0Ow0KMDAwMDc7R0lNRVIgTGF1cmVudDtHSU1FUjswMDAwMTAwMDIzMTkyMTg7MDYvMDgvMjAxOTswNi8wOC8yMDE5OzMwLjAwOzI2LjAwOzQuMDA7MjE4MzUuNzA7MTg3MDMuNjA7MjkzNC4wMDsxNS4wMDswLjAwOzE1LjAwOzExMzMyLjIwOzAuMDA7MTEzMzIuMjA7MC4wMDswLjAwOzAuMDA7MTY2OC4zNzswLjAwOzIwNjg0LjAwOzIwNDQzLjI0OzE2NjUwLjQ3OzAuMDA7NDI1MDQuMDA7MjA2ODQuMDA7MC4wMDswLjAwOzAuMDA7MTk4MjAuMjQ7MTk0NzEuNDQ7NDUyNS4xMzs5MTIuNjk7MC4wMDsyNDYxLjM0OzAuMDA7MTEvMjAyNDsNCjAwMDMyO0xFQkFTIENocmlzdG9waGU7TEVCQVM7OzE4LzExLzIwMjQ7MTgvMTEvMjAyNDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDsxLjA4OzAuMDA7MS4wODs4NDYuMzA7MC4wMDs4NDYuMzA7MC4wMDswLjAwOzAuMDA7NzAuMDA7MC4wMDs4NDYuMzA7MTI3Ni43NDs2ODEuODA7MC4wMDsxNjc0LjQwOzg0Ni4zMDswLjAwOzAuMDA7MC4wMDs4MzEuNjA7ODMxLjYwOzIwOS4zMDs0Mi4yMjswLjAwOzcyLjQ2OzAuMDA7MTEvMjAyNDsNCjAwMDI1O0xFTE9VQVJEIE1heGltZTtMRUxPVUFSRDswMDAwMTsxMS8xMC8yMDI0OzExLzEwLzIwMjQ7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7NC4yNTswLjAwOzQuMjU7MjY1OS44MDswLjAwOzI2NTkuODA7MC4wMDswLjAwOzAuMDA7MjIwLjAwOzAuMDA7MjY1OS44MDsyODEzLjc2OzIxNDIuODE7MC4wMDs1NTU1LjUwOzI2NTkuODA7MC4wMDswLjAwOzAuMDA7MjYxMy42MDsyNTkyLjkwOzY0My40MzsxMjkuNzc7MC4wMDsyNDQuOTc7MC4wMDsxMS8yMDI0Ow0KMDAwMjk7TEVURUxMSUVSIE1hdHRoaWV1O0xFVEVMTElFUjs7MTgvMTEvMjAyNDsxOC8xMS8yMDI0OzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzEuMDg7MC4wMDsxLjA4Ozg0Ni4zMDswLjAwOzg0Ni4zMDswLjAwOzAuMDA7MC4wMDs3MC4wMDswLjAwOzg0Ni4zMDs5NzYuNzQ7NjgxLjgwOzAuMDA7MTY3NC40MDs4NDYuMzA7MC4wMDswLjAwOzAuMDA7ODMxLjYwOzgzMS42MDsyMDkuMzA7NDIuMjI7MC4wMDs3Mi40NjswLjAwOzExLzIwMjQ7DQowMDAyMjtQSUVSUkVUIENocnlzdGVsbGU7UElFUlJFVDswMDAwMTswOC8wNy8yMDI0OzA4LzA3LzIwMjQ7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzAuMDA7MTIuMDA7MC4wMDsxMi4wMDs1MDYxLjcwOzAuMDA7NTA2MS43MDswLjAwOzAuMDA7MC4wMDs0MTguNjg7MC4wMDs1MDYxLjg0OzU3ODMuMzA7NDA3OC4wMTswLjAwOzEwNTQxLjYxOzUwNjEuODQ7MC4wMDswLjAwOzAuMDA7NDk3My45Mjs0ODk3LjU3OzExOTguODE7MjQxLjc5OzAuMDA7NDk3LjEwOzAuMDA7MTEvMjAyNDsNCjAwMDI0O1NPQVJFUyBIdWdvO1NPQVJFUzs7MTAvMTAvMjAyNDsxMC8xMC8yMDI0OzAuMDA7MC4wMDswLjAwOzAuMDA7MC4wMDswLjAwOzQuMzM7MC4wMDs0LjMzOzI3MzIuMzA7MC4wMDsyNzMyLjMwOzAuMDA7MC4wMDswLjAwOzIyNi4wMDswLjAwOzI3MzIuMzQ7Mjg4NS4zNDsyMjAxLjI3OzAuMDA7NTY2Mi4zMzsyNzMyLjM0OzAuMDA7MC4wMDswLjAwOzI2ODQuODg7MjY2Mi44MDs2NjAuNTE7MTMzLjIzOzAuMDA7MjUyLjE4OzAuMDA7MTEvMjAyNDsNCjtUb3RhbCBn6W7pcmFsOzs7OzsxMjAuMDA7NDUuMDA7NzUuMDA7ODU5NzUuNDA7MzI3OTQuNjA7NTUxMDcuMTA7ODIuOTg7MC4wMDs4Mi45ODs1Nzg1Ni44MDswLjAwOzU3ODU2LjgwOzAuMDA7MC4wMDswLjAwOzY5MTIuMTM7MC4wMDs4NTg0Mi4yMDs4ODMzMy40Mzs2OTEyNS44ODswLjAwOzE3NDcwNy4yNTs4NTg0Mi4yMDswLjAwOzAuMDA7MC4wMDs4MjExNi4xMDs4MDg4Ni4xOTsxODgzMi4zNDszNzk4LjM5OzAuMDA7OTk4Mi44NDs0OS40NTs7DQo="
    
    testTauxAT("271ZF",2025,7.38)
    testTauxAT("271ZF",2024,7.38)
    testTauxAT("271ZF",2023,8.83)
    testTauxAT("27.1ZF",2024,7.38)
    testTauxAT("unknown",2024,None)
    
    JOURNALPAIE=r".\data\in\base64JournalPaie"
    with open(JOURNALPAIE, encoding="utf-8") as f:
        content = base64.b64decode(f.read())
    with open(r".\data\out\edition_journal_paie.xml",'w',encoding="utf-8") as f:
        f.write(str(content))