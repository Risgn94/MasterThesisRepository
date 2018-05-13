import sys
sys.path.append("..")
from BagOfWords import MasterClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
import os

masterClassifier = MasterClassifier

#bernoulliClassifier = masterClassifier.Classifier()
#bernoulliClassifier.defineClassifier(BernoulliNB(), "Bernoulli")

logisticRegression = masterClassifier.Classifier()
logisticRegression.defineClassifier(LogisticRegression(multi_class="multinomial", solver="newton-cg",), "Logistic Regression")

#multinominal = masterClassifier.Classifier()
#multinominal.defineClassifier(MultinomialNB(), "Multinominal")

#complement = masterClassifier.Classifier()
#complement.defineClassifier(ComplementNB(), "ComplementNB")

"""
@Content: Set to either column (Title, Content, TitlePrefix, ContentPrefix) or "Both" for combination of Title and Content or "BothPrefix" for combination of TitlePrefix and ContentPrefix
@Target: Target variable. Can be:
    - UpDown
    - Original Bins
    - RealBins
    - PriceBasedBins
    - ZeroBasedRealBins
@File: The Excel file which will be targeted
@Analyzer: "word" or "char"
@Ngram_Range: The range of either words or characters
@Max_Features: Maximum amount of features available
@Min_DF: Minimum document frequency
@Max_DF: Maximum document frequency
@Lowercase=None
@Limit=None



bernoulliClassifier.defineParameters(
    Content="BothPrefix",
    Target="ZeroBasedRealBins",
    File="../Data/DataReadyForClassifier/MasterDataFile.xlsx",
    Analyzer="word",
    Ngram_Range=(2,3),
    Max_Features=12000000,
    Min_DF=0,
    Max_DF=75
)

"""

logisticRegression.defineParameters(
    Content="BothPrefix",
    Target="ZeroBasedRealBins",
    File="../Data/DataReadyForClassifier/MasterDataFile.xlsx",
    Analyzer="word",
    Ngram_Range=(2,4),
    Max_Features=12000000,
    Min_DF=0,
    Max_DF=100
)

"""

multinominal.defineParameters(
    Content="BothPrefix",
    Target="ZeroBasedRealBins",
    File="../Data/DataReadyForClassifier/MasterDataFile.xlsx",
    Analyzer="word",
    Ngram_Range=(2,3),
    Max_Features=12000000,
    Min_DF=0,
    Max_DF=75
)
"""

tries =[
    "BothPrefix",
    "Both",
    "Title",
    "Content"
]

for data in tries:
    logisticRegression.Content = data
    logisticRegression.runClassifierCrossValidate(folds=3, repeats=3)
    logisticRegression.printResults()
    logisticRegression.cleanForNewRun()

from os import system
system('say Finished with classifying')