


# https://opendart.fss.or.kr/api/fnlttSinglAcnt.json?crtfc_key=f1f64632cabe19da450a98456722f7bccf8d5c0f&corp_code=00126380&bsns_year=2018&reprt_code=11011
# https://opendart.fss.or.kr/api/fnlttSinglAcnt.json?crtfc_key=f1f64632cabe19da450a98456722f7bccf8d5c0f&corp_code=00126380&bsns_year=2018&reprt_code=11013
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


apiKey       = "f1f64632cabe19da450a98456722f7bccf8d5c0f"
dartSingleAnt= "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json"
'''
'''

def getFromDart(url, params):

    with Session() as s:
        s.headers.update({'user-agent': UserAgent().chrome})

        req = Request('GET', url, params=params)
        prepped = s.prepare_request(req)
        print(prepped.url)

        resp = s.send(prepped)

    return resp

def getSingleAccount():
    param0 = \
    {
        "crtfc_key": apiKey,
        "corp_code":"00126380",
        "bsns_year":"2018",
        "reprt_code":"11013"
    }

    resp = getFromDart(dartSingleAnt, param0) 

    return resp

'''
'''
if __name__ =="__main__":
    resp = getSingleAccount()

    resp.content