import pandas as pd
import numpy as np
import json
import os


PATH_GISAID = "gisaid.txt"
PATH_WHO = "who.txt"

df_gisaid = None
df_who = None

month_dict = {
                    1 : 0.00,
                    2 : 0.31,
                    3 : 0.60,
                    4 : 0.91,
                    5 : 1.21,
                    6 : 1.52,
                    7 : 1.82,
                    8 : 2.13,
                    9 : 2.44,
                    10 : 2.74,
                    11 : 3.05,
                    12 : 3.35
                }


def assert_file_exist (path) :

    path_tmp = os.path.join(os.getcwd(), path)
    if not os.path.exists(path_tmp) :
        raise Exception("Error 1 : File {} does not Exists." .format(path))


def file_exist_check () :

    assert_file_exist(PATH_GISAID)
    assert_file_exist(PATH_WHO)


def stack_data () :
    global df_gisaid
    global df_who

    file_exist_check()

    df_gisaid = pd.read_json(PATH_GISAID)
    df_who = pd.read_json(PATH_WHO)


def drop_columns () :
    global df_gisaid
    global df_who

    df_gisaid = df_gisaid[["date", "GISAID_clade"]]
    df_who = df_who[["Date_reported", "New_cases", "New_deaths"]]


def rename_columns () :
    global df_gisaid
    global df_who

    df_gisaid = df_gisaid.rename(columns = { "date" : "Date" , "GISAID_clade" : "Clade"})
    df_who = df_who.rename(columns = { "Date_reported" : "Date" })


def sort_by_date () :
    global df_gisaid
    global df_who

    df_gisaid = df_gisaid.sort_values("Date")
    df_who = df_who.sort_values("Date")


def reindex_data () :
    global df_gisaid
    global df_who

    df_gisaid = pd.DataFrame(np.array(df_gisaid), columns = df_gisaid.columns)
    df_sho = pd.DataFrame(np.array(df_who), columns = df_who.columns)


def drop_irregular_date (df_each) :

    drop_list = []
    for idx in range(len(df_each)) :
        
        date_tmp = df_each.iloc[idx]["Date"]
        if len(date_tmp.split('-')) != 3 or date_tmp.endswith("XX") :
            drop_list.append(idx)

    return df_each.drop(drop_list)


def drop_forward_date (df_each) :

    drop_list = []
    for idx in range(len(df_each)) :

        date_tmp = df_each.iloc[idx]["Date"]
        if int(date_tmp.split('-')[0]) < 2020 :
            drop_list.append(idx)

    return df_each.drop(drop_list)


def drop_rows () :
    global df_gisaid
    global df_who

    df_gisaid = df_gisaid[df_gisaid["Clade"] != ""]
    df_gisaid = pd.DataFrame(np.array(df_gisaid), columns = df_gisaid.columns)

    df_gisaid = drop_irregular_date(df_gisaid)
    df_gisaid = pd.DataFrame(np.array(df_gisaid), columns = df_gisaid.columns)
    df_gisaid = drop_forward_date(df_gisaid)

    df_who = drop_irregular_date(df_who)


def make_who_data_absolute () :
    global df_who

    df_New_cases_New_deaths = np.abs(df_who[["New_cases", "New_deaths"]].astype(int))
    df_who = df_who.drop(["New_cases", "New_deaths"], axis = 1).join(df_New_cases_New_deaths)


def initialize_data (df_gisaid_tmp, df_who_tmp) :
    global df_gisaid
    global df_who

    df_gisaid = df_gisaid_tmp
    df_who = df_who_tmp

    drop_columns()

    rename_columns()
    sort_by_date()
    reindex_data()

    drop_rows()
    make_who_data_absolute()


def clade_one_hot () :
    global df_gisaid

    df_gisaid = pd.get_dummies(df_gisaid, columns = ["Clade"])


def get_start_idx () :

    start_idx = None
    for idx in range(len(df_gisaid.columns)) :

        if df_gisaid.columns[idx].startswith("Clade") :
        
            start_idx = idx
            break

    return start_idx


def stack_clade () :
    global df_gisaid

    stack = [ 0, 0, 0, 0, 0, 0, 0 ]
    
    start_stack_idx = get_start_idx()
    arr_gisaid = np.array(df_gisaid)

    for each in arr_gisaid :
        
        for idx in range(7) :
            if stack[idx] | each[idx + start_stack_idx] :
                stack[idx] = 1
                each[idx + start_stack_idx] = 1

    df_gisaid = pd.DataFrame(arr_gisaid, columns = df_gisaid.columns)


def remove_redundant_clade () :
    global df_gisaid

    df_gisaid = df_gisaid.drop_duplicates()


