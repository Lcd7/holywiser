import requests
import execjs 
import json
from requests_html import HTMLSession
import re
import traceback
import shutil
import time
from htmlClass import File

class Holywiser:
    num = 1

    def __init__(self):
        self.token = ''
        self.userGuid = '6582a145-9c58-48cc-b931-c961e8296ef3-soda'
        self.url1 = 'https://www.holywiser.com/api2/api/soda/public/login/user'
        self.url2 = 'https://www.holywiser.com/api2/api/soda/public/search/showdoc'
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '166',
            'Content-Type': 'application/json',
            'Host': 'www.holywiser.com',
            'Origin': 'https://www.holywiser.com',
            'Referer': 'https://www.holywiser.com/search?classid=',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'xen': 'true',
            'xguid': '6582a145-9c58-48cc-b931-c961e8296ef3',
            'xrd': 'eNfyqX0is3dFP',
            'xsn': '364a80f8b3c65e12896a85409b33ee51',
            'xts': '1599549965915',
        }
        self.payload = {
            'randstr': "fcEE2usoda",
            'sign': "sodaf0baf6132d5e6078688c749ab94f3281",
            'tempuserguid': "TMPb624cd93-db38-4a0d-9558-6dabe5c90f8asoda",
            'timestamp': "1599548818176",
            'userid': "lcdsodatest",
        }

    def login(self):
        mainPage = requests.post(url = self.url1, data = json.dumps(self.payload), headers = self.headers)
        mainPage.encoding = 'utf-8'
        response = json.loads(mainPage.text)
        self.token = response.get('token')
        print(f"登录：{response}")

    def jsonStringify(self, textDocId):
        ctx = execjs.compile(
            """
            function jsonStringify(textDocId) {
                var bodyJson = {docid: 123456, h1hit: Array(0), chit: Array(0), cutwords: Array(0), chitseq: Array(0)}
                bodyJson['docid'] = Number(textDocId)
                return JSON.stringify(bodyJson);
            }
            """
        )
        return ctx.call("jsonStringify", textDocId)

    def getSign(self, timestamp, randStr, body):
        import hashlib
        oriStr = ''
        oriStr += 'randstr=' + randStr
        oriStr += '&timestamp=' + timestamp
        oriStr += '&token=' + self.token
        oriStr += '&body=' + body
        # print(oriStr)

        m = hashlib.md5()
        m.update(oriStr.encode("utf8"))
        md5 = m.hexdigest()
        return md5

    def getAeskey(self, passKey):
        ctx = execjs.compile(
            """
            function getAeskey(passKey, token) {
                if (token === undefined || token === "") { return passKey }
                while (passKey.length < 24) {
                passKey += token
                }
                return passKey.substr(0, 24);
            }
            """
        )
        return ctx.call("getAeskey", passKey, self.token)

    def randomWord(self, randomFlag, minNum, maxNum):
        ctx = execjs.compile(
            """
            function randomWord(randomFlag, min, max) {
                var str = ''
                var range = min
                var arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
                ]

                if (randomFlag) {
                    range = Math.round(Math.random() * (max - min)) + min // 任意长度
                }
                for (var i = 0; i < range; i++) {
                    var pos = Math.round(Math.random() * (arr.length - 1))
                    str += arr[pos]
                }
                return str
            }
            """
        )
        return ctx.call("randomWord", randomFlag, minNum, maxNum)

    def getTimeStamp(self):
        return execjs.eval("(new Date()).valueOf().toString()")

    def moveFile(self):
        try:
            shutil.move("D:/Chrome Download/spider.txt", f"C:/Users/user/Desktop/holywiser/{num}.html")
            self.num += 1
        except:
            pass

    def postReqst(self, textDocId):
        randomStr = self.randomWord(True, 10, 16)
        timestamp = self.getTimeStamp()
        aesKey = self.getAeskey(randomStr)
        body = get_flask_TripleDES_Encode(aesKey, textDocId)
        strBodyJson = self.jsonStringify(textDocId)
        sign = self.getSign(timestamp, randomStr, strBodyJson)
        _headers = {
            'content-type': 'application/json',
            'xrd': randomStr,
            'xts': timestamp,
            'xguid': self.userGuid,
            'xsn': sign,
            'xen': 'true',
        }
        response = requests.post(url = self.url2, headers = _headers, data = body)
        print(f"response:   {response}")
        responseData = response.text
        get_flask_TripleDES_Decode(aesKey, responseData)
        # self.moveFile()


def get_flask_TripleDES_Encode(aesKey, textDocId):
    url = f'http://127.0.0.1:8058/encode?key={aesKey}&textDocId={textDocId}'
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    html = r.html.html
    body = re.search(r'console"><h1>[\s\S]*?</h1>', html).group(0)[13:-5]
    return body

def get_flask_TripleDES_Decode(aesKey, text):
    url = f'http://127.0.0.1:8058/decode?key={aesKey}&text={text}'
    session = HTMLSession()
    session.get(url)
    time.sleep(0.5)


if __name__ == "__main__":
    textDocId = '119427'
    holywiser = Holywiser()
    holywiser.login()
    while True:
        textDocId = str(input("输入文件ID:"))
        try:
            if textDocId == '0':
                break
            elif textDocId == '1':
                holywiser.login()
            else:
                holywiser.postReqst(textDocId)
        except:
            print(traceback.print_exc())

# 119621
# 119631
# 119509