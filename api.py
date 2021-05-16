"""
Things are painful ahead, go through the code with patience.....
This fight is gonna go for long, very long...
"""

from bs4 import BeautifulSoup as bs
import requests as rq
import json
import re
from flask import Flask,request,abort
from flask_cors import cross_origin;
import sys

app=Flask(__name__)

"""V1: Doesn't work with new updated youtube !!!! (EXPIRED)
def Crawler(qstring):
    base="https://www.youtube.com/results?search_query="
    
    r=rq.get(base+qstring)
    #print(r.content)
    page=r.content
    soup=bs(page,'html.parser')

    #vids = soup.findAll('a',attrs={'class':'yt-uix-tile-link'})
    vids = soup.findAll('a',attrs={'id':'video-title'})
    print(soup.find('div'))
    videolist=[]
    for v in vids:
        vimg='https://i.ytimg.com/vi/'+ v['href'][9:] +'/hqdefault.jpg'
        videolist.append({'VideoId':v['href'][9:],'title':v['title'],'url':vimg})
    
    return json.dumps(videolist)

#print(Crawler("imagine+dragon"))
"""

"""V2: Ready to be used with new YouTube (MODIFIED)"""
def Crawler(qstring):
    headers={
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    url='https://www.youtube.com/results?search_query='+qstring
    searched=rq.get(url,headers=headers)
    soup=bs(searched.text,'html.parser')
    """
    V3 update (EXPIRED):
    Youtube stores data in window['ytInitialData'] keys which need to be
    parsed to use stuff for furthur process

    Note: Though this thing is expired but was efficient to keep scarrper
    out of the page, and also tool me a hell lot of time to fix XP.

    
    extracted_josn_text=str(aid).split(';')[0].replace('window["ytInitialData"] =','').strip()
    print(str(aid).split(';')[0].split('\n')[0][59:])
    extracted_josn_text=str(aid).split(';')[0].split('\n')[2].replace('window["ytInitialData"] =','').strip()
    """


    """
    V4 update (CURRENT):
    Youtube now secures/preserves data in one key under script tag with
    no utilization of window["ytInitialData"]

    Note: In case of further updates keep in kind to take a keen note of
    'ytInitialData' param/variable, it is important for operation of this API
    and resultant application :| 
    """
    aid=str(soup.find('script',string=re.compile('ytInitialData')))
    #print(aid)
    #extracted_josn_text=str(aid).split(';')[0].split('\n')[0][39:]
    """
    Filtering the no needed "ytInitialData =" syntax out of the page....
    """
    #print(extracted_josn_text)
    start=-1
    for i in range(len(aid)):
        if aid[i]=='{':
            start=i
            break
    end=len(aid)-1
    for i in range(len(aid)-1, -1, -1):
        if aid[i]=='}':
            end=i
            break
    
    extracted_josn_text=str(aid[start:end+1])
    #print('--------->')
    #extracted_josn_text=str(extracted_josn_text).strip("'<>() ").replace('\'', '\"')
    print(extracted_josn_text)
    sys.stdout.flush()
    video_results=json.loads(extracted_josn_text)
    item_section=video_results["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
    videolist=[]

    for item in item_section:
        try:            
            vimg='https://i.ytimg.com/vi/'+ item["videoRenderer"]['videoId'] +'/hqdefault.jpg'
            videolist.append({'VideoId':item["videoRenderer"]['videoId'],'title':item["videoRenderer"]['title']['runs'][0]['text'],'url':vimg})
        except KeyError:
            pass
    #print(len(videolist))
    return json.dumps(videolist)


@app.route('/youtube/<string:q>',methods=['POST','GET'])
@cross_origin()
def index(q):
    q=q.replace(' ','+')
    # try:
    #     return Crawler(q)
    # except:
    #     return json.dumps([])
    return Crawler(q)


if __name__=="__main__":
    app.run(debug=True)
