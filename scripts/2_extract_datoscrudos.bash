cd /home/henry_grupo10_v1/1_data/1_external && sudo rm -rf *
#sudo gdown --folder --remaining-ok https://drive.google.com/drive/folders/1TI-SsMnZsNP6t930olEEWbBQdo_yuIZF
sudo gdown --folder 1TI-SsMnZsNP6t930olEEWbBQdo_yuIZF
sudo rename 'y/A-Z/a-z/' *
sudo mkdir gmaps && cd gmaps && sudo mkdir reviews_estados metadata_sitios
#cd reviews_estados && sudo gdown --folder --remaining-ok https://drive.google.com/drive/folders/19QNXr_BcqekFNFNYlKd0kcTXJ0Zg7lI6
cd reviews_estados && sudo gdown --folder --remaining-ok 19QNXr_BcqekFNFNYlKd0kcTXJ0Zg7lI6
cd ..
# gdrive henry
cd metadata_sitios && sudo gdown --folder 1RN879XLrXdtaXltzijPOmFA2Ir54mWBb

# gdrive manuel
#cd metadata_sitios && sudo gdown --folder 1olnuKLjT8W2QnCUUwh8uDuTTKVZyxQ0Z