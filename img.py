#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @ 2016-05-27 11:27:48


import urllib2
import re
import requests
import os
import json


url = 'https://www.zhihu.com/question/22468846'

if not os.path.exists('images'):
    os.mkdir("images")

page_size = 50
offset = 0
url_content = urllib2.urlopen(url).read()
answers = re.findall('h3 data-num="(.*?)"', url_content)#答案数目
limits = int(answers[0])

count = 1
while offset < limits:
    post_url = "http://www.zhihu.com/node/QuestionAnswerListV2"
    params = json.dumps({
        'url_token': 22468846,
        'pagesize': page_size,
        'offset': offset
    })
    data = {
        '_xsrf': '',
        'method': 'next',
        'params': params
    }
    header = {
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
        'Host': "www.zhihu.com",
        'Referer': url
    }
    response = requests.post(post_url, data=data, headers=header)
    answer_list = response.json()["msg"]
    reg = re.compile('img .*?src="(.*?_b.*?)"')
    img_urls = re.findall(reg, ''.join(answer_list))
    for img_url in img_urls:
        try:
            img_data = urllib2.urlopen(img_url).read()
            with open('images/'+str(count)+img_url[-4:], 'wb') as f:
                f.write(img_data)
            print '正在下载第%s张图片' % count
            count += 1
        except:
            pass
    offset += page_size

print '下载完毕'
