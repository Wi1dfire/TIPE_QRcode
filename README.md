# Conseils

* Programmation objets
* Principes de programation : SOLID
* Versioning via git et github --> ok
* Typing python --> ok
* Specifier ses dependences requirements.txt (installation via `pip install -r requirements.txt`) --> ok
  * voir `pip freeze > requirements.txt`
* Utilisation de `venv` pour garder ses dependences propres --> ok
  * Creation de venv: `python -m venv .venv`
* Ecrire du code python avec des paquets

# Tâches à faire


* Généralement
  * placer des kwargs dans les fonctions
* Dans main.py
  * Placer les cases en arg des fct `lecture` et `ecriture` une fois les fonctions `encode` et `decode` suffisemment aboutit (voir terminé)
  * écrire la fct `reedsolomon_decode`
  * 2 bit en plus dans un 'Hello World' dans la fonction `encode_info`
* Dans image_QRcode_to_liste.py
  * revoir `recalibrage`
* Dans structure.py
  * trouver les `emplacement des motif d'alignement` et la `taille` des QRcode en foonction des versions
* Dans reed-solomon.py
  * Tout