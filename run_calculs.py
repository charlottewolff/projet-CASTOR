#!/usr/bin/python

# -*- coding: utf-8 -*--


""" Auteur : Charlotte Wolff
    Date d'implementation : 13/12/2016
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime, date, time


from classe_Acquisition import *
from classe_Camion import *
from classe_Essieu import *
from classe_parametres import *

def fichier2matrice(chemintrafic,cheminLigne):
    """Recuperation des informations du fichier sous forme de matrice"""
    """Retourne la taille du pont, la matrice du trafic et la matrice de la ligne d'influence"""

    ligneInfluence= np.genfromtxt(cheminLigne, skip_header=2)
    taillePont = float(ligneInfluence[-1][0])*100

    with open(chemintrafic,'r') as fichier:
        lecture = csv.reader(fichier)
        enregistrement = list(lecture)
    return enregistrement,ligneInfluence,taillePont

def importDonnees(parametres):
    """Recuperation des colonnes des fichiers necessaires au calcul"""
    """Retourne 1 si format des colonnes invalide et la liste des indices de chaque colonne sinon"""
    enregistrement,ligneInfluence,taillePont = fichier2matrice(parametres.cheminFichierTrafic,parametres.cheminFichierLigneInfluence)
    ligne = enregistrement[0]

    #date, contresens,long,vit,vitmoy,d_1, d_2, d_3, d_4, d_5, d_6, d_7, d_8,poids, pmoy_1, pmoy_2, pmoy_3, pmoy_4, pmoy_5, pmoy_6, pmoy_7, pmoy_8
    testValid = 0
    iDate=-1
    iContresens = -1
    iLongueur = -1
    iVitesse = -1
    iVitmoy = -1
    iPoids = -1
    iPoidsEssieu = []
    iDistanceEssieu = []
    
    for c in range(len(ligne)):
        if ligne[c] == 'date':
            iDate = c
            testValid +=1
        if ligne[c] == 'contresens':
            iContresens = c
            testValid += 1
        if ligne[c] == '_long':
            iLongueur = c
            testValid += 1
        if ligne[c] == 'vit':
            iVitesse = c
            testValid += 1
        if ligne[c] == 'vitmoy':
            iVitmoy = c
            testValid += 1
        if ligne[c] == 'poids':
            iPoids= c
            testValid += 1
        for k in range(parametres.nbEssieux+1):
            if ligne[c] == 'pmoy_' + str(k):
                iPoidsEssieu.append(c)
                testValid += 1
            if ligne[c] == 'd_' + str(k):
                iDistanceEssieu.append(c)
                testValid += 1
    if testValid == 6+parametres.nbEssieux*2:
        return ([iDate,iContresens,iLongueur,iVitesse,iVitmoy,iPoids,iPoidsEssieu,iDistanceEssieu,ligneInfluence,taillePont,enregistrement])

    else:
        print 'Erreur dans le format des fichiers'
        return 1


