# Projet Tutoré

Projet Tutoré a l'ENSTA fait par des élèves en cursus robotique qui cherchent créer un application capable de donner des coordonnées cartésiennes a cibles dans un environnement 3D avec un caméra.

## Usage

```command
run ...
```

## Equipe

Kai Zhang

Iad Abdul

David Velasquez

Ricardo RICO

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Branche iad

ExtraImgCalGround.bash est le script du processus automatique de reconstruction de la scene 3D

groundControlAndPhotogramme.bash est une ancienne version de ExtraImgCalGround.bash qui ne permet pas d'utiliser moins d'image pour la reconstruction dense (Malt) que pour la calibration et le ground control

noMarker.bash est une version de ExtraImgCalGround.bash sans les marker ArUco (pas de ground control donc)

dicoAppuisXML.py et markerToMicmac.py sont respectivement les script python de conversion du csv en xml et de detection des marker dans l'image et ecris dans un xml

affichage.py permet d'afficher les nuage de points .ply (non utilisé dans le processus)

marker.py permet de generer des marker pour impression ou des les detecter et de les afficher dans l'image (non utilisé dans le processus)
