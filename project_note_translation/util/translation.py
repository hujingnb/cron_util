import hashlib
import time
import uuid
import requests
from .config import *


def youdao_translation(q: str) -> str:
    """
    调用有道 API 翻译句子
    :param q: 需要翻译的句子
    :return: 返回翻译后的中文内容
    """
    curtime = str(int(time.time()))
    salt = str(uuid.uuid1())
    # 计算签名
    size = len(q)
    q_truncate = q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]
    sign_str = YOUDAO_APP_KEY + q_truncate + salt + curtime + YOUDAO_APP_SECRET
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(sign_str.encode('utf-8'))
    sign = hash_algorithm.hexdigest()
    data = {
        'from': 'auto',
        'to': 'zh-CHS',
        'signType': 'v3',
        'curtime': curtime,
        'appKey': YOUDAO_APP_KEY,
        'q': q,
        'salt': salt,
        'sign': sign
    }
    # 发起翻译请求
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post('https://openapi.youdao.com/api', data=data, headers=headers)
    ret_json = response.json()
    # 若出错了, 返回 空
    if str(ret_json['errorCode']) != '0':
        return ''
    return "\n".join(ret_json['translation'])
