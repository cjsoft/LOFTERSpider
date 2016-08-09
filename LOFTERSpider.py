#coding=utf-8
import urllib2, re, threading, copy
from Queue import Queue as TaskQ
import os
import time
# -------------- settings --------------
st = 1 # 起始页
ed = 160 # 结束页
album_host = "menvshenying.lofter.com" # po主二级域名
get_gif = True # 是否获取gif
img_thread_cnt = 50 # 获取图片的线程数
pth = 'img' # 保存图片的相对路径， 需手动新建文件夹
# cookies 请在下面的hed2中修改
# hed是获取图片的header，hed2是打开po主主页的header
# -------------- settings --------------
finder = re.compile(r'<img src="(http://(imglf\d?\.(?:nosdn\.127|ph\.126)\.net)(?:/img)?/[=a-zA-Z\d/\-]+\.jpg)[\?"]')
def get_content(uri, headers=dict()):
    req = urllib2.Request(uri)
    for i in headers:
        req.add_header(i, headers[i])
    return urllib2.urlopen(req).read()
def pting():
    while True:
        if ppq.empty() == False:
            print ppq.get()
def ppt(s):
    ppq.put(s)
q = TaskQ()
ppq = TaskQ()
cnt = 0
tls = list()
ppp = threading.Thread(target = pting)
ppp.start()
if get_gif == True:
    finder = re.compile(r'<img src="(http://(imglf\d?\.(?:nosdn\.127|ph\.126)\.net)(?:/img)?/[=a-zA-Z\d/\-]+\.(?:gif|jpg))[\?"]')
hed = {
    "host": "imglf0.nosdn.127.net",
    "connection": "keep-alive",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36 OPR/39.0.2256.48",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-language": "zh-CN,zh;q=0.8"
}
hed2 = {
    "Host": album_host,
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36 OPR/39.0.2256.48",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Cookie": r"usertrack=ZUcIilZhRaAsh2opAxANAg==; _ntes_nnid=6cce163cb95991fa6dd2e4ac53174247,1449238680067; JSESSIONID-WLF-XXD=bc81ffe98c8e5c49b59fca887fdf1c2eab57503243d8efaba18c9e60ea0ca919420cedd91f0db48d37f38f308095b5915de33d4f85ef1f8b8c871748de6a83784849cdadabfe95101e713321e0103202b0105e0f2b2a51985a6a8c66f222d1b031229c0fdaf11d1d41da4675b0730a1b78a7da95b45349a2129473f2889b2cf212f3bded; firstentry=%2Flogin.do%3FX-From-ISP%3D2|; regtoken=1000; __utma=61349937.795668768.1449238679.1468313430.1470729651.6; __utmb=61349937.26.7.1470729884394; __utmc=61349937; __utmz=61349937.1449238692.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gat=1; _ga=GA1.2.795668768.1449238679; reglogin_isLoginFlag=1; reglogin_isLoginFlag=1"
}
def organise(i, slp):
    # time.sleep(slp)
    l = 0
    while (l < 1):
        p = get_content('http://%s/?page=%d'%(album_host, i), hed2)
        lst = finder.findall(p)
        l = len(lst) + 1 # 修改了finder， 无需循环尝试了
        # ppt(l)
    pcnt = 0
    for j in lst:
        # ppt(j)
        tmph = copy.copy(hed)
        tmph['host'] = j[1]
        q.put((j[0], tmph))
        pcnt = pcnt + 1
    ppt(str(pcnt) + ' Done ' + str(i))
    global cnt
    cnt = cnt + 1
for i in xrange(st, ed + 1, 1):
    tls.append(threading.Thread(target = organise, args = (i, (ed - st + 1) / 10)))
    tls[-1].start()
while cnt < ed - st + 1:
    pass

def fetch():
    while q.empty() == False:
        try:
            tmp = q.get()
            fname = pth + '\\' + tmp[0].split('/')[-1].split('/')[-1]
            p = get_content(tmp[0], tmp[1])
            f = open(fname, 'wb')
            f.write(p)
            f.close()
            ppt(str(q.qsize()) + ' Fetch ' + fname)
        except BaseException:
            if os.path.isfile(fname):
                try:
                    f.close()
                except BaseException:
                    pass
                os.remove(fname)
            if q.empty() == True:
                ppt('Thread terminated')
            ppt('oops ' + tmp[0])
tlst = list()
for i in xrange(img_thread_cnt):
    tlst.append(threading.Thread(target = fetch))
    tlst[-1].start()