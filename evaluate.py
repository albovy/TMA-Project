import pandas as pd
import joblib
import sys
import os
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
        #File without extension if user has set it
        destination_file = os.path.splitext(sys.argv[3])[0]
        clf = PClassification('Decision Tree', DecisionTreeClassifier(), "model/"+sys.argv[2])
        print("SAVING PREDICTIONS")
        f = open("predictions/" + destination_file + ".txt", "w")
        f.write(str(dt["preds"].value_counts()))
        f.close()
        print("PREDICTIONS CORRECTLY SAVED")
        print("GENERATING CSV")
        dt.to_csv("predictions/"+ destination_file + ".csv", "\t")
        print("COMPLETED")
    except Exception as excp:
        print(excp)
