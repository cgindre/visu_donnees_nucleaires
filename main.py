# -*- coding: utf-8 -*-

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtUiTools import *
import sys
import time

from gestion_temps import Instant, ListeInstant, periode_demi_vie
import conversions
import donnees_nucleaires


class MainWindow(QMainWindow):
    def __init__(self):
        self.win_nucl_data = None
        self.donnees_nucl = donnees_nucleaires.DonneesNucleaires()

    def display_nucl_data(self, list_elements, list_radionucleides, expand=False):
        """Affiche les listes d'elements et de radinucleides dans QTreeWidget"""

        tw_nucl_data = self.win_nucl_data.tw_nucl_data

        list_tw_items = []  # H, He, ...
        list_tw_items_child = []  # H1, H2, ..., C14

        for element in list_elements:
            print(" PROBLEME element = ", element)
            tw_item = QTreeWidgetItem(tw_nucl_data, [element])
            list_tw_items.append(tw_item)

            if expand:
                tw_nucl_data.expandItem(tw_item)

            z_element = self.donnees_nucl.get_z_from_elements(element)
            print("z_element = ", z_element)
            # list_isotopes_from_element = self.donnees_nucl.list_isotopes_from_z(z_element)
            # print("list_isotopes_from_element = ", list_isotopes_from_element)

            for radionucleide in list_radionucleides:
                list_tw_items_child.append(QTreeWidgetItem(list_tw_items[-1], [radionucleide]))

            # for isotope in list_isotopes_from_element:
            #     list_tw_items_child.append(QTreeWidgetItem(list_tw_items[-1], [isotope]))

        self.win_nucl_data.show()

    def on_visu_nucl_data(self):
        """Affiche fenêtre 'Visualisation des données nucléaires'"""
        if self.win_nucl_data is None:
            ui_file_name = "donnees_nucleaires.ui"
            ui_file = QFile(ui_file_name)
            loader = QUiLoader()
            self.win_nucl_data = loader.load(ui_file)
            ui_file.close()
        tw_nucl_data = self.win_nucl_data.tw_nucl_data
        tw_nucl_data.setHeaderLabels(["Radionucléides"])

        list_elements = self.donnees_nucl.list_fields_from_table("symbole", "Elements")
        print("list_elements = ", list_elements)
        list_radionucleides = self.donnees_nucl.list_fields_from_table("symbole", "RNs")
        print("list_radionucleides = ", list_radionucleides)

        # list_z_element = []
        # list_radionucleides = []
        # for element in list_elements:
        #     z_element = donnees_nucleaires.get_z_from_elements(element)
        #     print("z_element = ", z_element)
        #     #list_radionucleides.append(donnees_nucleaires.list_isotopes_from_z(z_element))
        #     list_isotopes_from_z = donnees_nucleaires.list_isotopes_from_z(z_element)
        #     print("list_isotopes_from_z = ", list_isotopes_from_z)
        #     #list_radionucleides = [isotope for isotope in list_isotopes_from_z]
        #     [list_radionucleides.append(isotope) for isotope in list_isotopes_from_z]
        #
        # print("list_radionucleides = ", list_radionucleides)

        for element in list_elements:
            z_element = self.donnees_nucl.get_z_from_elements(element)
            print("z_element = ", z_element)
            # list_isotopes_from_element = self.donnees_nucl.list_isotopes_from_z(z_element)
            # print("list_isotopes_from_element = ", list_isotopes_from_element)

            list_radionucleides = self.donnees_nucl.list_isotopes_from_z(z_element)
            print("list_radionucleides = ", list_radionucleides)

        self.display_nucl_data(list_elements, list_radionucleides)

        tw_nucl_data.itemClicked.connect(self.on_radionucleide_info)

        le_nucl_search = self.win_nucl_data.le_nucl_search
        le_nucl_search.textChanged.connect(self.on_le_nucl_search)

    def on_le_nucl_search(self):
        """permet la recherche d'un RN dans QLineEdit et affiche suggestions pertinentes"""
        print("IN on_le_nucl_search")
        saisie = self.win_nucl_data.le_nucl_search.text()
        print("saisie = ", saisie)

        elements_match, radionucleides_match = self.donnees_nucl.get_str_element_from_str_radionucleides(saisie)
        print("elements_match = ", elements_match)
        print("radionucleides_match = ", radionucleides_match)

        tw_nucl_data = self.win_nucl_data.tw_nucl_data
        tw_nucl_data.clear()

        # # Si des elemments et des radinoucleides peuvent correspondre à la saisie, on les affiche
        # if elements_match != None and radionucleides_match != None :
        #     if saisie != "":
        #         self.display_nucl_data(elements_match, radionucleides_match, expand = True)
        #     else:
        #         self.display_nucl_data(elements_match, radionucleides_match, expand=False)
        # # Sinon aucune correspondance ne peut être effectuée et aucun radionucléide n'est suggéré
        # else:
        #     pass

        if elements_match != None and radionucleides_match != None:
            list_tw_items = []  # H, He, ...
            list_tw_items_child = []  # H1, H2, ..., C14
            for element in elements_match:
                print("element = ", element)
                tw_item = QTreeWidgetItem(tw_nucl_data, [element])
                list_tw_items.append(tw_item)
                tw_nucl_data.expandItem(tw_item)

                z_element = self.donnees_nucl.get_z_from_elements(element)
                print("z_element = ", z_element)
                list_isotopes_from_element = self.donnees_nucl.list_isotopes_from_z(z_element)
                print("list_isotopes_from_element = ", list_isotopes_from_element)

                for radionucleide in radionucleides_match:
                    list_tw_items_child.append(QTreeWidgetItem(list_tw_items[-1], [radionucleide]))

        self.win_nucl_data.show()

    def on_radionucleide_info(self, item):
        if item.parent() is not None:
            print("IN on_radionucleide_info")
            isotope_name = item.text(0)

            z_a_lambda = self.donnees_nucl.get_z_a_lambda_from_rns(isotope_name)
            isotope_Z = str(z_a_lambda[0])
            isotope_A = str(z_a_lambda[1])
            isotope_periode = periode_demi_vie(z_a_lambda[2])

            lw_nucl_data = self.win_nucl_data.lw_nucl_data
            lw_nucl_data.item(0).setText(" Nom : " + isotope_name)
            lw_nucl_data.item(1).setText(" Z : " + isotope_Z)
            lw_nucl_data.item(2).setText(" A : " + isotope_A)
            lw_nucl_data.item(3).setText(" Période : " + isotope_periode)

            tw_nucl_decay = self.win_nucl_data.tw_nucl_decay
            mode_fils_proba_nrj = self.donnees_nucl.get_mode_fils_proba_nrj_from_desintegrations(isotope_name)
            nb_rows = len(mode_fils_proba_nrj)
            tw_nucl_decay.setRowCount(nb_rows)

            for i in range(0, nb_rows):
                mode = QTableWidgetItem(self.donnees_nucl.str_mode(mode_fils_proba_nrj[i][0]))
                tw_nucl_decay.setItem(i, 0, mode)
                fils = QTableWidgetItem(mode_fils_proba_nrj[i][1])
                tw_nucl_decay.setItem(i, 1, fils)
                proba = QTableWidgetItem(conversions.scientific_notation(str(mode_fils_proba_nrj[i][2] * 100)))
                tw_nucl_decay.setItem(i, 2, proba)
                nrj = QTableWidgetItem(conversions.scientific_notation(str(mode_fils_proba_nrj[i][3])))
                tw_nucl_decay.setItem(i, 3, nrj)
                print("mode = ", mode.text(), " fils = ", fils.text(), " proba = ", proba.text(), " nrj = ", nrj.text())

if __name__ == '__main__':

    start = time.time()
    print("he toto !!!")
    end = time.time()
    elapsed = end - start
    print(f'Temps d\'exécution : {elapsed:.2}ms')

    app = QApplication()
    window = MainWindow()
    window.on_visu_nucl_data()
    sys.exit(app.exec())