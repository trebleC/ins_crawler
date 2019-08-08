# -*- coding: utf-8 -*-
from lxml import etree
import json
import requests
import time
from pymongo import MongoClient

BASE_URL= "https://www.google.com"
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
    ,"accept-encoding": "gzip, deflate, br"
    ,"accept-language": "zh-CN,zh;q=0.9,en;q=0.8"
    ,"cache-control": "max-age=0"
    ,"cookie": "SID=nAegM4UUKFsMe4mPEirFFD8OFFo4svLWEpccdYnUgOrOxiDwmBsa1ueU7FvHBJn6w5doyA.; HSID=Aj00GzaLom98if9aW; SSID=AbiIhnWO0lsFjyrC0; APISID=1ylqPaJ76ndd2JfI/ARezHXyJDiPxFhNWX; SAPISID=mD1ACuwkeyFMVDTV/An6zUtbDmrc_NGLEc; NID=188=ulRFficOF1iUP5qnNRr_xT-ZtdtTc2rMDi4dDpxAG7ur1VJhFmSSgxHxkuFupR7XeGMuTBAp94lHW7gV88gMxhubjd2UbcHGgBVxBiFUxTON-1DAZaWver_XV4sfPqNDY1ow9AM55IDPDiZ83raRUWUG0YJymIRUdVGt_0C4zlj_3izKSr6WpdXno-gOc-y3auH8cV-CK1rh_FhdwC5mqy-0GIKF7NxgG1EeZs3al76hAVbQC5u92cr55dsb0KslJw; SIDCC=AN0-TYsiFfyt2jIw5gX4tnQms5LxOWJ97RiyO2BqR6S0lltuQ495iGe1EFYwD7rNvcHO9pLJ5bE; 1P_JAR=2019-8-8-18"
    ,"sec-fetch-mode": "navigate"
    ,"sec-fetch-site": "none"
    ,"sec-fetch-user":"?1"
    ,"upgrade-insecure-requests": "1"
    ,"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    ,"x-client-data": "CJW2yQEIo7bJAQjBtskBCImSygEIqZ3KAQioo8oBCOKoygEIl63KAQjNrcoBCMyuygEIya/KAQ=="
}
res = requests.get(BASE_URL) 
#html = etree.HTML(res.content.decode()) #获取html
print(res.status_code)