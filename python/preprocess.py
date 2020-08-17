from dotenv import load_dotenv
import pandas as pd
import numpy as np
import json
import os

# 환경변수 받아서 적용
# 문자열로 받기 때문에 공백문자에 주의 필요
load_dotenv(verbose = True) # .env 없으면 에러 던짐
LIST_DROPPED_COLUMNS = os.environ.get("LIST_DROPPED_COLUMNS").split(",")


def drop_columns (data) :
    
    '''
    DataFrame 에서 column 을 drop 한다.

    parameter : pandas.DataFrame

    return : pandas.DataFrame
    '''

    if type(data) is pd.DataFrame :

        list_dropped_columns = LIST_DROPPED_COLUMNS
        dropped_data = data.drop(list_drooped_columns, axis = 1)

        return dropped_data

    else : 
        raise Exception("Error : ")


def strigify_with_record_form (data) :
    
    '''
    DataFrame 을 json 형식처럼 보이는 string data 로 변환한다.

    parameter : pandas.DataFrame

    return : string
    '''
    pass


def parse_json_form (data) :
    
    '''
    string data를 json 모듈을 이용해서 parsing 한다.

    parameter : string

    return : list of dictionary
    '''
    return json.loads(data)


# main function
if __name__ == "__main__" :
    try : 
        pass
    except Exception as e :
        print("Error : preprocess test fail.", e)