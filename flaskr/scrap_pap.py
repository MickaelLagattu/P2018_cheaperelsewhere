#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 13:02:11 2019

@author: souheillassouad
"""

from bs4 import BeautifulSoup
import requests
import urllib

import re

import time


# links=set()
#
# for i in range(1,20):
#    print("page",i)
#    response=requests.get("https://www.pap.fr/annonce/vente-immobilier-paris-75-g439-{}".format(i)).text
#    print("https://www.pap.fr/annonce/vente-immobilier-paris-75-g439-{}".format(i))
#    flag=True
#    while flag==True:
#        try:
#            index1=response.index("<a")
#            index2=response.index("a>")
#            frame=response[index1:index2]
#            # print(frame)
#            try:
#                if "Lire la suite" in frame:
#                    index3=frame.index("/annonce/")
#                    frame = frame[index3:]
#                    links.add("https://www.pap.fr"+frame[:frame.index('"')])
#            except Exception as e:
#                pass
#
#            response=response[index2+1:]
#        except Exception as e:
#            flag=False
#
#    time.sleep(3)
#
# print(links)
def scrapp_all_pap():
    url_base = "https://www.pap.fr/annonce/vente-appartement-maison-paris-75-g439-"
    for i in range(21):
        page_links = search_links_pap(url_base + str(i))
        time.sleep(2)
        for element in page_links:
            a = scrapp_pap(element)
            time.sleep(1)
            yield a, element


def search_links_pap(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")
    a = soup.findAll("a", {"class": ["img-liquid", "item-thumb "]})
    page_links = []

    for i in range(len(a)):
        if re.findall("/annonce/", a[i]['href']) != []:
            page_links.append("https://pap.fr" + a[i]['href'])
    return page_links


def scrapp_pap(url):
    prix = None
    nombre_pieces = None
    nombre_chambres = None
    surface_totale = None
    arrondissement = None
    texte = None
    titre = None

    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')

    # prix de vente
    a = soup.find_all("span", "item-price")
    try:
        prix = a[0].contents[0]
    except IndexError:
        pass

    b = soup.find_all("ul", "item-tags")
    # nombre pièces
    try:
        nombre_pieces = b[0].contents[1].contents[1].contents[0][0]
    except IndexError:
        pass
    # nombre chambres
    try:
        nombre_chambres = b[0].contents[3].contents[1].contents[0][0]
    except IndexError:
        pass
    # surface_totale
    try:
        surface_totale = b[0].contents[5].contents[1].contents[0]
    except IndexError:
        pass
    # arrondissement

    c = soup.find_all("h2")
    try:
        arrondissement = re.findall("([0-9]{5})", c[0].contents[0])[0]
    except IndexError:
        pass

    # texte

    p = soup.find_all("div", "margin-bottom-30")
    lista_texte = list()
    try:
        liste = [elt for idx, elt in enumerate(p[1].contents) if idx % 2 != 0]
        for i in range(len(liste)):
            for element in liste[i].contents:
                if element.string != None:
                    lista_texte.append(element.string.replace("\n", "."))
        texte = re.sub("\r|\t|\n", " ", " ".join(lista_texte))
    except Exception:
        pass

        # Titre

    t = soup.find_all("h1")
    try:
        titre = t[0].contents[0].string + " " + t[0].contents[1].string
    except IndexError:
        pass
        # Liens_Images
    im = soup.find_all("a", "img-liquid owl-thumb-item")
    liste_liens_images = []
    try:
        for i in range(len(im)):
            liste_liens_images.append(im[i].contents[1]['src'])
    except IndexError:
        pass

    # identifiant annonce + site
    site = "pap"
    identifiant = re.findall("r[0-9]{7,}", url)
    site_identifiant = site + " " + identifiant[0]
    
    # extractions_images
    try:
        identifiant_image = site+identifiant[0]
        for i,element in enumerate(liste_liens_images):
            urllib.request.urlretrieve(element,"/static/images/"+identifiant_image + str(i))
    except urllib.error.HTTPError:
        pass
    
    return (prix, nombre_pieces, nombre_chambres, surface_totale, arrondissement, liste_liens_images, texte, titre,
            site_identifiant)

#    for i,element in enumerate(links) :
#        req = requests.get(element)
#        soup = BeautifulSoup(req.text,"lxml")
#        p= soup.find_all("div","margin-bottom-30")
#        lista_texte = list()
#        liste = [elt for idx, elt in enumerate(p[1].contents) if idx % 2 != 0]
#        print(element)
#        print("\n Annonce"+str(i))
#        for i in range(len(liste)):
#            for element in liste[i].contents:
#                if element.string != None:
#                    lista_texte.append(element.string.replace("\n","."))



