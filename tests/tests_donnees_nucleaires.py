# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
import donnees_nucleaires
import unittest


class TestTables(unittest.TestCase):

    def setUp(self):
        """ Prépare des données avant de lancer les tests """
        self.dn = donnees_nucleaires.DonneesNucleaires()

    def tearDown(self):
        """ Nettoyer/changer des données après chaque test """
        pass

    def test_list_radionucleides(self):
        list_radionucleides = self.dn.list_fields_from_table("symbole", "RNs")
        # print(list_radionucleides)
        self.assertEqual(list_radionucleides[0], "H1")

    def test_list_symbole(self):
        list_symbole = self.dn.list_fields_from_table("symbole", "Elements")
        # print("list_symbole = ", list_symbole, "\n")
        self.assertEqual(list_symbole[78], "Au")

    def test_list_isotopes_from_z(self):
        list_isotopes_helium = ['He3', 'He4', 'He5', 'He6', 'He7', 'He8', 'He9', 'He10']
        list_isotopes = self.dn.list_isotopes_from_z(2)
        self.assertEqual(list_isotopes, list_isotopes_helium)

    def test_get_z_from_elements(self):
        z = self.dn.get_z_from_elements("Fe")
        self.assertEqual(z, 26)

    def test_get_z_a_lambda_from_rns(self):
        z_a_lambda = self.dn.get_z_a_lambda_from_rns("Ag100")
        print("z_a_lambda =", type(z_a_lambda))
        self.assertEqual(z_a_lambda, (47, 100, 0.0057474890547))


if __name__ == '__main__':
    unittest.main()


