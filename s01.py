import re
from requests import Request, Session
from fake_useragent import UserAgent
from urllib.parse import unquote
import os

from io import BytesIO
import zipfile

import xmltodict
import collections
import pandas as pd
import json
import os.path

'''
'''
apiKey       = "f1f64632cabe19da450a98456722f7bccf8d5c0f"
# apiKey = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

dartSingleAnt= "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json"

'''
    reference : https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019016
'''

def getFromDart(url, params):

    with Session() as s:
        s.headers.update({'user-agent': UserAgent().chrome})

        req = Request('GET', url, params=params)
        prepped = s.prepare_request(req)
        print(prepped.url)

        resp = s.send(prepped)

    return resp

def getSingleAccount(corp_code, ts, te):
    #
    #
    accDic   = {}
    for year in range(ts, te):

        fname = "./data/" + corp_code+ "_" + str(year)+".json"

        if os.path.isfile(fname) == True:
            with open(fname, "r") as json_file:
                data = json.load(json_file)
        else:
            param0 = {
                "crtfc_key" : apiKey, "corp_code" : corp_code, "bsns_year" : str(year), "reprt_code":"11011"
            }
            resp = getFromDart(dartSingleAnt, param0)

            '''parsing'''
            data = json.loads(resp.content)
            with open(fname, "w") as json_file:
                json.dump(data, json_file)

        if data['status'] != '000':
            print(data['status'], data['message'])
            continue

        rows = {}
        for i,  item in enumerate(data["list"]):
            if item["sj_nm"] == "재무상태표" and item["fs_div"] == "OFS":
                idx  = item["bsns_year"]
                col  = item["account_nm"]
                val  = item["thstrm_amount"]
                
                rows[col] = val        
        
        accDic[str(year)]= rows

    return accDic

'''
'''
def getAccount(*argv):
    accDic = getSingleAccount(*argv)

    df = pd.DataFrame(accDic).T
    df = df.apply( lambda x : x.str.replace(",",""))
    # df = df.astype("float")

    return df    


'''
''--------------------------------------------------------
'''
def load():
    company = pd.read_excel("./t00/data/ref.xlsx", dtype=object)
    part    = list(company['corp_code'][:-1])
    part    = ['00126380', '00401731']

    for i,com in enumerate(part):
        print(i, com)
        a = getAccount(com, 2015, 2021)

'''--------------------------------------------------------
'''
def cal00():
    company = pd.read_excel("./t00/data/ref.xlsx", dtype=object)
    part    = list(company['corp_code'][:-1])
    part    = ['00126380', '00401731']

    infos = {}
    for i,com in enumerate(part):
        df = getAccount(com, 2015, 2021)
        if len(df) != 0:
            print(i, com)
            capital = df["자본총계"].astype("int")
            
            infos[com]={"자본총계": capital.max()}
    
    df = pd.DataFrame(infos).T

    pass



'''--------------------------------------------------------
'''
if __name__ =="__main__":
    # load()
    cal00()
