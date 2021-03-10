
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

'''
my API_KEY!!
'''
apiKey = "f1f64632cabe19da450a98456722f7bccf8d5c0f"

'''
download xmlFile from Dart
'''
def downloadCorpCode(FileUrl):

    with Session() as s:
        s.headers.update({'user-agent': UserAgent().chrome})

        req = Request('GET', FileUrl, params={'crtfc_key':apiKey})
        prepped = s.prepare_request(req)
        resp = s.send(prepped)

    # check header
    headers = resp.headers.get('Content-Disposition')
    if headers is None or not re.search('attachment', headers):
        return []

    z = zipfile.ZipFile(BytesIO(resp.content))
    z.extractall()
    z.close()

    return z.namelist()

def getCorpCodeFromDart():
    url = "https://opendart.fss.or.kr/api/corpCode.xml"
    xmlFile = downloadCorpCode(url)

    return xmlFile[0]

'''
'''


'''
'''
def darkListFormatting(doc):
    # mangling..
    dartSrc = collections.defaultdict(list)

    for item in doc['result']['list']:
        for key in item:
            dartSrc[key].append(item[key])

    # merge by stock coce
    df1 = pd.DataFrame  (dartSrc)
    df2 = pd.read_excel ("./data/list.xlsx")
    df2['종목코드'] = df2['종목코드'].apply(lambda x: '{:0>6d}'.format(x))

    df3 = pd.merge(df2, df1, how="left", left_on="종목코드", right_on="stock_code")
    df3 = df3[['회사명', '종목코드', 'corp_code','업종', '주요제품', '상장일', '결산월', '대표자명', '홈페이지', '지역']]
    df3.to_excel("./data/ref.xlsx")

    return df3

'''
TODO: use halo lib for texting
'''
def makeDarkDB(loadFromDart=False):
    dartFile = "CORPCODE.xml"

    if loadFromDart == True:
        print("download file form DART")            
        dartFile = getCorpCodeFromDart()
    try:
        with open(dartFile) as fd:
            doc = xmltodict.parse(fd.read())
    except Exception() as e:
        return None

    df = darkListFormatting(doc)

    return df

'''
'''
if __name__ == "__main__":
    df = makeDarkDB(loadFromDart=True)