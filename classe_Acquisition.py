#!/ usr/bin/ python3

# -*- coding: utf-8 -*-


""" Auteur : Charlotte Wolff
    Date d'implementation : 13/12/2016
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, time, timedelta

from classe_Camion import *
from classe_Essieu import *
from classe_parametres import *

"""
Classe Acquisition
"""


class Acquisition:
    def __init__(self,cVitesse,cDate,cPoids,cPoidsEssieux,cPoidsEssieuHisto,cDistanceEssieu,cDistanceEssieuxHisto,cLongueur,cTemps,taillePont,dateDebut,dateFin,vMoyenne,ligneInfluence,cNbEssieu,valeursCNbEssieu,lCamions=[],ligneFichier=0):
        self.cVitesse = cVitesse
        self.cDate = cDate
        self.cPoids = cPoids
        self.cPoidsEssieux = cPoidsEssieux
        self.cPoidsEssieuxHisto = cPoidsEssieuHisto
        self.cDistanceEssieu = cDistanceEssieu
        self.cDistanceEssieuxHisto = cDistanceEssieuxHisto
        self.cLongueur = cLongueur
        self.cTemps = cTemps
        self.taillePont = taillePont
        self.dateDebut = dateDebut
        self.dateFin = dateFin
        self.vMoyenne = vMoyenne
        self.ligneInfluence = ligneInfluence
        self.lCamions = lCamions
        self.ligneFichier = ligneFichier
        self.cNbEssieu = cNbEssieu
        self.valeursCNbEssieu = valeursCNbEssieu

        print('Acquisition des donnees necessaires au calcul')

    #---------DEFINITION DES SETTERS
    def setcVitesse(self,ncVitesse):
        self.cVitesse = ncVitesse
        return 0
    def setcDate(self,ncDate):
        self.cDate = ncDate
        return 0
    def set(self,ncVitesse):
        self.cVitesse = ncVitesse
        return 0
    def setcPoids(self,ncPoids):
        self.cPoids = ncPoids
        return 0
    def setPoidsEssieu(self,ncPoidsEssieu):
        self.cPoidsEssieux = ncPoidsEssieu
        return 0
    def setPoidsEssieuHisto(self,ncPoidsEssieuHisot):
        self.cPoidsEssieuxHisto = ncPoidsEssieuHisot
        return 0
    def setDistanceEssieu(self,ncDistanceEssieu):
        self.cDistanceEssieu = ncDistanceEssieu
        return 0  
    def setDistanceEssieuxHisto(self,ncDistanceEssieuxHisto):
        self.cDistanceEssieuxHisto = ncDistanceEssieuxHisto
        return 0  
    def setTemps(self,ncTemps):
        self.cTemps = ncTemps
        return 0 
    def setTaillePont(self,nTaillePont):
        self.taillePont = nTaillePont
        return 0
    def setDateDebut(self,nDateDebut):
        self.cDateDebut = nDateDebut
        return 0
    def setDateFin(self,nDateFin):
        self.cDateFin = nDateFin
        return 0
    def setVMoyenne(self,nVMoyenne):
        self.vMoyenne = nVMoyenne
        return 0
    def setLilgneInfluence(self, nLigneInfluence):
        self.ligneInfluence = nLigneInfluence
        return 0
    def setcNbEssieu(self, ncNbEssieu):
        self.cNbEssieu = ncNbEssieu
        return 0
    def setValeurcNbEssieu(self, nValeurcNbEssieu):
        self.valeursCNbEssieu = nValeurcNbEssieu
        return 0

    def affiche(self):
        print ('Colonne date : ', self.cDate)
        print ('Colonne vitesse : ', self.cVitesse)
        print ('Colonne poids : ', self.cPoids)
        print ('Colonne poids essieu : ', self.cPoidsEssieux)
        print ('Colonne distance essieu : ', self.cDistanceEssieu)
        print ('Taille pont : ', self.taillePont)
        print('Date de debut : ', self.dateDebut)
        print('Date de fin : ', self.dateFin)
        return 0


    def calculEffetTotalDate(self,date):
        """Calcul pour les differentes dates de l'effet du trafic sur le pont et creation d'un fichier trafic"""
        """Retourne l'effet total sur le pont a la date consideree"""
        effetTotal = 0
        for camion in self.lCamions:
            effetTotal += camion.calculEffetCamion(self.ligneInfluence,date)
        return effetTotal


    def calculEffetTotal(self,fichierCheminSortie,pas):
        """Calcul des effets au cours du temps et creation du fichier des effets en sortie"""
        """Retourne la matrice des effets au cours du temps"""
        print ("Calcul des effets et creation du fichier de sortie")
        fichierSortie = open(fichierCheminSortie, "w")
        dateCalcul = self.dateDebut
        matriceEffet = []

        #--- Definition des effets min et max
        minEffet = 0
        maxEffet = 0

        while dateCalcul < self.dateFin:
            self.setLcamions(self.ligneFichier,dateCalcul) #--- Mise a jour de la liste de camions sur le pont
            if len(self.lCamions) > 0: #--- Si camion sur pont, on calcule les effets
                effetDate = self.calculEffetTotalDate(dateCalcul) #--- Calcul de l'effet
                ecriture = str(dateCalcul) + ',' + str(effetDate) + '\n'
                fichierSortie.write(ecriture)

                #--- Mise a jour min et max
                if effetDate<minEffet:
                    minEffet = effetDate
                if effetDate> maxEffet:
                    maxEffet = effetDate

                if effetDate != 0: #---Prise en compte pour l'histogramme si valeur non nulle
                    matriceEffet.append(effetDate)
                dateCalcul += timedelta(0, 0, pas * 10 ** 4) #--- Incrementation de la date
            elif len(self.lCamions) == 0 and self.ligneFichier < len(self.cDate)-1: #--- Saut de temps au prochain camion si plus de camion sur le pont
                dateCalcul = self.cDate[self.ligneFichier+1]
            else: #---Saut de date dans le cas du dernier camion du fichier
                dateCalcul = self.dateFin

        fichierSortie.close()
        self.effet = matriceEffet

        #--- Affichage des minimum et maximum
        print'Effet minimum : ', minEffet, 'MPa.'
        print'Effet maximum : ', maxEffet, 'MPa.'

        return matriceEffet


    def setLcamions(self,ligne,date):
        """Mise a jour de la liste des camions presents sur le pont la date du calcul
           Retourne la prochaine ligne du fichier a traiter
        """
        k = 0
        l = ligne
        while self.cDate[l] <= date: #--- Creation des nouveaux camions sur le pont
            newCamion = self.createCamion(l,date)
            newCamion.verifIsPont() #--- Verification si encore sur le pont
            if newCamion.isSurPont == 1:
                self.lCamions.append(newCamion)
                k += 1
            l += 1
        self.ligneFichier = l #--- Recuperation de la ligne

        for camion in self.lCamions[k:]: #--- Mise a jour des coordonnees des autres camions presents sur pont
            for essieu in camion.lEssieux:
                essieu.setCoor(self.vMoyenne,date,self.taillePont)
            camion.verifIsPont()
            if camion.isSurPont == 0: #--- Suppression des camions qui ne sont plus sur le pont
                self.lCamions.remove(camion)
        return 0


    def createCamion(self,ligne, date):
        """Creation d'un camion de la classe camion"""
        """Retourne le camion cree"""
        camion = Camion(ligne,self.cDate[ligne],self.vMoyenne,self.cPoids[ligne],[],1)
        d = 0 #--- distance au parechoc
        distance = 0 #--- distance au premier essieu
        for essieu in range(len(self.cPoidsEssieux[ligne])):
            if essieu != 0:
                distance += int(self.cDistanceEssieu[ligne][essieu]) #---calcul de la distance au premier essieu
            d += int(self.cDistanceEssieu[ligne][essieu]) #---calcul de la distance au pare choc
            dateArriveeEssieu = self.cDate[ligne] + timedelta(0,float(d)/(self.vMoyenne*10**5/3600)) #---calcul de la date d'arrivee de lessieu sur le pont
            essieu = Essieu(ligne,essieu,self.cPoidsEssieux[ligne][essieu],distance,dateArriveeEssieu) #---creation de lessieu
            essieu.setCoor(self.vMoyenne,date,self.taillePont) #---calcul des coordonnees sur le pont
            camion.lEssieux.append(essieu)
        return camion


    def createHistogramme(self, vecteur, titre,legende):
        """Creation de l'histogramme choisi"""
        plt.figure()
        n, bins, patches = plt.hist(np.asarray(vecteur, dtype=float), normed=1, facecolor='b', alpha=1)
        plt.title(titre)
        plt.xlabel(legende)
        plt.ylabel(u'Frequences')
        # plt.axis([mini, maxi, 0, 10])
        plt.grid(True)
        plt.show()
        return 0
    
    def createCamembert(self,vecteurNom, vecteurValeur, titre):
        """Creation d'un camembert de vecteurValeur avec comme legende vecteurNom"""
        plt.pie(vecteurValeur, labels=vecteurNom, startangle=0, autopct='%1.1f%%',shadow=True)
        plt.axis('equal') 
        plt.title(titre)
        plt.show()
        return 0

    def createListeHisto(self,listeHisto):
        """Creation des histogrammes choisis par l'utilisateur"""
        print ('Creation des histogrammes')
        if 'effet' in listeHisto:
            self.createHistogramme(self.effet,'Histogramme des effets', 'Valeurs (MPa)')
        if 'vitesse' in listeHisto:
            self.createHistogramme(self.cVitesse, 'Histogramme des vitesses', 'Valeurs (km/h)')
        if 'poids' in listeHisto:
            self.createHistogramme(self.cPoids, 'Histogramme des poids par vehicule', 'Valeurs (kg)')
        if 'poidsEssieu' in listeHisto:
            self.createHistogramme(self.cPoidsEssieuxHisto, 'Histogramme des poids par essieux', 'Valeurs (kg)')
        if 'longueurEssieu' in listeHisto:
            self.createHistogramme(self.cDistanceEssieuxHisto, 'Histogramme des longueurs entre deux essieux consecutifs', 'Valeurs (cm)')
        if 'nombreEssieu' in listeHisto:
            self.createCamembert(self.valeursCNbEssieu,self.cNbEssieu,"Repartition du nombre d'essieux")
        if 'longueur' in listeHisto:
            self.createHistogramme(self.cLongueur,'Histogramme des longueurs de camion', 'Valeurs (kg)')
        if 'temps' in listeHisto:
             self.createHistogramme(self.cTemps,"Histogramme des durees entre l'arrivee consecutive de 2 camions", 'Valeurs (s)')           
        return 0
