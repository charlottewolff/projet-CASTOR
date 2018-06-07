# -*- coding: utf-8 -*-
"""
Created on Sun Jan 08 21:35:38 2017

@author: cwolff
"""

from PyQt4 import QtGui
import sys
import csv
from datetime import datetime
 

import squelette_interface
from classe_parametres import *
import run_calculs as calc
import fonction_interface as fct_inter



class traitementInterface(QtGui.QMainWindow, squelette_interface.Ui_CASTOR):
    def __init__(self):

        super(self.__class__, self).__init__()
        self.setupUi(self) 
        print('Chargement de l\'interface graphique')
    
    def fButtonTrafic(self):
        """recherche du fichier trafic"""
        chemin = fct_inter.rechercheChemin(self.texteCheminTrafic)
        return 0
        
    def fButtonLInfluence(self):
        """recherche du fichier ligne influence"""
        chemin = fct_inter.rechercheChemin(self.texteCheminLigneInfluence)
        return 0
        
    def fButtonSortie(self):
        """recherche du fichier où enregistrer les effets en sortie"""
        chemin = fct_inter.rechercheChemin(self.texteSortie)
        return 0
        
    def fValider(self):
        """lancement des calculs"""
    
        #--- recuperation des chemins des fichiers
        cheminLigneInfluence = self.texteCheminLigneInfluence.text()
        cheminTrafic = self.texteCheminTrafic.text()
        cheminSortie = self.texteSortie.text()
        
        #--- recuperation des parametres de filtrage
        pas = self.pas.value()
        vMoyenne = self.vitMoy.value()
        minPoids = self.poidsMin.value()
        maxPoids = self.poidsMax.value()
        minPoidsEssieu = self.poidsEssieumin.value() 
        maxPoidsEssieu = self.poidsEssieumax.value()
        minVitesse = self.vitMin.value()
        maxVitesse = self.vitesseMax.value()
        minLongueur = self.longCamionMin.value() 
        maxLongueur = self.longCamionMax.value()
        minLongueurEssieu = self.longEssieuMin.value()
        maxLongueurEssieu = self.longEssieuMax.value()
        minNombreEssieu = self.nbEssieuMin.value()
        maxNombreEssieu = self.nbEssieuMax.value()
        
        #--- recuperation de la liste des histogrammes
        listeHisto = []
        if self.checkEffet.isChecked() == True:
            listeHisto.append('effet')
        if self.checkVitesse.isChecked() == True:
            listeHisto.append('vitesse')
        if self.checkPoids.isChecked() == True:
            listeHisto.append('poids')
        if self.checkPoidsEssieu.isChecked() == True:
            listeHisto.append('poidsEssieu')
        if self.checkNombreEssieu.isChecked() == True:
            listeHisto.append('nombreEssieu')
        if self.checkLongueur.isChecked() == True:
            listeHisto.append('longueur')        
        if self.checkDistanceEssieux.isChecked() == True:
            listeHisto.append('longueurEssieu') 
        if self.checkTemps.isChecked() == True:
            listeHisto.append('temps') 
            
        #--- verification de la presence des informations
        testOK = 0        
        if listeHisto == []: #--- histogrammes choisis
            msg = "Attention ! \n Vous n'avez pas coche d'histogrammes a afficher"
            testOK = fct_inter.messageBox(msg)
        if  cheminTrafic == '':  #--- fichier trafic
            print cheminTrafic
            msg = "Attention ! \n Vous n'avez pas rentre de fichier trafic"
            testOK = fct_inter.messageBox(msg)
        if cheminLigneInfluence == '': #--- ligne d'influence            
            msg = "Attention ! \n Vous n'avez pas rentre de fichier ligne d'influence"
            testOK = fct_inter.messageBox(msg)
        if 'effet' in listeHisto and cheminSortie == "":
            msg = "Attention ! \n Vous n'avez pas donne le chemin du fichier de sortie du calcul des effets"
            testOK = fct_inter.messageBox(msg) 
        #verification que les valeurs des parametres de filtrages sont coherentes
        if minPoids>maxPoids or minPoidsEssieu>maxPoidsEssieu or minVitesse>maxVitesse or minLongueur>maxLongueur or minLongueurEssieu>maxLongueurEssieu or minNombreEssieu>maxNombreEssieu:
            msg = "Attention ! \n Verifiez les valeurs de parametres de filtrage, il semble qu'il y ait un maximum<minimum"
            testOK = fct_inter.messageBox(msg)            
            
            
        if testOK == 0: #--- lancement du calcul si toutes les informations sont presentes
            #--- Creation des parametres de filtres        
            parametres = Parametres(cheminTrafic,cheminLigneInfluence,pas,vMoyenne,minPoids,maxPoids,minPoidsEssieu,maxPoidsEssieu,minVitesse,maxVitesse,minLongueur,maxLongueur,minLongueurEssieu,maxLongueurEssieu,minNombreEssieu,maxNombreEssieu,listeHisto)
            parametres.affiche()
            parametres.maj_historique()
        
            #--- Lancement des calculs
            date1 = datetime.today()
            retour = calc.valider(parametres,cheminSortie, date1)
            
            #--- Affichage d'un message d'erreur si probleme de format
            if retour == 1:
                msg = "Attention ! \n Probleme dans le format du fichier trafic \n Verifiez le format de la premiere ligne."
                test = fct_inter.messageBox(msg)                
        
        return 0
        
    def fInfo(self):
        """Information sur le format du fichier trafic"""
        #--- Definition du message a afficher        
        msg = "La premiere ligne du fichier doit contenir les termes : \n date \n contresens \n long_ \n vit \n vitmoy \n poids \n  \nPour chaque essieu i : \n pmoy_i \n d_i "          
        #--- Creation de boite de dialogue
        infoBox = QtGui.QMessageBox()
        infoBox.setIcon(QtGui.QMessageBox.Information)
        infoBox.setStandardButtons(QtGui.QMessageBox.Ok)
        infoBox.setWindowTitle('Format fichier Trafic')
        infoBox.setText(msg)
        ret = infoBox.exec_()
        return 0
        
        
    def fHistorique(self):
        """Remplissage avec les donnees de l'historique"""
        #--- recuperation de l'historique
        print'mise a jour'
        with open('historique.txt','r') as historique:
            histo = csv.reader(historique)
            histo = list(histo)
            #--- mise a jour des informations 
            self.texteCheminLigneInfluence.setText(str(histo[0][0]))
            self.texteCheminTrafic.setText(str(histo[1][0]))           
            self.pas.setValue(float(histo[2][0]))
            self.vitMoy.setValue(int(histo[3][0]))
            self.poidsMin.setValue(float(histo[4][0]))        
            self.poidsMax.setValue(float(histo[5][0]))
            self.poidsEssieumin.setValue(float(histo[6][0]))
            self.poidsEssieumax.setValue(float(histo[7][0]))
            self.vitMin.setValue(int(histo[8][0]))
            self.vitesseMax.setValue(int(histo[9][0]))
            self.longCamionMin.setValue(float(histo[10][0]))
            self.longCamionMax.setValue(float(histo[11][0]))  
            self.longEssieuMin.setValue(float(histo[12][0]))
            self.longEssieuMax.setValue(float(histo[13][0]))  
            self.nbEssieuMin.setValue(float(histo[14][0]))
            self.nbEssieuMax.setValue(float(histo[15][0]))
            historique.close()
        return 0
        
    def fDefaut(self):
        """Remplissage avec les donnees de l'historique"""
        #--- recuperation de l'historique
        print('Parametres par defaut')
        with open('defaut.txt','r') as dDefaut:
            defaut = csv.reader(dDefaut)
            defaut = list(defaut)
            #--- mise a jour des informations 
            self.pas.setValue(int(defaut[2][0]))
            self.vitMoy.setValue(int(defaut[3][0]))
            self.poidsMin.setValue(float(defaut[4][0]))        
            self.poidsMax.setValue(float(defaut[5][0]))
            self.poidsEssieumin.setValue(float(defaut[6][0]))
            self.poidsEssieumax.setValue(float(defaut[7][0]))
            self.vitMin.setValue(int(defaut[8][0]))
            self.vitesseMax.setValue(int(defaut[9][0]))
            self.longCamionMin.setValue(float(defaut[10][0]))
            self.longCamionMax.setValue(float(defaut[11][0]))  
            self.longEssieuMin.setValue(float(defaut[12][0]))
            self.longEssieuMax.setValue(float(defaut[13][0]))  
            self.nbEssieuMin.setValue(float(defaut[14][0]))
            self.nbEssieuMax.setValue(float(defaut[15][0]))
            dDefaut.close()
        return 0
    
    def fEffet(self):
        """Affiche l'histogramme des effets d'un fichier deja cree"""
        chemin = fct_inter.rechercheChemin(self.texteEffet)
        calc.lectureHistogramme(chemin)
        return 0
        
    def fTOUT(self):
        """Coche tous les histogrammes"""
        if self.checkTOUT.isChecked() == True: #--- on coche tout
            fct_inter.cocherDecocher(self,True)
        else: #--- on decoche tout
            fct_inter.cocherDecocher(self,False)
        return 0
        
        
    def run(self):
        """Definition de la fonction de chaque bouton"""
        self.buttonTrafic.clicked.connect(self.fButtonTrafic)
        self.buttonLigneInlfuence.clicked.connect(self.fButtonLInfluence) 
        self.buttonSortie.clicked.connect(self.fButtonSortie)
        self.buttonInfoFormat.clicked.connect(self.fInfo)
        self.buttonValider.clicked.connect(self.fValider)
        self.buttonHistorique.clicked.connect(self.fHistorique)
        self.buttonDefaut.clicked.connect(self.fDefaut)
        self.buttonEffet.clicked.connect(self.fEffet)
        self.checkTOUT.stateChanged.connect(self.fTOUT)
        return 0

def main():
    """fonction pour lancer l'interface"""
    app = QtGui.QApplication(sys.argv)  
    form = traitementInterface()
    form.run()                 
    form.show()                         
    app.exec_()


#------------------------------------------------------
if __name__ == '__main__':              
    main()  
#------------------------------------------------------