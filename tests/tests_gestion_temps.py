# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from gestion_temps import Instant, ListeInstant
import unittest

class TestInstant(unittest.TestCase):
    def setUp(self):
        """ Prépare des données avant de lancer les tests """
        self.mon_instance = Instant("60s manu")

    def tearDown(self):
        """ Nettoyer/changer des données après chaque test """
        pass

    def test_instant_is_instance_of_instant(self):
        self.assertIsInstance(self.mon_instance, Instant)

    def test_equal(self):
        un_instant = Instant("1mn auto")
        self.assertEqual(un_instant, self.mon_instance, "ECHEC : devraient être egaux")

    def test_no_equal(self):
        un_instant = Instant("130s auto")
        self.assertNotEqual(un_instant, self.mon_instance, "ECHEC : devraient être différents")

    def test_instant_value(self):
        str_deux_instant = "5.0mn auto"
        deux_instant= Instant(str_deux_instant)
        self.assertEqual(deux_instant.value, 5 * 60)

    def test_instant_unit(self):
        str_trois_instant = "400an manu"
        trois_instant = Instant(str_trois_instant)
        self.assertEqual(trois_instant.unite(), "an")

    def test_instant_auto_str(self):
        str_instant = "5.0mn manu"
        instant = Instant(str_instant)
        self.assertEqual(instant.auto_str(), "manu")

    def test_instant_str_instant(self):
        str_instant = "5.0mn manu"
        instant = Instant(str_instant)
        self.assertEqual(str(instant), "5.0000e+00mn manu")

class TestListeInstant(unittest.TestCase):
    def setUp(self):
        """ Prépare des données avant de lancer les tests """
        self.listeinstant = ListeInstant()


    def tearDown(self):
        """ Nettoyer/changer des données après chaque test """
        pass

    def test_listeinstant_is_instance_of_listeinstant(self):
        self.assertIsInstance(self.listeinstant, ListeInstant)

if __name__ == '__main__':
    unittest.main()


def methodes_instant(unite_instant, valeur_instant):
    un_instant = Instant()
    result = []
    un_instant.set_unit(unite_instant)
    result.append(un_instant.unit)
    un_instant.set_value_secondes(valeur_instant)
    result.append(un_instant.value)
    result.append(un_instant.str_instant())
    print("result=", result)
    return result


# assert methodes_instant('s', 3) == [0, 3, '3.0s manu']
# assert methodes_instant('mn', 2) == [1, 120, '2.0mn manu']
# assert methodes_instant('m', 2) == [1, 120, '2.0mn manu']
# assert methodes_instant('h', 2) == [2, 7200, '2.0h manu']
# assert methodes_instant('j', 2) == [3, (7200 * 24), '2.0j manu']
# assert methodes_instant('an', 2) == [4, (7200 * 24 * 365), '2.0an manu']


def methodes_liste_instant():
    liste_instant = ListeInstant()
    assert len(liste_instant) == 0
    str_deux_instant = "5.0mn auto"
    liste_instant.ajoute_instant(str_deux_instant)
    assert len(liste_instant) == 1
    assert liste_instant.data[0].value == 300
    assert liste_instant.data[0].unit == 1
    print(liste_instant.data[0])

    # str_quatre_instant = "60s auto"
    # str_cinq_instant = "0.0h auto"
    # liste_instant_2 = ListeInstant()
    # liste_instant_2.ajoute_auto(str_quatre_instant, str_cinq_instant, 6, 0)
    # for i in range(6) :
    #     assert liste_instant_2.data[i] == Instant(str(i * 10) + 's auto')
    #                                 ['60.0s auto',
    #                                 '50.0s auto',
    #                                 '40.0s auto',
    #                                 '30.0s auto',
    #                                 '20.0s auto',
    #                                 '10.0s auto']


methodes_liste_instant()
# str_deux_instant = "5.0mn auto"
# str_quatre_instant = "1.0h auto"
# str_cinq_instant = "0.0h auto"
#
# def methodes liste_instant
# deux_instant= Instant(str_deux_instant)
# trois_instant = Instant(deux_instant)
#
# liste_instant = ListeInstant()
# assert len(liste_instant) == 0
# liste_instant.ajoute(str_deux_instant)
# liste_instant.ajoute(str_deux_instant)
# assert len(liste_instant) == 2
#
# type(liste_instant.data)
# print(liste_instant.data[0])
# t_ini = '30.0s manu'
# t_fin = '2.0h manu'
# liste_instant.ajoute_auto(t_ini, t_fin, 20, 0)
# print("liste_instant = ", liste_instant.data[0])

