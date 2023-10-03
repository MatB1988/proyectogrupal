cd ~ && sudo mkdir -p 0_external 1_data_extract
cd /home/henry_grupo10_v1/1_data_extract
#sudo rm -rf *
# gdrive henry: yelp
#sudo gdown --folder https://drive.google.com/drive/folders/1TI-SsMnZsNP6t930olEEWbBQdo_yuIZF
#sudo rename 'y/A-Z/a-z/' *

# gdrive manuel
#sudo gdown --folder https://drive.google.com/drive/folders/1ZheujPb0-kmlZEhi_dKo6Ge9o_7dUfEg

# gdrive henry: reviews_estados
#sudo mkdir -p gmaps && cd gmaps && sudo mkdir -p reviews_estados metadata_sitios
#cd reviews_estados && sudo gdown --folder --remaining-ok 19QNXr_BcqekFNFNYlKd0kcTXJ0Zg7lI6
cd ..

# gdrive henry: metadata_sitios
#cd metadata_sitios && sudo gdown --folder 1RN879XLrXdtaXltzijPOmFA2Ir54mWBb
# gdrive manuel
#cd metadata_sitios && sudo gdown --folder https://drive.google.com/drive/folders/1olnuKLjT8W2QnCUUwh8uDuTTKVZyxQ0Z

cd /home/henry_grupo10_v1/0_external
sudo gdown 1_gDjMlGEVETNIG_iixvP5IGKE9Hjy9Vu # census_api.csv
sudo gdown 1_ohYtbNddF-M4p2xVj9XcnSd2dB2uiPa # census_vars.csv
cd /home/henry_grupo10_v1/1_data_extract && sudo mkdir -p uscensus
cd ~
sudo wget -O r_us_census.R https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/r_requirements.R
sudo Rscript r_us_census.R

# actualizamos goolge storage
gsutil -m rsync -r /home/henry_grupo10_v1/1_data_extract/* gs://0_datoscrudos/