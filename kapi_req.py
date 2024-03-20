import requests
import uuid
import time
import kapi_gencookie
import json
from flask import Flask
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def genuid():
    return str(uuid.uuid4()).replace('-', '')[0:20]

def gentimecode():
    return str(time.time()).replace('.', '')[0:15]

def replchars(strn):
    vstring = strn
    vstring.replace('%20', '+').replace('%22', '%5C%22').replace('%0A', '%5Cn')
    return vstring

def gettime():
    return round(time.time())

def defaultheader(vcookie):
    vheader = {
        'User-Agent' : ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\Safari/537.36'),
        'accept' : ('application/json'),
        'accept-encoding' : ('gzip, deflate, br'),
        'accept-language' : ('ko'),
        'content-type' : ('application/x-www-form-urlencoded; charset=UTF-8'),
        'referer' : ('https://story.kakao.com/'),
        'x-kakao-apilevel' : ('49'),
        'x-kakao-deviceinfo' : ('web:d;-;-'),
        'x-kakao-vc' : (genuid()),
        'x-requested-with' : ('XMLHttpRequest'),
        'cookie' : vcookie,
    }
    return vheader

def writeheader(lent,vcookie):
    vheader = {
        'User-Agent' : ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\Safari/537.36'),
        'accept' : ('application/json'),
        'accept-encoding' : ('gzip, deflate, br'),
        'accept-language' : ('ko'),
        'content-type' : ('application/x-www-form-urlencoded; charset=UTF-8'),
        'content-length' : (str(len(lent))),
        'referer' : ('https://story.kakao.com/'),
        'x-kakao-apilevel' : ('49'),
        'x-kakao-deviceinfo' : ('web:d;-;-'),
        'x-kakao-vc' : (genuid()),
        'x-requested-with' : ('XMLHttpRequest'),
        'cookie' : vcookie,
    }
    return vheader

def kget(kurl,kcookie):
    response = requests.get(kurl,headers = defaultheader(kcookie))
    return [response.status_code,response.text]

def kpost(kurl,kdata,kcookie):
    response = requests.post(kurl,data=kdata,headers = writeheader(kdata,kcookie))
    return [response.status_code,response.text]

def kdel(kurl,kcookie):
    response = requests.delete(kurl,headers = defaultheader(kcookie))
    return [response.status_code,response.text]

def kput(kurl,kdata,kcookie):
    response = requests.put(kurl,data=kdata,headers = writeheader(kdata,kcookie))
    return [response.status_code,response.text]

def gencookie(uid,upw):
    vcook = kapi_gencookie.gencookie(uid,upw)
    if vcook == None:
        return 'n'

@app.route('/', methods = ['GET'])
def data_GET():
    url = request.headers.get('Xurl')
    if url == "test1":
        return "ok"
    cmds = request.headers.get('Xcmd')
    datas = request.headers.get('Xdata')
    vcookie = request.headers.get('Xcookie')
    if cmds == "login":
        uid, upw = json.loads(datas)
        return gencookie(uid,upw)
    if cmds == "get":
        return kget(url,vcookie)
    if cmds == "del":
        return kdel(url,vcookie)
    if cmds == "post":
        return kpost(url,datas,vcookie)
    if cmds == "put":
        return kput(url,datas,vcookie)

app.run(host='0.0.0.0', port=5000)


#우분투 백그라운드 실행
#nohup python -u kapi_req.py &

#프로세스 확인
#lsof -i :5000

#프로세스 종료
#sudo kill -9 12345
#sudo kill -9 (pid)
