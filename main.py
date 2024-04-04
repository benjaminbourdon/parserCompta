import csv
from datetime import datetime
from decimal import Decimal

DATE_RELEVE = datetime.strptime("18/01/2023", "%d/%m/%Y")


class CompteAuxiliaire:
    def __init__(self, extraction):
        ligne = next(extraction)
        self.id, self.nom = ligne["Id pièce"][9:].split(" - ", 2)

        ligne = next(extraction)
        self.soldeInitial = self.soldeStrToDecimal(ligne["Solde (EUR)"])
        self.dateInitiale = datetime.strptime(str(ligne["Intitulé"][-10:]), "%d/%m/%Y")

        ligne = next(extraction)
        self.mouvements = ListLignesComptables()
        while ligne["Id pièce"] != "Fin":
            self.mouvements.append(LigneComptable(ligne))
            ligne = next(extraction)

        self.soldeActuel = self.soldeStrToDecimal(ligne["Solde (EUR)"])

    def exportMessageDette(self, dateRelevé=datetime.now):

        cheminSortie = f"Sorties/message-{self.id}-{self.nom}.html"

        with open("modele-dette.html", "r", encoding="utf-8") as modele, open(
            cheminSortie, "w", encoding="utf-8"
        ) as sortie:
            for ligne in modele:
                ligneFormatée = ligne.format(dateRelevé=dateRelevé, **vars(self))
                sortie.write(ligneFormatée)

            return True
        return False

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
        self.idPiece = ligne["Id pièce"]
        self.date = datetime.strptime(ligne["Date"], "%d/%m/%Y")
        self.intitule = ligne["Intitulé"]
        self.personne = ligne["Personne"]
        self.nouveau = True

        if ligne["Débit (EUR)"] != "" and ligne["Crédit (EUR)"] == "":
            self.montant = (-1) * Decimal(ligne["Débit (EUR)"].replace(",", "."))
            self.type = "debit"
        elif ligne["Crédit (EUR)"] != "" and ligne["Débit (EUR)"] == "":
            self.montant = Decimal(ligne["Crédit (EUR)"].replace(",", "."))
            self.type = "credit"

        if self.montant > 0 and (
            "Paiement" in self.intitule or "paiement" in self.intitule
        ):
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
                    listeEcriture.append(
                        f"<th>{self.__getattribute__(demande):{param}}</th>"
                    )
                else:
                    listeEcriture.append(f"<th>{self.__getattribute__(demande)}</th>")
            return f'<tr class="{self.type}">' + "".join(listeEcriture) + "</tr>\n"

        return f"{self.date} | {self.intitule} | {self.montant} \n"


def main():
    with open("export.csv", encoding="utf-8") as f:
        lectureCSV = csv.DictReader(f)

        extraction = []
        for ligne in lectureCSV:
            if ligne["Id pièce"] != "":
                extraction.append(ligne)
            else:
                auxiliaire = CompteAuxiliaire(iter(extraction))
                if auxiliaire.soldeActuel < Decimal(0):
                    auxiliaire.exportMessageDette(dateRelevé=DATE_RELEVE)
                extraction = []


main()
