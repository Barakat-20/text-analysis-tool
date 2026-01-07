import yfinance as yf
import time
from datetime import datetime, date
def extractBasicInfo(company):
    data = company.fast_info

    keysToExtract = [
        'longName',
        'sector',
        'fullTimeEmployees',
        'marketCap',
        'totalRevenue',
        'trailingEps'
    ]

    basicInfo = {}
    for key in keysToExtract:
        basicInfo[key] = data.get(key, "")

    return basicInfo

def getPriceHistory(company):
    historyDf = company.history(period="12mo")
    prices = historyDf['Open'].tolist()
    dates = historyDf.index.strftime("%Y-%m-%d").tolist()
    return {
        'price': prices,
        'date': dates
    }

def getEarningsDates(company):
    earningDatesDf = company.earnings_dates
    allDates = earningDatesDf.index.strftime("%Y-%m-%d").tolist()
    date_objects = [datetime.strptime(d, "%Y-%m-%d") for d in allDates]
    currentDate = datetime.now()
    futureDates = [d for d in date_objects if d > currentDate]
    futureDatesStr = [d.strftime("%Y-%m-%d") for d in futureDates]
    return futureDatesStr

def getCompanyNews(company):
    newsList = company.news
    allNewsArticles =[]
    for newsDict in newsList:
        content = newsDict.get('content', {})
        newsDictToAdd = {
            'title': content.get('title', ''),
            'link': content.get('canonicalUrl', {}).get('url', '')
        }
        allNewsArticles.append(newsDictToAdd)
    return allNewsArticles

def getCompanyStockInfo(tickerSymbol):
# Get data from Yahoo Finance API
    company = yf.Ticker(tickerSymbol)

# Get basic info on company  
    basicInfo = extractBasicInfo(company)
    time.sleep(2)
    priceHistory = getPriceHistory(company)
    futureEarningsDates = getEarningsDates(company)
    newsArticles = getCompanyNews(company)

getCompanyStockInfo('MSFT')
