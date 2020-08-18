from dotenv import load_dotenv # 환경변수 받는 모듈
from datetime import datetime # 파일이름을 지정하기 위함

# 노션에 상대경로 저장되는거 적어주기

# 전처리 및 data 관리
from preprocess import Preprocess
import pandas as pd
import numpy as np

import json
import os

# 환경변수 받아서 적용
# 문자열로 받기 때문에 공백문자에 주의 필요
load_dotenv(verbose = True) # .env 없으면 에러 던짐
PATH_METADATA = os.environ.get("PATH_METADATA") # 메타데이터 위치
PATH_PROCESSED_DATA = os.environ.get("PATH_PROCESSED_DATA") # 전처리 끝난 데이터 위치

# 파일 형식 
# input output 이 동일한 형태임
FILE_EXT = ".txt"
INDENT_SPACE = 2


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

    if count is 1 :
        return True
    elif count is 0 :
        raise Exception("Error : There is no file.")
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


def preprocess_data (data) :

    '''
    data 전처리 

    parameter : pandas.DataFrame
    
    return : list of dictionary
    '''
    
    processed_data = Preprocess(data)

    return processed_data


def write_file (data) :

    '''
    text extension으로 파일 저장

    parameter : list of dictionary

    return : None
    '''
    indent_space = INDENT_SPACE

    # file 이름을 임시로 지정하기 위해 datetime 을 쓴다.
    current_time = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
    file_name = current_time + FILE_EXT

    file_path = PATH_PROCESSED_DATA
    path_tmp = os.path.join(file_path, file_name)

    trial_num = 3

    while(trial_num) :

        try : 
            with open(path_tmp, "w", encoding = "utf-8") as f :
                json.dump(data, f, indent = indent_space)

            return
        except : 
            trial_num -= 1

    raise Exception("Error : File write fail.")


if __name__ == "__main__" :
    try :
        data = read_file()
        processed_data = preprocess_data(data)
        write_file(processed_data)
        
        print("0")
    except Exception as e :
        print("1", e)