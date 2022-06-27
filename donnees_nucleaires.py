# -*- coding: utf-8 -*-

import os
import sqlite3
# import utils

DATABASE_NAME = "Jeff.db"


class DonneesNucleaires:
    def __init__(self):
        self.cursor = self.init_cursor()

    def init_cursor(self):
        """retourne Connection.cursor avec la base de donnees "Jeff.db" """
        # bdd = os.path.join(utils.appDirPath(), 'data', DATABASE_NAME)
        bdd = DATABASE_NAME
        sqliteConnection = sqlite3.connect(bdd)
        # Creating cursor object using connection
        cursor = sqliteConnection.cursor()
        return cursor

    def list_fields_from_table(self, fields, table):
        """Retourne liste de champs issus d'une table"""
        self.cursor.execute("SELECT " + fields + " FROM " + table)
        list_fields = self.cursor.fetchall()
        # Transforme une liste de tuples d'objets en liste d'objet(tuple[0])
        list_fields = [ field[0] for field in list_fields ]
        return list_fields

    def list_isotopes_from_z(self, z):
        """Retourne la liste de tous les istopes trouvés à l'aide de la table RNs de Jeff.db"""
        print("z recherchee vaut : ", z)
        self.cursor.execute("SELECT symbole FROM RNs where Z=" + str(z))
        list_isotopes = self.cursor.fetchall()
        # Transforme une liste de tuples d'objets en liste d'objet(tuple[0])
        list_isotopes = [ isotopes[0] for isotopes in list_isotopes ]
        return list_isotopes

    def get_z_from_elements(self, element):
        """Renvoie la valeur de Z à partir du symbole chimique de l'élement"""
        # Probleme de symbole pour le Lawrencium dans Jeff.db
        if element == "Lr":
            element = "Lw"

        self.cursor.execute("SELECT Z FROM elements where symbole='" + element + "'")
        z = self.cursor.fetchall()
        # try:
        #     z = z[0][0]
        # except:
        #     pass
        z = z[0][0]
        return z

    def get_z_a_lambda_from_rns(self, isotope):
        """Renvoie un tuple (Z, A, T1/2) à partir du nom du RN, dans la table RNs de Jeff.db"""
        self.cursor.execute("SELECT Z, A, Lambda  FROM RNs where symbole='" + isotope + "'")
        z_a_lambda = self.cursor.fetchall()
        z_a_lambda = z_a_lambda[0]

        return z_a_lambda

    def get_mode_fils_proba_nrj_from_desintegrations(self, isotope):
        """Renvoie un tuple (mode, fils, proba, nrj) à partir du nom du père, dans la table RNs de Jeff.db"""
        self.cursor.execute("SELECT Mode, Fils, proba, Energie FROM desintegrations where Pere='" + isotope + "'")
        mode_fils_proba_nrj = self.cursor.fetchall()
        print("mode_fils_proba_nrj = ", mode_fils_proba_nrj)

        return mode_fils_proba_nrj

    def str_mode(self, mode):
        """retourne le mode de désintégration en fonction de la valeur de mode"""
        dict_mode = {
            1 : 'Beta -',
            2 : 'Beta +',
            3 : 'TI', # Transition Isomérique
            4 : 'Alpha',
            5 : 'Neutron',
            6 : 'SF', # Fission Spontanée
            7 : 'Proton'
        }
        return dict_mode[mode]

    def get_str_element_from_str_radionucleides(self, saisie):
        """
        A partir d'une saisie clavier, recherche les RNs correspondants,
        retourne liste d'elements et de RNs associées
        """
        # Vérifie que le symbole du radionucléide existe...
        list_radionucleides = self.list_fields_from_table("symbole", "RNs")
        radionucleides_match = [radionucleide for radionucleide in list_radionucleides if saisie in radionucleide]
        elements_match = []

        # S'ils existent, retourne les symboles des éléments associés
        if radionucleides_match:
            print("Au moins une correspondance de RN a été trouvée")
            for radionucleide in radionucleides_match:
                # Prise en compte de quelques radionucleides avec des suffixes particuliers
                if radionucleide[-4:] == 'aero':
                    radionucleide = radionucleide[:-4]
                elif radionucleide[-6:] == 'elevap':
                    radionucleide = radionucleide[:-6]
                elif radionucleide[-3:] in ('org', 'CH4', 'CO2'):
                    radionucleide = radionucleide[:-3]
                elif radionucleide[-2:] == ('TO'):
                     radionucleide = radionucleide[:-2]

                # L'ordre des 'if' est important car e.g. 'Maero' possible
                if radionucleide[-1] in ('M', 'N', 'T', 'O'):
                    radionucleide = radionucleide[:-1]

                # Suppression des chiffres
                symbole_element = ''.join([i for i in radionucleide if not i.isdigit()])

                if symbole_element not in elements_match:
                    elements_match.append(symbole_element)

            return elements_match, radionucleides_match
        else:
            print("Aucune correspondance de RN trouvé")
            return None, None


