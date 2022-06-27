# -*- coding: utf-8 -*-

from random import random
# from abc import ABC, abstractmethod
#
#
# class Element(ABC):
#     def une_methode(self):
#         pass
#
#
# Importance de déclarer la classe comme abstraite ... Necessaire ?


class Element:
    def __init__(self, nom, genre):
        self.nom = nom
        self.identifiant = "ID_"+ str(int(100000 * random()))
        self.genre = genre


class Milieu(Element):
    def __init__(self, nom, genre, volume, hauteur, x, y, cheminee):
        self.volume = volume
        self.hauteur = hauteur
        self.x = x
        self.y = y
        self.cheminee = cheminee
        Element.__init__(self, nom, genre)


class Compartiment(Milieu):
    def __init__(self, nom, volume, hauteur, x, y, cheminee):
        Milieu.__init__(self, nom, 'compartiment', volume, hauteur, x, y, cheminee)


class Jonction(Milieu):
    def __init__(self, nom, x, y, cheminee):
        Milieu.__init__(self, nom, 'jonction', 1, 0, x, y, cheminee)


class Filtre(Milieu):
    def __init__(self, nom, x, y):  # nom doit valoir "THE" ou "PaI"
        Milieu.__init__(self, nom, 'compartiment', 1, 0, x, y, False)


class Transfert(Element):
    def __init__(self, nom, genre, origine, arrivee, delta):
        self.origine = origine
        self.arrivee = arrivee
        self.delta = delta  # avoir une meilleure compréhension de delta dans le code
        Element.__init__(self, nom, genre)


class Fractionnement(Transfert):
    def __init__(self, nom, origine, arrivee, delta):
        Transfert.__init__(self, nom, 'fractionnement', origine, arrivee, delta)


class Renouvellement(Transfert):
    def __init__(self, nom, origine, arrivee, delta):
        Transfert.__init__(self, nom, 'renouvellement', origine, arrivee, delta)


class Multiplicateur(Transfert):
    def __init__(self, nom, origine, arrivee, delta, source_continue, cheminee):
        self.source_continue = source_continue
        self.cheminee = cheminee
        Transfert.__init__(self, nom, 'multiplicateur', origine, arrivee, delta)


if __name__ == "__main__":
    A = Compartiment('mon_compartiment', 1, 1, 1, 1, False)
    print("A.genre = ", A.genre)
    print("A.identifiant = ", A.identifiant)
    B = Jonction('ma_jonction', 1, 1, False)
    C = Filtre('mon_filtre', 1, 1)
    D = Fractionnement('mon_fractionnement', 'ID_51', 'ID_52', 0)
    E = Renouvellement('mon_renouvellement', 'ID_53', 'ID_54', 0)
    F = Multiplicateur('mon_multiplicateur', 'ID_55', 'ID_56', -1, False, False)
