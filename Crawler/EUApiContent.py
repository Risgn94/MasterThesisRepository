#importing pandas library as pd
#import library
import pandas as pd
from EUApi import CrawlerFunctions
import datetime

import sys
sys.path.append("..")

start = 0
iterations = 23000
#Reading existing data from excel file and converting to pandas dataframe
print("Loading data...")
df = pd.read_excel('NewEUArticleContentData.xlsx')
print("Finished loading data")

#Iterate over all instances in dataframe
for index, row in df.iterrows():
    if(index > start):
        try:
            #Print how many percent has been iterated
            print("Iteration: " + str(((index-start)/iterations)*100)+"%")
            #Only iterate if row content is equal "None"
            if (row['Content'] == "None" or row['Content'] == ""):
                startTime = datetime.datetime.now()
                crawlerValue = CrawlerFunctions.runCrawl(row)

                if (crawlerValue != "None"):
                    df.loc[index, ('Content')] = crawlerValue
                    endTime = datetime.datetime.now()
                    diff = endTime - startTime
                    print(diff)
            if (index == iterations+start):
                break

        except Exception as e:
            print("Exception occurred. Trying so make backup")
            print(e)
            writer = pd.ExcelWriter('NewEUArticleContentData.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})
            df.to_excel(writer, 'Sheet1')
            writer.save()
            print("Backup save.")
    else:
        print(index)

writer = pd.ExcelWriter('EUArticleContentData2018.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})
df.to_excel(writer, 'Sheet1')
writer.save()
print("Document saved.")

