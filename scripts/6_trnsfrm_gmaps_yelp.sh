# gmaps_metadata_limpiar.py
cd /home/henry_grupo10_v1/2_pipeline && sudo mkdir -p gmaps yelp
cd ~ && [ -f gmaps_metadata_limpiar.py ] && sudo rm gmaps_metadata_limpiar.py
sudo wget -O gmaps_metadata_limpiar.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/3a_trnsfrm_gmaps_metadata_limpiar.py
source /home/henry_grupo10_v1/env_extract/bin/activate && sudo python3 gmaps_metadata_limpiar.py && deactivate

# gmaps_metadata_geo.py
cd ~ && [ -f gmaps_metadata_geo.py ] && sudo rm gmaps_metadata_geo.py
cd ~ && sudo wget -O gmaps_metadata_geo.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/3b_trnsfrm_gmaps_metadata_geo.py
source /home/henry_grupo10_v1/env_extract/bin/activate && sudo python3 gmaps_metadata_geo.py  && deactivate

# gmaps_reviews_norm.py
cd ~ && [ -f gmaps_reviews_norm.py ] && sudo rm gmaps_reviews_norm.py
cd ~ && sudo wget -O gmaps_reviews_norm.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/4a_trnsfrm_gmaps_reviews_norm.py
source /home/henry_grupo10_v1/env_extract/bin/activate && sudo python3 gmaps_reviews_norm.py  && deactivate

# gmaps_reviews_cnsldr.py
cd ~ && [ -f gmaps_reviews_cnsldr.py ] && sudo rm gmaps_reviews_cnsldr.py
cd ~ && sudo wget -O gmaps_reviews_cnsldr.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/4b_trnsfrm_gmaps_reviews_cnsldr.py
source /home/henry_grupo10_v1/env_extract/bin/activate && sudo python3 gmaps_reviews_cnsldr.py  && deactivate

# yelp_2parquet.py
cd ~ && [ -f yelp_2parquet.py ] && sudo rm yelp_2parquet.py
cd ~ && sudo wget -O yelp_2parquet.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/5a_trnsfrm_yelp_to_parquet.py
source /home/henry_grupo10_v1/env_extract/bin/activate && sudo python3 yelp_2parquet.py  && deactivate

# yelp_cnsldr.py
cd ~ && [ -f yelp_cnsldr.py ] && sudo rm yelp_cnsldr.py
cd ~ && sudo wget -O yelp_cnsldr.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/5b_trsnfrm_yelp_etl.py
source /home/henry_grupo10_v1/env_extract/bin/activate && sudo python3 yelp_cnsldr.py  && deactivate