def filtrage(chemin, enregistrement,parametres,ligneInfluence,iDate,iContresens,iLongueur,iVitesse,iVitmoy,iPoids,iPoidsEssieu,iDistanceEssieu,taillePont):
    """Filtrage du fichier de trafic"""
    """Retourne l'acquisition de la classe Acquisition qui a ete creee"""

    fichierFiltre = open(chemin, "w")
    ecriture = ecritureLigne(enregistrement,0,iDate,iContresens,iLongueur,iVitesse,iVitmoy,iPoids,iPoidsEssieu,iDistanceEssieu)
    fichierFiltre.write(ecriture)
    
    cDate = []  #--- contient les dates
    cContresens = []  #--- contient les contresens
    cLongueur = []  #--- contient les longueurs des camions
    cVitesse = []  #--- contient les vitesses
    cPoids = []  #--- contient les poids totaux
    cPoidsEssieu = []  #--- contient les poids par essieux (forme matrice)
    cDistanceEssieu = []  #--- contient les distances entre essieux
    cPoidsEssieuxHisto = []  #--- contient les poids par essieux sous forme liste pour faire les histogrammes
    cDistanceEssieuxHisto = []  #--- contient les distances entre essieux sous forme liste pour faire les histogrammes
    cTemps = [] #--- contient les durees entre arrivee de deux camions consecutifs
    dt = 0  #--- contiendra la date pour la ligne i
    
    #--- Creation des vecteurs necessaire a la realisation du camembert du nombre d'essieux
    cNbEssieu = [] 
    valeursCNbEssieu = [] 
    for i in range (parametres.minNombreEssieu,parametres.maxNombreEssieu+1,1):
        valeursCNbEssieu.append(str(i))
        cNbEssieu.append(0)
    
    #  indices = (iDate,iContresens,iLongueur,iVitesse,iVitmoy,iPoids,iPoidsEssieu,iDistanceEssieu)
    for ligne in range(len(enregistrement)):
        # -----------------------------verification des conditions de filtrage
        if ligne!= 0:
            #-- recherche du nombre d'essieux du camion
            compteurEssieu = 0
            for i in range (parametres.nbEssieux):
                if enregistrement[ligne][iPoidsEssieu[i]] !='':
                    compteurEssieu+=1
            
            #-- definition des conditions de filtrage
            ajout_V = 0
            ajout = 0
            ajout_vMoy = 0
            if int(enregistrement[ligne][iContresens]) == 0: #--- pas de contresens
                if int(enregistrement[ligne][iLongueur])>parametres.minLongueur and int(enregistrement[ligne][iLongueur])<parametres.maxLongueur: #--- longueur du camion
                    if int(enregistrement[ligne][iPoids])>parametres.minPoids and int(enregistrement[ligne][iPoids])<parametres.maxPoids: #--- poids total du camion
                        testPoidsEssieu = 1
                        testDistanceEssieu = 1
                        if compteurEssieu>parametres.minNombreEssieu and compteurEssieu<parametres.maxNombreEssieu: #--- nombre d'essieux
                            for essieu in range(compteurEssieu):
                                if int(enregistrement[ligne][iPoidsEssieu[essieu]])<parametres.minPoidsEssieu or int(enregistrement[ligne][iPoidsEssieu[essieu]])>parametres.maxPoidsEssieu: #--- poids des essieux
                                    testPoidsEssieu = -1
                                    break
                                if int(enregistrement[ligne][iDistanceEssieu[essieu]])<parametres.minLongueurEssieu or int(enregistrement[ligne][iDistanceEssieu[essieu]])>parametres.maxLongueurEssieu: #--- longueur entre essieux
                                    testDistanceEssieu = -1
                                    break
                            if testDistanceEssieu == 1 and testPoidsEssieu ==1:
                                if int(enregistrement[ligne][iVitesse]) > parametres.minVitesse and int(enregistrement[ligne][iVitesse]) < parametres.maxVitesse:  # ---vitesse du camion
                                    ajout_V = 1
                                    ajout = 1
                                elif int(enregistrement[ligne][iVitmoy]) > parametres.minVitesse and int(enregistrement[ligne][iVitmoy]) < parametres.maxVitesse:
                                    ajout_vMoy = 1
                                    ajout = 1


            if ajout ==1 :
                #-----------------------------mise a jour du vecteur comptant le nombre d'essieux
                cNbEssieu[compteurEssieu-parametres.minNombreEssieu] = cNbEssieu[compteurEssieu-parametres.minNombreEssieu]+1
                # -----------------------------ajout valeurs dans les colonnes
                if enregistrement[ligne][iDate].find('.')== -1:
                    dt1 = datetime.strptime(enregistrement[ligne][iDate], "%Y-%m-%d %H:%M:%S")
                else:
                    dt1 = datetime.strptime(enregistrement[ligne][iDate], "%Y-%m-%d %H:%M:%S.%f")
                cDate.append(dt1)
                cContresens.append(enregistrement[ligne][iContresens])
                cLongueur.append(enregistrement[ligne][iLongueur])
                cPoids.append(enregistrement[ligne][iPoids])
                pEssieu = []
                dEssieu = []
                
                #remplissage de la matrice des temps entre arrivee de 2 camions consecutifs
                if ligne > 1:
                    temps = (dt1-dt).total_seconds()
                    cTemps.append(temps)
                dt = dt1
                    
                for essieu in range (compteurEssieu):
                    pEssieu.append(enregistrement[ligne][iPoidsEssieu[essieu]])
                    dEssieu.append(enregistrement[ligne][iDistanceEssieu[essieu]])
                    cPoidsEssieuxHisto.append(enregistrement[ligne][iPoidsEssieu[essieu]])
                    cDistanceEssieuxHisto.append(enregistrement[ligne][iDistanceEssieu[essieu]])
                cPoidsEssieu.append(pEssieu)
                cDistanceEssieu.append(dEssieu)
                if ajout_V == 1:
                    cVitesse.append(enregistrement[ligne][iVitesse])
                elif ajout_vMoy == 1:
                    cVitesse.append(enregistrement[ligne][iVitesse])
                # -----------------------------ecriture du fichier
                # format ligne ecriture : date,contresens,longueur,vitesse,
                ecriture = ecritureLigne(enregistrement,ligne,iDate,iContresens,iLongueur,iVitesse,iVitmoy,iPoids,iPoidsEssieu,iDistanceEssieu)
                fichierFiltre.write(ecriture)
    fichierFiltre.close()
    dateDebut = cDate[0]
    dateFin = cDate[-1]
    acquisition = Acquisition(cVitesse,cDate,cPoids,cPoidsEssieu,cPoidsEssieuxHisto,cDistanceEssieu,cDistanceEssieuxHisto,cLongueur,cTemps,taillePont,dateDebut,dateFin,parametres.vMoyenne,ligneInfluence,cNbEssieu,valeursCNbEssieu)
    
    nbLignesEnlevees = len(enregistrement)-len(cDate)
    print 'Nombre de lignes enlevees : ', nbLignesEnlevees
    return acquisition

