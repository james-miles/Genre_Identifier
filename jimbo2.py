#!/usr/bin/env python
# coding: utf-8

# In[46]:


import requests, bs4
import re
import pandas as pd

song = input('Enter your song: ')
song2 = song.replace(" ","+")
artist = input('Enter artist: ')
artist2 = artist.replace(" ","+")

discogs_url = 'https://www.discogs.com/'
url = f'https://www.discogs.com/search/?q={song2}&type=release'
url2 = f'https://www.discogs.com/search/?q={song2}+{artist2}&type=release'


# In[146]:


# Page 1
discogs = requests.get(url)
discogs.raise_for_status()

bSoup = bs4.BeautifulSoup(discogs.text, 'html.parser')

#Shortening html to Releases only

releases=bSoup.find_all('div', {"data-object-type": "release"})

urllist = []

#url parsing - url1, checking songname and artistname of each release

for release in releases:
    songnametag = release.findChild("h4" , recursive=False)
    artistnametag = release.findChild("h5" , recursive=False)
    
    
    if songnametag.find('a', text=re.compile(song + r'.*')):
            if artistnametag.find('a', text=re.compile(artist + r'.*')):
                    linkElem = release.select('h4>a')
                    new_url = linkElem[0].get('href')
                    discogs_url_1 = discogs_url + new_url
                    
                    urllist.append(discogs_url_1)
                    
                    
#if list is empty, try url2

if len(urllist) == 0:
        url = url2
        discogs = requests.get(url)
        discogs.raise_for_status()

        bSoup = bs4.BeautifulSoup(discogs.text, 'html.parser')

        releases=bSoup.find_all('div', {"data-object-type": "release"})

        #creating a list of all releases that have the correct songname and artistname
        for release in releases:
            songnametag = release.findChild("h4" , recursive=False)
            artistnametag = release.findChild("h5" , recursive=False)


            if songnametag.find('a', text=re.compile(song + r'.*')):
                    if artistnametag.find('a', text=re.compile(artist + r'.*')):
                            linkElem = release.select('h4>a')
                            new_url = linkElem[0].get('href')
                            discogs_url_1 = discogs_url + new_url

                            urllist.append(discogs_url_1)
                            


# In[156]:


# Load 1st Release page

discogs = requests.get(urllist[0])
discogs.raise_for_status()

# Shortening html to Release Header only

bSoup = bs4.BeautifulSoup(discogs.text, 'html.parser')
releaseheader=bSoup.find("div", {"id": "release-header"})

#Genre


Genres = releaseheader.select('a[href^="/genre/"]')
Genrelist =[]
for Genre in Genres:
    genrename = Genre.contents
    
    Genrelist.append(genrename[0])


# Style


Styles = releaseheader.select('a[href^="/style/"]')
Stylelist =[]
for Style in Styles:
    stylename = Style.contents
    Stylelist.append(stylename[0])


#dataframe and load to csv

d1 = pd.DataFrame({'url':url, 'Song_Title':song,'Artist':artist,'Genres':[Genrelist],'Styles':[Stylelist]})
d2 = (pd.DataFrame(d1.pop('Genres').values.tolist(), index=d1.index)

        .rename(columns = lambda x: 'Genre_{}'.format(x+1)))
d2
d3 = (pd.DataFrame(d1.pop('Styles').values.tolist(), index=d1.index)

        .rename(columns = lambda x: 'Style_{}'.format(x+1)))
d3
df = d1.join(d2)
dfinal =df.join(d3)
dfinal

dfinal.to_csv(song+' - '+artist+' '+'- Genres & Styles.csv',index=False)


# In[ ]:





# In[ ]:





# In[ ]:




