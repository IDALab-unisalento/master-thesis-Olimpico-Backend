import csv
import sys

import numpy as np
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import *


from threading import Thread
import time

class HealthClassifier (Thread):
    def run(self):
        print("\nHealth Periodic Training: STARTED\n")
        while True:
            dataset = pd.read_csv(r'C:\Users\solimpico\Desktop\health_project\health\AI\datasets\health_dataset.csv', delimiter=',', header=0, low_memory=False)
            dataset.dropna()
            shuffeled_df = dataset.sample(frac=1)

            X_train = shuffeled_df.iloc[:int(shuffeled_df.shape[0] * 0.8), :shuffeled_df.shape[1] - 1]
            scaler = MinMaxScaler()
            scaler.fit(X_train.values)

            y_train = shuffeled_df.iloc[:int(shuffeled_df.shape[0] * 0.8), [-1]]

            X_test = shuffeled_df.iloc[int(shuffeled_df.shape[0] * 0.8):, :shuffeled_df.shape[1] - 1]
            scaler = MinMaxScaler()
            scaler.fit(X_test.values)

            y_test = shuffeled_df.iloc[int(shuffeled_df.shape[0] * 0.8):, [-1]]

            LR_clf = LogisticRegression(random_state=0, fit_intercept=False, max_iter=200000).fit(X_train.values, np.ravel(y_train))
            yhat = LR_clf.predict(X_test.values)

            # creating csv
            with open(r'C:\Users\solimpico\Desktop\health_project\health\AI\parameters\health_parameters.csv', 'w',
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                entry = []
                entry.append(precision_score(y_test, yhat))
                for value in LR_clf.coef_[0]:
                    entry.append(value)
                writer.writerow(entry)

            time.sleep(60) #every week