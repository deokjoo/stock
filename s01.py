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

apiKey       = "f1f64632cabe19da450a98456722f7bccf8d5c0f"
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
    columns = ['유동자산', '비유동자산', '자산총계', '유동부채', '비유동부채', '부채총계', '자본금', '이익잉여금', '자본총계']
    df = pd.DataFrame( columns=columns)

    #
    for year in range(ts, te):
        param0 = \
        {
            "crtfc_key" : apiKey, "corp_code" : corp_code, "bsns_year" : str(year), "reprt_code":"11011"
        }

        resp = getFromDart(dartSingleAnt, param0) 
        data = json.loads(resp.content)
        if data['status'] != '000':
            continue

        rows = {}
        for i,  item in enumerate(data["list"]):
            if item["sj_nm"] == "재무상태표" and item["fs_div"] == "OFS":
                idx       = item["bsns_year"]
                col       = item["account_nm"]
                rows[col] = item["thstrm_amount"]
                
        df.loc[idx] =rows

        print("load %s", year)

    df = df.apply( lambda x : x.str.replace(",",""))
    df = df.astype("float") / 1000000

    return df

'''
'''
if __name__ =="__main__":
    company = ['00126380', '00401731']

    with pd.ExcelWriter("1.xlsx") as writer:
        for i, com in  enumerate(company):
                a = getSingleAccount(com, 2015, 2021)
                a.to_excel(writer, com)