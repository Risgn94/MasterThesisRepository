from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse
import datetime
import pandas as pd
import time


#http://emm.newsbrief.eu/NewsBrief/dynamic?language=en&page=1&edition=searcharticles&option=advanced&all=bitcoin&dateFrom=2016-01-01&dateTo=2016-01-01&lang=en&_=1518084825191
#article link: .headline_link href
#article title: .headline_link text
#article source: //Get root from link
#article datetime: .center_headline_source text

startDate = datetime.datetime.strptime('01022018', "%d%m%Y").date()
endDate = datetime.datetime.strptime('28022018', "%d%m%Y").date()

delta = endDate - startDate

daysDiff = delta.days

dataArray = []

urlArray = []

print("start date: "+str(startDate))
print("end date: "+str(endDate))

date = startDate
for i in range(daysDiff):
    date += datetime.timedelta(days=1)
    urlArray.append("http://emm.newsbrief.eu/NewsBrief/dynamic?language=en&page=1&edition=searcharticles&option=advanced&all=bitcoin&dateFrom="+str(date)+"&dateTo="+str(date)+"&lang=en&_=1518084825191")

for urls in urlArray:
    hasData = True
    iterator = 1
    while hasData:

        #time.sleep(1)
        pageString = "page="+str(iterator)
        crawlUrl = urls.replace("page=1", pageString)
        print(crawlUrl)
        page = urlopen(crawlUrl)
        soup = BeautifulSoup(page, 'html.parser')

        articleLinks = soup.select(".headline_link")
        articleDateTimes = soup.select(".center_headline_source")

        articleContainer = soup.select(".articlebox_big")

        articleLength = len(articleLinks)

        if(articleLength < 1):
            hasData = False
            break

        for idx, articles in enumerate(articleLinks):
            articleLink = articles['href']
            articleHeader = articles.text
            parsed_uri = urlparse(articleLink)
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            articleDateTime = soup.select(".center_headline_source")[idx].text

            #Manipulate datetime string
            print(articleDateTime)
            articleDateTime = articleDateTime[(articleDateTime.find(",")+2):]
            articleDateTime = articleDateTime.replace("|", "")
            articleDateTime = articleDateTime.replace("info", "")
            articleDateTime = articleDateTime.replace("[other]", "")
            articleDateTime = articleDateTime.replace("    ", "")

            datetime_object = datetime.datetime.strptime(articleDateTime, '%B %d, %Y %I:%M:%S %p %Z ')

            dataArray.append({
                "Title": articleHeader,
                "Domain":domain,
                "Link": articleLink,
                "DateTime":datetime_object
            })
        iterator +=1

df = pd.DataFrame(dataArray)
writer = pd.ExcelWriter('EUExport2018Februar.xlsx', engine='xlsxwriter',options={'strings_to_urls': False})
df.to_excel(writer,'Sheet5')
writer.save()