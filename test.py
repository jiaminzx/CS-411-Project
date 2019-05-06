import joblib
import pickle

with open("model.sav", "rb") as f:
    model = pickle.load(f,protocol=2)

# model=joblib.load('model.sav',protocol=2)
array=[1,0,0,0,1,10]
proba=model.predict_proba([array])
print(proba[0][0])