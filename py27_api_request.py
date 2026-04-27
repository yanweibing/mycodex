#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Python 2.7 示例：不依赖任何 Web 框架发起接口请求，并对返回数据进行 JSON 处理。
"""

import json
import urllib
import urllib2


def request_json(url, params=None, headers=None, timeout=10):
    """
    发起 GET 请求并将返回体解析为 JSON。

    :param url: 接口地址
    :param params: dict，请求参数（会拼接到 URL）
    :param headers: dict，请求头
    :param timeout: 超时时间（秒）
    :return: 解析后的 Python 对象（dict/list）
    """
    params = params or {}
    headers = headers or {}

    query = urllib.urlencode(params)
    full_url = url + ('?' + query if query else '')

    req = urllib2.Request(full_url)
    for k, v in headers.items():
        req.add_header(k, v)

    try:
        resp = urllib2.urlopen(req, timeout=timeout)
        raw = resp.read()

        # Python 2.7 下接口常返回 bytes，先按 UTF-8 解码。
        if isinstance(raw, str):
            raw = raw.decode('utf-8')

        data = json.loads(raw)
        return data

    except urllib2.HTTPError as e:
        print('HTTPError:', e.code, e.reason)
    except urllib2.URLError as e:
        print('URLError:', e.reason)
    except ValueError as e:
        # JSON 解析失败会进入这里
        print('JSON decode error:', e)

    return None


if __name__ == '__main__':
    api_url = 'https://httpbin.org/get'
    params = {
        'page': 1,
        'size': 10,
        'keyword': 'python2'
    }
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'python2.7-urllib2-demo'
    }

    result = request_json(api_url, params=params, headers=headers)
    if result is not None:
        # ensure_ascii=False 便于直接查看中文
        print(json.dumps(result, indent=2, ensure_ascii=False))
