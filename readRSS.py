import requests
import datetime
import yfinance as yf
from bs4 import BeautifulSoup
import csv

filename = 'nasdaq.csv'
key_class = ["merge","collab","partner","buyout","acqui"]
ticker_list = []
name_list = []
with open(filename) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row2 in readCSV:
        ticker_list.append(row2[1])
        name_list.append(row2[2])
    
with open(filename) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    ct = 0
    perc_inc_list =[[]]

    for row in readCSV:
       # row[1] = 'ABBV'
        
        URL = "https://www.biopharmcatalyst.com/company/"+row[1]+"/news"
        tickcur = yf.Ticker(row[1])
        c1Cap = int(tickcur.info['marketCap']/1000000)
        print(row[1],row[2])
        print(c1Cap) #
        #print(URL)
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib')
        #print(soup.prettify())
        newslist = soup.findAll('li', attrs={'class': 'news-item'})
        datetimelist = soup.findAll(attrs={'class':'news-item__time'})
        perc_inc = []
        #print(len(newslist))
        for news in newslist:
            title = news.findNext('a', attrs={'class': 'news-item__link'})
            body = news.findNext('div', attrs={'class': 'teaser'})
            datetime1 = news.findNext(attrs={'class':'news-item__time'})
            for key1 in key_class:
                if key1 in title.text.lower():
                    
                    date_time_str = datetime1.text
                    date_time_obj = datetime.datetime.strptime(date_time_str, '%d %B %Y')
                    #print('Date:', date_time_obj.date())
                    #print(datetime1.text)
                    
                    othercomp = ""
                    otherCap = -1
                    #readCSV2 = csv.reader(csvfile, delimiter=',')
                    for i in range(len(ticker_list)):
                         test = body.text#.replace("COVID","")
                         if (ticker_list[i] in test) and (name_list[i].split()[0] in test) and ticker_list[i]!=row[1]:
                        #if (row2 in body.text):
                             print(ticker_list[i],name_list[i])
                             othercomp = ticker_list[i]
                             tick = yf.Ticker(othercomp)
                             otherCap = int(tick.info['marketCap']/1000000)
                             print(otherCap) # million
                             break
                       
                    #print('==================================')
                    smallcomp = ""
                    if(otherCap==-1):
                        continue
                    print(title.text)

                    if(otherCap<c1Cap):
                        smallcomp = othercomp
                    else:
                        smallcomp = row[1]
                    
                    #print(body.text) 
                    #input()
                    #print("Input received")
                    data = yf.download(smallcomp,start=date_time_obj.date()-datetime.timedelta(days=1),end=date_time_obj.date()+datetime.timedelta(days=90))
                    #print(tick.info['marketCap'])
                    ref_value =  data['Open'][0]
                    next_day1 = data['Open'][1] if len(data['Open'])>2 else ref_value
                    next_day2 = data['Open'][2] if len(data['Open'])>3 else ref_value
                    next_day7 = data['Open'][7] if len(data['Open'])>8 else ref_value
                    next_day30 = data['Open'][30] if len(data['Open'])>31 else ref_value
                    next_day60 = data['Open'][60] if len(data['Open'])>61 else ref_value

                    
                    perc_inc = [(next_day1-ref_value) / ref_value*100.0, 
                                 (next_day2-ref_value) / ref_value*100.0, 
                                 (next_day7-ref_value) / ref_value*100.0, 
                                 (next_day30-ref_value) / ref_value*100.0, 
                                 (next_day60-ref_value) / ref_value*100.0]
                    perc_inc_list.append(perc_inc)      
                    print(perc_inc)
                    break
        if(len(perc_inc)==0):
            print("No mergers")
        else:
            print("All mergers done")
            #print(perc_inc_list)
        ct = ct+1
       # if(ct>25):
            #break
print("COMPLETED")
        


