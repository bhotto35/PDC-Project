from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
import pandas as pd
import numpy as np
import re
import time
def scrape_ticker(ticker):
    global newdf0
    url = "https://finviz.com/quote.ashx?t="+ticker
    html_text = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'}).text
    soup = bs(html_text,"html.parser")
    table = soup.find("table",{"class":"fullview-news-outer"})
    company = None
    try:
        company = soup.find("table",{"class":"fullview-title"}).find("a",{"class":"tab-link"}).find("b").decode_contents()
    except:
        company = ""
    #print(table)
    rows = table.find_all("tr")
    datelist = []
    headlines = []
    count = 0
    for row in rows:
        datecell = row.find("td",{"align":"right"})
        date_content = datecell.decode_contents()
        #print(date_content)
        try:
            datetime_object = datetime.strptime(str(date_content).strip(), '%b-%d-%y %I:%M%p')
            date_string = str(datetime_object).split()[0]
        except ValueError:
            date_string = datelist[count-1]
        #if date_string not in datelist:
        datelist.append(date_string)
        newscell = row.find("a",{"class":"tab-link-news"})
        news_content = newscell.decode_contents()
        headlines.append(news_content)
        count+=1
    tickers = [ticker for i in range(len(datelist))] 
    companies = [company for i in range(len(tickers))]
    df = pd.DataFrame({"date":datelist,"ticker": tickers,"company":companies,"headline":headlines})
    return df