#!/bin/bash


## initialisation

# add micmac to path. You can remove this and put it in your ~/.bashrc
export PATH=/home/iad/Documents/ENSTA/3A/projet_tuteure/micmac/bin:$PATH

# parameters : dataset and master image
dataset="../test/marker/bedroomMoreMarkerDataset/"
##cal_and_ground_imgs_bash="1_*" # expression reguliere tel qu'acceptee par le shell bash
cal_and_ground_imgs_MM="1_.*" # expression reguliere tel qu'acceptee par MICMAC
imgs_MM="(1_3|1_5)" 
master="1_5"
csv="3D_target.csv"

# parameters : output directory
outDir="../test/marker/AllCalibTwodepth_RadialBasic_-1_noMarker_Out/" # don't create this directory inside the dataset (or it is going to be removed)

# parameters : script
##markerToMicmacpy="./markerToMicmac.py"
##dicoAppuisXMLpy="./dicoAppuisXML.py"
thisBashFile="./ExtraImgCalGround.bash"

# parameters : other MICMAC paramters
cameraModel="RadialBasic" # RadialBasic 5 parameters, RadialStd 8 parameters
tapiocaImgResolution="-1" #1500 seems standard. -1 for full resolution
Arbitrary="Arbitrary"
##Ground_Init="Ground_Init"
Ground="Arbitrary"

# display paramters value (for debug)
echo "dataset="$dataset
echo "cal_and_ground_imgs_bash="$cal_and_ground_imgs_bash
echo "cal_and_ground_imgs_MM="$cal_and_ground_imgs_MM
echo "imgs_MM="$imgs_MM
echo "master="$master
echo "csv="$csv
echo "outDir="$outDir
echo "markerToMicmacpy="$markerToMicmacpy
echo "dicoAppuisXMLpy="$dicoAppuisXMLpy
echo "thisBashFile="$thisBashFile
echo "cameraModel="$cameraModel
echo "tapiocaImgResolution="$tapiocaImgResolution
echo "Arbitrary="$Arbitrary
echo "Ground_Init="$Ground_Init
echo "Ground="$Ground

# create the output directory
mkdir -p $outDir

# setup python3 environnement
conda activate ptutO3d


## Everything is ready. Let's go !!

# convert the csv of 3D coordinates into a mimac compatible xml file
##python3 $dicoAppuisXMLpy $dataset$csv $dataset
##echo "dicoAppuisXML.py DONE"

# detect marker in dataset images and put them into a mimac compatible xml file
##python3 $markerToMicmacpy $dataset$cal_and_ground_imgs_bash".jpg" $dataset
##echo "markerToMicmac.py DONE"


# perform calibration again using the previous one and then photogrammetry using MICMAC
mm3d Tapioca All $dataset$cal_and_ground_imgs_MM".jpg" $tapiocaImgResolution | cat > $outDir"Tapioca.log"
echo "Tapioca DONE"
mm3d Tapas $cameraModel $dataset$cal_and_ground_imgs_MM".jpg" Out=$Arbitrary | cat > $outDir"Tapas.log"
echo "Tapas DONE"
mm3d AperiCloud $dataset$cal_and_ground_imgs_MM".jpg" $Arbitrary | cat > $outDir"AperiCloud_"$Arbitrary".log"
echo "AperiCloud Arbitrary DONE "
##mm3d GCPBascule $dataset$cal_and_ground_imgs_MM".jpg" $Arbitrary $Ground_Init Dico-Appuis.xml Mesure-Appuis.xml | cat > $outDir"GCPBascule.log"
##echo "GCPBascule DONE"
##mm3d Campari $dataset$cal_and_ground_imgs_MM".jpg" $Ground_Init $Ground | cat > $outDir"Campari.log"
##echo "Campari DONE"
### mm3d AperiCloud $dataset$cal_and_ground_imgs_MM".jpg" $Ground | cat > $outDir"AperiCloud_"$Ground".log"
### echo "AperiCloud Ground DONE"
mm3d Malt GeomImage $dataset$imgs_MM".jpg" $Ground Master=$master".jpg" ZoomF=2 | cat > $outDir"Malt.log"
echo "Malt DONE"
# Usefull in dev only. To be removed. *.ply point cloud usefull only for visualisation
mm3d Nuage2Ply $dataset"MM-Malt-Img-"$master"/NuageImProf_STD-MALT_Etape_7.xml" Attr=$dataset$master".jpg" Out=$dataset$master.ply RatioAttrCarte=2 | cat > $outDir"Nuage2Ply.log"
echo "Nuage2Ply DONE"

# save output
mv $dataset"AperiCloud_"$Arbitrary".ply" $outDir # Usefull in dev only. To be removed.
mv $dataset$master".ply" $outDir # Usefull in dev only. To be removed.
mv $dataset"MM-Malt-Img-"$master"/NuageImProf_STD-MALT_Etape_7.xml" $outDir
cp $thisBashFile $outDir

# remove all data and micmac by-product in the dataset
# rm -r $dataset"/"!(*.jpg|*.csv) # for safety, comment this when you share this script with other poeple who can remove important files by mistake.

