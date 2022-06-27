# -*- coding: utf-8 -*-

import conversions
from numpy import log, log10, exp
#from gestion_fichiers_cas_calculs import FichierEra

class Instant:
    """Classe relative à un instant de calcul et aux méthodes de gestion de temps"""
    def __init__(self, id_instant ="T0", auto = False):
        self.value = str() # valeur
        self.unit = int() # choix parmi (0->s , 1->mn, 2->h, 3->j, 4->an)
        self.auto = auto

        if isinstance(id_instant, Instant):
            self.unit = id_instant.unit
            self.value = id_instant.value
            self.auto = id_instant.auto
            return

        if isinstance(id_instant, str):
            if id_instant == "T0": return
            else:
                id_instant = id_instant.split()

                if id_instant[-1] in ["manu", "auto"]:
                    if id_instant[-1] == "manu": self.auto = False
                    else: self.auto = True

                id_instant.pop()  # supprime dernier element
                # gere si il y a un espace ou pas
                if len(id_instant) == 1:
                    if id_instant[0][-1] == "n":  # minutes ou annees
                        id_instant.append(id_instant[0][-2:])
                        id_instant[0] = id_instant[0][:-2]
                    else:
                        id_instant.append(id_instant[0][-1:])
                        id_instant[0] = id_instant[0][:-1]
                # calcul de temps en secondes, et de l'unite associee
                self.set_unit(id_instant[1])
                self.set_value_secondes(float(id_instant[0]))

                # si besoin deboguer
                #print("dans __init__, self.unit = ", self.unit)
                #print("dans __init__, self.value = ", self.value)

    def __eq__(self, other):
        if self.value == other.value:
            return True
        else:
            return False

    def set_value_secondes(self,value_to_set):
        """Convertit valeur en secondes"""
        self.value = conversions.convertit_temps(value_to_set, self.unite(), 's')

    def set_unit(self, unit_to_set):
        """Fixe la valeur de l'attribut u en fonction de la valeur de unite"""
        if (unit_to_set == "s") : self.unit = 0;
        elif (unit_to_set == "m") : self.unit = 1; # 'm' peut aussi indiquer des minutes
        elif (unit_to_set == "mn") : self.unit = 1;
        elif (unit_to_set == "h"): self.unit = 2;
        elif (unit_to_set == "j"): self.unit = 3;
        elif (unit_to_set == "an"): self.unit = 4;

    def unite(self):
        """Renvoie chaine de caractere correpondante a l'unite, en fonction de la valeur de u"""
        if (self.unit == 0): return "s";
        elif (self.unit == 1) : return "mn";
        elif (self.unit == 2) : return "h";
        elif (self.unit == 3) : return "j";
        elif (self.unit == 4) : return "an"

    def valeur(self):
        """Renvoie ligne qui correspond self.value apres une conversion """
        ligne = 0.0
        ligne = conversions.convertit_temps(self.value, 's', self.unite())
        return ligne

    def meilleure_unite_temps(self, temps):
        """ recherche l'unite de temps optimale"""
        if (temps < 60.0):
            return 0;  # secondes
        elif (temps < 3600.0):
            return 1;  # minutes
        elif (temps < 86400.0):
            return 2;  # heures
        elif (temps < 86400.0 * 365):
            return 3;  # jours
        else:
            return 4;  # ans

    def auto_str(self):
        """Renvoie 'auto' ou 'manu' suivant booleen auto"""
        if self.auto: return 'auto'
        else: return 'manu'

    def str_instant(self):
        """Concatene les attributs d'un instant dans une chaine de caracteres."""
        return str(conversions.scientific_notation(self.valeur())) + self.unite() + " " + self.auto_str()

    def __str__(self):
        return self.str_instant()

