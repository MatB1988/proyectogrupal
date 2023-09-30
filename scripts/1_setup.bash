# which gcloud
sudo rm -rf *
sudo apt update && sudo apt upgrade -y && sudo apt install python3-pip -y && sudo apt-get install tree -y
sudo mkdir 0_scripts 1_data && cd 1_data
sudo mkdir 1_external 2_pipeline 3_output
cd /home/henry_grupo10_v1/0_scripts
sudo wget -O python_requirements.txt https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/python_requirements.txt
cd ~

# creamos entorno de python
sudo apt install python3.8-venv && sudo apt update && sudo apt upgrade -y
sudo python3 -m venv /home/henry_grupo10_v1/env_etl
source /home/henry_grupo10_v1/env_etl/bin/activate
sudo pip install -r /home/henry_grupo10_v1/0_scripts/requirements.txt
deactivate

# instalamos entorno de R
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
sudo add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"
sudo apt install r-base -y && sudo apt update #&& sudo apt upgrade -y
cd /home/henry_grupo10_v1/0_scripts
sudo wget -O r_requirements.R https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/r_requirements.R
sudo Rscript r_requirements.R
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