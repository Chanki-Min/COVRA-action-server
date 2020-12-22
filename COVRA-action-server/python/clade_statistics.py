import pandas as pd
import numpy as np
import json
import os


PATH_GISAID = "gisaid.txt"
# PATH_WHO = "who.txt"
PATH_COUNTRY = "country.json"

df_gisaid = None
# df_who = None
df_country = None

ENUM_CLADES = ['S', 'L', 'V', 'G', 'GR', 'GH', 'O']

cladePopulation = {}
# death = {}
# confirmed = {}

# FIRST_DATE = None
# END_DATE = None

CHANGE_COUNTRY_FROM = ["South Korea", "USA"]
CHANGE_COUNTRY_TO = ["Republic of Korea", "United States of America"]


def assert_file_exist (path) :

    path_tmp = os.path.join(os.getcwd(), path)
    if not os.path.exists(path_tmp) :
        raise Exception("Error 1 : File {} does not Exists." .format(path))


def file_exist_check () :

    assert_file_exist(PATH_GISAID)
    # assert_file_exist(PATH_WHO)
    assert_file_exist(PATH_COUNTRY)


def replace_country_name () :
    global df_gisaid

    df_gisaid = df_gisaid.replace(CHANGE_COUNTRY_FROM, CHANGE_COUNTRY_TO)


def stack_data () :
    global df_gisaid
    # global df_who
    global df_country

    file_exist_check()

    df_gisaid = pd.read_json(PATH_GISAID)
    # df_who = pd.read_json(PATH_WHO)
    df_country = pd.read_json(PATH_COUNTRY)

    replace_country_name()


def set_each_clade_statistic (df_each, country_name = "global") :
    global cladePopulation
    
    str_label = "label"
    str_data = "data"

    list_label = []
    list_data = []

    series_clade = df_each["GISAID_clade"].value_counts(dropna = True, sort = False)
    
    for str_clade in ENUM_CLADES :

        list_label.append(str_clade)
        if series_clade.keys().isin([str_clade]).any() :
            list_data.append(series_clade[str_clade])
        else :
            list_data.append(0)

    cladePopulation[country_name] = {}
    cladePopulation[country_name][str_label] = list_label
    cladePopulation[country_name][str_data] = list_data


def set_clade_statistics () :

    df_clade = df_gisaid[["GISAID_clade", "country"]]
    set_each_clade_statistic(df_clade)

    for country_name in df_country["Country"] :
        set_each_clade_statistic(df_clade[df_clade["country"] == country_name], country_name)


def main(df_gisaid_tmp, df_who_tmp) :
    global df_gisaid
    global df_country
    # global df_who

    df_gisaid = df_gisaid_tmp
    # df_who = df_who_tmp
    df_country = pd.read_json(PATH_COUNTRY)

    set_clade_statistics()
    
    return cladePopulation


if __name__ == "__main__" :
    main()