def ecritureLigne(enregistrement,ligne,iDate,iContresens,iLongueur,iVitesse,iVitmoy,iPoids,iPoidsEssieu,iDistanceEssieu):
    """Met en forme la ligne a ecrire dans le fichier trafic filtre"""
    """retourne la ligne ecrite"""
    ecriture = enregistrement[ligne][iDate] + ',' + enregistrement[ligne][iContresens] + ',' + enregistrement[ligne][
        iLongueur] + ',' + enregistrement[ligne][iVitesse]
    ecriture = ecriture + ',' + enregistrement[ligne][iVitmoy] + ',' + enregistrement[ligne][iPoids] + ','
    for essieu in range(len(iPoidsEssieu)):
        ecriture = ecriture + enregistrement[ligne][iPoidsEssieu[essieu]] + ','
    for essieu in range(len(iDistanceEssieu)):
        ecriture = ecriture + enregistrement[ligne][iDistanceEssieu[essieu]] + ','
    ecriture = ecriture + '\n'
    return ecriture


def valider(parametres, cheminSortie, date1):
    """Fonction de lancement de tout le programme"""
    #recuperation des fichiers necessaires au calcul
    retour = importDonnees(parametres)
    if retour == 1: #--- format invalide
        return 1
    #iDate,iContresens,iLongueur,iVitesse,iVitmoy,iPoids,iPoidsEssieu,iDistanceEssieu,ligneInfluence,taillePont,enregistrement
    else: #--- filtrage des lignes, creation du fichier trafic filtre et creation des matrices pour le calcul
        iDate = retour[0]
        iContresens = retour[1]
        iLongueur = retour[2]
        iVitesse = retour[3]
        iVitmoy = retour[4]
        iPoids = retour[5]
        iPoidsEssieu = retour[6]
        iDistanceEssieu = retour[7]
        ligneInfluence = retour[8]
        taillePont = retour[9]
        enregistrement = retour[10]
        cheminFiltre = parametres.cheminFichierTrafic.replace('.','_FILTRE.')
        acquisition = filtrage(cheminFiltre,enregistrement,parametres,ligneInfluence,iDate,iContresens,iLongueur,iVitesse,iVitmoy,iPoids,iPoidsEssieu,iDistanceEssieu,taillePont)
    
        #calcul des effets au cours du temps
        if 'effet'in parametres.listeHisto:
            effet = acquisition.calculEffetTotal(cheminSortie,parametres.pas)
    
        date2 = datetime.today()
        print(date2 - date1)
    
        acquisition.createListeHisto(parametres.listeHisto)
        print 'Calculs terminees'
        return 0

def createHistogramme(vecteur, titre):
    """Creation de l'histogramme choisi"""
    plt.figure()
    n, bins, patches = plt.hist(np.asarray(vecteur, dtype=float), normed=1, facecolor='b', alpha=1)
    plt.title(titre)
    plt.xlabel('Valeurs')
    plt.ylabel(u'Frequences')
    # plt.axis([mini, maxi, 0, 10])
    plt.grid(True)
    plt.show()
    return 0 
       
def lectureHistogramme(chemin):
    """Creation de l'histogramme des effets d'un fichier deja calcule"""
    #Retrace un ancien histogramme
    #effet = np.genfromtxt(fichier,usecols=1)
    with open(chemin,'r') as fichier:
        lecture = csv.reader(fichier)
        lecture = list(lecture)
        fichier.close()
    effet = []
    for ligne in lecture:
        effet.append(float(ligne[1]))
    createHistogramme(effet,'Histogramme des effets 2')
    return 0
    
def createCamembert(vecteurNom, vecteurValeur, titre):
    plt.pie(vecteurValeur, labels=vecteurNom, startangle=0, autopct='%1.1f%%',shadow=True)
    plt.axis('equal') 
    plt.title(titre)
    plt.show()
    return 0

#####################################################
##                    MAIN                         ##
#####################################################
if __name__ == '__main__':
    date1 = datetime.today()

    # -----------------------------Recuperation des deux fichiers necessaires au calcul
    cheminFichierTrafic = "C:\Users\cwolff\Desktop\charlotte_wolff_CASTOR\TestTRAFIC.csv"
    cheminFichierLigneInfluence = "C:\Users\cwolff\Desktop\charlotte_wolff_CASTOR\donnees\Pontdeuxtraveesmomentamitravee1_L=5m.inf"
    cheminSortie = "C:\Users\cwolff\Desktop\charlotte_wolff_CASTOR\effet.csv"
    # -----------------------------

    # creation des parametres de filtrage
    parametres = Parametres(cheminFichierTrafic, cheminFichierLigneInfluence)
    parametres.maj_historique()

    valider(parametres,cheminSortie,date1)
    
    lectureHistogramme("test.csv")

