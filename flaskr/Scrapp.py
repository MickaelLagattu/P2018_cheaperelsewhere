#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 10:11:56 2018

@author: souheillassouad
"""

from bs4 import BeautifulSoup
import requests

import re
import time


def scrapp_all_century_21():
    pre_url_page = "https://www.century21.fr/annonces/achat-appartement/d-75_paris/s-0-/st-0-/b-0-/page-"
    i = 1
    url_page = pre_url_page + str(i) + "/"
    req = requests.get(url_page)
    soup = BeautifulSoup(req.text, "lxml")
    a = soup.find_all("div", "zone-photo-exclu")
    while a != None:
        l = search_links_century_21(url_page)
        for element in l:
            yield scrapp_century21(element), element
            time.sleep(1)
        i += 1
        time.sleep(1)


def search_links_century_21(url_page):
    req = requests.get(url_page)
    soup = BeautifulSoup(req.text, "lxml")
    liste_links = []
    a = soup.find_all("div", "zone-photo-exclu")
    for i in range(len(a)):
        liste_links.append("https://century21.fr" + a[i].contents[1]['href'])
    print(liste_links)
    return liste_links


def scrapp_century21(url):
    nombre_pieces = None
    arrondissement = None
    req = requests.get(url)
    source_code = req.text
    soup = BeautifulSoup(source_code, "lxml")

    # Prix de vente du bien
    pre_prix_vente = soup.find_all("section", "tarif")
    prix_vente = pre_prix_vente[0].contents[1].contents[1].string[:-2]
    prix_vente = prix_vente.replace(" ", "")
    prix_vente = int(prix_vente)

    # Surface totale
    pre_surface_totale = soup.find_all("div", "box")
    surface_totale = pre_surface_totale[0].contents[3].contents[3].contents[1]
    surface_totale = surface_totale[3:-2]
    surface_totale = surface_totale.replace(",", ".")
    surface_totale = float(surface_totale)

    # Surface habitable
    pre_surface_habitable = soup.find_all("div", "box")
    surface_habitable = pre_surface_habitable[0].contents[3].contents[5].contents[1]
    surface_habitable = surface_habitable[3:-2]
    surface_habitable = surface_habitable.replace(",", ".")
    # surface_habitable = float(surface_habitable)

    # Type d'appartement

    pre_type_appartement = soup.find_all("div", "box")
    type_appartement = pre_type_appartement[0].contents[3].contents[1].contents[1][3:]

    # Nombre pièces
    pre_nombre_pieces = soup.find_all("div", "box")
    try:
        nombre_pieces = pre_nombre_pieces[0].contents[3].contents[7].contents[1][0]
    except IndexError:
        pass

    # print("avant le sleep")
    # time.sleep(5)
    # print("apres le sleep")
    # Arrondissement et commune
    pre_arrond_comm = soup.find_all("h1")

    try:
        arrondissement = re.findall("([0-9]{5})", pre_arrond_comm[0].string)[0]
    except:
        pass

    # Annonce Texte
    pre_annonce_texte = soup.find_all("p", "font16 LH19 justify")
    l = []
    for element in pre_annonce_texte[0].contents:
        if element.string != None:
            l.append(element.string)
    annonce_texte = " ".join(l)

    # Nom de l'annonce
    titre = soup.find("title").string

    # arrondissement bis
    try:
        arrondissement = re.findall("([0-9]{5})", titre)[0]
    except IndexError:
        pass
    # Liens Images
    pre_images = soup.find_all("a", "fancybox")
    liste_liens_images = []
    for element in pre_images:
        liste_liens_images.append(element['href'])
    del liste_liens_images[0]

    for i in range(len(liste_liens_images)):
        liste_liens_images[i] = "https://www.century21.com" + liste_liens_images[i]

    # site + identifiant à scrapper

    site = "century21"
    identifiant = re.findall("/[0-9]{6,}/", url)
    site_identifiant = site + " " + identifiant[0][1:-1]
    
    
    # extractions_images
    identifiant_image = site+identifiant[0][1:-1]
    for i,element in enumerate(liste_liens_images):
        urllib.request.retrieve(element,"/static/images/"+identifiant_image + str(i))  

    return [prix_vente, surface_totale, surface_habitable, type_appartement, arrondissement, nombre_pieces,
            annonce_texte, titre, liste_liens_images, site_identifiant]
    # except UnboundLocalError:
    # return [prix_vente,surface_totale,surface_habitable,type_appartement,annonce_texte,titre,liste_liens_images]












