# setup para transformacion
sudo mkdir -p 2_pipeline 3_output
cd /home/henry_grupo10_v1/0_scripts
sudo wget -O python_requirements.txt https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/python_requirements.txt
cd ~

# creamos entorno de python
sudo apt install python3.8-venv
sudo python3 -m venv /home/henry_grupo10_v1/env_extract
source /home/henry_grupo10_v1/env_extract/bin/activate
sudo pip install -r /home/henry_grupo10_v1/0_scripts/python_requirements.txt
deactivate
