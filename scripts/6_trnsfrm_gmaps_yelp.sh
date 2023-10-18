cd /home/henry_grupo10_v1/2_pipeline && sudo mkdir -p gmaps yelp

# gmaps_metadata_limpiar.py
cd ~ && [ -f gmaps_metadata_limpiar.py ] && sudo rm gmaps_metadata_limpiar.py
sudo wget -O gmaps_metadata_limpiar.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/3a_trnsfrm_gmaps_metadata_limpiar.py
sudo ~/anaconda3/envs/pandas_geo/bin/python gmaps_metadata_limpiar.py

# gmaps_metadata_geo.py
cd ~ && [ -f gmaps_metadata_geo.py ] && sudo rm gmaps_metadata_geo.py
cd ~ && sudo wget -O gmaps_metadata_geo.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/3b_trnsfrm_gmaps_metadata_geo.py
sudo ~/anaconda3/envs/pandas_geo/bin/python gmaps_metadata_geo.py

# gmaps_reviews_norm.py
cd ~ && [ -f gmaps_reviews_norm.py ] && sudo rm gmaps_reviews_norm.py
cd ~ && sudo wget -O gmaps_reviews_norm.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/4a_trnsfrm_gmaps_reviews_norm.py
sudo ~/anaconda3/envs/pandas_geo/bin/python gmaps_reviews_norm.py

# gmaps_reviews_cnsldr.py
cd ~ && [ -f gmaps_reviews_cnsldr.py ] && sudo rm gmaps_reviews_cnsldr.py
cd ~ && sudo wget -O gmaps_reviews_cnsldr.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/4b_trnsfrm_gmaps_reviews_cnsldr.py
sudo ~/anaconda3/envs/pandas_geo/bin/python gmaps_reviews_cnsldr.py

# yelp_metadata_geo.py
cd ~ && [ -f yelp_metadata_geo.py ] && sudo rm yelp_metadata_geo.py
cd ~ && sudo wget -O yelp_metadata_geo.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/5c_trnsfrm_yelp_metadata_geo.py
sudo ~/anaconda3/envs/pandas_geo/bin/python yelp_metadata_geo.py

# yelp_reviews_norm.py
cd ~ && [ -f yelp_reviews_norm.py ] && sudo rm yelp_reviews_norm.py
cd ~ && sudo wget -O yelp_reviews_norm.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/5d_trsnfrm_yelp_reviews_norm.py
sudo ~/anaconda3/envs/pandas_geo/bin/python yelp_reviews_norm.py

# business_metadata.py
cd ~ && [ -f business_metadata.py ] && sudo rm business_metadata.py
cd ~ && sudo wget -O business_metadata.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/5e_cnsldr_business_metadata.py
sudo ~/anaconda3/envs/pandas_geo/bin/python business_metadata.py

# business_reviews.py
cd ~ && [ -f business_reviews.py ] && sudo rm business_reviews.py
cd ~ && sudo wget -O business_reviews.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/5f_cnsldr_business_reviews.py
sudo ~/anaconda3/envs/pandas_geo/bin/python business_reviews.py

#gsutil -m rsync -r /home/henry_grupo10_v1/3_output/ gs://1_transform/
#gsutil -m cp /home/henry_grupo10_v1/2_pipeline/*.parquet gs://2_pipelines