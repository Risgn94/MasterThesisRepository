""" Script demonstrating various methods of classifying JP articles """
import time
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
import math
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.feature_selection import SelectFromModel
import csv

class Classifier():
    def __init__(self, fileName=None):
        self.results = []
        self.y_results = []
        self.coefficients = []
        self.FileName = fileName

    def defineClassifier(self,Classifier=None, ClassifierName=None):
        self.Classifier = Classifier
        self.ClassifierName = ClassifierName


    def defineParameters(self, Content=None, Target=None, File=None, Analyzer=None, Ngram_Range=(1,2), Max_Features=None, Min_DF=0, Max_DF=100, Lowercase=True, Limit=None):
        self.Content = Content
        self.Target = Target
        self.File = File
        self.Analyzer = Analyzer
        self.Ngram_Range = Ngram_Range
        self.Max_Features = Max_Features
        self.Min_DF = Min_DF
        self.Max_Df = Max_DF
        self.Lowercase = Lowercase
        self.Limit = Limit

        print("Loading data...")
        begin = time.time()
        self.Dataframe = pd.read_excel(self.File, index_col=None)
        print("Done in %.1f seconds" % (time.time() - begin))
        if(self.Content == "Both"):
            self.Dataframe["allContent"] = self.Dataframe["Title"]+self.Dataframe["Content"]
        elif(self.Content == "BothPrefix"):
            self.Dataframe["allContent"] = self.Dataframe["TitlePrefix"]+self.Dataframe["ContentPrefix"]
        else:
            self.Dataframe["allContent"] = self.Dataframe[self.Content]

    def runClassifierCrossValidate(self, folds, repeats):
        inner_Results = {
            self.ClassifierName: []
        }
        inner_Results[self.ClassifierName].append(0)
        for x in range(0, repeats):
            df_random = self.Dataframe.sample(frac=1).reset_index(drop=True)

            num_folds = folds
            subset_size = math.ceil(30000 / num_folds)

            currentFoldResults = []

            for i in range(num_folds):
                classifier_list = []

                training_start = (i * subset_size) + 1
                training_end = int(round(training_start + (0.9 * subset_size)))

                test_start = int(round(training_end + 1))
                test_end = int(round((test_start + (0.1 * subset_size)) - 1))

                if (i == 0):
                    training_start = 0

                training_set = df_random[training_start:training_end]
                testing_set = df_random[test_start:test_end]

                X_train = training_set["allContent"].values
                y_train = training_set[self.Target].values

                X_test = testing_set["allContent"].values
                y_test = testing_set[self.Target].values

                clf = Pipeline([
                    ("tf-idf", TfidfVectorizer(analyzer=self.Analyzer, ngram_range=self.Ngram_Range,
                                               max_features=self.Max_Features, lowercase=self.Lowercase,
                                               min_df=self.Min_DF, max_df=self.Max_Df)),
                    (self.ClassifierName, self.Classifier)
                ])

                clf.fit(X_train, y_train)
                classifier_list.append(clf)
                y_pred = clf.predict(X_test)

                vectorizer = clf.steps[0][1]
                localClassifier = clf.steps[1][1]

                if((i+1)*(x+1) == 1):
                    self._show_most_informative_features(vectorizer, localClassifier, str((i + 1) * (x + 1)))

                currentFoldResults.append([y_test, y_pred])
                inner_Results[self.ClassifierName].append(precision_score(y_test, y_pred, average='weighted'))
            self.y_results.append(currentFoldResults)
        with open(("WordFiles/CoefficientWords"+ '-' +self.ClassifierName+'-'+self.Target+'-'+self.Content+ '-' + str(self.Ngram_Range)+ str('-DF')+ str(self.Max_Df)+"-"+str(self.Min_DF)+"-"+self.Analyzer +".csv"), 'w', encoding='UTF-8',) as myfile:
            wr = csv.writer(myfile, delimiter=';')
            wr.writerows(self.coefficients)
            print(self.coefficients)

    def cleanForNewRun(self):
        self.results = []
        self.y_results = []
        self.coefficientDataframe = []

    def printResults(self):
        fileName = 'Logfiles/Log'+self.ClassifierName+'-'+self.Target+'-'+self.Content+ '-' + str(self.Ngram_Range)+ str('-DF')+ str(self.Max_Df)+"-"+str(self.Min_DF)+"-"+self.Analyzer+'.txt'
        logFile = open(fileName, 'w')
        overallAveragePrecisionScore = 0
        overallAverageAccuracyScore = 0
        overallAverageF1Score = 0
        overallAverageRecallScore = 0
        overallFolds = 0
        precisionArray = []
        crossPrecisionArray = []

        for idx, results in enumerate(self.y_results):
            averagePrecisionScore = 0
            averageAccuracyScore = 0
            averageF1Score = 0
            averageRecallScore = 0
            folds = 0

            for innerIdx, innerResults in enumerate(results):
                logFile.write("Confusion matrix and classification report for %i cross validation in %i repeat \n" %(innerIdx, idx))
                print("Confusion matrix and classification report for %i cross validation in %i repeat " %(innerIdx, idx))
                cm = confusion_matrix(innerResults[0], innerResults[1])
                logFile.write(str(cm)+"\n")
                print(confusion_matrix(innerResults[0], innerResults[1]))
                #print(classification_report(innerResults[0], innerResults[1]))

                averagePrecisionScore = averagePrecisionScore + precision_score(innerResults[0], innerResults[1],
                                                                                average='weighted')

                #print("Fold precision: "+precision_score(innerResults[0], innerResults[1],average='weighted'))
                precisionArray.append(float(precision_score(innerResults[0], innerResults[1],
                                                                                average='weighted')))
                averageAccuracyScore = averageAccuracyScore + accuracy_score(innerResults[0], innerResults[1])
                averageF1Score = averageF1Score + f1_score(innerResults[0], innerResults[1], average='weighted')
                averageRecallScore = averageRecallScore + recall_score(innerResults[0], innerResults[1], average='weighted')

                folds = folds + 1

            crossPrecisionArray.append(averagePrecisionScore / folds)

            overallAveragePrecisionScore = overallAveragePrecisionScore + (averagePrecisionScore / folds)
            overallAverageAccuracyScore = overallAverageAccuracyScore + (averageAccuracyScore / folds)
            overallAverageF1Score = overallAverageF1Score + (averageF1Score / folds)
            overallAverageRecallScore = overallAverageRecallScore + (averageRecallScore / folds)
            overallFolds = overallFolds + 1

        #print("Average accuracy for all repeats: "+ str(overallAverageAccuracyScore / overallFolds))
        print("Average precision for all repeats: "+ str(overallAveragePrecisionScore / overallFolds))
        logFile.write("Average precision for all repeats: "+ str(overallAveragePrecisionScore / overallFolds) + "\n")
        stdDev = np.array(precisionArray)
        print("Standard Deviation for all repeats: "+str(np.std(stdDev, axis=0)))
        logFile.write("Standard Deviation for all repeats: "+str(np.std(stdDev, axis=0)) + "\n")
        for idx, scores in enumerate(crossPrecisionArray):
            logFile.write("%i. repeat precision score: %f\n" %((idx+1), scores))
            print("%i. repeat precision score: %f" %((idx+1), scores))

        for idx, scores in enumerate(precisionArray):
            logFile.write("%i. cross validation precision score: %f\n" %((idx+1), scores))
            print("%i. cross validation precision score: %f" %((idx+1), scores))

        logFile.close()

    def plotResults(self):
        newPlot = plt.figure()
        for value in self.results:
            for key in value:
                values = value[key]
                ax1 = newPlot.add_subplot(111)
                ax1.plot(list(range(len(values))), values, color="black", label=key)
                ax1.legend(key, loc="upper right")
        plt.show()

    def _show_most_informative_features(self, vectorizer, clf, run, n=15):
        feature_names = vectorizer.get_feature_names()
        self.coefficients.append(["Word", "Coefficient", "Target"])
        for idx, targets in enumerate(clf.classes_):
            coefs_with_fns = sorted(zip(clf.coef_[idx], feature_names))
            top = zip(coefs_with_fns[:n], coefs_with_fns[:-(n + 1):-1])
            for (coef_1, fn_1), (coef_2, fn_2) in top:
                self.coefficients.append([fn_1, str(coef_1).replace(".", ","), targets])
                self.coefficients.append([fn_2, str(coef_2).replace(".", ","), targets])

    def generateCsvFileForInformativeFeatures(self):
        results = {}
        for keys in self.coefficients:
            results[keys] = {}

        for keys in self.coefficients:
            innerResults = {}
            for k, v in self.coefficients[keys]:
                innerResults.setdefault(k, []).append(v)
            results[keys] = innerResults

        for elements in self.coefficients:
            #elements = Higher
            formattedDict = {}
            for key, innerElem in self.coefficients[elements]:
                #Key = word
                coef_1 = 0
                odd_1 = 0
                pos_neg_1 = ""
                coef_2 = 0
                odd_2 = 0
                pos_neg_2 = ""
                coef_3 = 0
                odd_3 = 0
                pos_neg_3 = ""
                print(key)
                for idx, data in enumerate(self.coefficients[elements]):
                    print(data)
                    if(idx == 0):
                        coef_1 = data[0]
                        odd_1 = data[1]
                        pos_neg_1 = data[2]

                newDict = {
                    "targer": elements,
                    "name":innerElem,
                    "pos_neg1": pos_neg_1,
                    "pos_neg2": pos_neg_2,
                    "pos_neg3": pos_neg_3,
                    "coeff_1": coef_1,
                    "odd_1": odd_1,
                    "coeff_2": coef_2,
                    "odd_2": odd_2,
                    "coeff_3": coef_3,
                    "odd_3": odd_3
                }

        print(results)