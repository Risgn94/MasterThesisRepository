import sys
sys.path.append("..")
from Cleaning import Clean
import datetime

cleaner = Clean.Cleaner("../Data/DataWithNominalPrice/RawContentDataWithDAYPLUSMINUS2016-2018.xlsx")
#dfMinus = cleaner.GetCleanedDataframe(["Title", "Content"], "PriceChangeDayBefore")
dfPlus = cleaner.GetCleanedDataframe(["Title", "Content"], "PriceChangeDayAfter")
#df = cleaner.GetCleanedDataNoStem(["Title", "Content"])

#cleaner.saveNew(dfMinus, "../Data/DataReadyForClassifier/FinalCleanDatawithDayMinus-2018.xlsx")
cleaner.saveNew(dfPlus, "../Data/DataReadyForClassifier/FinalCleanDataWithDayPlus-2018.xlsx")

