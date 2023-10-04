# para bajar a servers
cd ~/0_scripts
sudo wget https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/cronjobs/cron_1_extract.sh
sudo wget https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/cronjobs/cron_2_transform.sh
sudo wget https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/cronjobs/cron_3_cargar.sh

# cron job
00 03 * * sun sh ~/0_scripts/cron_1_extract.sh >/dev/null 2>&1
00 04 * * sun sh ~/0_scripts/cron_2_transform.sh >/dev/null 2>&1
00 05 * * sun sh ~/0_scripts/cron_3_cargar.sh >/dev/null 2>&1

# cron jobs para setup
wget -O - https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/1_setup_1_etl.bash | bash

# ejemplo crons jobs para ETL
cd ~/1_etl && wget -O - https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/2_extract_datoscrudos.bash | bash ;
cd ~/1_data && sudo wget -O transformar_v1.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/3_transformar_v1.py;
sudo python3 transformar_v1.py && gcloud storage cp ~/3_output/* gs://1_etl_output/ --recursive