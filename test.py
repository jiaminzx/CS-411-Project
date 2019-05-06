import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split


from sklearn.calibration import CalibratedClassifierCV
sheets_dict = pd.read_excel('data.xlsx')
print("done")#data cleaning and extraction

races={}
races[1]='Black'
races[2]='White'
races[3]='Latino'
races[4]='Asian'
races[5]='Native American'
races[6]='Other'

data = []
ids=[]
count=0
match_count=0

c=0
for index, row in sheets_dict.iterrows():

    inc=row['income']
    age2=row['age_o']
    race2=row['race_o']
    race=row['race']
    job=row['field_cd']
    age=row['age']
    match=row['match']
    
    if inc!=inc:
        inc=-1
    if age2!=age2:
        age2=18
    if race2!=race2:
        race2=6
    if race!=race:
        race=6
    if job!=job:
        job=18
    if age!=age:
        age=18
    if match!=match:
        continue
    data.append([age,race,job,inc,age2,race2,match])


# print(data)
# print(count)
# print(match_count)

train_df = ['age', 'race', 'job', 'income','age2','race2','match']
features=['age', 'race', 'job', 'income','age2','race2']
df = pd.DataFrame(data,columns=train_df)
print(df.loc[[3]])

#perform null check
print(df.isnull().values.any())

x = df.loc[:, features].values
y = df.loc[:,['match']].values

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

logistic =CalibratedClassifierCV(base_estimator=LinearSVC(penalty='l2', dual=False), cv=5)
pca = PCA()
pipe =Pipeline(steps=[('pca', pca), ('logistic', logistic)])
param_grid = {
    'pca__n_components': [1,2,3,4,5],
}
search = GridSearchCV(pipe, param_grid, iid=False, cv=5,return_train_score=False)
search.fit(x_train, y_train.ravel())

joblib.dump(search,'model.sav')
print("Best parameter (CV score=%0.3f):" % search.best_score_)
print(search.best_params_)

test_acc=np.mean(search.predict(x_test)==y_test)
print("testing accuracy"+str(test_acc))


a=np.array([21.0  , 4.0 , 1.0,  -1  ,23.0  , 2.0])
