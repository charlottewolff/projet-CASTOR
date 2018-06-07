#!/ usr/bin/ python3

# -* - coding : utf -8 -* -

""" Auteur : Charlotte Wolff
    Date d'implementation : 16/12/2016
"""

import numpy as np
import matplotlib as ptl


"""
Classe Parametres
"""


class Parametres:
    def __init__(self,cheminFichierTrafic,cheminFichierLigneInfluence,pas=1,vMoyenne=80,minPoids=10,maxPoids=1000000,minPoidsEssieu=10,maxPoidsEssieu=100000,minVitesse=50,maxVitesse=130,minLongueur=1,maxLongueur=1000,minLongueurEssieu=10,maxLongueurEssieu=1000,minNombreEssieu=2,maxNombreEssieu=8,listeHisto = ['effet','poidsEssieu','vitesse','nombreEssieu','temps']):
        self.cheminFichierLigneInfluence = cheminFichierLigneInfluence
        self.cheminFichierTrafic = cheminFichierTrafic
        self.pas = pas
        self.nbEssieux = maxNombreEssieu
        self.vMoyenne = vMoyenne
        self.minPoids = minPoids
        self.maxPoids = maxPoids
        self.minPoidsEssieu = minPoidsEssieu
        self.maxPoidsEssieu = maxPoidsEssieu
        self.minVitesse = minVitesse
        self.maxVitesse = maxVitesse
        self.minLongueur = minLongueur
        self.maxLongueur = maxLongueur
        self.minLongueurEssieu = minLongueurEssieu
        self.maxLongueurEssieu = maxLongueurEssieu
        self.minNombreEssieu = minNombreEssieu
        self.maxNombreEssieu = maxNombreEssieu
        self.listeHisto = listeHisto

        print 'Acquisition des parametres de filtrage'

    def affiche(self):
        print('pas : ',self.pas)
        print('Nombre Essieux : ',self.nbEssieux)
        print('Vitesse moyenne : ',self.vMoyenne)
        print(self.minPoids,'< Poids < ',self.maxPoids)
        print(self.minPoidsEssieu, '< Poids sur Essieu< ', self.maxPoidsEssieu)
        print(self.minVitesse, '< Vitesse < ', self.maxVitesse)
        print(self.minLongueur, '< Longueur < ', self.maxLongueur)
        print(self.minLongueurEssieu, '< Longueur entre essieux < ', self.maxLongueurEssieu)
        print('Liste des histogrammes a afficher : ')
        for histo in self.listeHisto:
            print histo
        return 0

    def maj_historique(self,chemin="./historique.txt"):
        historique = open(chemin, "w")
        historique.write(self.cheminFichierLigneInfluence+'\n')
        historique.write(self.cheminFichierTrafic+'\n')
        historique.write(str(self.pas)+'\n')
        historique.write(str(self.vMoyenne)+'\n')
        historique.write(str(self.minPoids)+'\n')
        historique.write(str(self.maxPoids)+'\n')
        historique.write(str(self.minPoidsEssieu)+'\n')
        historique.write(str(self.maxPoidsEssieu)+'\n')
        historique.write(str(self.minVitesse)+'\n')
        historique.write(str(self.maxVitesse)+'\n')
        historique.write(str(self.minLongueur)+'\n')
        historique.write(str(self.maxLongueur)+'\n')
        historique.write(str(self.minLongueurEssieu)+'\n')
        historique.write(str(self.maxLongueurEssieu)+'\n')
        historique.write(str(self.minNombreEssieu)+'\n')
        historique.write(str(self.maxNombreEssieu)+'\n')
        historique.write(str(self.listeHisto)+'\n')
        historique.close()
        return 0


if __name__ == '__main__':
    print('TEST : Classe des parametres')
    cheminFichierTrafic = "C:\Users\cwolff\Desktop\moindre_carre\CASTOR\TestTRAFIC.csv"
    cheminFichierLigneInfluence = "C:\Users\cwolff\Desktop\moindre_carre\CASTOR\Pontdeuxtraveesmomentamitravee1_L=5m.inf"
    parametres = Parametres(cheminFichierTrafic,cheminFichierLigneInfluence)
    parametres.maj_historique()
