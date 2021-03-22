import requests, bs4

song = input('Enter your song: ')
artist = input('Enter artist: ')

discogs_url = 'https://www.discogs.com/'
url = f'https://www.discogs.com/search/?q={song}+{artist}&type=all'

# Page 1
discogs = requests.get(url)
discogs.raise_for_status()

bSoup = bs4.BeautifulSoup(discogs.text, 'html.parser')

linkElem = bSoup.select('#search_results > div:nth-child(1) > h4 > a')

new_url = linkElem[0].get('href')
discogs_url_1 = discogs_url + new_url


# Page 2
discogs = requests.get(discogs_url_1)
discogs.raise_for_status()

# Genre

bSoup = bs4.BeautifulSoup(discogs.text, 'html.parser')

classElem = bSoup.find_all("div", {"class": "content_3IW3p"})

info_list = []
for i in range(len(classElem)):
    # print(classElem[i].getText())
    info_list.append(classElem[i].getText())

with open('test.csv', 'a') as csv_file:
    csv_file.write(info_list[-2] + '\n')
    csv_file.write(info_list[-1] + '\n')

print(info_list[-2])
print(info_list[-1])

# genreElem = bSoup.select('#page_content > div.body > div.profile > div:nth-child(3)')


# for i in range(len(genreElem)):
#     print(genreElem[i].getText())

# # Style

# styleElem = bSoup.select('#page_content > div.body > div.profile > div:nth-child(5)')

# for i in range(len(styleElem)):
#     print(styleElem[i].getText())