from bs4 import BeautifulSoup as bs
import requests as rq
import json
import re
from flask import Flask,request,abort
from flask_cors import cross_origin;

app=Flask(__name__)

"""V1: Doesn't work with new updated youtube !!!!
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

"""V2: Ready to be used with new YouTube"""
def Crawler(qstring):
    headers={
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    url='https://www.youtube.com/results?search_query='+qstring
    searched=rq.get(url,headers=headers)
    soup=bs(searched.text,'html.parser')
    aid=soup.find('script',string=re.compile('ytInitialData'))
    #extracted_josn_text=str(aid).split(';')[0].replace('window["ytInitialData"] =','').strip()
    #print(str(aid).split(';')[0].split('\n')[1].replace('window["ytInitialData"] =','').strip())
    extracted_josn_text=str(aid).split(';')[0].split('\n')[2].replace('window["ytInitialData"] =','').strip()
    #print(extracted_josn_text)
    video_results=json.loads(extracted_josn_text[20:])
    #print(item_section=video_results["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][1])
    #print(video_results["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][""])
    item_section=video_results["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
    videolist=[]

    for item in item_section:
        #print("---------------------------------------------------------------------------------------")
        try:
            #print(item["videoRenderer"]['videoId'])
            #print(item["videoRenderer"]['title']['runs'][0]['text'])
            """video_info=item["videoRenderer"]
            title=video_info["title"]["simpleText"]
            url=video_info["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]
            print('Title:',title)
            print('Url:',url)
            """
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
    return Crawler(q)

if __name__=="__main__":
    app.run(debug=True)
