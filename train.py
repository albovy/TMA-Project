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
    if saveFilename: joblib.dump(clf, "model/"+saveFilename)

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
        del df
        filter = ['id.orig_p','id.resp_p', 'missed_bytes', 'orig_pkts', 'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes', 'detailed-label']
        dt = dt[filter]
        NROWS, NCOLS = dt.shape
        print()
        print("- rows  =", NROWS)
        print("- atrs =", NCOLS)
        print(dt.head())
        dt = pd.DataFrame(shuffle(dt))
        THRESHOLD = NROWS * 2 // 3
        clf = PClassification('Decision Tree', DecisionTreeClassifier(), THRESHOLD, sys.argv[2])
    except Exception as excp:
        print(excp)
