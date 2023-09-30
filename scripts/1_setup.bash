# which gcloud
sudo rm -rf *
sudo apt update && sudo apt upgrade -y && sudo apt install python3-pip -y
sudo apt install python3.8-venv && sudo apt update && sudo apt upgrade -y
#sudo mkdir 1_etl && cd ~/1_etl
sudo mkdir 0_scripts 1_data && cd 1_data
sudo mkdir 1_external 2_pipeline 3_output
cd /home/henry_grupo10_v1/0_scripts
sudo wget -O requirements.txt https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/3_transformar_v1.py
cd ~
sudo python3 -m venv /home/henry_grupo10_v1/env_etl
source /home/henry_grupo10_v1/env_etl/bin/activate
sudo pip install -r requirements.txt
deactivate

#sudo mkdir 2_ml && cd ~/2_ml
#sudo mkdir 0_scripts 1_data && cd 1_data
#sudo mkdir 1_external 2_pipeline 3_output
#cd ~
#sudo python3 -m venv ~/2_ml/env_ml
#source ~/2_ml/env_ml/bin/activate
#sudo sudo pip install pandas
#deactivate