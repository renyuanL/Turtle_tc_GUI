#!/usr/bin/env python

#
# old version fails, maybe transfer to newer version
# 2915/04/29
#

#
# https://github.com/soimort/translate-shell
#

# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <terry.yinzhe@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return to Terry Yin.
#
# The idea of this is borrowed from <mort.yao@gmail.com>'s brilliant work
#    https://github.com/soimort/google-translate-cli
# He uses "THE BEER-WARE LICENSE". That's why I use it too. So you can buy him a 
# beer too.
# ----------------------------------------------------------------------------
'''
This is a simple, yet powerful command line translator with google translate
behind it. You can also use it as a Python module in your code.
'''
#
# Thanks to https://github.com/terryyin/google-translate-python/blob/master/translate.py
#

import re
import json
from textwrap import wrap
try:
    import urllib2 as request
    from urllib import quote
except:
    from urllib import request
    from urllib.parse import quote

def main():

    translator= Translator(from_lang='en', to_lang= 'zh-TW')#'zh-tw')

    #text= 'Hello, world.'
    
    text= """turtle-example-suite:

            tdemo_bytedesign.py

            An example adapted from the example-suite
            of PythonCard's turtle graphics.

            It's based on an article in BYTE magazine
            Problem Solving with Logo: Using Turtle
            Graphics to Redraw a Design
            November 1982, p. 118 - 134

            -------------------------------------------

            Due to the statement

            t.delay(0)

            in line 152, which sets the animation delay
            to 0, this animation runs in "line per line"
            mode as fast as possible."""

    translation = translator.translate(text)

    print(text, '\n','-'*10,'\n', translation)

class Translator:
    def __init__(self, to_lang, from_lang= 'en'):

        if from_lang == 'auto': from_lang= 'en'
        
        self.from_lang = from_lang
        self.to_lang = to_lang

    def translate(self, source):
        if self.from_lang == self.to_lang:
            return source
        
        #self.source_list = wrap(source, 1000, replace_whitespace=False)
        
        #
        # renyuan: maybe 1000 is too much, make it smaller
        #
        
        #self.source_list = wrap(source, 100, replace_whitespace=False)
        
        self.source_list = source.split('\n')
        # 先照 \n  來切句子。
        # 如此，換行符號才能在以下保留，重新接回來。
        # 但要預防 句子太長，目前尚未預防！
        #
        
        #
        # renyuan: avoid it too long
        # use \n to split it
        #
        '''
        self.source_list = source.split(sep= '\n')
        self.source_list.remove('')
        '''
        X= []
        for s in self.source_list:
            
            if s != '':
                x= self._get_translation_from_google(s)
            else: x= ''
            
            x+= '\n'
            X += [x]
            
        S= ''.join(X)
        S.rstrip('\n') #  刪掉最後一個 \n
        
        return S #''.join(self._get_translation_from_google(s) for s in self.source_list)

    def _get_translation_from_google(self, source):
        json5 = self._get_json5_from_google(source)
        return json.loads(json5)['responseData']['translatedText']

    def _get_json5_from_google(self, source):
        escaped_source = quote(source, '')
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
        req = request.Request(
             url="http://mymemory.translated.net/api/get?q=%s&langpair=%s|%s" % (escaped_source, self.from_lang, self.to_lang)
                 , headers = headers)
        # print("http://mymemory.translated.net/api/get?q=%s&langpair=%s|%s" % (escaped_source, self.from_lang, self.to_lang))
             #url="http://translate.google.com/translate_a/t?clien#t=p&ie=UTF-8&oe=UTF-8"
                 #+"&sl=%s&tl=%s&text=%s" % (self.from_lang, self.to_lang, escaped_source)
                 #, headers = headers)
        r = request.urlopen(req)
        return r.read().decode('utf-8')

def main00():

    import argparse
    import sys
    import locale
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('texts', metavar='text', nargs='+',
                   help='a string to translate(use "" when it\'s a sentence)')
    parser.add_argument('-t', '--to', dest='to_lang', type=str, default='zh-TW',
                   help='To language (e.g. zh, zh-TW, en, ja, ko). Default is zh.')
    parser.add_argument('-f', '--from', dest='from_lang', type=str, default='auto',
                   help='From language (e.g. zh, zh-TW, en, ja, ko). Default is auto.')
    args = parser.parse_args()
    translator= Translator(from_lang=args.from_lang, to_lang=args.to_lang)
    for text in args.texts:
        translation = translator.translate(text)
        if sys.version_info.major == 2:
            translation =translation.encode(locale.getpreferredencoding())
        sys.stdout.write(translation)
        sys.stdout.write("\n")



class Translator00:

    string_pattern = r"\"(([^\"\\]|\\.)*)\""
    match_string =re.compile(
                        r"\,?\[" 
                           + string_pattern + r"\," 
                           + string_pattern + r"\," 
                           + string_pattern + r"\," 
                           + string_pattern
                        +r"\]")

    def __init__(self, to_lang, from_lang='auto'):
        self.from_lang = from_lang
        self.to_lang = to_lang

    def translate(self, source):
        self.source_list = wrap(source, 1000, replace_whitespace=False)
        return ' '.join(self._get_translation_from_google(s) for s in self.source_list)

    def _get_translation_from_google(self, source):
        json5 = self._get_json5_from_google(source)
        return self._unescape(self._get_translation_from_json5(json5))

    def _get_translation_from_json5(self, content):
        result = ""
        pos = 2
        while True:
            m = self.match_string.match(content, pos)
            if not m:
                break
            result += m.group(1)
            pos = m.end()
        return result 

    def _get_json5_from_google(self, source):
        escaped_source = quote(source, '')
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = request.Request(
        
            # update 2015/04/29
            url= "http://mymemory.translated.net/api/get?q=%s&langpair=%s|%s"%(
                escaped_source, self.from_lang, self.to_lang), 
            headers= headers )
                 
            #url="http://translate.google.com/translate_a/t?client=t&ie=UTF-8&oe=UTF-8"
            #    +"&sl=%s&tl=%s&text=%s" % (self.from_lang, self.to_lang, escaped_source)
            #    , headers = headers)
        
        r = request.urlopen(req)
        return r.read().decode('utf-8')

    def _unescape(self, text):
        return json.loads('"%s"' % text)

if __name__ == "__main__":
    
    main()
    #main01()








