# script para el setup
wget -O - https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/1_setup_1_etl.bash | bash

# para bajar a servers
cd ~/0_scripts
[ -f cron_1_extract.sh ] && sudo rm cron_1_extract.sh
sudo wget https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/cronjobs/cron_1_extract.sh
[ -f cron_2_transform.sh ] && sudo rm cron_2_transform.sh
sudo wget https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/cronjobs/cron_2_transform.sh
[ -f cron_3_cargar.sh ] && sudo rm cron_3_cargar.sh
sudo wget https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/cronjobs/cron_3_cargar.sh

# cron job
00 01 * * * bash ~/0_scripts/cron_1_extract.sh >/dev/null 2>&1
00 02 * * * bash ~/0_scripts/cron_2_transform.sh >/dev/null 2>&1
00 03 * * * bash ~/0_scripts/cron_3_cargar.sh >/dev/null 2>&1