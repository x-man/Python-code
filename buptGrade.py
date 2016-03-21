#coding:utf-8
import urllib2,urllib,re,cookielib
from PIL import Image,ImageEnhance,ImageFilter
import pytesser
from HTMLParser import HTMLParser
import codecs
#from bs4 import BeautifulSoup

cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support)
urllib2.install_opener(opener)

class BruteParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results={}

    def handle_starttag(self,tag,attrs):
        if tag=="input":
            tag_name = None
            tag_value=None
            for name,value in attrs:
                if name=='name':
                    tag_name=value
                if name=='value':
                    tag_value = value
            if tag_name is not None:
                self.tag_results[tag_name] = tag_value

def getData(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    text = response.read().decode('utf-8')
    return text


def postData(url , data):
    headers = {'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'}
    data = urllib.urlencode(data)
    request = urllib2.Request(url , data , headers)
    response = urllib2.urlopen(request)
    text = response.read().decode('utf-8')
    return text

def getValidator():
    url = 'http://yjxt.bupt.edu.cn/Public/ValidateCode.aspx?image=1079919554'
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    text = response.read()
    fd=open('validator.png','wb')
    fd.write(text)
    fd.close()

    threshlod = 200
    table=[]
    for i in range(256):
        if i<threshlod:
            table.append(0)
        else:
            table.append(1)
    name = 'validator.png'
    im = Image.open(name)
    imgry = im.convert('L')
    imgry.save('g'+name)
    out = imgry.point(table,'1')
    text = pytesser.image_to_string(out)[:4]
    return text

	

def login(username,password):
    url = 'http://yjxt.bupt.edu.cn/'
    validator = getValidator()
    page = getData('http://yjxt.bupt.edu.cn/')
    parser = BruteParser()
    parser.feed(page)
    post_tags = parser.tag_results

    post_tags['UserName'] = username
    post_tags['PassWord'] = password
    post_tags['ValidateCode'] = validator
    post_tags['ScriptManager1'] = 'UpdatePanel2%7CbtLogin'
    post_tags['__EVENTTARGET'] = 'btLogin'
    post_tags['__EVENTARGUMENT'] = ''
    post_tags['__LASTFOCUS'] = ''
    post_tags['drpLoginType'] = '1'
    post_tags['__ASYNCPOST'] = 'true'
    del post_tags['ValidateImage']

    #print post_tags
    # for k,v in post_tags.items:
    #     print k,':',v

    page = postData(url,post_tags)
    
    #page = getData('http://yjxt.bupt.edu.cn/Gstudent/Default.aspx')
    page = getData('http://yjxt.bupt.edu.cn/Gstudent/Course/StudentScoreQuery.aspx?EID=l3PZkHTW3Su1WxpIyiJt7xg!oXf-MKDVwRsqQS-VmXPTktNXfJg51w==')
    # fp = codecs.open('yeah.html' , 'wb','utf-8')
    # fp.write(page)
    # fp.close()
    pattern = re.compile(r'<th align="center" scope="col">(.*?)</th><th align="center" scope="col">(.*?)</th><th align="center" scope="col">(.*?)</th><th align="center" scope="col">(.*?)</th><th align="center" scope="col">(.*?)</th><th align="center" scope="col">(.*?)</th><th align="center" scope="col">(.*?)</th><th align="center" scope="col" nowrap="nowrap">(.*?)</th><th align="center" scope="col">(.*?)</th><th align="center" scope="col">(.*?)</th><th align="center" scope="col">(.*?)</th>',re.S)
    items = re.findall(pattern,page)
    for item in items:
        print item[1]+' '*31+item[5]+' '*5+item[6]+' '*5+item[7]
    print '----------------------------------------------------------------------'
    pattern = re.compile(r'<td align="center">(.*?)</td><td align="center">(.*?)</td><td align="center">(.*?)</td><td align="center">(.*?)</td><td align="center">(.*?)</td><td align="center">(.*?)</td><td align="center">(.*?)</td><td align="center">(.*?)</td><td align="center" nowrap="nowrap">(.*?)</td><td align="center" nowrap="nowrap">(.*?)</td><td align="center">(.*?)</td>',re.S)
    items2 = re.findall(pattern,page)

    total_grade=0
    total_credit=0

    for item in items2:
        item1 = item[1].strip()
        l = 40-len(item1)*2
        print item1+' '*l+item[5]+' '*10+item[6]+' '*10+item[7]
        total_credit += int(item[3])
        total_grade += int(item[6])*int(item[3])

    GPA = total_grade/total_credit
    print '----------------------------------------------------------------------'
    print 'your GPA is %s' %GPA



    










login('学号','密码')


# ScriptManager1=UpdatePanel2%7CbtLogin
# __EVENTTARGET=btLogin
# __EVENTARGUMENT=
# __LASTFOCUS=
# __VIEWSTATE=%2FwEPDwUJNzUwNTQ3ODM1D2QWAgIDD2QWBgIND2QWAmYPZBYCAgEPDxYCHghJbWFnZVVybAUqfi9QdWJsaWMvVmFsaWRhdGVDb2RlLmFzcHg%2FaW1hZ2U9MzE0ODA1MzQ3ZGQCEQ9kFgJmD2QWAgIBDxBkZBYBZmQCFQ9kFgJmD2QWAgIBDw8WAh4LTmF2aWdhdGVVcmwFLX4vUHVibGljL0VtYWlsR2V0UGFzc3dkLmFzcHg%2FRUlEPVpwZGJQdTFxVHEwPWRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQ1WYWxpZGF0ZUltYWdldY7PwGZjFAhTz6%2BQjna0ZUDv9SU%3D
# __EVENTVALIDATION=%2FwEdAApK1L4fQxJJ7QLR9tBIbfczR1LBKX1P1xh290RQyTesRQa%2BROBMEf7egV772v%2BRsRJUvPovksJgUuQnp%2BWD%2F%2B4LQKymBEaZgVw9rfDiAaM1opWKhJheoUmouOqQCzlwTSNWlQTw3DcvmMLY3PAqFoA%2BuFSTy5ozCEG4XBxL%2FYkep0cgC%2FIrwlr9d8VObb8MnYO0GRqRfbdgDIW2dtIsr6rbZUBMh8u%2Bj4bXr4xO5xKabn5AapI%3D
# UserName=
# PassWord=
# ValidateCode=
# drpLoginType=1
# __ASYNCPOST=true
