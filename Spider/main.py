#-*-coding:utf-8-*-
from importlib import reload

import requests
import random
from bs4 import BeautifulSoup
from datashape import unicode
from lxml import etree
from wordc import makewordc
import os
import re
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')
import HTMLParser
#例子:周杰伦专辑:https://y.qq.com/portal/singer/0025NhlN2yWrP4.html?ADTAG=baidualdhsy#tab=album&
albumsurl = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_album.fcg?g_tk=5381&jsonpCallback=MusicJsonCallbacksinger_album&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&order=time&begin=0&num=300&exstatus=1&singermid='

headers3 = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36',
        'Accept': '*/*'
}
headers2 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept': '*/*'
}
headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept': '*/*'
}
headers = [
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
        {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
        {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
    ]

class Songs():
    lyrics=''
    def __init__(self,albumname,songname,songid,songmid):
        self.albumname = albumname
        self.songname = songname
        self.songid = songid
        self.songmid = songmid
class Albums():
    def __init__(self,albumName,albumMID):
        self.albumName = albumName
        self.albumMID = albumMID

def getAlbums(singer):
    respons = requests.get(albumsurl+singer['singermid'],headers=headers3)
    print(respons.content)
    searchObj = re.search('MusicJsonCallbacksinger_album\((.*)$',respons.content, re.M | re.I)
    albums = searchObj.group(1)
    # print(albums)
    for album in eval(albums)['data']['list']:
        # album = Albums(album['albumName'],album['albumMID'])
        print(album)
        if '演唱会' not in album['albumName'] and '演唱会' not in album['desc'] and '精选' not in album['albumName'] and '精选' not in album['desc']:
            getSongs('https://y.qq.com/portal/album/'+album['albumMID']+'.html',singer)
            time.sleep(10)

def getSongs(url,singer):
    headers3['Referer'] = url
    respons = requests.get(url, headers=headers3)
    print(respons.content)
    searchObj = re.search("getSongInfo : (.*),.*",respons.content)
    if searchObj:
        songcents = searchObj.group(1)
        songs = eval(songcents)
        for song in songs:
            s = Songs(song['albumname'].replace('?',"问号"),song['songname'],song['songid'],song['songmid'])
            print(song['songname'])
            getlyrics(s,singer)
    else:
        print(url)

def getlyrics(song,singer):
    headers3['Referer'] = 'https://y.qq.com/portal/album/'+song.songmid+'.html'
    headers3['Host'] = 'c.y.qq.com'
    url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg?nobase64=1&callback=jsonp1&g_tk=1171713782&jsonpCallback=jsonp1&loginUin=261696254&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&musicid='+str(song.songid)
    respons = requests.get(url, headers=headers3)
    searchObj = re.search("jsonp1\((.*)\)", respons.content, re.M | re.I)
    lyric = searchObj.group(1)
    print("歌词:"+lyric)
    #设置默认的歌词就是没有歌词
    lyrics = eval(lyric).get('lyric','无歌词')
    # print(lyrics)
    # lrc2dict(lyrics)
    # print(searchObj.groups(0))
    song.lyrics = lyrics
    saveFile(song,singer)


def saveFile(song, singer):
    html_parser = HTMLParser.HTMLParser()
    path = "../Songs/" +singer['name']+'/'+ unicode(song.albumname, 'utf8')
    print(path)
    if not os.path.exists(path):
        os.makedirs(path)
    fo = open(path + "/" + unicode(song.songname, 'utf8') + ".txt", "wb")
    print("文件名: ", fo.name)
    fo.write(html_parser.unescape(song.lyric))
    # 关闭打开的文件
    # print(html_parser.unescape(unicode(song.lyric,'utf8')))
    fo.close()

    #==================================以下是清洗歌词=======================================
def getAlllrc(singer):
    lrcsfile = open('../songs/'+singer['name']+'/lrcs.txt',"wb")
    for parent, dirnames, filenames in os.walk('../Songs/'+singer['name']):
        for filename in filenames:  # 输出文件信息
            print("parent is:" + parent.decode('gbk'))
            print("filename is:" + filename.decode('gbk'))
            # print "the full name of the file is:" + os.path.join(parent,filename) #输出文件路径信息
            file = open(os.path.join(parent,filename))
            lrc = file.readlines()
            i=0
            for line in lrc:
                i=i+1
                if i>9:
                    lrcsfile.write(lrc2dict(line))

def lrc2dict(lrc):
    time_stamps = re.findall(r'\[[^\]]+\]', lrc)
    html_parser = HTMLParser.HTMLParser()
    if time_stamps:
        # 截取歌词
        lyric = lrc
        for tplus in time_stamps:
            lyric = lyric.replace(tplus, '').replace('\r', '').replace('\n', '')
            lyric = lyric.replace('周杰伦', '')
        # 解析时间
        # tplus: [02:31.79]
        # t 02:31.79
        # print(lyric)
        print(html_parser.unescape(lyric))
        return html_parser.unescape(lyric)
    else:
        return ''


def go(singer):
    # 获取所有歌词
    getAlbums(singer)
    # 获取某个专辑的所有歌词
    # getSongs('https://y.qq.com/portal/album/000f01724fd7TH.html',singer)
    getAlllrc(singer)
    makewordc(singer['name'])


if __name__ == '__main__':
    singer={'name':'jaychou','singermid':'0025NhlN2yWrP4'}
    # 获取所有歌词
    # getAlbums(singer)
    # 获取某个专辑的所有歌词
    # getSongs('https://y.qq.com/portal/album/003vnmqm4Y5U5Z.html',singer)
    getAlllrc(singer)
    makewordc(singer['name'])