# -*- coding: UTF-8 -*-
import urllib2

EscapeCharacterDict = {'&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': '\''}


def deal(response):
    html = response.read()

    global cnt
    global fp
    step = 24
    end = 1000

    while True:
        begin = html.find('data-pjax="true" title=', end, len(html))  # 获取 commit 首位置
        if begin == -1:
            break
        begin += step
        keywords = '">' if html[begin - 1] == '"' else '\'>'
        end = html.find(keywords, begin, len(html))
        s = html[begin:end]
        for k, v in EscapeCharacterDict.iteritems():
            s = s.replace(k, v)
        fp.write("%3d  %s\n" % (cnt, s))
        cnt += 1

USERNAME = 'rogerwang' # 修改这里
REPONAME = 'node-webkit' # 修改这里

fp = open(USERNAME + '#' + REPONAME + '#commits.txt', 'w')

cnt = 1
i = 1
while True:
    try:
        response = urllib2.urlopen('https://github.com/' + USERNAME + '/' + REPONAME + '/commits?page=' + str(i))
        deal(response)
        print 'Cheaked', i, 'page(s).'
        i += 1
    except urllib2.HTTPError, err:
        if err.code == 404:
            print ''
            print 'Cheaked', i - 1, 'page(s),', cnt - 1, 'commit(s) found.'
            break
        else:
            raise
