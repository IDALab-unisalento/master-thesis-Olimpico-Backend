import csv
import time
from threading import Thread

import numpy as np
import pandas as pd
from imblearn.under_sampling import RandomUnderSampler
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import *


class MortalityClassifier (Thread):
    def run(self):
        print("\nMortality Periodic Training: STARTED\n")
        while True:
            dataset = pd.read_csv(r'C:\Users\solimpico\Desktop\health_project\health\AI\datasets\mortality_dataset.csv', delimiter=',', header=0, low_memory=False)
            dataset.dropna()
            X_train = dataset.iloc[:int(dataset.shape[0] * 0.95), :dataset.shape[1] - 1]
            y_train = dataset.iloc[:int(dataset.shape[0] * 0.95), [-1]]

            X_train, y_train = RandomUnderSampler(sampling_strategy='majority').fit_resample(X_train, y_train)

            scaler = MinMaxScaler()
            scaler.fit(X_train.values)

            X_test = dataset.iloc[int(dataset.shape[0] * 0.95):, :dataset.shape[1] - 1]
            y_test = dataset.iloc[int(dataset.shape[0] * 0.95):, [-1]]

            X_test, y_test = RandomUnderSampler(sampling_strategy='auto').fit_resample(X_test, y_test)

            scaler = MinMaxScaler()
            scaler.fit(X_test.values)

            LR_clf = LogisticRegression(random_state=0, fit_intercept=False, max_iter=200000).fit(X_train.values, np.ravel(y_train))
            yhat = LR_clf.predict(X_test.values)

            # creating csv
            with open(r'C:\Users\solimpico\Desktop\health_project\health\AI\parameters\mortality_parameters.csv', 'w',
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                entry = []
                entry.append(precision_score(y_test, yhat))
                for value in LR_clf.coef_[0]:
                    entry.append(value)
                writer.writerow(entry)

            time.sleep(60)  # every week