class ListeInstant :
    """Classe representant une liste d instant"""
    def __init__(self):
        self.vide()

    def vide(self):
        """declare attribut data comme une liste vide"""
        self.data=[]

    def __len__(self):
        return len(self.data)

    def __str__(self):
        str_data = str()
        for i in range(len(self)):
            str_data += "\t" + str(self.data[i]) + "\n"
        return str_data

    def set_value_instant(self, index, value_to_set):
        """Fixe une valeur en secondes a un temps i de la liste (sans changer l'unite) et fixe booleen auto a False"""
        self.data[index].set_value_secondes(value_to_set)
        self.data[index].auto = False

    def get_value_instant(self, index):
        """Renvoie la valeur d'un temps i apres conversion"""
        return self.data[index].valeur()

    def set_unit_instant(self, i, unite):
        """Fixe self.unit selon l'unite desiree"""
        self.data[i].set_unit(unite)

    def ajoute_instant(self, instant_or_str, force=True):
        if isinstance(instant_or_str, str):
            instant_or_str = Instant(instant_or_str)
        if isinstance(instant_or_str, Instant):
            if force or not (instant_or_str in self.data or instant_or_str.value < 1e-45):
                self.data.append(Instant(instant_or_str))

    def liste(self):
        """Retourne une liste de caracteres contenant tout les temps dans data """
        str_listeinstant = str()
        for instant in self.data:
            str_listeinstant += "\t" + instant.str_instant() + "\n"
        return str_listeinstant

    def elimine(self):
        """Supprime les temps de la liste qui apparaissent plus d'une fois"""
        for temps in self.data:
            while self.data.count(temps) > 1:
                self.data.remove(temps)

    def supprime_instant(self, i):
        """Supprime un element i de la liste data"""
        self.data.pop(i)

    def modifie_instant(self, i, instant_or_str):
        """Modifie un instant de la liste"""
        old_instant = self.data[i]
        new_instant = Instant(instant_or_str)
        # si les valeurs sont differentes -> modification
        if old_instant.value != new_instant.value:
            self.data.pop(i)
            self.data.insert(i, new_instant)

    def supprime_instant_liste(self, liste):
        # liste triee par ordre croissant puis inversion, pourquoi supprimer element dont valeur inferieur longueur liste...
        liste.sort()
        liste.reverse()  # tri par ordre inverse pour pouvoir poper sans risque
        for i in liste:
            if i < len(self.data):
                self.supprime_instant(i)

    def trie(self):
        """trie la liste data par odre croissant..."""
        self.data.sort()

    def ajoute_auto(self, t_ini, t_fin, npas, mode):
        """ajoute a la liste N instants de Tini a Tfin suivant mode :
        0->lineaire  1->logarithmique  2->exponentielle
        """
        if (npas == 0): return
        else :
            instant_tmp = Instant(t_ini, auto=True)
            self.ajoute_instant(instant_tmp, False)
            t_ini_s = instant_tmp.value

            instant_tmp = Instant(t_fin, auto=True)
            t_fin_s = instant_tmp.value
            instant_tmp.auto = True

            if mode == 0:
                for i in range(1, npas):
                    instant_tmp.value = t_ini_s + i * (t_fin_s - t_ini_s) / npas
                    instant_tmp.unit = self.meilleure_unite_temps(instant_tmp.value)
                    self.ajoute_instant(instant_tmp, False)


            elif mode == 1:
                for i in range(1, npas):
                    instant_tmp.value = t_ini_s + (t_fin_s - t_ini_s) * log10(1 + 9.0 * i / npas)
                    instant_tmp.unit = self.meilleure_unite_temps(instant_tmp.value)
                    self.ajoute_instant(instant_tmp, False)

            elif mode == 2:
                alpha = 0.05;
                coeff = (t_fin_s - t_ini_s) / (exp(alpha * npas) - 1)
                for i in range(1, npas):
                    instant_tmp.value = t_ini_s + coeff * (exp(alpha * i) - 1)
                    instant_tmp.unit = self.meilleure_unite_temps(instant_tmp.value)
                    self.ajoute_instant(instant_tmp, False)

            instant_tmp = Instant(t_fin, auto=True)
            instant_tmp.unit = self.meilleure_unite_temps(instant_tmp.value)
            self.ajoute_instant(instant_tmp, False)

    def meilleure_unite_temps(self, temps):
        """ recherche l'unite de temps optimale"""
        if (temps < 60.0): return 0;  # secondes
        elif (temps < 3600.0): return 1;  # minutes
        elif (temps < 86400.0): return 2;  # heures
        elif (temps < 86400.0 * 365): return 3;  # jours
        else: return 4;  # ans

    def supprime_instants_auto(self):
        """Supprime tout les elements de la liste dont le temps a ete defini comme automatique"""
        i = 0
        while i < len(self.data):
            if self.data[i].auto:
                self.data.pop(i)
            else:
                i += 1

    def renvoie_liste_instant(self):
        """ Renvoie fonction liste; legitimite fonction ?"""
        return self.liste()

    def ajoute_instants_fichier(self, fichier):
        #print("appel ajoute_instants_fichier")
        tete = next(fichier)
        while tete.find("</Temps>") == -1:
            self.ajoute_instant(tete.strip())
            tete = next(fichier)