class TableFlux:
    def __init__(self):
        self.data = dict()
        self.cle1 = 'Rapide'
        self.cle2 = 'Thermique'
        self.data[self.cle1] = [0.0]
        self.data[self.cle2] = [0.0]
        self.unite_flux = "n/cm²/s"
        self.cles = self.data.keys() # cleTriees -> keys ne donnent pas les cles triees
        self.temps=['T0']
        self.colT0=0
        self.sommes=[0.0]
        self.isfiltre=False
        # self.setConfigAdv(copy.deepcopy(self.ws.ini.configFiltreDef))#preinitialisation du filtre au comportement par defaut


    def setConfigAdv(self, cfgAdv):
        self.adv=cfgAdv
        self.majConfigAdv()


    def getConfigAdv(self):
        return self.adv


    def majConfigAdv(self):
        if self.isfiltre:
            self.advRedef=[]
            for ki in self.adv:
                if ki in ['PaI','THE']:
                    #self.data[ki]=[1.0]*len(self.temps)
                    for mat in self.adv[ki]:
                        if not self.adv[ki][mat][1]:
                            self.advRedef.append(mat)
                            if mat not in self.data:
                                self.data[mat]=[1.0]*len(self.temps)
            self.cleTriees=[self.cle1, self.cle2]+self.advRedef


if __name__ == "__main__":
    dnuc = DonneesNucleaires()
    list_symbole = dnuc.list_fields_from_table("symbole", "Elements")
    print("list_symbole = ", list_symbole, "\n")

    list_radionucleides = dnuc.list_fields_from_table("symbole", "RNs")
    print("list_radionucleides =", list_radionucleides, "\n")

    list_isotopes = dnuc.list_isotopes_from_z(2)
    print("list_isotopes = ", list_isotopes)

    print("test Z = ", dnuc.get_z_from_elements("Fe"))

    print("get_mode_fils_proba_nrj_from_desintegrations(\"C14\") = ", dnuc.get_mode_fils_proba_nrj_from_desintegrations("C14"))
    tuple_isotopes = dnuc.get_mode_fils_proba_nrj_from_desintegrations("Ca38")

    print("tuple_isotopes = ", tuple_isotopes)
    for isotope in tuple_isotopes:
        print("isotope = ", isotope)
        print("isotope[0] = ", isotope[0])

    print(dnuc.str_mode(4))

    list_elem, list_rns = dnuc.get_str_element_from_str_radionucleides("Ca3")
    print("list_elem = ", list_elem)
    print("list_rns = ", list_rns)

    list_elem, list_rns = dnuc.get_str_element_from_str_radionucleides("Ca380")
    print("list_elem = ", list_elem)
    print("list_rns = ", list_rns)

    list_elem, list_rns = dnuc.get_str_element_from_str_radionucleides("Eu152N")
    print("list_elem = ", list_elem)
    print("list_rns = ", list_rns)

    list_elem, list_rns = dnuc.get_str_element_from_str_radionucleides("HT")
    print("list_elem = ", list_elem)
    print("list_rns = ", list_rns)

    list_elem, list_rns = dnuc.get_str_element_from_str_radionucleides("HTO")
    print("list_elem = ", list_elem)
    print("list_rns = ", list_rns)

    list_elem, list_rns = dnuc.get_str_element_from_str_radionucleides("I132Maero")
    print("list_elem = ", list_elem)
    print("list_rns = ", list_rns)

    list_elem, list_rns = dnuc.get_str_element_from_str_radionucleides("Lr262")
    print("list_elem = ", list_elem)
    print("list_rns = ", list_rns)