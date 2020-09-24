import pandas as pd
import numpy as np
import json
import os


# PATH_GISAID = "gisaid.txt"
PATH_WHO = "who.txt"
PATH_COUNTRY = "country.json"

# df_gisaid = None
df_who = None
df_country = None

# ENUM_CLADES = ['S', 'L', 'V', 'G', 'GR', 'GH', 'O']

# cladePopulation = {}
death = {}
confirmed = {}

FIRST_DATE = None
END_DATE = None

# CHANGE_COUNTRY_FROM = ["South Korea", "USA"]
# CHANGE_COUNTRY_TO = ["Republic of Korea", "United States of America"]

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

    # assert_file_exist(PATH_GISAID)
    assert_file_exist(PATH_WHO)
    assert_file_exist(PATH_COUNTRY)


# def replace_country_name () :
#     global df_gisaid

#     df_gisaid = df_gisaid.replace(CHANGE_COUNTRY_FROM, CHANGE_COUNTRY_TO)


def stack_data () :
    # global df_gisaid
    global df_who
    global df_country

    file_exist_check()

    # df_gisaid = pd.read_json(PATH_GISAID)
    df_who = pd.read_json(PATH_WHO)
    df_country = pd.read_json(PATH_COUNTRY)

    # replace_country_name()


def drop_data () :
    global df_who

    df_who = df_who[["Country", "Date_reported", "New_cases", "New_deaths"]]


def drop_irregular_date () :
    global df_who

    for idx in range(len(df_who)) :
        
        date_tmp = df_who.iloc[idx]["Date_reported"]
        if len(date_tmp.split('-')) != 3 or date_tmp.endswith("XX") :
            df_who = df_who.drop(idx)


def make_data_absolute () :
    global df_who

    df_New_cases_New_deaths = np.abs(df_who[["New_cases", "New_deaths"]].astype(int))
    df_who = df_who.drop(["New_cases", "New_deaths"], axis = 1).join(df_New_cases_New_deaths)


def sort_by_Date_reported () :
    global df_who
    global FIRST_DATE
    global END_DATE

    df_who = df_who.sort_values("Date_reported")

    FIRST_DATE = df_who.iloc[0]["Date_reported"]
    END_DATE = df_who.iloc[len(df_who) - 1]["Date_reported"]


def initialize_data (df_gisaid_tmp, df_who_tmp) :
    # global df_gisaid
    global df_who

    # df_gisaid = df_gisaid_tmp
    df_who = df_who_tmp

    drop_data()
    drop_irregular_date()
    make_data_absolute()
    sort_by_Date_reported()


def date_to_percent_scale (date_str) :
    
    # 12월은 생각 안 해놓은 상태(수정 필요)
    # 2021년은 생각 안 해놓은 상태(수정 필요)

    list_date = date_str.split('-')
    month = int(list_date[1])

    return round(month_dict[month] + int(list_date[2]) / 100, 2)


def get_numeric_date(country) :

    numeric_date = []
    for date in country["Date_reported"] :
        numeric_date.append(date_to_percent_scale(date))

    return numeric_date
    

def validate_numeric_is_isometric (country, numeric_date) :

    irregular_date = []
    is_date_irregular = False
    for idx in range(len(numeric_date)) :
        
        if idx == (len(numeric_date) - 1) :
            break
        
        if numeric_date[idx + 1] != round(numeric_date[idx] + 0.01, 2) :
            irregular_date.append(np.array(country["Date_reported"])[idx])
            is_date_irregular = True
    
    if is_date_irregular : 
        print("Irregular date is detected.")
        print(irregular_date)
        return False
    else :
        return True


def get_country_data (country) :
    
    numeric_date = get_numeric_date(country)
    if not validate_numeric_is_isometric(country, numeric_date) :
        raise Exception("TT")
    
    num_of_no_data = int(numeric_date[0] * 100) - 1
    
    dummy_list = []
    for _ in range(num_of_no_data) :
        dummy_list.append(0)
        
    daily_cases = dummy_list + list(country["New_cases"])
    daily_deaths = dummy_list + list(country["New_deaths"])
    
    return (daily_cases, daily_deaths)


def get_global_data (df_all) :
    
    df_sorted = df_all.sort_values("Date_reported")
    first_scale = date_to_percent_scale(df_sorted["Date_reported"].iloc[0])
    
    num_of_no_data = int(first_scale * 100) - 1
    dummy_list = []
    for _ in range(num_of_no_data) :
        dummy_list.append(0)
        
    new_global_cases = df_sorted["New_cases"].groupby(df_sorted["Date_reported"]).sum()
    new_global_deaths = df_sorted["New_deaths"].groupby(df_sorted["Date_reported"]).sum()
    
    daily_cases = dummy_list + list(new_global_cases)
    daily_deaths = dummy_list + list(new_global_deaths)
    
    return (daily_cases, daily_deaths)


def set_death_and_confirmed () :
    global death
    global confirmed

    death["from"] = FIRST_DATE
    death["to"] = END_DATE
    confirmed["from"] = FIRST_DATE
    confirmed["to"] = END_DATE

    confirmed["global"], death["global"] = get_global_data(df_who)
    
    for each_country_str in df_country["Country"] :

        each_country = df_who[df_who["Country"] == each_country_str].sort_values("Date_reported")
        confirmed[each_country_str], death[each_country_str] = get_country_data(each_country)


def get_global_scale_date () :

    return [str(round((idx + 1) * 0.01, 2)) for idx in range(len(death["global"]))]


def make_collective_df_who () :
    global df_who

    list_global_scale = get_global_scale_date()
    list_global_confirmed = confirmed["global"]
    list_global_death = death["global"]

    list_tmp = []
    list_tmp.append(list_global_scale)
    list_tmp.append(list_global_confirmed)
    list_tmp.append(list_global_death)

    df_who = pd.DataFrame(np.transpose(list_tmp), columns = ["Date", "Confirmed", "Death"])


def preprocess_who () :
    
    make_collective_df_who()


def main(df_gisaid_tmp, df_who_tmp) :
    global df_country

    df_country = pd.read_json(PATH_COUNTRY)
    initialize_data(df_gisaid_tmp, df_who_tmp)
    set_death_and_confirmed()
    preprocess_who()

    # df_who.to_csv("who_processed.txt", index = False)
    # print(df_who)

    return (df_who, death, confirmed)


if __name__ == "__main__" :
    main()