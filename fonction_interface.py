# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:10:36 2017

@author: cwolff
"""

from PyQt4 import QtGui
import csv

def messageBox(msg):
    """ouverture d'une fenetre d'information"""
    infoBox = QtGui.QMessageBox()
    infoBox.setIcon(QtGui.QMessageBox.Warning)
    infoBox.setStandardButtons(QtGui.QMessageBox.Ok)
    infoBox.setWindowTitle('Attention')
    infoBox.setText(msg)
    ret = infoBox.exec_()
    testOK = 1
    return testOK
    
def rechercheChemin(celluleEcriture):
    """Recherche le chemin d'un fichier et l'ecrit dans la cellule"""
    chemin = QtGui.QFileDialog.getOpenFileName()
    celluleEcriture.setText(chemin)
    return chemin
    
def cocherDecocher(traitementInterface,Bool):
    """coche ou decoche de tous les histogrammes de la classe traitementInterface"""
    traitementInterface.checkEffet.setChecked(Bool)
    traitementInterface.checkVitesse.setChecked(Bool)
    traitementInterface.checkPoids.setChecked(Bool)
    traitementInterface.checkPoidsEssieu.setChecked(Bool)
    traitementInterface.checkNombreEssieu.setChecked(Bool)
    traitementInterface.checkLongueur.setChecked(Bool)
    traitementInterface.checkDistanceEssieux.setChecked(Bool)
    traitementInterface.checkTemps.setChecked(Bool)
    return 0