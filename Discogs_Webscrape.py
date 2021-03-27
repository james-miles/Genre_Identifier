#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests, bs4
import re
import pandas as pd
from tkinter.filedialog import askopenfilename

#song = input('Enter your song: ')
#song2 = song.replace(" ","+")
#artist = input('Enter artist: ')
#artist2 = artist.replace(" ","+")

filepath = askopenfilename()

Songspd = pd.read_csv(filepath) 

discogs_url = 'https://www.discogs.com/'


# In[5]:


# defining final df

dfinal = []

# per song, begin the genre & style scrape

rows = Songspd.values.tolist()

for row in rows:
    song = row[0]
    artist = row[1]
    song2 = song.replace(" ","+")
    artist2 = artist.replace(" ","+")
    url = f'https://www.discogs.com/search/?q={song2}&type=release'
    url2 = f'https://www.discogs.com/search/?q={song2}+{artist2}&type=release'


    # Page 1
    discogs = requests.get(url)
    discogs.raise_for_status()

    bSoup = bs4.BeautifulSoup(discogs.text, 'html.parser')

    #Shortening html to Releases only

    releases=bSoup.find_all('div', {"data-object-type": "release"})

    urllist = []

    #url parsing - url1, checking songname and artistname of each release

    for release in releases:
        if len(urllist) == 3:
            break
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
                if len(urllist) == 3:
                    break
                songnametag = release.findChild("h4" , recursive=False)
                artistnametag = release.findChild("h5" , recursive=False)


                if songnametag.find('a', text=re.compile(song + r'.*')):
                        if artistnametag.find('a', text=re.compile(artist + r'.*')):
                                linkElem = release.select('h4>a')
                                new_url = linkElem[0].get('href')
                                discogs_url_1 = discogs_url + new_url

                                urllist.append(discogs_url_1)
    
    #take first three matching realease urls
    
    urlnames = urllist[0:3]
    
    #Defining Genre & Style List

    Genrelist =[]
    Stylelist =[]


    for urlname in urlnames:



            # Load each Release page

            discogs = requests.get(urlname)
            discogs.raise_for_status()


            # Shortening html to Release Header only

            bSoup = bs4.BeautifulSoup(discogs.text, 'html.parser')
            releaseheader=bSoup.find("div", {"id": "release-header"})

            #Genre


            Genres = releaseheader.select('a[href^="/genre/"]')

            for Genre in Genres:
                genrename = Genre.contents

                Genrelist.append(genrename[0])


            # Style


            Styles = releaseheader.select('a[href^="/style/"]')

            for Style in Styles:
                stylename = Style.contents
                Stylelist.append(stylename[0])

    # Unique values for Genre and Styles

    Genrelist = set(Genrelist)
    Genrelist = (list(Genrelist))

    Stylelist = set(Stylelist)
    Stylelist = (list(Stylelist))
    
    # creating df, Splitting Genres and Styles to seperate columns in df
    
    d1 = pd.DataFrame({'url1':urlnames[0],'url2':urlnames[1],'url3':urlnames[2], 'Song_Title':song,'Artist':artist,'Genres':[Genrelist],'Styles':[Stylelist]})
    d2 = (pd.DataFrame(d1.pop('Genres').values.tolist(), index=d1.index)

            .rename(columns = lambda x: 'Genre_{}'.format(x+1)))
    d2
    d3 = (pd.DataFrame(d1.pop('Styles').values.tolist(), index=d1.index)

            .rename(columns = lambda x: 'Style_{}'.format(x+1)))
    d3
    df = d1.join(d2)
    df4 =df.join(d3)
    
    #Appending each output df and merging to into one final df
    
    dfinal.append(df4)
    
df = pd.concat(dfinal)
df
df.to_csv('Genres & Styles Output.csv',index=False)


# In[ ]:




