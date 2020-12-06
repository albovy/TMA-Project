import pandas as pd
import joblib
import sys
from sklearn.tree import DecisionTreeClassifier

try:
    from StringIO import StringIO  ## for Python 2
except ImportError:
    from io import StringIO  ## for Python 3


def PClassification(name, clf, loadFilename=False):
    # Load model
    if loadFilename: clf = joblib.load(loadFilename)

    # Prediction
    preds = pd.Series(clf.predict(dt), name='preds')
    dt['preds'] = preds

    # Results
    print(name)
    print()
    print(preds)
    print()
    return clf


if __name__ == '__main__':
    printer = True
    try:
        if len(sys.argv) != 3:
            raise Exception("Error in arguments")
        filename = sys.argv[1]
        print("hola")
        df = pd.read_csv(filename, sep='\t', iterator=True, chunksize=100000)
        dt = pd.concat(df, ignore_index=True)
        w = ['tunnel_parents', 'duration', 'label', 'ts', 'detailed-label']
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
        for col in dt.columns:
            if col == 'detailed-label':

                dt[col] = dt[col].astype('str')
            else:
                dt[col] = dt[col].astype('float')

        if printer: dt.head()
        clf = PClassification('Decision Tree', DecisionTreeClassifier(), sys.argv[2])
        dt.to_csv("preds", "\t")
    except Exception as excp:
        print(excp)