def remove_redundant_date () :
    global df_gisaid

    df_gisaid = df_gisaid.sort_values("Date", ascending = False)
    df_gisaid = pd.DataFrame(np.array(df_gisaid), columns = df_gisaid.columns)

    stack_date = None
    list_of_date_reverse = list(df_gisaid["Date"])
    length_data = len(list_of_date_reverse)
    drop_list = []
    for idx in range(len(list_of_date_reverse)) :

        date = list_of_date_reverse[idx]
        if stack_date == date :
            drop_list.append(idx)

        stack_date = date

    df_gisaid = df_gisaid.drop(drop_list)


def get_date_to_percent_scale (date_str) :
    
    # 12월은 생각 안 해놓은 상태(수정 필요)
    # 2021년은 생각 안 해놓은 상태(수정 필요)

    list_date = date_str.split('-')
    month = int(list_date[1])
    day = int(list_date[2])

    return round(month_dict[month] + day / 100, 2)


def date_to_scale () :
    global df_gisaid

    list_date = df_gisaid["Date"]
    for idx in range(len(list_date)) :

        date = list_date[idx]
        list_date[idx] = str(get_date_to_percent_scale(date))

    df_gisaid = df_gisaid.drop(["Date"], axis = 1).join(pd.DataFrame(list_date, columns = ["Date"]))


def deep_copy (list_target) :

    list_tmp = []
    for each in list_target :
        list_tmp.append(each)

    return list_tmp


def make_front_dummy() :
    global df_gisaid

    list_gisaid = list(np.array(df_gisaid))
    list_gisaid_columns = df_gisaid.columns

    list_tmp = []
    start_date = float(df_gisaid.iloc[0]["Date"])
    if start_date == 0.01 :
        return
    for idx in range(round(start_date * 100) - 1) :
        
        clade_tmp = [0, 0, 0, 0, 0, 0, 0]
        date = (idx + 1) / 100

        if list_gisaid_columns[0].startswith("Date") :
            
            extended_list = deep_copy([date])
            extended_list.extend(clade_tmp)
            list_tmp.append(extended_list)
        else :

            extended_list = deep_copy(clade_tmp)
            extended_list.extend([date])
            list_tmp.append(extended_list)

    df_gisaid = pd.DataFrame(list_tmp + list_gisaid, columns = list_gisaid_columns)


def fill_middle_date() :
    global df_gisaid

    list_gisaid = list(np.array(df_gisaid))
    list_gisaid_columns = df_gisaid.columns

    full_stack_gisaid = []
    last_scale = float(df_gisaid.iloc[len(df_gisaid) -1]["Date"])
    stack_clade = None
    gisaid_idx = 0
    for idx in range(round(last_scale * 100)) :
        
        scale = str(round((idx + 1) * 0.01, 2))
        if list_gisaid_columns[0].startswith("Date") :
            
            date = str(list_gisaid[gisaid_idx][0])
            if scale == date :
                
                full_stack_gisaid.append(deep_copy(list_gisaid[gisaid_idx]))
                stack_clade = deep_copy(list(list_gisaid[gisaid_idx][1:]))
                gisaid_idx += 1

            else :
                
                list_tmp = deep_copy([scale])
                list_tmp.extend(stack_clade)
                full_stack_gisaid.append(list_tmp)
        else :

            date = str(list_gisaid[gisaid_idx][7])
            if scale == date :
                
                full_stack_gisaid.append(deep_copy(list_gisaid[gisaid_idx]))
                stack_clade = deep_copy(list(list_gisaid[gisaid_idx][:-1]))
                gisaid_idx += 1

            else :
                
                list_tmp = deep_copy(stack_clade)
                list_tmp.extend([scale])
                full_stack_gisaid.append(list_tmp)

    df_gisaid = pd.DataFrame(full_stack_gisaid, columns = list_gisaid_columns)


def make_clade_data_object () :
    global df_gisaid

    df_gisaid = df_gisaid[["Date"]].join(df_gisaid.drop(["Date"], axis = 1).astype("object"))


def preprocess_gisaid () :
    
    clade_one_hot()
    stack_clade()
    
    remove_redundant_clade()
    reindex_data()
    
    remove_redundant_date()
    sort_by_date()
    reindex_data()

    date_to_scale() 
    make_front_dummy()
    fill_middle_date()
    make_clade_data_object()


def main(df_gisaid_tmp, df_who_tmp) :

    initialize_data(df_gisaid_tmp, df_who_tmp)
    preprocess_gisaid()

    # df_gisaid.to_csv("gisaid_processed.txt", index = False)
    return df_gisaid


if __name__ == "__main__" :
    main()