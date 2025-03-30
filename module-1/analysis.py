# Author: Justin Xu
# INST 414- Module 1 Assignment 
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols 

DATA = pd.read_csv("tips.csv")
DATA["tip_percentage"] = DATA["tip"] / DATA["total_bill"]

model = ols('tip_percentage ~ C(day) * C(size) * C(time)', data=DATA).fit()
result = sm.stats.anova_lm(model, type=2)
print(result)