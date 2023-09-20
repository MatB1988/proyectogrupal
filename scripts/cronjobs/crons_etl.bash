wget -O - https://raw.githubusercontent.com/MatB1988/proyectogrupa/main/scripts/1_setup.bash | bash

# crons jobs para ETL
cd ~/1_etl && wget -O - https://raw.githubusercontent.com/MatB1988/proyectogrupa/main/scripts/2_extract_datoscrudos.bash | bash ;
cd ~/1_etl/1_data && sudo wget -O transformar_v1.py https://raw.githubusercontent.com/MatB1988/proyectogrupa/main/scripts/3_transformar_v1.py;
sudo python3 transformar_v1.py && gcloud storage cp ~/1_etl/1_data/3_output/* gs://1_etl_output/ --recursive