import pandas as pd
import re
import nltk.tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from html.parser import HTMLParser
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from Cleaning import CleanHTML

class Cleaner():
    def __init__(self, filePath):
        #Inherents from HTMLParser class and initialize
        self.filePath = filePath
        self.dataFrame = pd.read_excel(self.filePath)
        self.stem = SnowballStemmer("english")
        self.sia = SIA()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []


    def GetCleanedDataframe(self, columns=None, targetVar=None):
        columns.append(targetVar)
        localDf = pd.DataFrame(columns=columns)
        for index, row in self.dataFrame.iterrows():
            add = True
            print(index)
            rowList = []
            for column in columns:
                print(row[column])
                if (row[column] == "None" or str(row[column]) == "" or str(row[column]) == "nan"):
                    add = False
                elif (column != targetVar):
                    cleanValue = self._fullCleanString(row[column])
                    rowList.append(cleanValue)
            rowList.append(row[targetVar])
            if(add):
                localDf.loc[index] = rowList
        return localDf

    def GetCleanedDataNoStem(self, columns=None):
        localDf = pd.DataFrame(columns=columns)
        for index, row in self.dataFrame.iterrows():
            add = True
            print(index)
            rowList = []
            for column in columns:
                print(row[column])
                if (row[column] == "None" or str(row[column]) == "" or str(row[column]) == "nan"):
                    add = False
                else:
                    cleanValue = self._cleanHTMLString(row[column])
                    rowList.append(cleanValue)
            if(add):
                localDf.loc[index] = rowList
        return localDf

    def cleanDataframe(self, columns=None, targetVar=None):
        columns.append(targetVar)
        localDf = pd.DataFrame(columns=columns)
        for index, row in self.dataFrame.iterrows():
            if (index == 10):
                break
            rowList = []
            for column in columns:
                if (column != targetVar):
                    cleanValue = self._fullCleanString(row[column])
                    rowList.append(cleanValue)
            rowList.append(row[targetVar])
            localDf.loc[index] = rowList
        self.dataFrame = localDf



    def _cleanHTMLString(self, text):
        # Remove html tags, but keep inner text
        cleanhtml = CleanHTML.strip_tags
        noHTMLText = cleanhtml(text)
        nominal = str(noHTMLText)
        return nominal

    def _fullCleanString(self, text):
        #Remove html tags, but keep inner text
        cleanhtml = CleanHTML.strip_tags
        noHTMLText = cleanhtml(text)
        unique_instances = []
        nominal = str(noHTMLText)
        list1 = self._stemString(nominal)
        for listWords in list1:
            unique_instances.append(listWords)
        cleanText = " ".join(unique_instances)
        return cleanText

    def _fullCleanNoStem(self, text):
        cleanhtml = CleanHTML.strip_tags
        noHTMLText = cleanhtml(text)
        unique_instances = []
        nominal = str(noHTMLText)
        list1 = self._stemString(nominal)
        for listWords in list1:
            unique_instances.append(listWords)
        cleanText = " ".join(unique_instances)
        return cleanText

    def getUniqueWords(self, parameters):
        unique_instances = []
        for index, row in self.dataFrame.iterrows():
            for elements in parameters:
                nominal = str(row[elements])
                list1 = self._stemString(nominal)
                for listWords in list1:
                    unique_instances.append(listWords)
        unique_sets = list(set(unique_instances))
        return unique_sets

    def stemString(self, string):
        return self._stemString(string)

    def removeStopWords(self, parameters):
        unique_instances = []
        for index, row in self.dataFrame.iterrows():
            for elements in parameters:
                nominal = str(row[elements])
                list1 = self._stemString(nominal)
                for listWords in list1:
                    unique_instances.append(listWords)
        unique_sets = list(set(unique_instances))
        return unique_sets

    def getUniqueTitlesWords(self, parameters):
        unique_instances = []
        for index, row in self.dataFrame.iterrows():
            for elements in parameters:
                nominal = str(row[elements])
                list1 = self._stemString(nominal)
                for listWords in list1:
                    unique_instances.append(listWords)
        unique_sets = list(set(unique_instances))
        return unique_sets

    def getUniqueContentWords(self):
        unique_instances = []
        for index, row in self.dataFrame.iterrows():
            nominal = str(row["Content"])
            list1 = self._stemString(nominal)
            for listWords in list1:
                unique_instances.append(listWords)
        unique_sets = list(set(unique_instances))
        return unique_sets

    def countWords(self):
        print("Counting words...")
        localDf = pd.DataFrame(columns=["Domain", "Link", "Title", "date", "Content", "TitleCount", "ContentCount" ])
        for index, row in self.dataFrame.iterrows():
            print("Current row: "+str(index))
            try:
                titleCount = len(self._stemString(row["Content"]))
                contentCount = len(self._stemString(row["Title"]))
                localDf.loc[index] = [row["Domain"], row["Link"], row["date"], row["Title"], row["Content"], contentCount, titleCount]
            except:
                print("String could not be counted")
        return localDf

    def saveNew(self, file=None, fileName=None):
        print("Saving file...")
        writer = pd.ExcelWriter(fileName + '.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})
        file.to_excel(writer, 'Sheet1')
        writer.save()
        print("File saved.")

    def saveFile(self, fileName):
        print("Saving file...")
        writer = pd.ExcelWriter(fileName+'.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})
        self.dataFrame.to_excel(writer, 'Sheet1')
        writer.save()
        print("File saved.")

    def stemDataFrame(self, start, end, id, return_dict):
        print("Stemming words...")
        localDf = pd.DataFrame(columns=["Domain", "Link", "date", "TitleStemmed", "ContentStemmed", "TitleCount", "ContentCount", "TitlePolar", "ContentPolar"])
        df = self.dataFrame
        for index in range(start, end):
            if(str(df['Content'].values[index]) != "None"):
                try:
                    print("Current row: " + str(index))
                    #try:
                    #Getting sentiment
                    titleRes = self._polarScore(str(df['Title'].values[index]))
                    contentRes = self._polarScore(str(df['Content'].values[index]))
                    #stemming titles and content
                    titleStemmed = self._stemString(df['Title'].values[index])
                    contentStemmed = self._stemString(df['Content'].values[index])
                    #Getting length of stemmed
                    titleCount = len(titleStemmed)
                    contentCount = len(contentStemmed)
                    localDf.loc[index] = [df["Domain"].values[index], df["Link"].values[index], df["date"].values[index],
                                          " ".join(titleStemmed), " ".join(contentStemmed),
                                          titleCount, contentCount, titleRes, contentRes]
                except Exception as e:
                    print("String could not be stemmed")
        return_dict[id] = localDf
        #return localDf

    def _removeStopwords(self, str)


    def _stemString(self, str):
        # remove special characters & make into lowercase
        str = self._removeSpecialCharacters(str)
        # remove leading spaces
        str = str.lstrip()
        # word to lower
        str = str.lower()
        # create an empty list
        filtered_word_list = []
        # create a tokenlist
        tokenList = nltk.tokenize.word_tokenize(str)
        # for every word in token list:
        for words in tokenList:
            # if word is not a stopword do add to filtered word list
            if words not in stopwords.words('english'):
                filtered_word_list.append(words)
        filtered_word_list = [self.stem.stem(word) for word in filtered_word_list]
        return filtered_word_list

    def _removeSpecialCharacters(self,str):
        newStr = re.sub(r'\W+', ' ', str)
        newStr2 = re.sub(r"\d+", "", newStr)
        return newStr2

    # modtage dataframe row,
    def GetStanSingle(string):
        pass

    def importExcelfile(int):
        pass