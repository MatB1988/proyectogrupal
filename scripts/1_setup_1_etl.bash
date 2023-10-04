# setup para extraction
#which gcloud
#sudo rm -rf *
sudo apt update -qq -y && sudo apt upgrade -qq -y
sudo apt-get install tree -qq -y && sudo apt install rename  -qq -y
sudo apt install pip -qq -y
#sudo pip install -U --no-cache-dir gdown
sudo pip install gdown
#pip install testresources google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 google-cloud-storage
sudo apt autoremove -qq -y
sudo mkdir -p 0_scripts

# setup para transformacion
sudo mkdir -p 2_pipeline 3_output
cd /home/henry_grupo10_v1/0_scripts
[ -f python_requirements.txt ] && sudo rm python_requirements.txt
sudo wget -O python_requirements.txt https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/python_requirements.txt
cd ~

# creamos entorno de python
sudo apt install python3.8-venv
sudo python3 -m venv /home/henry_grupo10_v1/env_extract
source /home/henry_grupo10_v1/env_extract/bin/activate
sudo pip install -r /home/henry_grupo10_v1/0_scripts/python_requirements.txt
deactivate

# instalamos entorno de R
sudo apt update
sudo apt install software-properties-common dirmngr
# add the signing key (by Michael Rutter) for these repos
wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | sudo tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
# add the R 4.0 repo from CRAN -- adjust 'focal' to 'groovy' or 'bionic' as needed
sudo add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"
sudo apt install  -y r-base
sudo add-apt-repository  -y ppa:c2d4u.team/c2d4u4.0+ && sudo apt update
sudo apt-get install  -y r-cran-tidyverse
sudo apt-get install -y libssl-dev && sudo apt-get install -y libudunits2-dev # tidycensus requirements
sudo apt install -y libgdal-dev # tidycensus requirements
#sudo apt-get build-dep install -y r-cran-tidycensus E: Unable to find a source package for install
cd /home/henry_grupo10_v1/0_scripts
sudo wget -O r_requirements.R https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/r_requirements.R
sudo Rscript r_requirements.R
cd ~
sudo apt update -qq -y && sudo apt upgrade -qq -y
pip list --local
sudo R --version