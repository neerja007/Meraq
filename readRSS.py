import requests
from bs4 import BeautifulSoup
import csv
filename = 'nasdaq.csv'
with open(filename) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        URL = "https://www.biopharmcatalyst.com/company/"+row[1]+"/news"

        print(URL)
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib')
        #print(soup.prettify())
        newslist = soup.findAll('li', attrs={'class': 'news-item'})
        datetimelist = soup.findAll(attrs={'class':'news-item__time'})
        #print(len(newslist))
        for news in newslist:
            title = news.findNext('a', attrs={'class': 'news-item__link'})
            datetime = news.findNext(attrs={'class':'news-item__time'})
            print(datetime.text)
            print(title.text)
        break


