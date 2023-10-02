# setup para extraction
#which gcloud
sudo rm -rf *
sudo apt update -qq -y && sudo apt upgrade -qq -y
sudo apt-get install tree -qq -y && sudo apt install rename  -qq -y
sudo apt install pip -qq -y
#sudo pip install -U --no-cache-dir gdown
sudo pip install gdown
pip install testresources google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 google-cloud-storage
sudo apt autoremove -qq -y
sudo mkdir 0_scripts 1_data_extract
cd /home/henry_grupo10_v1/0_scripts && gdown 1V84jCqpgzLlKtnplEUJfAnV9Jy8_Fy2h
cd /home/henry_grupo10_v1/1_data/1_data_extract && 

# setup para transformacion
#sudo apt install python3-pip -qq -y
sudo mkdir 0_scripts 1_data && cd 1_data
sudo mkdir 1_external 2_pipeline 3_output
cd /home/henry_grupo10_v1/0_scripts
sudo wget -O python_requirements.txt https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/python_requirements.txt

cd ~

# creamos entorno de python
sudo apt install python3.8-venv
sudo python3 -m venv /home/henry_grupo10_v1/env_etl
source /home/henry_grupo10_v1/env_etl/bin/activate
sudo pip install -r /home/henry_grupo10_v1/0_scripts/python_requirements.txt
deactivate

# instalamos entorno de R
sudo apt update
sudo apt install software-properties-common dirmngr
# add the signing key (by Michael Rutter) for these repos
wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | sudo tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
# add the R 4.0 repo from CRAN -- adjust 'focal' to 'groovy' or 'bionic' as needed
sudo add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"
sudo apt install r-base -y
sudo add-apt-repository ppa:c2d4u.team/c2d4u4.0+ -y
sudo apt-get install r-cran-tidyverse -y && sudo apt-get install r-cran-tidycensus -y
cd /home/henry_grupo10_v1/0_scripts
sudo wget -O r_requirements.R https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/r_requirements.R
sudo Rscript r_requirements.R
sudo apt update -qq -y && sudo apt upgrade -qq -y
cd ~
sudo tree /home/henry_grupo10_v1/1_data

#sudo mkdir 2_ml && cd ~/2_ml
#sudo mkdir 0_scripts 1_data && cd 1_data
#sudo mkdir 1_external 2_pipeline 3_output
#cd ~
#sudo python3 -m venv ~/2_ml/env_ml
#source ~/2_ml/env_ml/bin/activate
#sudo sudo pip install pandas
#deactivate