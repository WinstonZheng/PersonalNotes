#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
    it is a simple script to creat a content for github readme.md
    Usage: python mk-dir-for-md.py RAW_PAGE_FORM_GITHUB
"""

__author__ = "winston"

import urllib2
import sys
import re


def getWebFile(url):
   response = urllib2.urlopen(url)
   return response
def valueToUrl(value):
    ''' change the content vaule to url , so we can link 
        " " -> "-"
        "-" or "_" -> same
        "~`!@#$%^&*()+={}[]|\:;"'<>,.?/" -> ""
        full-width only "-" is not change, others -> ""
    '''
    repalceChar = ['~','`','!','@','#','$','%','^','&','*',
            '(',')','+','=','{','}','[',']','|','\\',':',';',
            '\"','\'','<',',','>','.','?','/',
            '·','！','￥','……','（','）','——','【','】','、','：',
            '；','“','‘','《','》','，','。','？']
    value = value.strip()
    for singleChar in repalceChar:
        value = value.replace(singleChar, '')
    # remove the leading and trailing whitespace
    value = value.replace(' ','-')
    return value.lower()

def getSameContentNum(content, urlValue):
    ''' github use the -num to solve the same content problem
        For example,
        # haha -> haha
        # haha -> haha-1
    '''
    num = 0
    if not urlValue:
        num = 1
    for line in content:
        left = line.rfind("#") + 1
        right = line.rfind(")")
        key = line[ left : right ]
        if key == urlValue:
            num = num + 1
        if re.match(r'.*-\d$', key):
            realKey = key[:-2] 
            if urlValue == realKey: 
                num = int(key[-1]) + 1
    return num
    



def makeDirFromRawPage( page, isPrint = 1):
    ''' page is a file-like objext'''
    InCode = "```"
    contentTarget  = "#"
    isInCode = 0 
    content =[]
    for line in page.readlines():
        if line.count(InCode):
            if isInCode:
                isInCode = 0
            else:
                isInCode = 1
        if not isInCode and line[0] == contentTarget:
            count = line.find(" ")
            value = line[count + 1 : -1]
            # "# #" is used to back to top
            # empty string can not work
            if value == contentTarget or not value:
                continue
            # change content value to url
            urlValue = valueToUrl(value)
            # same content
            num = getSameContentNum( content, urlValue)
            if num:
                urlValue += ("-" + str(num))
            contentValue = (count - 1) * "\t" + "* [%s](#%s)" % (value , urlValue)
            if isPrint:
                print contentValue
            content.append(contentValue)
    return content
            


if __name__=='__main__':
    script, url = sys.argv
    result = getWebFile(url)
    content = makeDirFromRawPage(result)





