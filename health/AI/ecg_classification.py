import csv
import sys

import numpy as np
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from imblearn.pipeline import make_pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import *

from threading import Thread
import time


class ECGClassifier(Thread):
    def run(self):
        print("\nECG Periodic Training: STARTED\n")
        while True:
            ecg_data = pd.read_csv(r'C:\Users\solimpico\Desktop\health_project\health\AI\datasets\ecg_dataset.csv',delimiter=',', header=0, low_memory=False)
            ecg_data.dropna()

            df_mask = ecg_data['output'] == 1
            class1 = ecg_data[df_mask]
            df_mask = ecg_data['output'] == 2
            class2 = ecg_data[df_mask]
            df_mask = ecg_data['output'] == 3
            class3 = ecg_data[df_mask]
            df_mask = ecg_data['output'] == 4
            class4 = ecg_data[df_mask]

            cols = []
            for col in ecg_data:
                cols.append(col)
            data = pd.DataFrame(columns=cols)
            count = 1
            c_1 = 0
            c_2 = 0
            c_3 = 0
            c_4 = 0
            for i in range(class1.shape[0] * 4):
                if (count == 1):
                    data.loc[i] = class1.iloc[c_1]
                    c_1 += 1
                    count = 2
                elif (count == 2):
                    data.loc[i] = class2.iloc[c_2]
                    c_2 += 1
                    count = 3
                elif (count == 3):
                    data.loc[i] = class3.iloc[c_3]
                    c_3 += 1
                    count = 4
                elif (count == 4):
                    data.loc[i] = class4.iloc[c_4]
                    c_4 += 1
                    count = 1
            ecg_data = data

            X = ecg_data.iloc[:, :(ecg_data.shape[1]) - 1]
            y = ecg_data.iloc[:, ecg_data.shape[1] - 1]

            cols = []
            for col in X:
                cols.append(col)

            scaler = MinMaxScaler()
            scaler.fit(X)
            X = pd.DataFrame(scaler.transform(X), columns=cols)
            X.insert(0, 'intercept', np.ones((X.shape[0], 1)))

            train_X = X.iloc[:int(X.shape[0] * 0.9), :]
            train_y = y.iloc[:int(y.shape[0] * 0.9)]

            test_X = X.iloc[int(X.shape[0] * 0.9):, :]
            test_y = y.iloc[int(y.shape[0] * 0.9):]

            LR_clf = LogisticRegression(random_state=0, max_iter=100000,fit_intercept=False, C=0.01, multi_class='ovr').fit(train_X, train_y)
            LR_yhat = LR_clf.predict(test_X)
            precision = precision_score(test_y, LR_yhat, average='macro', zero_division=0)

            # creating csv
            with open(r'C:\Users\solimpico\Desktop\health_project\health\AI\parameters\ecg_parameters.csv', 'w',
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                entry = []
                entry.append(precision)
                for value in LR_clf.coef_[0]:
                    entry.append(value)
                writer.writerow(entry)

            time.sleep(60)  # every week
