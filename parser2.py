import requests
import simplejson as json
import re
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup


def slowtv_scrape():
    vgm_url = 'https://tv.idnes.cz/slow'
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    urllist=[]
    out_list=[]
    count=0

    for link in soup.find_all('a'):
        if "/slow/" in link.get('href'):
            urllist.append(link.get('href'))
    #        print(link.get('class'))
    #    else:
    #        print("fuk")

    #print(urllist)



    for url in urllist:
        html_text = requests.get(url).text
        #print("---------")
        #print("URL: "+url)
        soup = BeautifulSoup(html_text, 'html.parser')
        tento_item={}

        #print("Title: " + soup.title.string)
        tento_item['title'] = soup.title.string
        for img in soup.find_all('meta',attrs={"name": "twitter:image"}):
            #print("poster: https:"+img.get('content'))
            #print(count)
            tento_item['poster'] = ("https:"+img.get('content'))
            #print(tento_item['poster'])
        ## nasli jsme tuto URL: https://servix.idnes.cz/media/video.aspx?idvideo=V190130_125507_idnestv_taus&reklama=1&idrubriky=tv-slow&idnestv=1

        url_parse = urlparse(url)
        #print(url_parse.path)
        dict_result = parse_qs(url_parse.path)
        

        taus=url.split(".")[-1]
        #print(taus)
        year=str(taus.split("V")[1])[0:2]
        if "letiste" in url:
            year="16"
        #print(year)
        tento_item['year']="20"+year


        #if url
        #print(year)
        url_playlist = "https://1gr.cz/data/nocache/videostream/20"+year+"/"+taus+".js"
        #print("Playlist: "+url_playlist)

        playlist_data = requests.get(url_playlist).text
        #print(playlist_data)
        playlist_json = json.loads(playlist_data)
        
        if playlist_json['q720p'] == True:
            quality = "720p"
        if playlist_json['q1080p'] == True:
            quality = "1080p"
        
        #print(quality)
        try:
            videokey = playlist_json['video'] # data is a dict
            for video in videokey:
                if video['quality'] == quality:
                    if video['format'] == "mdash":
                        videourl = video['file']
        except KeyError:
            videourl = "no url given"

        #print("videourl: "+videourl)
        tento_item['url'] = videourl
        
        count=count+1
        tento_item['plot'] = "SlowTV"
        #print(tento_item)
        out_list.append(tento_item)

    return out_list

print(slowtv_scrape())
'''
    #nacti URL jako XML
    #html_text = requests.get(url).text
    #soup = BeautifulSoup(html_text, 'xml')
    #names = soup.find_all('name')
    #for name in names:
    #  print(name.text)




    # get neco jako https://1gr.cz/data/nocache/videostream/2019/V190326_153451_idnestv_taus.js

    # vem taus a pridej pred nej "https://1gr.cz/data/nocache/videostream/2019/" + taus+ ".js"




'''