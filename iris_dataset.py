# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

"""
1，数据来源为iris数据集，共150例，分为三类：iris-setosa, iris-versicolor, iris-virginica
2，在监督学习中使用标记。-1 ---> iris-setosa 0 --->iris-versicolor  1 ---> iris-virginica
3，训练集共选取120例，均匀分布三类标签。
4，测试集选择30例。
"""


def read_data():
    IRIS_TRAIN_URL = 'iris_training.csv'
    IRIS_TEST_URL = 'iris_test.csv'

    names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'species']
    train = pd.read_csv(IRIS_TRAIN_URL, names=names, skiprows=1)
    test = pd.read_csv(IRIS_TEST_URL, names=names, skiprows=1)

    x_train = train.drop('species', axis=1)
    x_test = test.drop('species', axis=1)

    y_train = train.species
    y_test = test.species

    for i in range(0, 3):
        y_train = y_train.replace(i, i - 1)
        y_test = y_test.replace(i, i - 1)

    return x_train, x_test, y_train, y_test


def pre_processing(x_train, x_test, y_train, y_test):
    x_train_list = np.array(x_train).tolist()
    x_test_list = np.array(x_test).tolist()

    y_train_one_list = np.array(y_train).tolist()
    y_train_list = []
    for i in y_train_one_list:
        y_train_list.append([i])

    y_test_one_list = np.array(y_test).tolist()
    y_test_list = []
    for i in y_test_one_list:
        y_test_list.append([i])

    iris_train_data = []
    for item in list(zip(x_train_list, y_train_list)):
        iris_train_data.append(list(item))

    iris_test_data = []
    for item in list(zip(x_test_list, y_test_list)):
        iris_test_data.append(list(item))

    return iris_train_data, iris_test_data
