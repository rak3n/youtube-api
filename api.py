from bs4 import BeautifulSoup as bs
import requests as rq
import json
from flask import Flask,request,abort
from flask_cors import cross_origin;

app=Flask(__name__)

def Crawler(qstring):
    base="https://www.youtube.com/results?search_query="
    
    r=rq.get(base+qstring)
    
    page=r.text
    soup=bs(page,'html.parser')

    vids = soup.findAll('a',attrs={'class':'yt-uix-tile-link'})
    
    videolist=[]
    for v in vids:
        vimg='https://i.ytimg.com/vi/'+ v['href'][9:] +'/hqdefault.jpg'
        videolist.append({'VideoId':v['href'][9:],'title':v['title'],'url':vimg})
    
    return json.dumps(videolist)

#print(Crawler("imagine+dragon"))

@app.route('/youtube/<string:q>',methods=['POST','GET'])
@cross_origin()
def index(q):
    q=q.replace(' ','+')
    sour=str(request.url).split('/')[2]
    if sour == 'reel-music-player.netlify.app':
        return Crawler(q)
    else:
        return json.dumps([]{'VideoId':sour,'title':sour,'url':sour})

if __name__=="__main__":
    app.run(debug=True)
