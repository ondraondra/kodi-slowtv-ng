import requests
import simplejson as json
import re
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

vgm_url = 'https://tv.idnes.cz/slow'
html_text = requests.get(vgm_url).text
soup = BeautifulSoup(html_text, 'html.parser')

urllist=[]

for link in soup.find_all('a'):
    if "/slow/" in link.get('href'):
        urllist.append(link.get('href'))
#        print(link.get('class'))
#    else:
#        print("fuk")

print(urllist)


for url in urllist:
    html_text = requests.get(url).text
    #print("---------")
    print("URL: "+url)
    soup = BeautifulSoup(html_text, 'html.parser')
    
    print("Title: " + soup.title.string)
    for img in soup.find_all('meta',attrs={"name": "twitter:image"}):
        print("img: https:"+img.get('content'))
    
    for match in soup.find_all('script'):
#        matched_video_url = soup.find_all(lambda tag: len(tag.find_all()) > 0)# and "video.aspx" in tag.text)
#        for matched_tag in matched_video_url:
#          print("Matched:", matched_tag)
        for i in match:
            if ("video.aspx" in i.string):
                #print (i)
                #ii = i.replace("Misc.video(", "",1)
                #iii = ii.replace(");","",1)
                #iiii = iii.replace("\'", "\"")
                #iiii = re.sub(r"(\w+):", r'"\1":',iii)
                #iiiii = re.sub(r": (\w+)", r': "\1"',iiii)
                #iiiiii = re.sub(r":(\w+)", r': "\1"',iiiii)
                
                #print(iiiiii)
                                

                #y = json.loads(iiii)
                #print(y)

                #print(i)
                ii = i.split("\"")
                url_xml = "https:"+ii[1]
                #print(url_xml)
                
                ## nasli jsme tuto URL: https://servix.idnes.cz/media/video.aspx?idvideo=V190130_125507_idnestv_taus&reklama=1&idrubriky=tv-slow&idnestv=1

                url_parse = urlparse(url_xml)
                #print(url_parse.query)
                dict_result = parse_qs(url_parse.query)
                taus=''.join(dict_result['idvideo'])
                year=str(taus.split("V")[1])[0:2]
                #if url
                #print(year)
                url_playlist = "https://1gr.cz/data/nocache/videostream/20"+year+"/"+''.join(dict_result['idvideo'])+".js"
                print("Playlist: "+url_playlist)

                playlist_data = requests.get(url_playlist).text
                #print(playlist_data)
                playlist_json = json.loads(playlist_data)
                
                if playlist_json['q720p'] == True:
                    quality = "720"
                if playlist_json['q1080p'] == True:
                    quality = "1080"
                
                print(quality)
                try:
                    videokey = playlist_json['video'] # data is a dict
                    for video in videokey:
                        if video['quality'] == "720p":
                            if video['format'] == "mdash":
                                videourl = video['file']
                except KeyError:
                    videourl = "no url given"

                print("videourl: "+videourl)
                

                #nacti URL jako XML
                #html_text = requests.get(url).text
                #soup = BeautifulSoup(html_text, 'xml')
                #names = soup.find_all('name')
                #for name in names:
                #  print(name.text)




                # get neco jako https://1gr.cz/data/nocache/videostream/2019/V190326_153451_idnestv_taus.js

                # vem taus a pridej pred nej "https://1gr.cz/data/nocache/videostream/2019/" + taus+ ".js"




