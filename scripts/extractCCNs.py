import pandas as pd
import sys
import os
# Ajoute le dossier parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logger

def extractFeuillesNames():
    nb = 0
    xl = pd.ExcelFile(r"C:\Users\e2rh0\Victor_E2RH\workspace\open-paye-migration\data\in\fusion.xlsx")
    tradDict = dict()
    tradDict["idcc"] = []
    tradDict["opcc"] = []
    for name in xl.sheet_names:
        size = len(name)
        if size != 8:
            logger.log(f"{name}")
        normName = name.replace(" ","").replace("a","").zfill(8)
        size = len(normName)
        if size != 8:
            logger.log(f"{name}")
        cut = int(size/2)
        opcc = normName[:cut]
        idcc = normName[cut:]
        if valid(idcc) and valid(opcc):
            nb = -~nb 
            tradDict["idcc"].append(idcc)
            tradDict["opcc"].append(opcc)
        else:
            logger.log(f"not ccn codes : {name}" )
        logger.log(f"{nb} valid ccn pairs extracted")
    df = pd.DataFrame(tradDict)
    with pd.ExcelWriter(path=r"C:\Users\e2rh0\Victor_E2RH\workspace\open-paye-migration\data\in\idcc_opcc.xlsx") as writer: 
        #logger.print(f"Writing to file : {df}")
        df.to_excel(writer)
    
def valid(ccn:str):
    return ccn.isdigit() and len(ccn) == 4

extractFeuillesNames()

