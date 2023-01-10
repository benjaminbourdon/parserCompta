import csv
from datetime import datetime
from decimal import *

DATE_RELEVE = datetime.strptime("30/06/2022", '%d/%m/%Y')

class CompteAuxiliaire:

    def __init__(self, extraction):
        ligne = next(extraction)
        self.id, self.nom = ligne['Id pièce'][9:].split(" - ", 2)

        ligne = next(extraction)
        self.soldeInitial = self.soldeStrToDecimal(ligne['Solde (EUR)'])
        self.dateInitiale = datetime.strptime(ligne['Intitulé'][-8:], '%d/%m/%y')

        ligne = next(extraction)
        self.mouvements = ListLignesComptables()
        while ligne['Id pièce'] != "Fin":
            self.mouvements.append(LigneComptable(ligne))
            ligne = next(extraction)

        self.soldeActuel = self.soldeStrToDecimal(ligne['Solde (EUR)'])

    def obtMessage(self):
        style =(f'<style type="text/css"">\n'
                f'.debit {{\n'
                f'  color : red ; }}\n'
                f'.credit {{\n'
                f'  color : green ; }}\n'
                f'</style>\n')
        intro = (
            f"<p style=\"gray\">Remarque : ce message est envoyé depuis une adresse générique, ne pas répondre.</p>\n"
            f"<p>Bonjour {self.nom},</p>\n"
            f"<p>En cette fin de saison, nous revenons vers toi afin de te permettre de régler les sommes que tu dois au club. \n"
            f"Ton solde actuel est de {self.soldeActuel:+.2f}€ au {DATE_RELEVE:%d/%m/%y}.</p>\n"
            f"<p>Afin d'équilibrer tes comptes, nous te demandons d'effectuer un virement de la somme exacte, "
            f"idéalement sous 7 jours.<br/>\n"
            f"Attention, le compte bancaire de l'association à changer. Les nouvelles coordonnées bancaires sont :<br/>\n"
            f"IBAN : FR76 1027 8060 7600 0207 5320 149<br/>\n"
            f"BIC : CMCIFR2A</p>\n"
            f"<p>Tu trouveras ci-dessous le détail de tes dettes et créances de la saison.\n"
            f"Je t'invite à revenir vers nous en cas de question : tresorier@revos.fr</p>\n")

        with open('modele-recap-HTML.html', encoding='utf-8') as modele:
            tableauSynthse = [ligne.format(dateReleve=DATE_RELEVE, **vars(self)) for ligne in modele.readlines()]

        return style + intro + "".join(tableauSynthse)

    @staticmethod
    def soldeStrToDecimal(solde):
        if solde == "0":
            return 0

        montant, typeSolde = solde.split()
        montant = Decimal(montant)
        if typeSolde == "D":
            montant *= -1
        return montant


class ListLignesComptables(list):

    def __format__(self, format_spec):
        return "".join([element.__format__(format_spec) for element in self])


class LigneComptable:

    def __init__(self, ligne):
        self.idPiece = ligne['Id pièce']
        self.date = datetime.strptime(ligne['Date'], '%d/%m/%Y')
        self.intitule = ligne['Intitulé']
        self.personne = ligne['Personne']
        self.nouveau = True

        if ligne['Débit (EUR)'] != '' and ligne['Crédit (EUR)'] == '':
            self.montant = (-1) * Decimal(ligne['Débit (EUR)'].replace(",", "."))
            self.type = "debit"
        elif ligne['Crédit (EUR)'] != '' and ligne['Débit (EUR)'] == '':
            self.montant = Decimal(ligne['Crédit (EUR)'].replace(",", "."))
            self.type = "credit"

        if self.montant > 0 and ("Paiement" in self.intitule or "paiement" in self.intitule):
            self.intitule = "Paiement reçu par le club "
            self.type = "credit paiement"
        elif " - Transaction #" in self.intitule:
            self.intitule = self.intitule.partition(" - Transaction #")[0]
            self.type = "debit transaction"

    def __format__(self, format_spec):
        if format_spec[:4] == "html":
            listeDemande = format_spec[5:].split("|")
            listeEcriture = []
            for demande in listeDemande:
                if ":" in demande:
                    demande, param = demande.split(":")
                    listeEcriture.append(f"<th>{self.__getattribute__(demande):{param}}</th>")
                else:
                    listeEcriture.append(f"<th>{self.__getattribute__(demande)}</th>")
            return f'<tr class="{self.type}">' + "".join(listeEcriture) + "</tr>\n"

        return f"{self.date} | {self.intitule} | {self.montant} \n"


def main():
    with open('export.csv', encoding='utf-8') as f:
        lectureCSV = csv.DictReader(f)

        extraction = []
        for ligne in lectureCSV:
            if ligne['Id pièce'] != '':
                extraction.append(ligne)
            else:
                auxiliaire = CompteAuxiliaire(iter(extraction))
                if auxiliaire.soldeActuel < Decimal(0):
                    message = auxiliaire.obtMessage()
                    print(message)
                extraction = []
                print()



main()
