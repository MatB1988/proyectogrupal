# setup para extraction
#which gcloud
#sudo rm -rf *
sudo apt update -qq -y && sudo apt upgrade -qq -y
sudo apt-get install tree -qq -y
sudo apt install rename  -qq -y
#sudo apt install unzip  -qq -y
sudo apt install pip -qq -y
#sudo pip install -U --no-cache-dir gdown
sudo pip install gdown
#pip install testresources google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 google-cloud-storage
sudo apt autoremove -qq -y
sudo mkdir -p 0_scripts

# setup para transformacion
sudo mkdir -p 2_pipeline 3_output

##### Anaconda: Entornos de python 3.10
# Instalamos anaconda
cd ~ && sudo mkdir -p downloads
cd downloads && sudo sudo wget https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh
#-b flag Batch mode with no PATH modifications to ~/.bashrc.
# Assumes that you agree to the license agreement.
# Does not edit the .bashrc or .bash_profile files.
cd ~ && bash ~/downloads/Anaconda3-2023.09-0-Linux-x86_64.sh -b
export PATH=$PATH:/anaconda3/bin
sudo ~/anaconda3/bin/conda init && bash -l
sudo ~/anaconda3/bin/conda config --set auto_activate_base false
sudo ~/anaconda3/bin/conda update --name base -c defaults conda

# entorno geopandas
cd ~/0_scripts
[ -f python_req_geopandas.txt ] && sudo rm python_req_geopandas.txt
sudo wget -O python_req_geopandas.txt https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/python_req_geopandas.txt
sudo ~/anaconda3/bin/conda create --yes --name pandas_geo python=3.10
sudo ~/anaconda3/bin/activate pandas_geo
sudo ~/anaconda3/bin/conda config --env --append channels conda-forge
sudo ~/anaconda3/bin/conda install --name pandas_geo --yes --file ~/0_scripts/python_req_geopandas.txt
sudo ~/anaconda3/bin/deactivate
sudo ~/anaconda3/bin/conda update --name pandas_geo --yes --all

# entorno ML
cd ~/0_scripts
[ -f python_req_scikit.txt ] && sudo rm python_req_scikit.txt
sudo wget -O python_req_scikit.txt https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/python_req_scikit.txt
sudo ~/anaconda3/bin/conda create --yes --name pandas_scikit python=3.10
sudo ~/anaconda3/bin/activate pandas_scikit
sudo ~/anaconda3/bin/conda config --env --append channels conda-forge
sudo ~/anaconda3/bin/conda install --name pandas_scikit --yes --file ~/0_scripts/python_req_scikit.txt
sudo ~/anaconda3/bin/deactivate
sudo ~/anaconda3/bin/conda update --name pandas_scikit --yes --all

#### R
# instalamos entorno de R
sudo apt update
sudo apt install -y software-properties-common ca-certificates apt-transport-https gnupg dirmngr
# add the signing key (by Michael Rutter) for these repos
wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | sudo tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
# add the R 4.0 repo from CRAN -- adjust 'focal' to 'groovy' or 'bionic' as needed
sudo add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"
sudo apt install  -y r-base

# Instalamos Librerias de R

# Dependencias
# tidyverse requirements
sudo add-apt-repository  -y ppa:c2d4u.team/c2d4u4.0+ && sudo apt update
sudo apt-get install -y libssl-dev libcurl4-openssl-dev unixodbc-dev libxml2-dev libmariadb-dev libfontconfig1-dev libharfbuzz-dev libfribidi-dev libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev
# tidycensus requirements
#sudo apt-get install -y libssl-dev libudunits2-dev libgdal-dev
sudo apt-get install -y libmysqlclient-dev default-libmysqlclient-dev libudunits2-dev libgdal-dev
# to allow the use of build-dep
#sudo cp /etc/apt/sources.list /etc/apt/sources.list~
#sudo sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list
#sudo apt-get update # but does not solve: E: Unable to find a source package for install
#sudo apt-get build-dep install -y r-cran-tidycensus E: Unable to find a source package for install
sudo apt update -qq -y

# Librerias
sudo R -e 'install.packages("xml2", dependencies = T, INSTALL_opts = c("--no-lock"))'
cd ~/0_scripts
[ -f r_requirements.R ] && sudo rm r_requirements.R
sudo wget -O r_requirements.R https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/r_requirements.R
sudo Rscript r_requirements.R
cd ~
sudo apt autoremove -y && sudo apt update -qq -y && sudo apt upgrade -qq -y

# Resultados
#sudo ~/anaconda3/bin/conda list
#sudo R --version