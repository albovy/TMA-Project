from sklearn.metrics import accuracy_score

import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier
import sys
try:
    from StringIO import StringIO  ## for Python 2
except ImportError:
    from io import StringIO  ## for Python 3


def PClassification(name, clf, loadFilename=False):
    # Dataset
    c = dt.shape[1] - 1
    check_data = dt.iloc[:,:c]
    check_answ = dt.iloc[:,c]

    # Load model
    if loadFilename: clf = joblib.load(loadFilename)

    # Prediction
    preds = pd.Series(clf.predict(check_data), name='preds')
    reals = pd.Series(check_answ, name='reales')
    reals.index = range(reals.shape[0])

    # Results
    print(name)
    print('acc: {:.4f}%'.format(100*accuracy_score(reals, preds)))
    print()
    a = pd.crosstab(reals,preds)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(a)
    print()
    return clf


if __name__ == '__main__':
    printer = True
    try:
        if len(sys.argv) != 3:
            raise Exception("Error in arguments")
        filename = sys.argv[1]
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

        clf = PClassification('Decision Tree', DecisionTreeClassifier(), sys.argv[2])
    except Exception as excp:
        print(excp)
