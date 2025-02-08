#TODO clean unneeded imports
import pandas as pd
import numpy as np
#from nltk import word_tokenize
#import re

from sklearn.feature_extraction.text import TfidfVectorizer#, CountVectorizer
#from sklearn.linear_model import LogisticRegression, LinearRegression, Lars, RidgeCV
#from sklearn.svm import SVC, SVR
#from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier #, GradientBoostingClassifier, ExtraTreesClassifier
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.tree import DecisionTreeClassifier
#from sklearn.multioutput import MultiOutputClassifier

from sklearn.model_selection import RandomizedSearchCV, GridSearchCV, train_test_split, cross_val_score

#from tqdm import tnrange, tqdm_notebook
#from time import sleep
#import gc

#from matplotlib import pyplot as plt
#import os

from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os
import gdown

def save_obj(obj, name):
    pickle.dump(obj,open(name + '.pkl', 'wb'), protocol=4)
    
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

#vec encoding of words
def alpha_vec2(w, mx, max_word_len, dic):
    vec=np.zeros((max_word_len,len(dic)))    
    for i in range(0, len(w)):
        #print(i,w[i])
        vec[i]=mx[dic.index(w[i])]
        
    vec=vec.astype('float16').flatten()
    vec[vec==np.inf]=0 
    vec[vec==-np.inf]=0        
    return vec



#ordinal encoding of words
def alpha_vec2ord(w, max_word_len):
    vec=np.zeros(max_word_len)    
    for i in range(0, len(w)):        
        vec[i]=ord(w[i])    
    return vec.astype('int')

#ordinal decoding of words
def decode_vec(vec):
    w=''.join([chr(int(v)) for v in vec if v!=0])    
    return w.strip()
    
# Get the absolute path of the current file (ar_stem.py)
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
    

max_word_len = 12
mx = load_obj(os.path.join(PACKAGE_DIR,'mx'))
dic = load_obj(os.path.join(PACKAGE_DIR,'dic'))

#model = load_obj(os.path.join(PACKAGE_DIR,'best_model'))
import os
import requests

#MODEL_URL = "https://drive.google.com/file/d/1s_OgF-hLtIcV5_2WL7_IYLV3RZWmNnY2/view?usp=sharing"
# Google Drive file ID of the model
FILE_ID = "1s_OgF-hLtIcV5_2WL7_IYLV3RZWmNnY2"
DESTINATION = os.path.join(os.path.dirname(__file__), "best_model.pkl")

def download_model():
    """Download the model from Google Drive using gdown."""
    if not os.path.exists(DESTINATION):
        print("Downloading model from Google Drive...")
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, DESTINATION, quiet=False)
        print(f"Model downloaded successfully: {DESTINATION}")
    else:
        print("Model already exists.")

# Ensure the model is available
download_model()

model = load_obj(os.path.join(PACKAGE_DIR,'best_model'))

def stem_it(word):
    if type(word) != list:
        vec_input = alpha_vec2(word, mx, max_word_len, dic)
        vec_pred = model.predict(vec_input.reshape(1, -1))[0]
        return decode_vec(vec_pred)
    else:
        vec_inputs = [alpha_vec2(w, mx, max_word_len, dic) for w in word]
        vec_preds = [model.predict(v.reshape(1, -1))[0] for v in vec_inputs]
        return [decode_vec(v) for v in vec_preds]