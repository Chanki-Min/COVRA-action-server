from dotenv import load_dotenv
import pandas as pd
import numpy as np
import os

# json 의 list 를 받아옴
# 다시 json 형식으로 저장
# catch 로 "1 " +
# 데이터 여러개? 그냥 지워버리기
# MongoDB 바로 연동? X
# HTTP 로 전송? X
# 전처리 어디까지?
# 스크립트는 얼마나


# 환경변수 받아서 적용
# 문자열로 받기 때문에 공백문자에 주의 필요
load_dotenv(verbose = True) # .env 없으면 에러 던짐
LIST_DROPPED_COLUMNS = os.environ.get("LIST_DROPPED_COLUMNS").split(",")


# 데이터가 존재하는지 확인
def check_and_return_file_name () :

    # csv 나 tsv 파일이 존재하는지 확인
    file_path = PATH_METADATA

    file_names = [ _ for _ in os.listdir(PATH_METADATA) if _.endswith(FILE_EXT_TSV) or _.endswith(FILE_EXT_CSV) ]

    # 일단 한개 이상이면 못 진행하게 해놨음
    if len(file_names) is not 1 :
        print("ERROR : Valid file number is {}" .format(len(file_names)))
        return [False]

    return file_names


# 데이터의 차이를 비교 (안 해도 된다고..?)
def analysis_diff_data (raw_data, transmission_data = None) :
    pass


# 파일을 실제로 읽는 부분
def read_file(file_name) :
    
    path_tmp = os.path.join(PATH_METADATA, file_name)

    if file_name.endswith(FILE_EXT_CSV) :
        file_tmp = pd.read_csv(path_tmp)
    elif file_name.endswith(FILE_EXT_TSV) :
        file_tmp = pd.read_csv(path_tmp, sep = "\t")

    return file_tmp


# write file
def write_file(data) :
    
    current_time = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
    file_name = current_time + ".csv"

    path_tmp = os.path.join(PATH_PROCESSED_DATA, file_name)
    data.to_csv(path_tmp)


# column drop 
def drop_columns (data) :
    
    return data.drop(LIST_DROPPED_COLUMNS, axis = 1)


# metadata 읽는 모든 과정
def read_metadata_and_drop () :

    file_name = check_and_return_file_name()[0]

    if not file_name :
        raise Exception("ERROR : Need one tsv or csv file.")

    metadata = read_file(file_name)
    dropped_metadata = drop_columns(metadata)

    if dropped_metadata.empty :
        raise Exception("ERROR : Fail drop columns. (Is there empty?)")

    return dropped_metadata


# preprocessing data
def preprocess_data () :
    
    try : 
        data = read_metadata_and_drop()

        # TODO : preprocessing
        processed_data = data

        return processed_data
    
    except Exception as e :
        print(e)


# main function
if __name__ == "__main__" :

    data = preprocess_data()

    try : 
        write_file(data)
    except Exception("ERROR : Fail write data") as e :
        print(e)