# librerias
library(tidyverse)
library(tidycensus)
library(zctaCrosswalk)

# entorno local
#folder_local <- "/Volumes/hd_mvf_datasets/henry_data/"
# entorno local
#setwd(file.path(folder_local))

# entorno gcloud
folder_external <- "0_external"
folder_data <- "1_data_extract"
folder_uscensus <- "uscensus"

## cargamos un csv con nuestras varibales de interes
data_census_vars<-readr::read_csv(file.path(folder_external,"census_vars.csv"))
glimpse(data_census_vars)
vars_acs<-c(data_census_vars$name)
vars_acs

data_census_vars_2join <- data_census_vars %>%
  dplyr::mutate(variable = str_sub(data_census_vars$name,0,-2)) %>%
  dplyr::select(variable,variable_name)
#glimpse(data_census_vars_2join)


## extraemos la informacion
census_api<-readr::read_csv(file.path(folder_external,"census_api.csv"))
census_api_key(census_api$census_api_key)
data_zcta_raw21 = get_acs(
  geography = "zcta",
  variables = vars_acs,
  year = 2021)
#glimpse(data_zcta_raw21)

## transformamos la informacion: generamos nuestras propias variables
data_zcta_varsxarea <- data_zcta_raw21 %>%
  dplyr::rename_with(tolower) %>%
  dplyr::rename(geo_name=name) %>%
  dplyr::ungroup() %>%
  dplyr::left_join(.,data_census_vars_2join) %>%
  dplyr::select(!c(variable,moe)) %>%
  tidyr::pivot_wider(names_from = variable_name, values_from = estimate) %>%
  #dplyr::mutate(geo_check = if_else(geoid != str_sub(geo_name,7),1,0)) %>% dplyr::filter(geo_check == 1)
  dplyr::rowwise() %>%
  dplyr::mutate(
    pop_race2_prctng=(pop_race_two/pop_total_race)*100,
    econ_unemp_prctng=(econ_pop_unemp/econ_pop_total)*100) %>%
  dplyr::select(!c(pop_total_race,pop_race_two,econ_pop_total,econ_pop_unemp))
#glimpse(data_zcta_varsxarea)

## asignamos area goegrafica
data_zcta_metadata <- zctaCrosswalk::get_zcta_metadata(data_zcta_varsxarea$geoid)%>%
  dplyr::select(!contains(c("fips","numeric")))
#glimpse(data_zcta_metadata)

data_zcta_varsxarea_metadata <- left_join(
  data_zcta_varsxarea,
  data_zcta_metadata,
  by = join_by(geoid == zcta)
  ) %>%
  dplyr::rename(zcta5_geoid=geoid,zcta5_name=geo_name)
#glimpse(data_zcta_varsxarea_metadata)

## exportamos
data_zcta_varsxarea_metadata %>% write_csv(.,
  file=file.path(folder_data,folder_uscensus,"data_zcta_varsxarea.csv"))
