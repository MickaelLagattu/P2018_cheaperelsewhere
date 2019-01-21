#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 13:02:11 2019

@author: souheillassouad
"""

from bs4 import BeautifulSoup
import requests
import os
import shutil
import urllib.request
import re 



def scrapp_pap(url):
     
    req = requests.get(url)
    soup = BeautifulSoup(req.text,'lxml')
    
    #prix de vente
    a = soup.find_all("span","item-price")
    prix = a[0].contents[0]
    
   
    b=soup.find_all("ul","item-tags")
    #nombre pièces
    nombre_pieces = b[0].contents[1].contents[1].contents[0][0]
    
    #nombre chambres
    nombre_chambres = b[0].contents[3].contents[1].contents[0][0]
    
    #surface_totale
    surface_totale = b[0].contents[5].contents[1].contents[0]
    
    #arrondissement
    
    c = soup.find_all("h2")
    arrondissement = re.findall("([0-9]{5})",c[0].contents[0])[0]
    
    
    #texte 
    
    p= soup.find_all("div","margin-bottom-30")
    texte = str()
    liste = [elt for idx, elt in enumerate(p[1].contents) if idx % 2 != 0]
    for i in range(len(liste)):
        for element in liste[i].contents:
            if element.string != None:
                texte += element.string 
                texte += "\n"
                
    #
                
    
    
    
    
    