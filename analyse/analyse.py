import csv
import json

class Analyse:

    # open plan comptable
    f = open('../reference/plan_comptable_m14_2016.json', 'r')
    plan_m14 = json.loads(f.read())

    def _analyse(self, file):
        comptes = {
            '10': 0,
            '11': 0,
            '12': 0,
            '13': 0,
            '15': 0,
            '16': 0,
            '18': 0,
            '19': 0,
        }

        for row in file:
            if row['NCompte'] in self.plan_m14:
                if row['NCompte'][0:2] in comptes:
                    comptes[row['NCompte'][0:2]] = float(comptes[row['NCompte'][0:2]]) + float(row['SoldeD'].replace(',', '.'))
                    comptes[row['NCompte'][0:2]] = float(comptes[row['NCompte'][0:2]]) + float(row['SoldeC'].replace(',', '.'))
            if False:
                print self.plan_m14[row['NCompte']] + ': ' + row['SoldeD'] + ' - ' + row['SoldeC']

        for key in comptes:
            print '('+key+') '+ self.plan_m14[key] + ': ' + str(comptes[key])

# Open a cvs
with open('../data/commune.csv', 'r') as csvfile:
    headers = ['ExerciceG', 'SIRET', 'Departement', 'LibBudget', 'INSEE', 'CRegion', 'TypeBudget', 'nomCompta', 'FINESS', 'SIREN', 'TypeEtab', 'STypeEtab', 'BalanceDef', 'NCompte', 'BEntreeD', 'BEntreeC', 'OBDNA', 'OBCNA', 'ONBD', 'ONBC', 'OOBD', 'OOBC', 'SoldeD', 'SoldeC']
    spamreader = csv.DictReader(csvfile, headers, delimiter=';')

    analyse = Analyse()
    analyse._analyse(spamreader)



