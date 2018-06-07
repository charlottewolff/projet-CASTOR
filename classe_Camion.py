#!/ usr/bin/ python3

# -* - coding : utf -8 -* -

""" Auteur : Charlotte Wolff
    Date d'implementation : 13/12/2016
"""

import numpy as np
import matplotlib as ptl
from datetime import datetime, date, time, timedelta

from classe_Essieu import *
from classe_parametres import *


"""
Classe Camion
"""


class Camion:
    def __init__(self,nomj,dateArrivee,vMoyenne,poidsMoyen,lEssieux,isSurPont):
        self.nomj = nomj
        self.dateArrivee = dateArrivee
        self.vMoyenne = vMoyenne
        self.poidsMoyen = poidsMoyen
        self.lEssieux = lEssieux
        self.isSurPont = isSurPont

    # ---------DEFINITION DES SETTERS
    def setNom(self,nNom):
        self.nomj = nNom
        return 0
    def setDateArrivee(self,nDate):
        self.dateArrivee = nDate
        return 0
    def setvMoyenne(self,nVitesse):
        self.vMoyenne = nVitesse
        return 0
    def setPoidsMoyen(self,nPoids):
        self.poidsMoyen = nPoids
        return 0
    def setlEssieux(self,nlEssieux):
        self.lEssieux = nlEssieux
        return 0
    def setSurPont(self,nPont):
        self.isSurPont = nPont
        return 0

    def affiche(self):
        print('Numero de camion : ', self.nomj)
        print("Date d'arrivee sur le pont : ", self.dateArrivee)
        print ('Vitesse moyenne : ', self.vMoyenne)
        print ('Poids moyen : ', self.poidsMoyen)
        print ('Presence sur le pont : ', self.isSurPont)
        #for essieu in self.lEssieux:
            #essieu.affiche()
        return 0

    def verifIsPont(self):
        """Verification de la presence du camion sur le pont"""
        """Mise a jour de isSurPont"""
        self.setSurPont(0)
        for essieu in self.lEssieux:
            if essieu.x != -1:
                self.setSurPont(1) #--un seul essieu sur le pont suffit pour camion sur le pont
                break
        return 0


    def calculEffetCamion(self,ligneInfluence,date):
        """ Calcul de l'effet d'un camion sur le pont """
        """retourne la valeur de l'effet d'un camion sur le pont"""
        effetCamion = 0
        for essieu in self.lEssieux:
            effetCamion += essieu.calculEffetEssieu(self.vMoyenne, ligneInfluence,date)
        return effetCamion
