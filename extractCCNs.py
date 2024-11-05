import pandas as pd

def extractFeuillesNames():
    xl = pd.ExcelFile(r"C:\Users\e2rh0\Victor_E2RH\workspace\open-paye-migration\data\in\fusion.xlsx")
    tradDict = dict()
    tradDict["idcc"] = []
    tradDict["opcc"] = []
    for name in xl.sheet_names:
        opcc = name[:4]
        idcc = name[4:]
        if valid(idcc) and valid(opcc):
            tradDict["idcc"].append(idcc)
            tradDict["opcc"].append(opcc)
        else:
            print(f"not ccn codes : {name}" )
    df = pd.DataFrame(tradDict)
    with pd.ExcelWriter(path=r"C:\Users\e2rh0\Victor_E2RH\workspace\open-paye-migration\data\in\idcc_opcc.xlsx") as writer: 
        print(f"Writing to file : {df}")
        df.to_excel(writer)
    
def valid(ccn:str):
    return ccn.isdigit() and len(ccn) == 4

extractFeuillesNames()

