Libsne
===========

Librairie Python gérant les échanges synchrones de numéros uniques avec le
Système National d'Enregistrement (SNE) des demandes de logements sociaux dans
le cadre de leur gestion.
----------

Cette librairie permet de gérer plusieurs étapes dans le processus
d'échanges de numéros uniques SNE :

- Récupération d'une chaîne de caractères ou d'un arbre lxml.etree
représentant la structure XML de la demande de logement
- Construction du message SOAP à envoyer au serveur SNE selon le protocole
XOP/MTOM (comme spécifié dans le cahier des charges des interfaces SNE:
<http://sne.info.application.logement.gouv.fr/IMG/pdf/cahier_des_charges_des_interfaces_sne_v5_cle749ba4.0-20170208>).
- Échanges avec le serveur SNE selon le protocole HTTPS/TLS grâce à
l'authentification et la signature par système de certificats.
- Analyse de la réponse du serveur SNE, construction des exceptions selon le
type d'erreur (enveloppe SOAP, anomalies dans le XML, ...), ou retour de
réponse si pas d'erreur.

5 services Web (sur les 6 proposés par SNE, voir cahier des charges) sont
disponibles. Au sein de la librairie, ces services sont définis en enlevant le
"get" et en remplaçant la première lettre par une minuscule (ex :
"getDemandeLogement" devient "demandeLogement") :

- getNumUnique ayant comme paramètre la demande de logement sous forme de
chaîne de caractères représentant la structure XML de la demande (paramètre
"xml").
- getDemandeLogement ayant comme paramètre le numéro unique SNE (paramètre
"num_unique").
- getDoublons ayant comme paramètre une demande de logement partielle sous
forme de chaîne de caractères représentant la structure XML de la demande
(paramètre "xml").
- (getNouveauxDaloDepuisLe ayant comme paramètre la date à partir de laquelle
chercher les nouveaux DALO (paramètre "date", format
"YYYY-MM-DDTHH:MM:SS.s+HH:MM" par rapport à UTC).)
- (getDemandesRadieesDepuisLe ayant comme paramètre la date à partir de
laquelle chercher les nouvelles demandes radiées (paramètre "date", format
"YYYY-MM-DDTHH:MM:SS.s+HH:MM" par rapport à UTC).)

Ces deux derniers services ne fonctionnent pas correctement, améliorations bienvenues :)

La librairie est compatible Python 2 et Python 3.

# Installation

En tant que logiciel libre, il est préférable d'utiliser la librairie SNE sur
les systèmes d'exploitation Linux (Debian, Ubuntu, Mint, ...).

## Installation via PIP

La librairie SNE (version alpha) est disponible sur PyPI et peut être installée
en ligne de commande :

    pip install --pre libsne

## Installation via Git

La librairie SNE est disponible sur <https://forge.cliss21.org/cliss21/libsne>
et peut être clonée via Git :

    git clone https://forge.cliss21.org/cliss21/libsne.git

# Configuration

Les fichiers ressources sont ajoutés automatiquement lors de l'installation. Cependant, ils peuvent
changer à tout moment ! Se renseigner sur
<http://sne.info.application.logement.gouv.fr/applications-interfacees-r48.html>

# Comment l'utiliser

## Python
 
Pour utiliser la librairie SNE depuis un code externe Python, il faut appeler
la fonction echanger qui prend en paramètres le nom du service, le chemin du
fichier contenant la chaîne publique de certificats, le chemin du fichier
contenant la clé privée, optionnellement le nom d'hôte de SNE (défaut à
"nuu-ws.ecole.application.developpement-durable.gouv.fr" sur le port 443 si
non fourni) et le paramètre du service sous forme de kwargs.

Exemples :

    reponse_serveur = libsne.echanger("demandeLogement", "certificats/public/fullchain.pem", "certificats/prive/key.pem", num_unique="0123456789ABCDEFGH")
    reponse_serveur = libsne.echanger("numUnique", "certificats/public/fullchain.pem", "certificats/prive/key.pem", xml=xml_demande)
    reponse_serveur = libsne.echanger("demandesRadieesDepuisLe", "certificats/public/fullchain.pem", "certificats/prive/key.pem", date="2017-01-13T14:55:43.5+02:00") #Ne fonctionne pas correctement actuellement

## Ligne de commande

La librairie est aussi utilisable en ligne de commande. Exemples:

    ./libsne.py demandeLogement 0123456789ABCDEFGH certificats/public/fullchain.pem certificats/prive/key.pem
    ./libsne.py numUnique [xml_demande] certificats/public/fullchain.pem certificats/prive/key.pem
    ./libsne.py demandesRadieesDepuisLe 2017-01-13T14:55:43.5+02:00 certificats/public/fullchain.pem certificats/prive/key.pem #Ne fonctionne pas correctement actuellement

# Documentation

Pas de documentation officielle pour le moment, cependant les docstrings
expliquent le fonctionnement de chaque classe et chaque méthode.

# Contacts

Cliss XXI

23 avenue Jean Jaurès 62800 Liévin, France

<tech@cliss21.com>

03 21 45 78 24

<http://www.cliss21.com>

# Licence

La librairie est disponible librement sous licence GNU AGPL : 

<https://www.gnu.org/licenses/agpl.html> ou voir LICENSE
