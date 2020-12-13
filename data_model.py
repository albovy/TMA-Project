import joblib
import pandas as pd
import os
from sklearn.tree import DecisionTreeClassifier


class DataModel:
    destination_path = "files/"

    def __pclassification(self, name, clf, loadFilename=False):
        # Load model
        if loadFilename: clf = joblib.load(loadFilename)
        # Prediction
        preds = pd.Series(clf.predict(dt), name='preds')
        dt['preds'] = preds
        return clf


    def classify(self, filename):
        try:
            df = pd.read_csv(filename, sep='\t', iterator=True, chunksize=100000)
            dt = pd.concat(df, ignore_index=True)
            del df

            filter = ['id.orig_p', 'id.resp_p', 'missed_bytes', 'orig_pkts', 'orig_ip_bytes', 'resp_pkts',
                      'resp_ip_bytes']
            dt = dt[filter]
            NROWS, NCOLS = dt.shape

            # File without extension if user has set it
            destination_file = destination_path +  os.path.splitext(filename)[0] + "response"
            clf = self.__pclassification('Decision Tree', DecisionTreeClassifier(), "model/train_data")

            f = open("predictions/" + destination_file + ".txt", "w")
            f.write(str(dt["preds"].value_counts()))
            f.close()
            dt.to_csv("predictions/" + destination_file + ".csv", "\t")
            return "predictions/" + destination_file

        except Exception as e:
            print(e)
