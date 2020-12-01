from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
# from ttictoc import TicToc
import pandas as pd
import numpy as np
import joblib
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier

try:
    from StringIO import StringIO  ## for Python 2
except ImportError:
    from io import StringIO  ## for Python 3


def PClassification(name, clf, loadFilename=False):
    # Dataset
    c = dt.shape[1] - 1
    check_data = dt.iloc[:,:c]

    # Load model
    if loadFilename: clf = joblib.load(loadFilename)

    # Prediction
    preds = pd.Series(clf.predict(check_data), name='preds')

    # Results
    print(name)
    print()
    print(preds)
    print(check_data)
    print()
    return clf


if __name__ == '__main__':
    printer = True

    filename = "prueba-2"
    df = pd.read_csv(filename, sep='\t', iterator=True, chunksize=100000)
    dt = pd.concat(df, ignore_index=True)
    # dt.loc[dt['Result']==1, 'Result'] = "Legitimate"
    # dt.loc[dt['Result']==0, 'Result'] = "Suspicious"
    # dt.loc[dt['Result']==-1, 'Result'] = "Phishy"
    w = ['tunnel_parents','duration', 'label', 'ts']
    for col in w:
        try:
            del dt[col]
            if printer: print('{} : deleted'.format(col))
        except:
            if printer: print('{} : not found'.format(col))
    NROWS, NCOLS = dt.shape
    print()
    print("- rows  =", NROWS)
    print("- atrs =", NCOLS)
    if printer: dt.head()

    # enc = preprocessing.LabelEncoder()

    for col in dt.columns:
        if col == 'detailed-label':

            dt[col] = dt[col].astype('str')
        else:
            dt[col] = dt[col].astype('float')

    if printer: dt.head()

    clf = PClassification('Decision Tree', DecisionTreeClassifier(), "train_data")
