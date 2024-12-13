import pandas as pd
import numpy as np
from typing import Optional, Tuple

import sys
import os
import json
# Ajoute le dossier parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logger
import silae
import utils

import argparse

def setup_argparser():
    parser = argparse.ArgumentParser(description='Compare deux fichiers Excel')
    parser.add_argument('domain', help='domain sur lequel récupérer les informations')
    parser.add_argument('numeros',nargs='+', help='Numeros dossiers à analyser')
    return parser

def collectCCNS(domain:str, numeros:list[str]) -> dict[str,dict]:
    headers = silae.getDomainHeader(domain)
    collectionCCN = silae.getCcnForNums(numeros, headers=headers)    
    print(collectionCCN)
    
    return collectionCCN


def transformdict(items:dict):
    transformed = {"numero":list(),"ccn":list(),"idcc":list()}
    for numero, data in items.items():
        transformed["numero"].append(numero)
        transformed["ccn"].append(data["ccnSociete"][0]["codeCCN"])
        transformed["idcc"].append(data["ccnSociete"][0]["idcc"])
    return transformed
    

if __name__ == "__main__":
    parser = setup_argparser()
    args = parser.parse_args()
    domain = args.domain
    numeros = args.numeros
    print(domain)
    print(numeros)
    # Configuration des chemins de fichiers
    fichier_sortie = r".\data\out"
    fichier_sortie = f"{fichier_sortie}\\export_ccn_{args.domain}.csv"

    items = collectCCNS(args.domain, args.numeros)
    items = transformdict(items)
    print(items)
    utils.dictToCSVFile(items, fichier_sortie)