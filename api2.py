from bs4 import BeautifulSoup as bs
import requests
import re
import json
headers={
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

url='https://www.youtube.com/results?search_query='+'gurenge'
searched=requests.get(url,headers=headers)
soup=bs(searched.text,'html.parser')
aid=soup.find('script',string=re.compile('ytInitialData'))
#extracted_josn_text=str(aid).split(';')[0].replace('window["ytInitialData"] =','').strip()
#print(str(aid).split(';')[0].split('\n')[1].replace('window["ytInitialData"] =','').strip())
extracted_josn_text=str(aid).split(';')[0].split('\n')[1].replace('window["ytInitialData"] =','').strip()
#print(extracted_josn_text)
video_results=json.loads(extracted_josn_text)
#print(item_section=video_results["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][1])
#print(video_results["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][""])
item_section=video_results["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]

for item in item_section:
    
    print("---------------------------------------------------------------------------------------")
    try:
        print(item["videoRenderer"]['videoId'])
        print(item["videoRenderer"]['title']['runs'][0]['text'])
        """video_info=item["videoRenderer"]
        title=video_info["title"]["simpleText"]
        url=video_info["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]
        print('Title:',title)
        print('Url:',url)
        """
    except KeyError:
            pass
