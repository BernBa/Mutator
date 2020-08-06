#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 09:13:26 2020

@author: bbauer
"""

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
# import csv
# import subprocess
import os


# =============================================================================
#  the csv.file needs to contain the following columns: 
#  ID_unique_number, Morph, Analysis, Lemma
#  Part_Of_Speech, Gender, Classification, Mutation, Causing_Mutation
#  open the csv-file as pandas dataframe
#  always check that the file is in utf-8
# =============================================================================

inputfile = "/Users/bbauer/Dropbox/Programming/Mutator/csv_files/07.csv"
outputname = inputfile[-6:-4]
df = pd.read_csv(inputfile, encoding="utf-8")
df.sort_values(by=['ID_unique_number'])

# Establish the necessary lists
IDs = []
nextIDs = []
mutIDs = []
mutID = []
muti = []
Mutated = []
LenMut = []
mutate = []
Non_Mutated = []
Causing = []
Non_Causing = []


# =============================================================================
# List of mutable letters
# =============================================================================
Lenition = ["m", "n", "r", "l", "s", "f", "p", "c", "t", "b", "d", "g",
            "M", "N", "R", "L", "S", "F", "P", "C", "T", "B", "D", "G"]
Lenited = ["ḃ", "ċ", "ḋ", "ḟ", "ġ", "ṁ", "ṗ", "ṡ", "ṫ",
           "Ḃ", "Ċ", "Ḋ", "Ḟ", "Ġ", "Ṁ", "Ṗ", "Ṡ", "Ṫ"]
Leni = ["h"]
Nasalisation = ["p", "c", "t", "b", "d", "g", "m", "n", "r", "l", "s", "f", "a", "e", "i", "o", "u",
                "P", "C", "T", "B", "D", "G", "M", "N", "R", "L", "S", "F", "A", "E", "I", "O", "U",
                "á", "é", "í", "ó", "ú", "Á", "É", "Í", "Ó", "Ú"]
Nasi = ["na", "ne", "ni", "no", "nu", "ṅa", "ṅe", "ṅi", "ṅo", "ṅu",
        "ná", "né", "ní", "nó", "nú", "ṅá", "ṅé", "ṅí", "ṅó", "ṅú",
        "nd", "ng", "ṅd", "ṅg", "nn", "ṅn",
        "mb", "mm", "ṁb", "ṁm", "rr", "ll"]
Gemination = ["p", "c", "t", "b", "d", "g", "m", "n", "r", "l", "s", "f", "a", "e", "i", "o", "u",
              "P", "C", "T", "B", "D", "G", "M", "N", "R", "L", "S", "F", "A", "E", "I", "O", "U",
              "á", "é", "í", "ó", "ú", "Á", "É", "Í", "Ó", "Ú"]
Gemi = ["ha", "he", "hi", "ho", "hu", "há", "hé", "hí", "hó", "hú", 
        "hA", "hE", "hI", "hO", "hU", "hÁ", "hÉ", "hÍ", "hÓ", "hÚ",
        "pp", "cc", "tt", "bb", "dd", "gg", "mm", "nn", "rr", "ll", "ss", "ff",
        "pP", "cC", "tT", "bB", "dD", "gG", "mM", "nN", "rR", "lL", "sS", "fF"]

# Ask which kind of mutation we are looking for
mutation = input("Are you looking for (1) Lenition, (2) Nasalisation or (3) Gemination? ") 

# Enter up to four conditions
field1, value1 = input("Enter the field and the value ('Analysis, dat.sg')" + "\n" + "Double-enter or 'n' to end the conditions: ").split(", ")
item = (df[field1]  == value1)
sf = df.loc[item]

more = input("More?")
if more == "n":
    IDs = sf.ID_unique_number.tolist()
else:
    field2, value2 = input("Enter the field and the value: ").split(", ")
    item = (df[field2]  == value2)
    sf2 = sf.loc[item]
    IDs = sf2.ID_unique_number.tolist()
    more = input("More?")
    if more == "n":
        pass
    else:
        field3, value3 = input("Enter the field and the value: ").split(", ")
        item = (df[field3]  == value3)
        sf3 = sf2.loc[item]
        IDs = sf3.ID_unique_number.tolist()
        more = input("More?")
        if more == "n":
            pass
        else:
            field4, value4 = input("Enter the field and the value: ").split(", ")
            item = (df[field4]  == value4)
            sf4 = sf3.loc[item]
            IDs = sf4.ID_unique_number.tolist()
            

# Set the names of the sfs to "sf"       
try:
    sf4
except NameError:
    pass
else:
    sf4 = sf
    try:
        sf3
    except NameError:
        pass
    else:
        sf3 = sf
        try:
            sf2
        except NameError:
            pass
        else:
            sf2 = sf

# Make a list of IDs for the following morphs
for n in IDs:
    nextIDs.append(n+1)   
    
# =============================================================================
# Looking at the Mutations
# =============================================================================
    
sf = df[df['ID_unique_number'].isin(nextIDs)]
sf['Muti'] = sf['Morph'].str[:1].copy(deep=True)    
    
# Lenition
if mutation == "1":     
    lf = sf[sf['Muti'].isin(Lenited)]
    if lf.empty is False:
        LenMut = lf.ID_unique_number.tolist()
    mf = sf[sf['Muti'].isin(Lenition)]
    if mf.empty is False:
        mutID = mf.ID_unique_number.tolist()

    # Make lists of lenited and non-lenited following morphs
    mf['Mor'] = mf['Morph'].str[1:2].copy(deep=True)
    muta = mf[mf['Mor'].isin(Leni)].copy(deep=True)
    nomu = mf[~mf['Mor'].isin(Leni)].copy(deep=True)
    mutate = muta.ID_unique_number.tolist()
    if not LenMut:
        Mutated = mutate
    else:
        Mutated = mutate + LenMut
    Non_Mutated = nomu.ID_unique_number.tolist()
    mutation = 'Lenition'

# Nasalisation
elif mutation == "2":   
    nf = sf[sf['Muti'].isin(Nasalisation)].copy(deep=True)
    if nf.empty is False:
        mutIDs = nf.ID_unique_number.tolist()
    
    nf['Mor'] = nf['Morph'].str[:2].copy(deep=True)
    nf['Lem'] = nf['Lemma'].str[:2].copy(deep=True)
    for x, y in zip(nf['Mor'], nf['Lem']):
        if x != y:
            muta = nf[nf['Mor'].isin(Nasi)]
            nomu = nf[~nf['Mor'].isin(Nasi)]
    
    Mutated = muta.ID_unique_number.tolist() #Achtung wenn nix nasaliert is – problem oida!
    Non_Mutated = nomu.ID_unique_number.tolist()  
    mutation = 'Nasalisation'
    

# Gemination
else:                   
    nf = sf[sf['Muti'].isin(Gemination)].copy(deep=True)
    if nf.empty is False:
        mutIDs = nf.ID_unique_number.tolist()
    
    nf['Mor'] = nf['Morph'].str[:2].copy(deep=True)
    nf['Lem'] = nf['Lemma'].str[:2].copy(deep=True)
    for x, y in zip(nf['Mor'], nf['Lem']):
        if x != y:
            muta = nf[nf['Mor'].isin(Gemi)].copy(deep=True)
            nomu = nf[~nf['Mor'].isin(Gemi)].copy(deep=True)
    
    Mutated = muta.ID_unique_number.tolist()
    Non_Mutated = nomu.ID_unique_number.tolist()  
    mutation = 'Gemination'
  

# =============================================================================
# Make lists of causing and non-causing mutation and double-check them
# =============================================================================
for c in Mutated:
    Causing.append(c-1)
for nc in Non_Mutated:
    Non_Causing.append(nc-1)


mutatedones = Causing + Mutated
nonmutatedones = Non_Causing + Non_Mutated

# Causing mutations
mf = df[df['ID_unique_number'].isin(mutatedones)]
mf.sort_values(by=['ID_unique_number'], inplace=True)
# The subframe is written to a .csv-file and opened in Libreoffice to double-check
mfcsv = '/Users/bbauer/Dropbox/Programming/Mutator/check_csv/' + outputname + '_mutated.csv'
mf.to_csv(r'/Users/bbauer/Dropbox/Programming/Mutator/check_csv/' + outputname + '_mutated.csv', index = False)
command = ('open ' + mfcsv)
os.system('cd check_csv')
os.system(command)

# Change Causing/Mutated
change = input('Have you checked the .csv-file? Which "Causing" need(s) to be removed? ')
if change:
    changelist = change.split(", ")
    for ch in changelist:
        ch = int(ch)
        Causing.remove(ch)
        Mutated.remove((ch+1))
        Non_Causing.append(ch)
        Non_Mutated.append((ch+1))


# The subframe is written to a .csv-file and opened in Libreoffice to double-check
nmf = df[df['ID_unique_number'].isin(nonmutatedones)]
nmf.sort_values(by=['ID_unique_number'], inplace=True)
nmfcsv = '/Users/bbauer/Dropbox/Programming/Mutator/check_csv/' + outputname + '_non_mutated.csv'
nmf.to_csv(r'/Users/bbauer/Dropbox/Programming/Mutator/check_csv/' + outputname + '_non_mutated.csv', index = False)
command = ('open ' + nmfcsv)
os.system('cd check_csv')
os.system(command)
    
# Change Non_Causing/Non_Mutated
change = input('Have you checked the .csv-file? Which "Non_Causing" need(s) to be removed? ')
if change:
    changelist = change.split(", ")
    for ch in changelist:
        ch = int(ch)
        Non_Causing.remove(ch)
        Non_Mutated.remove((ch+1))
        Causing.append(ch)
        Mutated.append((ch+1))

# # Remove the brackets from the lists   
Causing = str(Causing)[1:-1] 
Non_Causing = str(Non_Causing)[1:-1]
Mutated = str(Mutated)[1:-1]
Non_Mutated = str(Non_Mutated)[1:-1]

print(mutation)

# =============================================================================
# Print the sql-statements
# =============================================================================
print('Causing: ' + "\n", "update chronhib.MORPHOLOGY" + "\n", "set Causing_Mutation = '+ ", mutation + "'" + 
      "\n", "where ID_unique_number in (", Causing, ");")
print('Mutated: ' + "\n", "update chronhib.MORPHOLOGY" + "\n", "set Mutation = '+ ", mutation + "'" + 
      "\n", "where ID_unique_number in (", Mutated, ");")
print('Not Causing: '  + "\n", "update chronhib.MORPHOLOGY" + "\n", "set Causing_Mutation = '- ", mutation + "'" + 
      "\n", "where ID_unique_number in (", Non_Causing, ");")
print('Not Mutated: ' "\n", "update chronhib.MORPHOLOGY" + "\n", "set Mutation = '+ ", mutation + "'" + 
      "\n", "where ID_unique_number in (", Non_Mutated, ");")


    
    

