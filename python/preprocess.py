from dotenv import load_dotenv
import pandas as pd
import numpy as np
import json
import os

# 환경변수 받아서 적용
# 문자열로 받기 때문에 공백문자에 주의 필요
load_dotenv(verbose = True) # .env 없으면 에러 던짐
LIST_DROPPED_COLUMNS_GISAID = os.environ.get("LIST_DROPPED_COLUMNS_GISAID").split(",")
LIST_DROPPED_COLUMNS_WHO = os.environ.get("LIST_DROPPED_COLUMNS_WHO").split(",")

ORIGIN = "" # 출처
LIST_DROPPED_COLUMNS = ""


def set_origin(data_origin) :
    
    '''
    데이터 출처를 전역변수로 선언

    parameter : string

    return : None
    '''

    global ORIGIN
    ORIGIN = data_origin


def set_list_dropped_columns () :

    '''
    LIST_DROPPED_COLUMNS 를 출처에 따라서 할당

    parameter : None

    return : None
    '''

    global LIST_DROPPED_COLUMNS
    if ORIGIN == "GISAID" :

        LIST_DROPPED_COLUMNS = LIST_DROPPED_COLUMNS_GISAID

    elif ORIGIN == "WHO" :

        LIST_DROPPED_COLUMNS = LIST_DROPPED_COLUMNS_WHO

    else :
        raise Exception("Error : Data origin is undefined.")



def drop_columns (data) :
    
    '''
    DataFrame 에서 column 을 drop 한다.

    parameter : pandas.DataFrame

    return : pandas.DataFrame
    '''

    if type(data) is pd.DataFrame :

        set_list_dropped_columns()
        list_dropped_columns = LIST_DROPPED_COLUMNS
        dropped_data = data.drop(list_dropped_columns, axis = 1)

        return dropped_data

    else : 

        raise Exception("Error : Need data type as pandas.DataFrame")


def stringify_with_record_form (data) :
    
    '''
    DataFrame 을 json 형식처럼 보이는 string data 로 변환한다.

    parameter : pandas.DataFrame

    return : string
    '''
    
    # orient  = "records" 부분은 일반 Dictionary 나열 string 에서 list 요소를 wrapping 해준다.
    json_string_data = data.to_json(orient = "records") 

    return json_string_data


def parse_json_form (data) :
    
    '''
    string data를 json 모듈을 이용해서 parsing 한다.

    parameter : string

    return : list of dictionary
    '''

    parsed_data = json.loads(data)

    return parsed_data


# main preprocess
def Preprocess (data, origin) : 

    '''
    main preprocess code

    parameter : pandas.DataFrame

    return : list of dictionary
    '''

    try : 
        
        set_origin(origin)

        dropped_data = drop_columns(data)
        json_string_data = stringify_with_record_form(dropped_data)
        parsed_data = parse_json_form(json_string_data)

        return parsed_data

    except : 
        raise Exception("Error : Preprocess failed.")


# main function
if __name__ == "__main__" :

    print("Error : Preprocess test is only module.")