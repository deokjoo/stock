
import re
from requests import Request, Session
from fake_useragent import UserAgent
from urllib.parse import unquote
import os

from io import BytesIO
import zipfile

import xmltodict

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
    z.extractall("./data/")
    z.close()

    return z.namelist()

def getCorpCodeFromDart():
    url = "https://opendart.fss.or.kr/api/corpCode.xml"
    xmlFile = downloadCorpCode(url)

    return xmlFile

'''
'''
def makeDarkDB():
    with open("./data/CORPCODE.xml") as fd:
        doc = xmltodict.parse(fd.read())

'''
'''
if __name__ == "__main__":
    getCorpCodeFromDart()