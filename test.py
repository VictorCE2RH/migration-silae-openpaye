import extract
import utils
import silae
import logger
import parser
import statut_pro as sp


def testEmploiCCN(sCode, statutCode, opcc, empCode, statut=sp.PAS_STATUT):
    print(f"Résultat emploiCCN {sCode} {statutCode} = {opcc} {empCode} {statut} {logger.SuccessStatement(
        "OK") if extract.emploiCCN(sCode, statutCode, opcc) == [opcc, empCode, statut] else logger.ErrorStatement("KO")}")


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

    testEmploiCCN(sCode="A018.02.008", statutCode="02",
                  opcc=1880, empCode=130, statut=sp.EMPLOYE)
    testEmploiCCN(sCode="A018.06.004", statutCode="29",
                  opcc=1880, empCode=700, statut=sp.CADRE)
    testEmploiCCN(sCode="A018.06.005", statutCode="04",
                  opcc=1880, empCode=710, statut=sp.AGENT_MAITRISE)
    testEmploiCCN(sCode="A018.06.005", statutCode="29",
                  opcc=1880, empCode=720, statut=sp.CADRE)
    testEmploiCCN(sCode="A018.09.002", statutCode="12",
                  opcc=1880, empCode=900, statut=sp.CADRE_SUP)
    testEmploiCCN(sCode="A018.09.002", statutCode="13",
                  opcc=1880, empCode=910, statut=sp.CADRE_DIRIGEANT)
    testEmploiCCN(sCode="unknown", statutCode="unknown",
                  opcc=1880, empCode=9999)

    testEmploiCCN(sCode="E161.01.029", statutCode="01",
                  opcc=7023, empCode=570, statut=sp.OUVRIER)
    testEmploiCCN(sCode="E161.01.029", statutCode="02",
                  opcc=7023, empCode=580, statut=sp.EMPLOYE)

    testEmploiCCN(sCode="A023.07",     statutCode="", opcc=9578, empCode=9999)
    testEmploiCCN(sCode="A032.03.005", statutCode="02",
                  opcc=2571, empCode=400, statut=sp.EMPLOYE)
    testEmploiCCN(sCode="A032.03.005", statutCode="03",
                  opcc=2571, empCode=410, statut=sp.TECHNICIEN)
    testEmploiCCN(sCode="A032.03.005", statutCode="04",
                  opcc=2571, empCode=420, statut=sp.AGENT_MAITRISE)
    testEmploiCCN(sCode="A032.04.001", statutCode="02",
                  opcc=2571, empCode=430, statut=sp.EMPLOYE)
    testEmploiCCN(sCode="A032.04.001", statutCode="03",
                  opcc=2571, empCode=440, statut=sp.TECHNICIEN)
    testEmploiCCN(sCode="A032.05.004", statutCode="02",
                  opcc=2571, empCode=580, statut=sp.EMPLOYE)
    testEmploiCCN(sCode="A032.06.003", statutCode="29",
                  opcc=2571, empCode=610, statut=sp.CADRE)

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
    # cumulMap = utils.CsvToMap(utils.dict_to_csv(utils.base64ToCsv(OR10420),".\\data\\out\\output.csv"))
    codeDict = {"OR104-20": 1}
    contratsCrees = [{
        "matricule_salarie":"00007",
        "date_debut_contrat": "01/01/2024",
        "id": 1
    },
    {
        "matricule_salarie":"00009",
        "date_debut_contrat": "01/01/2024",
        "id": 2
    },
    {
        "matricule_salarie":"00004",
        "date_debut_contrat": "01/01/2024",
        "id": 3
    },
    {
        "matricule_salarie":"00003",
        "date_debut_contrat": "01/01/2024",
        "id": 4
    },
    {
        "matricule_salarie":"00008",
        "date_debut_contrat": "01/01/2024",
        "id": 5
    }]
    matriculeContratId = dict(list(map(lambda contratCree: (contratCree["matricule_salarie"], {
        "id": contratCree["id"], "date_debut_contrat": contratCree["date_debut_contrat"]}), contratsCrees)))
    cumul_detailsMap = silae.getCumulsContrats("E2RH", codeDict)
    op_cumuls, op_contratsIdToDSN = parser.parseCumuls(
        cumul_detailsMap, matriculeContratId)

    logger.printStat(list(map(lambda cumul: cumul["DateReprise"], op_cumuls)))
    # cumulMapDetails = {}
    # cumulMapDetails["OR104-20"] = OR10420
    # matContratsInfos = {}
    # # contratCree["matricule_salarie"]:{"id":contratCree["id"],"date_debut_contrat":contratCree["date_debut_contrat"]
    # matContratsInfos["00003"] = {"id":"","date_debut_contrat":"", }
    # parser.parseCumuls(cumul_detailsMap=cumulMapDetails,matriculeContratId=matContratsInfos)
