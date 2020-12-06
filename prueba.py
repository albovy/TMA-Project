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
        del df
        filter = ['id.orig_p','id.resp_p', 'missed_bytes', 'orig_pkts', 'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes', 'detailed-label']
        dt = dt[filter]
        NROWS, NCOLS = dt.shape
        print()
        print("- rows  =", NROWS)
        print("- atrs =", NCOLS)
        print(dt.head())
        clf = PClassification('Decision Tree', DecisionTreeClassifier(), "model/"+sys.argv[2])
    except Exception as excp:
        print(excp)
