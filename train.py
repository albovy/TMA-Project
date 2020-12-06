from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle
import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier
import sys

try:
    from StringIO import StringIO  ## for Python 2
except ImportError:
    from io import StringIO  ## for Python 3


def PClassification(name, clf, THRESHOLD, saveFilename=False, ejTrain=True):
    # Dataset
    r = THRESHOLD
    c = dt.shape[1] - 1
    train_data = dt.iloc[:r, :c]
    train_answ = dt.iloc[:r, c]
    check_data = dt.iloc[r:, :c]
    check_answ = dt.iloc[r:, c]

    # Train model
    if ejTrain: clf.fit(train_data, train_answ)

    # Save model
    if saveFilename: joblib.dump(clf, saveFilename)

    # Prediction
    preds = pd.Series(clf.predict(check_data), name='preds')
    reals = pd.Series(check_answ, name='reales')
    reals.index = range(reals.shape[0])

    # Results
    print(name)
    print('acc: {:.2f}%'.format(100 * accuracy_score(reals, preds)))
    print()
    print(pd.crosstab(reals, preds))
    print()
    return clf


if __name__ == '__main__':
    try:
        print(len(sys.argv))
        if len(sys.argv) != 3:
            raise Exception("No necessary arguments given")
        printer = True
        filename = sys.argv[1]
        df = pd.read_csv(filename, sep='\t', iterator=True, chunksize=100000)
        dt = pd.concat(df, ignore_index=True)
        w = ['tunnel_parents', 'duration', 'label', 'ts']
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
        dt.head()
        dt = pd.DataFrame(shuffle(dt))
        if printer: dt.head()
        THRESHOLD = NROWS * 2 // 3
        print('67% + 33%')
        print(THRESHOLD, '+', NROWS - THRESHOLD)
        for col in dt.columns:
            if col == 'detailed-label':

                dt[col] = dt[col].astype('str')
            else:
                dt[col] = dt[col].astype('float')

        if printer: dt.head()

        clf = PClassification('Decision Tree', DecisionTreeClassifier(), THRESHOLD, sys.argv[2])
    except Exception as excp:
        print(excp)
