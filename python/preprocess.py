import clade_statistics
import who_statistics
import gisaid_statistics

import pandas as pd
import numpy as np
import json
import os


PATH_GISAID = "gisaid.txt"
PATH_WHO = "who.txt"

df_gisaid = None
df_who = None


def test_stack () :
    global df_gisaid
    global df_who

    df_gisaid = pd.read_json(PATH_GISAID)
    df_who = pd.read_json(PATH_WHO)


def make_json_data (cladePopulation, death, confirmed) :

    json_data = {}

    json_data["cladePopulation"] = cladePopulation
    json_data["death"] = death
    json_data["confirmed"] = confirmed

    return json_data


def casting_df_to_float () :
    global df_gisaid
    global df_who 

    df_gisaid = df_gisaid.astype(float)
    df_who = df_who.astype(float)


def make_dummy_gisaid (who_end_scale) :
    global df_gisaid

    list_gisaid = list(np.array(df_gisaid))

    start_scale = df_gisaid.iloc[len(df_gisaid) - 1]["Date"]
    iteration_range = int(round((who_end_scale - start_scale) * 100))
    for idx in range(iteration_range) :

        list_tmp = []
        scale = round(start_scale + (idx + 1) * 0.01, 2)
        if df_gisaid.columns[0] == "Date" :
            
            list_tmp.append(scale)
            list_tmp.extend([1., 1., 1., 1., 1., 1., 1.])

        else :
            
            list_tmp = [1., 1., 1., 1., 1., 1., 1.]
            list_tmp.append(scale)

        list_gisaid.append(list_tmp)

    df_gisaid = pd.DataFrame(list_gisaid, columns = df_gisaid.columns)


def cut_gisaid (who_end_scale) :
    global df_gisaid

    df_gisaid = df_gisaid[df_gisaid["Date"] <= who_end_scale]


def make_global_dataset () :
    
    who_end_scale = df_who.iloc[len(df_who) - 1]["Date"]
    gisaid_end_scale = df_gisaid.iloc[len(df_gisaid) - 1]["Date"]

    if who_end_scale < gisaid_end_scale :
        cut_gisaid(who_end_scale)
    elif who_end_scale > gisaid_end_scale :
        make_dummy_gisaid(who_end_scale)

    data = df_gisaid.join(df_who.drop(["Date"], axis = 1))
    return data


# main preprocess
def Preprocess (df_gisaid_tmp, df_who_tmp) :

    '''
    main preprocess code

    parameter : pandas.DataFrame

    return : list of dictionary
    '''

    global df_gisaid
    global df_who

    try : 

        cladePopulation = clade_statistics.main(df_gisaid_tmp, df_who_tmp)
        df_who, death, confirmed = who_statistics.main(df_gisaid_tmp, df_who_tmp)
        df_gisaid = gisaid_statistics.main(df_gisaid_tmp, df_who_tmp)

        json_data = make_json_data(cladePopulation, death, confirmed)

        casting_df_to_float()
        learning_data = make_global_dataset()

        return (json_data, learning_data)

    except : 
        raise Exception("Error : Preprocess failed.")


# main function
if __name__ == "__main__" :
    
    test_stack()
    a, b = Preprocess(df_gisaid, df_who)
    print(b)