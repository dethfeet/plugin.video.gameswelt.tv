import json
import re
import urllib2
from urllib import quote, unquote, urlencode
from BeautifulSoup import BeautifulSoup

MAIN_URL = 'http://www.gameswelt.tv'
USER_AGENT = 'XBMC Add-on gameswelt.tv'

class NetworkError(Exception):
    pass

def get_categories():
    url = MAIN_URL
    categories = []
    ul = __get_tree(url).find(id='menu')
    for a in ul.findAll('a'):
        categories.append({
            'path': a['href'],
            'title': a.find('span').string,
            'thumb': a.find('img')['src'],
        })
    return categories

def get_videos(path):

    def video_id(path):
        return path.rsplit(',')[1]
    
    url = MAIN_URL+path
    page = __get_tree(url)    
    
    videos = []
    ul = page.find(id='videoList')
    for li in ul.findAll('li',{'class':'videoEntry'}):
        div = li.find('div',{'class':'videoPreview'})
        ulVideoInfo = li.find('ul',{'class':'videoInfo'})
        title = ulVideoInfo.find('li',{'class':'title'}).find('a').string
        subline = ulVideoInfo.find('li',{'class':'subline'}).find('a').string
        videos.append({
            'parameter': video_id(div.find('a')['href']),
            'title': title+' - '+subline,
            'thumb': div.find('img')['src'],
            'type': 'video'
        })
    
    #Next page
    div = page.find('div',{'class':'paging'})
    aNext = div.find('a',text='>>')
    if aNext:
        href = aNext.parent['href'][len(MAIN_URL):]
        videos.append({
            'parameter': href,
            'title': '>>',
            'type': 'category'
        })
        
    return videos

    
def get_video_urls(videoId):
    url = MAIN_URL+"/player/xml.php?videoID="+videoId
    channel = __get_tree(url).find('channel')
    
    video_urls = {
                  'SD':channel.findAll('media:content')[0]['url'],
                  'HD':channel.findAll('media:content')[1]['url']
    }
    return video_urls
    
    
def __get_tree(url):
    log('__get_tree opening url: %s' % url)
    headers = {}
    req = urllib2.Request(url, None, headers)
    try:
        html = urllib2.urlopen(req).read()
    except urllib2.HTTPError, error:
        raise NetworkError('HTTPError: %s' % error)
    log('__get_tree got %d bytes' % len(html))
    tree = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
    return tree

def log(msg):
    print(u'%s scraper: %s' % (USER_AGENT, msg))