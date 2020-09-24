from dotenv import load_dotenv # 환경변수 받는 모듈
from datetime import datetime # 파일이름을 지정하기 위함

# 노션에 상대경로 저장되는거 적어주기

# 전처리 및 data 관리
from preprocess import Preprocess
import pandas as pd
import numpy as np

import json
import sys 
import os

# 환경변수 받아서 적용
# 문자열로 받기 때문에 공백문자에 주의 필요
load_dotenv(verbose = True) # .env 없으면 에러 던짐

LIST_ORIGIN = os.environ.get("LIST_ORIGIN").split(",") # 출처 리스트

PATH_METADATA_GISAID = os.environ.get("PATH_METADATA_GISAID") # GISAID 메타데이터
PATH_METADATA_WHO = os.environ.get("PATH_METADATA_WHO") # WHO 메타데이터

PATH_PROCESSED_DATA_GISAID = os.environ.get("PATH_PROCESSED_DATA_GISAID") # 전처리 후 GISAID 데이터
PATH_PROCESSED_DATA_WHO = os.environ.get("PATH_PROCESSED_DATA_WHO") # 전처리 후 WHO 데이터

ORIGIN = "" # 출처
PATH_METADATA = ""
PATH_PROCESSED_DATA = ""

# 파일 형식 
# input output 이 동일한 형태임
FILE_EXT = ".txt"


def set_excution_place () :
    
    '''
    현재 실행하는 directory 를 path/to/COVRA-ACTION-SERVER/python 으로 옮긴다.

    parameter : None

    return : None
    '''

    scriptAbsPath = os.path.abspath(__file__)
    dirname = os.path.dirname(scriptAbsPath)
    os.chdir(dirname)


def set_data_origin (data_origin) :

    '''
    전역변수 PATH_METADATA, PATH_PROCESSED_DATA 를 업데이트하는 function

    parameter : string

    return : None
    '''

    global ORIGIN
    global PATH_METADATA
    global PATH_PROCESSED_DATA

    ORIGIN = data_origin
    if ORIGIN == "GISAID" :

        PATH_METADATA = PATH_METADATA_GISAID
        PATH_PROCESSED_DATA = PATH_PROCESSED_DATA_GISAID

    elif ORIGIN == "WHO" :

        PATH_METADATA = PATH_METADATA_WHO
        PATH_PROCESSED_DATA = PATH_PROCESSED_DATA_WHO

    else :
        raise Exception("Error : Data origin is undefined.")


def is_file_exist () :

    '''
    확장자에 맞는 파일 존재를 확인하는 function

    parameter : None

    return : boolean
    '''

    file_path = PATH_METADATA
    file_ext = FILE_EXT
    count = 0

    for _ in os.listdir(file_path) :
        if _.endswith(file_ext) :
            count += 1

    if count == 1 :
        return True
    elif count == 0 :
        raise Exception("Error : There is no file. in {}" .format(file_path))
    else :
        raise Exception("Error : Too many file exist.")


def get_file_name () :

    '''
    파일이름을 가져오는 function

    parameter : None

    return : string 
    '''

    if is_file_exist() :
        
        file_path = PATH_METADATA
        file_ext = FILE_EXT
        file_name = [ _ for _ in os.listdir(file_path) if _.endswith(file_ext)]

        return file_name[0]


def read_file () :

    '''
    JSON 파일을 읽어서 pandas의 DataFrame 으로 가공해서 넘겨줌
    
    parameter : None

    return : pandas.DataFrame
    '''

    file_name = get_file_name()
    file_path = PATH_METADATA
    trial_num = 3

    path_tmp = os.path.join(file_path, file_name)

    while(trial_num) :

        try :
            with open(path_tmp, 'r', encoding = "utf-8") as f :
                json_data = json.load(f)

            return pd.DataFrame(json_data)
        
        except ValueError as e :
            raise Exception("Error : DataFrame casting fail.")

        except : 
            trial_num -= 1

    raise Exception("Error : File read fail.")


def preprocess_data (df_gisaid, df_who) :

    '''
    data 전처리 

    parameter : pandas.DataFrame
    
    return : list of dictionary
    '''
    
    json_data, processed_data = Preprocess(df_gisaid, df_who)

    return (json_data, processed_data)


def write_file (data, file_name = None) :

    '''
    text extension으로 파일 저장
    파일이름을 return 한다.

    parameter : list of dictionary

    return : string
    '''

    file_name_tmp = None
    if file_name == None : 
        current_time = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
        file_name_tmp = current_time + FILE_EXT
    else :
        file_name_tmp = file_name

    file_path = PATH_PROCESSED_DATA
    path_tmp = os.path.join(file_path, file_name_tmp)

    trial_num = 3

    while(trial_num) :

        try : 
            if type(data) == pd.DataFrame :
                data.to_json(path_tmp)
            else :
                with open(path_tmp, "w", encoding = "utf-8") as f :
                    json.dump(str(data), f)
                
            return
        except : 
            trial_num -= 1

    raise Exception("Error : File write fail.")


def main () :
    
    '''
    main function, 파일 이름을 return 한다.

    parameter : string

    return : string
    '''

    origin = None
    set_excution_place()
    
    origin = "GISAID"
    set_data_origin(origin.upper())
    df_gisaid = read_file()

    origin = "WHO"
    set_data_origin(origin.upper())
    df_who = read_file()

    json_data, processed_data = preprocess_data(df_gisaid, df_who)
    
    origin = "GISAID"
    set_data_origin(origin.upper())
    write_file(processed_data, "processed_data.txt")

    origin = "WHO"
    set_data_origin(origin.upper())
    write_file(json_data, "json_data.json")


if __name__ == "__main__" :
    try :
        main()
        print("0")
    except Exception as e :
        print("1", e)