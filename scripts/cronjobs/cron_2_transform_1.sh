cd ~ && [ -f gmaps_reviews_norm.py ] && sudo rm gmaps_reviews_norm.py
sudo wget -O gmaps_reviews_norm.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/4_etl_gmaps_rev_1_trnsfrmr.py
source /home/henry_grupo10_v1/env_extract/bin/activate && sudo python3 gmaps_reviews_norm.py