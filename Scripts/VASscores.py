#!/usr/bin/env python
# coding: utf-8

# In[82]:


import pandas as pd 
import csv
import os
import numpy as np


sheets = pd.read_csv('PsychVariablesVOP_comma_sep.csv',sep=',')


id_vas=sheets.loc[:,['ID']].sum(axis=1)

goed_score_2=sheets.loc[:,['tevreden2','krachtig2','prettig2']].sum(axis=1)
slecht_score_2=sheets.loc[:,['boos2','gespannen2','neerslachtig2']].sum(axis=1)

goed_score_3=sheets.loc[:,['tevreden3','krachtig3','prettig3']].sum(axis=1)
slecht_score_3=sheets.loc[:,['boos3','gespannen3','neerslachtig3']].sum(axis=1)

goed_score_4=sheets.loc[:,['tevreden4','krachtig4','prettig4']].sum(axis=1)
slecht_score_4=sheets.loc[:,['boos4','gespannen4','neerslachtig4']].sum(axis=1)

DASS_gemiddelde=sheets.loc[:,['DASS_ANXIETY','DASS_DEPRESSION','DASS_STRESS']].sum(axis=1)/3
DASS_anxiety=sheets.loc[:,['DASS_ANXIETY']].sum(axis=1)
DASS_depression=sheets.loc[:,['DASS_DEPRESSION']].sum(axis=1)
DASS_stress=sheets.loc[:,['DASS_STRESS']].sum(axis=1)
RRS_Treynor_Totaal=sheets.loc[:,['RRS_Treynor_Totaal']].sum(axis=1)
RRS_Brooding=sheets.loc[:,['RRS_Brooding']].sum(axis=1)



#negatief geeft aan dat gevoelens in algemeen verslecht zijn, positief verbeterd
goed_delta=goed_score_3 - goed_score_2
slecht_delta=slecht_score_3 - slecht_score_2
delta=goed_delta - slecht_delta

#delta tussen voor en na 2e rust om brooding te controleren
goed_delta2=goed_score_4 - goed_score_3
slecht_delta2=slecht_score_4 - slecht_score_3
delta2=goed_delta2 - slecht_delta2

id_delta=np.vstack((id_vas,delta,goed_delta,slecht_delta,delta2,DASS_anxiety,DASS_depression,DASS_stress,DASS_gemiddelde,RRS_Treynor_Totaal,RRS_Brooding)).T
print(id_delta)

df = pd.DataFrame(id_delta, columns=['ID', 'VAS Delta', 'pos Delta', 'neg Delta','VAS Delta 2e rust', 'anxiety DASS', 'depressie DASS', 'stress DASS', 'gem DASS', 'TT RRS', 'brooding RRS'])
df['ID'] = df['ID'].astype(int)
df.sort_values('ID',inplace=True)
df.set_index('ID',inplace=True)

df.to_csv('VASscores.csv',sep=',')

#puur uit interesse nog eens bekeken welke gevoelens voornamelijk beinvloed worden 
gespannen2=sheets.loc[:,['gespannen2']].sum(axis=1)
gespannen3=sheets.loc[:,['gespannen3']].sum(axis=1)
gespannen=gespannen3-gespannen2

boos2=sheets.loc[:,['boos2']].sum(axis=1)
boos3=sheets.loc[:,['boos3']].sum(axis=1)
boos=boos3-boos2

neerslachtig2=sheets.loc[:,['neerslachtig2']].sum(axis=1)
neerslachtig3=sheets.loc[:,['neerslachtig3']].sum(axis=1)
neerslachtig=neerslachtig3-neerslachtig2

tevreden2=sheets.loc[:,['tevreden2']].sum(axis=1)
tevreden3=sheets.loc[:,['tevreden3']].sum(axis=1)
tevreden=tevreden3-tevreden2

prettig2=sheets.loc[:,['prettig2']].sum(axis=1)
prettig3=sheets.loc[:,['prettig3']].sum(axis=1)
prettig=prettig3-prettig2

krachtig2=sheets.loc[:,['krachtig2']].sum(axis=1)
krachtig3=sheets.loc[:,['krachtig3']].sum(axis=1)
krachtig=krachtig3-krachtig2


delta_int=(delta.sum()/6)/148
print("gemiddelde verandering in totale gemoedstoestand=", delta_int)
gespannen_int=gespannen.sum()/148
print("gemiddelde verandering in gespannenheid=", gespannen_int)
boos_int=boos.sum()/148
print("gemiddelde verandering in boosheid=", boos_int)
neerslachtig_int=neerslachtig.sum()/148
print("gemiddelde verandering in neerslachtigheid=", neerslachtig_int)
tevreden_int=tevreden.sum()/148
print("gemiddelde verandering in tevredenheid=", tevreden_int)
prettig_int=prettig.sum()/148
print("gemiddelde verandering in prettigheid=", prettig_int)
krachtig_int=krachtig.sum()/148
print("gemiddelde verandering in krachtigheid=", krachtig_int)
#valt op dat er qua verandering in gemoedstoestand gemiddeld vooral een daling in tevredenheid is, gevolgd door een stijging in gespannenheid



