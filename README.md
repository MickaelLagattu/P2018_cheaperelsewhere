# P2018_cheaperelsewhere
Site de comparaison d'annonces immobilières

## Installation
Pour lancer le site, il faut lancer la commande
```pip install -r requirement.txt```
pour installer les modules requis. Parfois, la bibliothèque _imageai_ ne réussit pas à s'installer via ``pip``,
on peut l'installer depuis le lien ``pip3 install https://github.com/OlafenwaMoses/ImageAI/releases/download/2.0.2/imageai-2.0.2-py3-none-any.whl``.

Ensuite, il faut télécharger le fichier wiki.fr.vec depuis https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.fr.vec et
le mettre dans le sous-dossier flaskr/ce_text_processing.

Ensuite, il faut créer un dossier qui s'appelle "images" dans flaskr/static, puis télécharger le fichier https://github.com/fizyr/keras-retinanet/releases/download/0.2/resnet50_coco_best_v2.0.1.h5 et le mettre dans le dossier flaskr/static/images

Enfin, il faut installer le logiciel mongodb Server depuis le site https://www.mongodb.com/download-center/community.
Après l'installation, il faudra lancer l'exécutable mongod.exe. Le programme fonctionne s'il affiche "Waiting for connections".

Pour lancer le serveur CheaperElsewhere, il suffit ensuite de se placer dans le dossier flaskr et de lancer la commmande
``flask run``. Le serveur démarrera et la page d'accueil sera accessible sur le navigateur à l'adresse
``localhost:5000``.
