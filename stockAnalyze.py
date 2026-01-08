import yfinance as yf
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
import analyze
import json

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
        basicInfo[key] = data.get(key, '')
    return basicInfo

def getPriceHistory(company):
    historyDf = company.history(period='12mo')
    prices = historyDf['Open'].tolist()
    dates = historyDf.index.strftime('%Y-%m-%d').tolist()
    return {
        'price': prices,
        'date': dates
    }

def getEarningsDates(company):
    earningDatesDf = company.earnings_dates
    allDates = earningDatesDf.index.strftime('%Y-%m-%d').tolist()
    date_objects = [datetime.strptime(d, '%Y-%m-%d') for d in allDates]
    currentDate = datetime.now()
    futureDates = [d for d in date_objects if d > currentDate]
    futureDatesStr = [d.strftime('%Y-%m-%d') for d in futureDates]
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

def extractNewsArticleTextFromHtml(soup):
    allText = ''
    result = soup.find_all('div',{'class':'article yf-1pvk4a5'})
    for res in result:
        allText += res.text
    return allText

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
}

def extractCompanyNewsArticles(newsArticles):
    allArticlesText = ''
    for newsArticle in newsArticles:
        url = newsArticle['link']
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        if not soup.find_all(string='Continue reading'):
            allArticlesText += extractNewsArticleTextFromHtml(soup)
    return allArticlesText

def getCompanyStockInfo(tickerSymbol):
# Get data from Yahoo Finance API
    company = yf.Ticker(tickerSymbol)

# Get basic info on company  
    basicInfo = extractBasicInfo(company)
    time.sleep(2)
    priceHistory = getPriceHistory(company)
    futureEarningsDates = getEarningsDates(company)
    newsArticles = getCompanyNews(company)
    newsArticlesAllText = extractCompanyNewsArticles(newsArticles)
    newsTextanalysis = analyze.analyzeText(newsArticlesAllText)

    finalStockAnalysis = {
        'basicInfo': basicInfo,
        'priceHistory': priceHistory,
        'futureEarningsDates': futureEarningsDates,
        'newsArticles': newsArticles,
        'newsTextAnalysis': newsTextanalysis
    }
    return finalStockAnalysis

#companyStockAnalysis = getCompanyStockInfo('MSFT')
#print(json.dumps(companyStockAnalysis, indent=4))