#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 10:11:56 2018

@author: souheillassouad
"""

from bs4 import BeautifulSoup
import requests
import os
import shutil
import urllib.request
import re 



def scrapp_all_century_21():
    pre_url_page = "https://www.century21.fr/annonces/achat-appartement/d-69_lyon/s-0-/st-0-/b-0-/page-"
    i=1
    url_page = pre_url_page+str(i)+"/"
    req = requests.get(url_page)
    soup = BeautifulSoup(req.text,"lxml")
    a = soup.find_all("div","zone-photo-exclu")
    while a != None:
        l = search_links_century_21(url_page)
        for element in l:
            scrapp_century21(element)
        i +=1
            
        





def search_links_century_21(url_page):
    req = requests.get(url_page)
    soup = BeautifulSoup(req.text,"lxml")
    liste_links = []
    a = soup.find_all("div","zone-photo-exclu")
    for i in range(len(a)):
        liste_links.append("https://century21.fr"+a[i].contents[1]['href'])
    print(liste_links)
    return liste_links
    



def scrapp_century21(url):
    
    req=requests.get(url)
    source_code = req.text
    soup = BeautifulSoup(source_code,"lxml")
    
    #Prix de vente du bien 
    pre_prix_vente = soup.find_all("section","tarif")
    prix_vente = pre_prix_vente[0].contents[1].contents[1].string[:-2]
    prix_vente = prix_vente.replace(" ","")
    prix_vente = int(prix_vente)
    
    #Surface totale 
    pre_surface_totale = soup.find_all("div","box")
    surface_totale = pre_surface_totale[0].contents[3].contents[3].contents[1]
    surface_totale = surface_totale[3:-2]
    surface_totale = surface_totale.replace(",",".")
    surface_totale = float(surface_totale)
    
    #Surface habitable 
    pre_surface_habitable = soup.find_all("div","box")
    surface_habitable = pre_surface_habitable[0].contents[3].contents[5].contents[1]
    surface_habitable = surface_habitable[3:-2]
    surface_habitable = surface_habitable.replace(",",".")
    surface_habitable = float(surface_habitable)
    
    #Type d'appartement 
    
    pre_type_appartement = soup.find_all("div","box")
    type_appartement = pre_type_appartement[0].contents[3].contents[1].contents[1][3:]
    
    #Nombre pièces 
    pre_nombre_pieces = soup.find_all("div","box")
    nombre_pieces = pre_nombre_pieces[0].contents[3].contents[7].contents[1][0]
    nombre_pieces = int(nombre_pieces) 
    
    #Arrondissement et commune 
    pre_arrond_comm = soup.find_all("h1","h1_page")
    
    arrondissement = re.findall("([0-9]{2:5})",pre_arrond_comm[0].contents[0])[0]
    
    
    
    #Annonce Texte 
    pre_annonce_texte = soup.find_all("p","font16 LH19 justify")
    l=[]
    for element in pre_annonce_texte[0].contents : 
        if element.string != None : 
            l.append(element.string)
    annonce_texte = " ".join(l)    
    
    
    #Nom de l'annonce 
    titre = soup.find("title").string
    
    #Liens Images 
    pre_images = soup.find_all("a","fancybox")
    liste_liens_images = []
    for element in pre_images : 
        liste_liens_images.append(element['href'])
    del liste_liens_images[0]
    
    for i in range(len(liste_liens_images)):
        liste_liens_images[i] = "https://www.century21.com"+liste_liens_images[i]
    
    # Création répertoire annonce + stockage images annonces 
   
     
        
    print(prix_vente,surface_totale,surface_habitable,type_appartement,nombre_pieces,arrondissement,annonce_texte,titre,liste_liens_images)    
    return [prix_vente,surface_totale,surface_habitable,type_appartement,nombre_pieces,arrondissement,annonce_texte,titre,liste_liens_images]    
    
        
        

    
    
    
    
            
            
            
    
        
        
        


