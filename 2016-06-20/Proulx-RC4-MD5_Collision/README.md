# MMB's Strawberry Strudel Maker 3000

## Contexte
Le challenge se présente sous la forme d'une Web App de monitoring du
"Strawberry Studel Maker 3000" (GIF animé).

## Flag
(se trouve dans `webapp/flag.txt`) 42a6031175d227c7eae06d03fbc16360

## Déploiement
Il s'agit d'une Web App Python (en Bottle.py - le framework est self-contained
dans le dossier, donc PAS besoin de PIP).

En ce moment, le daemon écoute sur le port 8080, mais on peut le changer pour
80 ou le reverse proxy (devrait pas avoir d'impact).

### Exécution
`python app.py` (working directory dans le dossier `webapp`)

### Nom de domain souhaité
strudelmaker.marcusmadisonbakery.ctf

## Solution (WARNING: Spoilers)
En inspectant le code source HTML de la page, les participants découvrent que
le personnel de maintenance peut activer un mode spécial. Ils doivent deviner
(indice dans la phrase sur la page) que l'URL doit contenir
`/?support=authorized`. La page contient alors une section supplémentaire (pas
visible directement, puisque caché par CSS `display: none;`). En modifiant le
CSS (ou avec un proxy d'attaque), il peuvent découvrir un formulaire HTML
`POST` vers `/upload_license_key`. Un paramètre `hidden` appelé `debug` est
présent et mis à `false` par défaut. S'ils le changent à `true` et tente
d'upload un fichier quelconque un message d'erreur caché est mis dans la page.
Cela leur indique que le fichier doit s'appeler `license_validator.py` et doit
avoir le hash MD5 indiqué. 

À ce stade, les participants n'ayant pas le fichier en question et sachant
qu'il doit avoir un MD5 particulier, ils sont bloqués.

Les participants doivent alors avoir l'intuition de gratter un peu plus
l'arborescence de la Web App et voit le dossier `/static` (où le GIF animé est
placé). Ils peuvent essayer `flag.txt` et voir `Try harder`. Connaissant le nom
exact du fichier `license_valiator.py`, ils verront qu'une copie de celui-ci a
été oublié dans le dossier `/static`. Ils peuvent le télécharger et confirmer
par eux-même la valeur du MD5 indiqué.

L'audit du code source de `license_validator.py` leur fait remarquer un blob
binaire étrange nommé `LICENSE_KEY`, puis une fonction de validation plutôt
étrange qui contient un `Command Injection` si la license est incorrecte.
Cependant le code qui reçoit l'upload de la nouvelle license vérifie le MD5 du
fichier en entier (MD5 du fichier vs MD5 de la variable `LICENSE_KEY`).

Ainsi, les participants devinent qu'ils sont devant un challenge de collision MD5.

Un indice se trouve dans le fichier - indique que l'algo provient du
cryptograhe Wang - reconnu comme l'auteur du premier papier sur une collision
MD5 efficace et aussi pour le `Wang-type collision block`. La lecture du papier
académique ou la recherche d'outils existants (tel que `fastcoll` par Marc
Stevens) leur indique que cela ne fonctionne que si les fichiers ont un format
très particulier - soit 2 blocs de 512 bits (64 octets) consécutifs suivant une
formule de manipulation algébrique particulière pour rendre la collision très
efficace - soit `O(1)`.

L'analyse avec un éditeur hexa du fichier `license_validator.py` permet de voir
que celui-ci a "par hasard" *exactement* ce format - 64 octets de préfixe, puis
2 blocs de 64 octets aléatoires. Cela tombe *exactement* dans la variable
`LICENSE_KEY` et donc récomforte l'idée qu'il est possible de faire un
collision MD5 de ce fichier pour inverser la condition du `if/else` et
déclancher le `Command Injection` - tout en conservant la même valeur MD5
externe.

Ils doivent alors découper le fichier en 3 morceaux (préfixe, blocs de collision, suffixe).

La technique la plus efficace que j'ai trouvé est de télécharge le code source
de `fastcoll` de Marc Stevens
(http://www.win.tue.nl/hashclash/fastcoll_v1.0.0.5-1_source.zip) - on peut
simplifier considérablement le code du `main()` pour utiliser uniquement les
fonctions intéressante de lecture par bloc et l'algorithme qui détermine la
collision à partir d'un premier bloc aléatoire - `O(1)`. En passant les "blocs
de collision" extraits ci-haut, ils peuvent générer la paire.

Ils doivent alors réassembler le préfixe, l'ouput de leur programme (solution),
le suffixe. Ils peuvent alors confirmer que leur nouveau fichier a le même MD5
que le premier, mais un SHA1 différent - ainsi le `Command Injection` est alors
possible.

Ils peuvent upload leur fichier, le nommant avec le bon nom
`license_validator.py`. L'application Python est configuré en mode `autoReload`
et devrait détecter que le fichier source a changé, recompiler le `.pyc` et
redémarrer le tout.

Ils doivent devenir (en fonction du nom du paramètre de querystring est `c`).
Ils doivent conserver les paramètres `support=authorized&debug=true` pour avoir
l'output de la commande. Ils peuvent donc explorer avec `ls -lah` et voir un
fichier `flag.txt`, puis faire un `cat flag.txt`.
