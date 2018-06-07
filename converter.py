import numpy as np
import pandas as pd

file_path = '/export/home/fm247393/Perso/Donnes_individuelles_A9_Guallargues_2013.csv'

data_frame = pd.DataFrame.from_csv(file_path)
#data_frame = pd.read_csv(file_path, nrows = 1000)

nb_lignes = data_frame.shape[0]

num_1 = np.array(range(nb_lignes))+1

data_frame.set_index(num_1, inplace=True)

num_2 = np.array(['20000']*nb_lignes)

date_orig = data_frame['date']
date = np.empty_like(date_orig)
heure = np.empty_like(date_orig)

ind_ligne = 0
for line in date_orig:
      first_split = line.split(' ')
      date_split = first_split[0].split('-')
      date[ind_ligne] =str(date_split[-1]) + str(date_split[1])+str(date_split[0][-2:])
      hour_split = first_split[1].split(':')
#      print hour_split
#      hour_split = [hour_split[0], hour_split[1], hour_split[2][:2], hour_split[2][-2:]]
      heure[ind_ligne] = str(hour_split[0]) + str(hour_split[1]) + str(hour_split[2][:2])  + str(hour_split[2][3:]).ljust(2,'0') 
      ind_ligne += 1

vitesse = []
ind_vitesse = 0
for line in data_frame['vit']:
     vitesse.append(str(int(line*10000 / 3600)).zfill(3))
vitesse =np.array(vitesse)


PTC = []
for line in data_frame['poids']:
	PTC.append(str(line).zfill(4))
PTC=np.array(PTC)

longueur = []
for line in data_frame['_long']:
	longueur.append(str(line).zfill(3))
longueur=np.array(longueur)

nb_essieux =  []
for ind_nb_essieux in range(1, num_1[-1]+1):
       print ind_nb_essieux
       no_essieu = 8
       id_essieu = 'n_'+str(no_essieu)
       while  (no_essieu >0 and np.isnan(data_frame.get_value(ind_nb_essieux, id_essieu))):
           no_essieu = no_essieu - 1
           id_essieu = 'n_'+str(no_essieu)
       nb_essieux.append(no_essieu)
nb_essieux=np.array(nb_essieux)


print 'at pdp'

pdp = []
for ind_pdp in range(1, num_1[-1]+1):
     print ind_pdp
     pdp.append(str(int(round(data_frame.get_value(ind_pdp, 'pmoy_1')))).zfill(3))
     for ind_essieu in range(2,nb_essieux[ind_pdp-1]+1):
         id_dist = 'd_'+str(ind_essieu) 
         id_poids = 'pmoy_'+str(ind_essieu)
         pdp[-1] = pdp[-1]+str(int(round(data_frame.get_value(ind_pdp, id_dist)/10))).zfill(2)
         pdp[-1] = pdp[-1]+str(int(round(data_frame.get_value(ind_pdp, id_poids)))).zfill(3)
     #print ind_pdp, pdp[-1]
pdp=np.array(pdp)

total = []
for i in range(nb_lignes):
     total.append(str(num_1[i]).zfill(5) + str(num_2[i]) + str(date[i]) + str(heure[i]) + str(vitesse[i]) + str(PTC[i]) + str(longueur[i]) + str(nb_essieux[i]) + str(pdp[i]))
total = np.array(total)

#total.tofile('result.txt', sep='\n')

with open("result.txt", "a+") as myfile:
    # Convert all of the items in lst to strings (for str.join)
    total = map(str, total)  
    # Join the items together with commas                   
    line = "\n".join(total)
    # Write to the file
    myfile.write(line)


