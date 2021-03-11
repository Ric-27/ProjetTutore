#!/bin/bash


## initialisation

# add micmac to path. You can remove this and put it in your ~/.bashrc
export PATH=/home/iad/Documents/ENSTA/3A/projet_tuteure/micmac/bin:$PATH

# parameters : dataset and master image
dataset="../test/marker/debug4Dataset/"
imgs_bash="1_*" # expression reguliere tel qu'acceptee par le shell bash
imgs_MM="1_.*" # expression reguliere tel qu'acceptee par MICMAC
master="1_5"
csv="3D_target.csv"

# parameters : output directory
outDir="../test/marker/debug4Out/" # don't create this directory inside the dataset (or it is going to be removed)

# parameters : script
markerToMicmacpy="./markerToMicmac.py"
dicoAppuisXMLpy="./dicoAppuisXML.py"
thisBashFile="./groundControlAndPhotogramme.bash"

# parameters : other MICMAC paramters
cameraModel="FraserBasic"
Arbitrary="Arbitrary"
Ground_Init="Ground_Init"
Ground="Ground"

# display paramters value (for debug)
echo "dataset="$dataset
echo "imgs_bash="$imgs_bash
echo "imgs_MM="$imgs_MM
echo "master="$master
echo "csv="$csv
echo "outDir="$outDir
echo "markerToMicmacpy="$markerToMicmacpy
echo "dicoAppuisXMLpy="$dicoAppuisXMLpy
echo "thisBashFile="$thisBashFile
echo "Arbitrary="$Arbitrary
echo "Ground_Init="$Ground_Init
echo "Ground="$Ground

# create the output directory
mkdir -p $outDir

# setup python3 environnement
conda activate ptutO3d


## Everything is ready. Let's go !!

# convert the csv of 3D coordinates into a mimac compatible xml file
python3 $dicoAppuisXMLpy $dataset$csv $dataset
echo "dicoAppuisXML.py DONE"

# detect marker in dataset images and put them into a mimac compatible xml file
python3 $markerToMicmacpy $dataset$imgs_bash".jpg" $dataset
echo "markerToMicmac.py DONE"

# perform camera calibration and then photogrammetry using MICMAC
mm3d Tapioca All $dataset$imgs_MM".jpg" 1500 | cat > $outDir"Tapioca.log"
echo "Tapioca DONE"
mm3d Tapas $cameraModel $dataset$imgs_MM".jpg" Out=$Arbitrary | cat > $outDir"Tapas.log"
echo "Tapas DONE"
mm3d AperiCloud $dataset$imgs_MM".jpg" $Arbitrary | cat > $outDir"AperiCloud_"$Arbitrary".log"
echo "AperiCloud Arbitrary DONE "
mm3d GCPBascule $dataset$imgs_MM".jpg" $Arbitrary $Ground_Init Dico-Appuis.xml Mesure-Appuis.xml | cat > $outDir"GCPBascule.log"
echo "GCPBascule DONE"
mm3d Campari $dataset$imgs_MM".jpg" $Ground_Init $Ground | cat > $outDir"Campari.log"
echo "Campari DONE"
mm3d AperiCloud $dataset$imgs_MM".jpg" $Ground | cat > $outDir"AperiCloud_"$Ground".log"
echo "AperiCloud Ground DONE"
mm3d Malt GeomImage $dataset$imgs_MM".jpg" $Ground Master=$master".jpg" ZoomF=2 | cat > $outDir"Malt.log"
echo "Malt DONE"
# Usefull in dev only. To be removed. *.ply point cloud usefull only for visualisation
mm3d Nuage2Ply $dataset"MM-Malt-Img-"$master"/NuageImProf_STD-MALT_Etape_7.xml" Attr=$dataset$master".jpg" Out=$dataset$master.ply RatioAttrCarte=2 | cat > $outDir"Nuage2Ply.log"
echo "Nuage2Ply DONE"

# save output
mv $dataset"AperiCloud_"$Ground".ply" $outDir # Usefull in dev only. To be removed.
mv $dataset$master".ply" $outDir # Usefull in dev only. To be removed.
mv $dataset"MM-Malt-Img-"$master"/NuageImProf_STD-MALT_Etape_7.xml" $outDir
cp $thisBashFile $outDir

# remove all data and micmac by-product
# rm -r $dataset"/"!(*.jpg|*.csv) # extra "/" just for security

