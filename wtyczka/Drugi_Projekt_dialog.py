# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DrugiProjektDialog
                                 A QGIS plugin
 wtyczka na zajecia z informatyki
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-06-05
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Zuzanna Mazurkiewicz Szymon Mika 
        email                : gwiazdaroku@interia.pl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.utils import iface
from qgis.core import QgsWkbTypes
import numpy as np
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from math import atan2

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Drugi_Projekt_dialog_base.ui'))


class DrugiProjektDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(DrugiProjektDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.radioButton_pole.clicked.connect(self.obliczanie)
        self.radioButton_przewyzszenia.clicked.connect(self.obliczanie)
        self.zlicz_elementy.clicked.connect(self.zlicz_elementy_funkcja)
        
    def zlicz_elementy_funkcja(self):
        elementy = len(self.mMapLayerComboBox.currentLayer().selectedFeatures())
        self.zlicz_elementy_wynik.setText(str(elementy))

    def obliczanie(self):
        aktywna_warstwa = iface.activeLayer()
        liczba_elementow = self.mMapLayerComboBox.currentLayer().selectedFeatures()
        X = []
        Y = []
        H = []
        nr = []
        i = 0
     
        for punkt in liczba_elementow:
            wsp = punkt.geometry().asPoint()
            x = wsp.x()
            y = wsp.y()
            X.append(x)
            Y.append(y)
            i+=1
            nr.append(i)
            
        wysokosci =iface.activeLayer().selectedFeatures()
        for i in wysokosci:
            H.append(i[2])
            
        if self.radioButton_przewyzszenia.isChecked() == True and len(liczba_elementow) == 2:
            dh = H[1] - H[0]
            punkt_1 = nr[0]
            punkt_2 = nr[1]
            iface.messageBar().pushMessage('Różnica wysokosci między punktem '+ str(punkt_1)+ ' oraz punktem '+str(punkt_2) + ' to: '+str(round(dh,3))+' |m|')
            
        elif self.radioButton_pole.isChecked()  == True and len(liczba_elementow) >2:
            punkty = []
            for i in range(0, len(X)):
                punkty.append([X[i], Y[i] ])
            pa = 0
            for i in range(len(punkty)):
                if i ==len(punkty) - 1:
                    pa += (punkty[i][0]+ punkty[0][0]) * (punkty[i][1] - punkty[0][1])
                else:
                    pa += (punkty[i][0] + punkty[i + 1][0]) * (punkty[i][1]-punkty[i+1][1])
            P = abs( -pa/2)
                      
            iface.messageBar().pushMessage('Pole obszaru wynosi: '+str(round(P,5))+' [m2]')
       
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Zła liczba zaznaczonych punktów do tej operacji!')
            msg.setInformativeText
            msg.setWindowTitle("Błąd przy zaznaczaniu punktów!!")
            msg.exec_()                   
            
    def katy(self, p, punkt1):
        dx = p[0] - punkt1[0]
        dy = p[1] - punkt1[1]
        kat = atan2(dx, dy)
        return kat
    
    def sortowanie_punktow(self, k):
        k = []
        elementy = self.mMapLayerComboBox_layers.currentLayer().selectedFeatures()
        for element in elementy:
            wspolrzedne = element.geometry().asPoint()
            X = wspolrzedne.x()
            Y = wspolrzedne.y()
            k.append([X, Y])
        punkt1 = [sum(p[0] for p in k) / len(k), sum(p[1] for p in k) / len(k)]
        posortowane = sorted(k, key = lambda p: self.katy(p, punkt1))
        return posortowane
    
   
    
    