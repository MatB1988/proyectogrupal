# gmaps_metadata_limpiar.py
cd ~ && [ -f gmaps_metadata_limpiar.py ] && sudo rm gmaps_metadata_limpiar.py
sudo wget -O gmaps_metadata_limpiar.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/3a_trnsfrm_gmaps_metadata_limpiar.py
source /home/henry_grupo10_v1/env_extract/bin/activate && sudo python3 gmaps_metadata_limpiar.py && deactivate