
import re
from requests import Request, Session
from fake_useragent import UserAgent
from urllib import parse

from io import BytesIO
import zipfile


apiKey = "f1f64632cabe19da450a98456722f7bccf8d5c0f"

# https://opendart.fss.or.kr/api/corpCode.xml

def download(FileUrl):
    from .spinner import Spinner
    from .file import create_folder
    from urllib.parse import unquote
    import os


    s = Session()
    s.headers.update({'user-agent': UserAgent().chrome})


    data = {'crtfc_key':apiKey}

    req = Request('GET', FileUrl, params=data)
    prepped = s.prepare_request(req)

    resp = s.send(prepped)
    headers = resp.headers.get('Content-Disposition')
    if headers is None or not re.search('attachment', headers):
        raise FileNotFoundError('target does not exist')

    filename = unquote(re.findall(r'filename="?([^"]*)"?', headers)[0])
    with open(filename, "wb") as f:
        f.write(BytesIO(resp.content).getbuffer())

    return filename




if __name__ == "__main__":
    url = "https://opendart.fss.or.kr/api/corpCode.xml"

    download(url)