# script para el setup
wget -O - https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/1_setup_1_etl.bash | bash

# para bajar a servers
cd ~/0_scripts
sudo wget https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/cronjobs/cron_1_extract.sh
sudo wget https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/cronjobs/cron_2_transform.sh
sudo wget https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/cronjobs/cron_3_cargar.sh

# cron job
00 03 * * * sh ~/0_scripts/cron_1_extract.sh >/dev/null 2>&1
00 04 * * * sh ~/0_scripts/cron_2_transform.sh >/dev/null 2>&1
00 05 * * * sh ~/0_scripts/cron_3_cargar.sh >/dev/null 2>&1