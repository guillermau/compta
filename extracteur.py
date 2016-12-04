import csv
import json
import couchdb

couch = couchdb.Server('http://localhost:5985/')
db = couch['open_data']

def save(count, array):
    print "Importation de " + count["LibBudget"] + "(" + count["SIRET"] + ") ..."
    count['comptes'] = array
    db.save(count)
    print "Importation de " + count["LibBudget"] + "(" + count["SIRET"] + ") Terminee"

def parse_count(row):
    return {
        "ExerciceG": row['ExerciceG'],
        "SIRET": row['SIRET'],
        "Departement": row['Departement'],
        "LibBudget": row['LibBudget'].decode('utf8', 'replace'),
        "INSEE": row['INSEE'],
        "CRegion": row['CRegion'],
        "TypeBudget": row['TypeBudget'],
        "nomCompta": row['nomCompta'],
        "FINESS": row['FINESS'],
        "SIREN": row['SIREN'],
        "TypeEtab": row['TypeEtab'],
        "STypeEtab": row['STypeEtab'],
    }


def parse_row(row):
    return {
        "BalanceDef": row['BalanceDef'],
        "NCompte": row['NCompte'],
        "BEntreeD": row['BEntreeD'],
        "BEntreeC": row['BEntreeC'],
        "OBDNA": row['OBDNA'],
        "OBCNA": row['OBCNA'],
        "ONBD": row['ONBD'],
        "ONBC": row['ONBC'],
        "OOBD": row['OOBD'],
        "OOBC": row['OOBC'],
        "SoldeD": row['SoldeD'],
        "SoldeC": row['SoldeC']
    }

with open('/home/guigui/Documents/OpenSource/Commune/Balance_Commune_2013.csv', 'r') as csvfile:
    headers = ['ExerciceG', 'SIRET', 'Departement', 'LibBudget', 'INSEE', 'CRegion', 'TypeBudget', 'nomCompta', 'FINESS', 'SIREN', 'TypeEtab', 'STypeEtab', 'BalanceDef', 'NCompte', 'BEntreeD', 'BEntreeC', 'OBDNA', 'OBCNA', 'ONBD', 'ONBC', 'OOBD', 'OOBC', 'SoldeD', 'SoldeC']
    spamreader = csv.DictReader(csvfile, headers, delimiter=';')

    lastSIRET = ''
    lastCount = {}
    lastArray = []

    for row in spamreader:
        if row['SIRET'] != lastSIRET:
            if lastCount is not None and len(lastArray) > 0:
                save(lastCount, lastArray)
                lastArray = []
            lastSIRET = row['SIRET']
            lastCount = parse_count(row)
            lastArray.append(parse_row(row))
        else:
            lastArray.append(parse_row(row))
