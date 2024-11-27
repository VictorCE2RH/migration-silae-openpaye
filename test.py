import extract
import utils
import logger
import parser
import statut_pro as sp

def testEmploiCCN(sCode,statutCode,opcc,empCode,statut=sp.PAS_STATUT):
    print(f"Résultat emploiCCN {sCode} {statutCode} = {opcc} {empCode} {statut} {logger.SuccessStatement("OK") if extract.emploiCCN(sCode,statutCode,opcc) == [opcc,empCode,statut] else logger.ErrorStatement("KO")}")

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

    
    testEmploiCCN(sCode = "A018.02.008", statutCode="02",opcc=1880,empCode=130,statut=sp.EMPLOYE)
    testEmploiCCN(sCode = "A018.06.004", statutCode="29",opcc=1880,empCode=700,statut=sp.CADRE)
    testEmploiCCN(sCode = "A018.06.005", statutCode="04",opcc=1880,empCode=710,statut=sp.AGENT_MAITRISE)
    testEmploiCCN(sCode = "A018.06.005", statutCode="29",opcc=1880,empCode=720,statut=sp.CADRE)
    testEmploiCCN(sCode = "A018.09.002", statutCode="12",opcc=1880,empCode=900,statut=sp.CADRE_SUP)
    testEmploiCCN(sCode = "A018.09.002", statutCode="13",opcc=1880,empCode=910,statut=sp.CADRE_DIRIGEANT)
    testEmploiCCN(sCode = "unknown",statutCode="unknown",opcc=1880,empCode=9999)
    
    testEmploiCCN(sCode = "E161.01.029", statutCode="01",opcc=7023,empCode=570,statut=sp.OUVRIER)
    testEmploiCCN(sCode = "E161.01.029", statutCode="02",opcc=7023,empCode=580,statut=sp.EMPLOYE)
    
    testEmploiCCN(sCode = "A023.07",     statutCode=""  ,opcc=9578,empCode=9999)
    testEmploiCCN(sCode = "A032.03.005", statutCode="02",opcc=2571,empCode=400,statut=sp.EMPLOYE)
    testEmploiCCN(sCode = "A032.03.005", statutCode="03",opcc=2571,empCode=410,statut=sp.TECHNICIEN)
    testEmploiCCN(sCode = "A032.03.005", statutCode="04",opcc=2571,empCode=420,statut=sp.AGENT_MAITRISE)
    testEmploiCCN(sCode = "A032.04.001", statutCode="02",opcc=2571,empCode=430,statut=sp.EMPLOYE)
    testEmploiCCN(sCode = "A032.04.001", statutCode="03",opcc=2571,empCode=440,statut=sp.TECHNICIEN)
    testEmploiCCN(sCode = "A032.05.004", statutCode="02",opcc=2571,empCode=580,statut=sp.EMPLOYE)
    testEmploiCCN(sCode = "A032.06.003", statutCode="29",opcc=2571,empCode=610,statut=sp.CADRE)
    

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
    
    # OR10420 = "TWF0cmljdWxlO1NhbGFyaek7Tm9tO051belybyBkZSBjb250cmF0IDtEYXRlIGRlIGTpYnV0IGRlIGNvbnRyYXQ7RGF0ZSBkZSBk6WJ1dCBkJ2VtcGxvaTtKb3VycyBBY3F1aXMgTi0xO0pvdXJzIFByaXMgTi0xO0pvdXJzIFNvbGRlIE4tMTtCYXNlIENQIE4tMTtCYXNlIENQIFByaXMgTi0xO0Jhc2UgQ1AgU29sZGUgTi0xO0pvdXJzIEFjcXVpcyBOO0pvdXJzIFByaXMgTjtKb3VycyBTb2xkIE47QmFzZSBDUCBOO0Jhc2UgQ1AgUHJpcyBOO0Jhc2UgQ1AgU29sZGUgTjtSVFQgQUNRVUlTO1JUVCBQUklTO1JUVCBTT0xERTtIZXVyZXM7SGV1cmVzIFN1cHA7QnJ1dDtOZXQg4CBwYXllcjtOZXQgaW1wb3NhYmxlO0FiYXR0ZW1lbnQ7UE1TUztUcmFuY2hlIEE7VHJhbmNoZSBCO1RyYW5jaGUgQztUcmFuY2hlIDIgQUZJUkMgQVJSQ087U01JQyBoZXVyZXMgdHJhdmFpbGzpZXM7U01JQyBGSUxMT247VG90YWwgUmVkdWN0aW9uIEfpbulyYWxlIFVyc3NhZjtUb3RhbCBSZWR1Y3Rpb24gR+lu6XJhbGUgUmV0cmFpdGU7TW9udGFudCBuZXQgZmlzY2FsIOl4b27pcmF0aW9uIHN1ciBIUy9IQztDaGFyZ2VzIFBhdHJvbmFsZXM7UmV0ZW51ZSBBIGxhIHNvdXJjZTsNCjAwMDA3O0FCUlkgVmFs6XJpZTtBQlJZO0NUMDAwMDAxOzAzLzA1LzIwMjI7MDMvMDUvMjAyMjszMDAuMDA7MjAxLjAwOzk5LjAwOzQ5OTY1LjAwOzUzNzIzLjEwOzUxNzU1LjQwOzE2Mi41MDswLjAwOzE2Mi41MDs1ODY5Mi4wMDswLjAwOzk2Mjk3LjgwOzAuMDA7MC4wMDswLjAwOzgzNDEuODU7MC4wMDsxMDg2NTcuMDA7ODQwNDUuOTg7ODgxNzMuNjY7MC4wMDsyMTI1MjAuMDA7MTA4NjU3LjAwOzAuMDA7MC4wMDswLjAwOzk3MTgyLjU1Ozk3MTgyLjgwOzIwMjQwLjgwOzQ2OTEuNDk7MC4wMDsxNDQ5NC4yMjsyMDU0LjA0Ow0KMDAwMDk7Q0hFVlJPVCBBbGV4YW5kcmU7Q0hFVlJPVDtDVDAwMDAwMzswMi8wMS8yMDI0OzAyLzAxLzIwMjQ7NjUuMDA7Ni4wMDs1OS4wMDs0NzI0MC4wMDs0MzYwLjUwOzQyODgwLjQwOzc1LjUwOzAuMDA7NzUuNTA7NTc0OTQuMjA7MC4wMDs1NzQ5NC4yMDswLjAwOzAuMDA7MC4wMDs4MzQxLjg1OzAuMDA7MTA0NzM0LjI5Ozc5NTM0Ljc3Ozg1MzEzLjczOzAuMDA7MjExMjczLjUwOzEwNDczNC4yOTswLjAwOzAuMDA7MC4wMDs5NzE4Mi41NTs5NzE4Mi44MDsyMTkzNi4wODs1MDg0LjM0OzAuMDA7MTE4OTguMDI7MTIzNy4yMzsNCjAwMDAyO0RVQlVDIE3pbGlzc2E7RFVCVUM7OzAxLzEyLzIwMTE7MDEvMTIvMjAxMTsxODAuMDA7NDAuMDA7MTQwLjAwOzAuMDA7MTg2ODEuNjA7MjE5NDUuMDA7MTM1LjAwOzAuMDA7MTM1LjAwOzI5MTQ4LjQwOzAuMDA7MjExNjEuMzA7MC4wMDswLjAwOzAuMDA7Mjc2Ny40MDswLjAwOzUyOTk2LjA0OzU2Nzc0LjQ4OzQzMTYzLjc4OzAuMDA7NTQ1NTkuMTg7NDY2MTMuMjI7NjM4Mi44MjswLjAwOzYzODIuODI7MzIyNDAuMjE7MzAwNjYuNzA7MjA2My42ODs0NzguMzI7MC4wMDsyMTY4My4xODswLjAwOw0KMDAwMDQ7TEVDTEVSQyBTdOlwaGFuZTtMRUNMRVJDO0NUMDAwMjU7MjkvMDgvMjAxNjsyOS8wOC8yMDE2OzMyMC4wMDsxOTIuMDA7MTI4LjAwOzc5OTQ1LjAwOzk1Mjk5LjcwOzE0ODczNi4wMDsxNjIuNTA7MC4wMDsxNjIuNTA7OTU2ODcuNTA7MC4wMDsxOTI4NTguNTA7MC4wMDswLjAwOzAuMDA7Nzg5My44NTs0MTYuMzI7MTY5MTM2LjIyOzEzNzEyMy4yNjsxMjk3ODcuMzY7MC4wMDsyMDk1MjguNDg7MTY5MTM2LjIyOzAuMDA7MC4wMDswLjAwOzk2ODEzLjQ4Ozk4NDgwLjU2OzAuMDA7MC4wMDs4ODYxLjkyOzYxNTEyLjU5OzYxMDEuNjI7DQowMDAwMztST1VJTExFVCBNb3JnYW47Uk9VSUxMRVQ7Q1QwMDAyMzsxNC8wMy8yMDE2OzE0LzAzLzIwMTY7MzQyLjUwOzE2NS41MDsxNzcuMDA7NjE5NjMuNTA7NTU3MTguMjA7MTU2NTMzLjAwOzE2Mi41MDswLjAwOzE2Mi41MDs3NDEzOS4yMDswLjAwOzE0NzQ0Ny41MDswLjAwOzAuMDA7MC4wMDs3NTM2Ljg1OzAuMDA7MTIzODE4LjQ0OzEwMjY0MS4xODsxMDA4MDAuNDE7MC4wMDsxOTM2NjkuNTI7MTIzODE4LjQ0OzAuMDA7MC4wMDswLjAwOzg3ODA0LjMwOzg4MjUwLjgxOzc1MTIuNTI7MTc0MS4xMDswLjAwOzM2NTM1LjAxOzM0NTMuNDY7DQowMDAwODtaQVJGQU5JIFRsYXl0bWFzc2U7WkFSRkFOSTtDVDAwMDAwMjswMS8wNi8yMDIyOzAxLzA2LzIwMjI7MzAwLjAwOzE2Mi4wMDsxMzguMDA7NTE2ODkuMDA7NjgxOTIuMzA7ODM4NDIuMTA7MTYyLjUwOzAuMDA7MTYyLjUwOzYwOTQ3LjAwOzAuMDA7MTAzMzI4LjYwOzAuMDA7MC4wMDswLjAwOzgzNDEuODU7MC4wMDsxMTI2MzYuNDA7ODU0ODguNTY7OTE3MjYuMzY7MC4wMDsyMTI1MjAuMDA7MTEyNjM2LjQwOzAuMDA7MC4wMDswLjAwOzk3MTgyLjU1Ozk3MTgyLjgwOzE4NTIxLjY5OzQyOTIuOTU7MC4wMDsxODk0Ni42MzsxMzI0LjU0Ow0KO1RvdGFsIGfpbulyYWw7Ozs7OzE1MDcuNTA7NzY2LjUwOzc0MS4wMDsyOTA4MDIuNTA7Mjk1OTc1LjQwOzUwNTY5MS45MDs4NjAuNTA7MC4wMDs4NjAuNTA7Mzc2MTA4LjMwOzAuMDA7NjE4NTg3LjkwOzAuMDA7MC4wMDswLjAwOzQzMjIzLjY1OzQxNi4zMjs2NzE5NzguMzk7NTQ1NjA4LjIzOzUzODk2NS4zMDswLjAwOzEwOTQwNzAuNjg7NjY1NTk1LjU3OzYzODIuODI7MC4wMDs2MzgyLjgyOzUwODQwNS42NTs1MDgzNDYuNDc7NzAyNzQuNzc7MTYyODguMjA7ODg2MS45MjsxNjUwNjkuNjU7MTQxNzAuODk7DQo="
    # cumulMap = utils.CsvToMap(utils.dict_to_csv(utils.base64ToCsv(OR10420),".\\data\\out\\output.csv"))
    # print(list(map(lambda cumul: (cumul["Matricule"],cumul["Date de début de contrat"]), cumulMap)))
    # cumulMapDetails = {}
    # cumulMapDetails["OR104-20"] = OR10420
    # matContratsInfos = {}
    # # contratCree["matricule_salarie"]:{"id":contratCree["id"],"date_debut_contrat":contratCree["date_debut_contrat"]
    # matContratsInfos["00003"] = {"id":"","date_debut_contrat":"", }
    # parser.parseCumuls(cumul_detailsMap=cumulMapDetails,matriculeContratId=matContratsInfos)