def periode_demi_vie(taux_desintegration):
    """Renvoie chaine de caractière contenant valeur demi_vie formatée avec unité adaptée"""
    if taux_desintegration == -1:
        return "Stable"
    else :
        value_demi_vie_s = log(2) / taux_desintegration
        demi_vie = Instant(str(value_demi_vie_s) + "s auto")
        demi_vie.unit = demi_vie.meilleure_unite_temps(demi_vie.value)
        conversions.NUMBER_OF_DIGITS = 4
        format_demi_vie_valeur = conversions.scientific_notation(demi_vie.valeur())

        return str(format_demi_vie_valeur) + demi_vie.unite()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    un_temps = Instant()
    un_temps.unit = 0
    un_temps.value = 58
    # print('un_temps = ', un_temps.value, un_temps.unit)

    un_temps.set_value_secondes(49)
    un_temps.set_unit('mn')
    # print('un_temps = ', un_temps.value, un_temps.unit)

    # print(un_temps.str_instant())
    # print(un_temps)

    liste_instant = ListeInstant()
    # print(len(liste_instant))
    str_deux_instant = "5.0mn auto"
    liste_instant.ajoute_instant(str_deux_instant)
    # print(len(liste_instant))
    print("result = ", str(liste_instant).find(str_deux_instant))

    # print(type(liste_instant.data[0]))
    # print(liste_instant.data[0].value)
    # print(liste_instant.data[0].unit)
    # print(liste_instant.data[0])

    liste_instant.ajoute_instant(str_deux_instant)
    # print(len(liste_instant))

    # for i in range(len(liste_instant)):
    #     print(liste_instant.data[i])

    # str_quatre_instant = "60s auto"
    # str_cinq_instant = "0.0h auto"
    str_quatre_instant = "0s auto"
    str_cinq_instant = "200s auto"
    liste_instant_2 = ListeInstant()
    # print("len(liste_instant_2) = ", len(liste_instant_2))
    liste_instant_2.ajoute_auto(str_quatre_instant, str_cinq_instant, 20, 0)
    # print("len(liste_instant_2) = ", len(liste_instant_2))
    # liste_instant_2.ajoute_instant('15s manu')

    print("len(liste_instant_2) = ", len(liste_instant_2))

    # for i in range(len(liste_instant_2)):
    #     print("data liste_instant_2", liste_instant_2.data[i])
    #     print("type(liste_instant_2.data[i]) = ", type(liste_instant_2.data[i]))
    # print("fin data")

    print("liste_instant_2", liste_instant_2)
    print("fin print liste_instant 1")
    liste_instant_2.modifie_instant(2, "30s manu")

    print("liste_instant_2", liste_instant_2)
    print("fin print liste_instant 1")

    liste_instant_2.supprime_instants_auto()
    # print("len(liste_instant_2) = ", len(liste_instant_2))

    # for i in range(len(liste_instant_2)):
    #     print("data liste_instant_2", liste_instant_2.data[i])

    deux_instant = Instant(str_deux_instant)
    trois_instant = Instant(deux_instant)

    print(periode_demi_vie(0.0057474890547))


    # mon_nombre = 123453
    # mon_nombre = 17.78603
    # print("scientific_notation of ", mon_nombre, " is : ", conversions.scientific_notation(mon_nombre))
