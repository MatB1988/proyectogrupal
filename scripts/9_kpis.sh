# kpi_popularidad.py
cd ~ && [ -f kpi_popularidad.py ] && sudo rm kpi_popularidad.py
sudo wget -O kpi_popularidad.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/7a_kpi_popularidad.py
sudo ~/anaconda3/envs/pandas_scikit/bin/python kpi_popularidad.py && deactivate

# kpi_satisfaccion.py
cd ~ && [ -f kpi_satisfaccion.py ] && sudo rm kpi_satisfaccion.py
sudo wget -O kpi_satisfaccion.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/7b_kpi_satisfaccion.py
sudo ~/anaconda3/envs/pandas_scikit/bin/python kpi_satisfaccion.py && deactivate

# kpi_cumplimiento.py


# kpi_unir.py
cd ~ && [ -f kpi_unir.py ] && sudo rm kpi_unir.py
sudo wget -O kpi_unir.py https://raw.githubusercontent.com/MatB1988/proyectogrupal/main/scripts/8_kpi_unir.py
sudo ~/anaconda3/envs/pandas_scikit/bin/python kpi_unir.py && deactivate