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
        if len(sys.argv) != 4:
            raise Exception("Error in arguments")
        filename = sys.argv[1]
        df = pd.read_csv(filename, sep='\t', iterator=True, chunksize=100000)
        dt = pd.concat(df, ignore_index=True)
        del df

        filter = ['id.orig_p','id.resp_p', 'missed_bytes', 'orig_pkts', 'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes']
        dt = dt[filter]
        NROWS, NCOLS = dt.shape
        print()
        print("- rows  =", NROWS)
        print("- atrs =", NCOLS)
        clf = PClassification('Decision Tree', DecisionTreeClassifier(), "model/"+sys.argv[2])
        dt.to_csv("predictions/"+sys.argv[3], "\t")
        print("COMPLETED")
    except Exception as excp:
        print(excp)
