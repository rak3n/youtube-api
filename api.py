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
import pymongo

client=pymongo.MongoClient("mongodb+srv://admin:admin1234@cluster0.qtnrv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=client['youtube-chacher']
app=Flask(__name__)

def mem_chacher(search_string):
    res=db['cached-search'].find_one({'search_string': search_string})
    print('memchached invoke')
    return res

def Crawler(qstring):

    available_in_memchache =  mem_chacher(qstring)

    if available_in_memchache:
        return available_in_memchache['result']

    proxies = { 'http': "socks5://206.123.14.245:4153"}
    cookies = dict(NID='215=snzV4Zav-yu6zFsSruVerEC9rBPEo9dhs9ekAWIk1kBQCujaojCnvK3PaqEs21k8hUvg3CKRBuomOBlQh4fsWdcdUH-LHFYu-xIThjxKsRIpdgpX6e5Ot1DTYgCoCzAcvCX6R3vq_-1mUAyB8KmvoQhTwNAUwXro8HHKL7x-hqQ', PREF='f4=4000000&tz=Asia.Calcutta', GPS='1', VISITOR_INFO1_LIVE='T6I0_p41yvU', YSC='sIAXxVVyZLo', CONSENT='YES+cb.20210509-17-p0.en-GB+FX+345')
    headers={
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    url='https://www.youtube.com/results?search_query='+qstring
    searched=rq.get(url,headers=headers, proxies=proxies, cookies=cookies)
    soup=bs(searched.text,'html.parser')
    aid=soup.find('script',string=re.compile('ytInitialData'))
    aid=str(aid)
    """
    Filtering the no needed "ytInitialData =" syntax out of the page....
    """
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

    video_results=json.loads(str(extracted_josn_text))
    item_section=video_results["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
    videolist=[]

    for item in item_section:
        try:            
            vimg='https://i.ytimg.com/vi/'+ item["videoRenderer"]['videoId'] +'/hqdefault.jpg'
            videolist.append({'VideoId':item["videoRenderer"]['videoId'],'title':item["videoRenderer"]['title']['runs'][0]['text'],'url':vimg})
        except KeyError:
            pass
    #print(len(videolist))
    add_res={'search_string': qstring, 'result':json.dumps(videolist)}
    db['cached-search'].insert_one(add_res)
    return add_res['result']

@app.route('/youtube/<string:q>',methods=['POST','GET'])
@cross_origin()
def index(q):
    q=q.replace(' ','+')
    try:
        return Crawler(q)
    except Exception as e: 
        print(e)
        return json.dumps([])


if __name__=="__main__":
    app.run(debug=True)