# kpi_popularidad_gmaps.py
cd ~ && [ -f kpi_popularidad_gmaps.py ] && sudo rm kpi_popularidad_gmaps.py
sudo wget -O kpi_popularidad_gmaps.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/7a_kpi_popularidad_gmaps.py
source /home/henry_grupo10_v1/env_extract/bin/activate && sudo python3 kpi_popularidad_gmaps.py && deactivate