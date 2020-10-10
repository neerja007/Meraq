import requests 
from bs4 import BeautifulSoup 
import csv

filename = 'nasdaq.csv'
with open(filename) as csvfile: 
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV: 
        print(row[3])
        
        
