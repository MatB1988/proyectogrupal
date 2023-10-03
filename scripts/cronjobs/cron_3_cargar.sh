#gcloud storage cp /home/henry_grupo10_v1/1_data_extract/* gs://0_datoscrudos/ --recursive
gsutil -m rsync -r /home/henry_grupo10_v1/1_data_extract/* gs://0_datoscrudos/