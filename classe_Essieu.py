#!/ usr/bin/ python3

# -* - coding : utf -8 -* -

""" Auteur : Charlotte Wolff
    Date d'implementation : 13/12/2016
"""

import numpy as np
import matplotlib as ptl
from datetime import datetime, date, time, timedelta


"""
Classe Essieu
"""


class Essieu:
    def __init__(self,camion,nbEssieu,poids,distance,dateArrivee,x=-1):
        self.camion = camion
        self.nbEssieu = nbEssieu
        self.x = x
        self.poids = poids
        self.distance = distance
        self.dateArrivee = dateArrivee

    # ---------DEFINITION DES SETTERS
    def setNom(self,nCamion):
        self.camion = nCamion
        return 0
    def setnbEssieu(self,nEssieu):
        self.nbEssieu = nEssieu
        return 0
    def setX(self,nX):
        self.x = nX
        return 0
    def setPoids(self,nPoids):
        self.poids = nPoids
        return 0
    def setDistance(self,nDistance):
        self.distance = nDistance
        return 0
    def setDateArrivee(self,nDate):
        self.dateArrivee = nDate
        return 0

    def affiche(self):
        print ('###')
        print('Numero de camion : ', self.camion)
        print ("Numero de l'essieu : ", self.nbEssieu)
        print ('Coordonnees : ', self.x)
        print("Poids sur l'essieu : ", self.poids)
        print ("Distance au premier essieu : ", self.distance)
        print("Date d'arrivee de l'essieu sur le pont : ", self.dateArrivee)
        print ('###')
        return 0

    def calculEffetEssieu(self,vitesse,ligneInfluence,date):
        """Calcul de l'effet d'un essieu sur le pont"""
        """Retourne l'effet d'un essieu"""
        effetEssieu = 0
        if self.x != -1:
            valeurLigneInfluence = self.calculVLigneInfluence(ligneInfluence)
            dt = date-self.dateArrivee
            effetEssieu = float(self.poids)*valeurLigneInfluence
        return effetEssieu

    def calculVLigneInfluence(self,ligneInfluence):
        """Interpolation de la valeur de la ligne d'influence en self.x"""
        """Retourne cette valeur"""
        nl,nc = ligneInfluence.shape
        y2 = y1 = x1 = x2 = 0
        for i in range(nl):
            if self.x <= 100*ligneInfluence[i][0]:
                x1 = 100*ligneInfluence[i-1][0]
                x2 = 100*ligneInfluence[i][0]
                y1 = ligneInfluence[i-1][1]
                y2 = ligneInfluence[i][1]
                break
        valeurLigneInfluence = (y2-y1)/(x2-x1)*(self.x-x1)+y1
        return valeurLigneInfluence


    def setCoor(self, vitesse,date,longueurPont):
        """Mise a jour des coordonnees de l'essieu sur le pont"""
        self.x = (float(vitesse)*10**5/3600)*(date-self.dateArrivee).total_seconds()
        if self.x>longueurPont: #--- Camion a traverse pont
            self.x = -1
        elif self.x < 0: #---Pare-choc sur le pont mais pas l'essieu. On le met au debut du pont -> pas deffet
            self.x = 0
        return 0




