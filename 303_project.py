# -*- coding: utf-8 -*-
"""303-project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19tDw1fLEq8wGV-asQstCQVhWmjH8PbSE
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn import metrics
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score
from sklearn.pipeline import make_pipeline
from sklearn import preprocessing

import matplotlib.pyplot as plt
import seaborn as sns

data_copy = pd.read_csv('covid_dataset.csv')
data_copy['Day'] = pd.to_datetime(data_copy['Day'])
data_copy.set_index('Day', inplace=True, drop=True)
 
data_fd = pd.read_csv('covid_first_dose.csv')
data_fd['Day'] = pd.to_datetime(data_fd['Day'])
data_fd.set_index('Day', inplace=True, drop=True)

data_sd = pd.read_csv('covid_second_dose.csv')
data_sd['Day'] = pd.to_datetime(data_sd['Day'])
data_sd.set_index('Day', inplace=True, drop=True)
 
data =  pd.concat([data_copy, data_fd, data_sd], axis=1, ignore_index=True)
data.rename(columns = {0:"Lab_Test",1:"Confirmed_case",2:"Death_Case",3:"First_Dose",4:"Second_Dose",}, inplace = True)

print(data.tail(20))
cnt = 0

data.isnull().sum()

data.fillna(0, inplace=True)

print(data.duplicated().sum())
data.drop_duplicates(inplace=True)
print(data.isnull().sum())

if cnt == 0:
    sum1 = 0
    sum2 = 0
    for i in range(data.shape[0]):
        sum1 += data.iloc[i,3]
        data.iloc[i,3] = sum1
        
        sum2 += data.iloc[i,4]
        data.iloc[i,4] = sum2
    
    cnt += 1

corr = data.corr() 

#corelation analysis
plt.figure(figsize=(10,10))
sns.heatmap(corr,cbar=True,square=True,fmt='.2f',annot=True,annot_kws={'size':8}, cmap='Reds')

df2 =  data.copy()
print(df2.head())
X_Death = df2.drop(columns = ['Death_Case', 'First_Dose', 'Second_Dose'])
Y_Death =  np.array(df2[['Death_Case']])

X_Confirmed = df2.drop(columns = ['Confirmed_case','Death_Case'])
Y_Confirmed =  np.array(df2[['Confirmed_case']])

df2["Lab_Test"] = df2["Lab_Test"].rolling(window=14, min_periods=1).mean()
df2["Lab_Test"] = df2["Lab_Test"].round(decimals = 0)

df2["Confirmed_case"] = df2["Confirmed_case"].rolling(window=14, min_periods=1).mean()
df2["Confirmed_case"] = df2["Confirmed_case"].round(decimals = 0)

df2["Death_Case"] = df2["Death_Case"].rolling(window=14, min_periods=1).mean()
df2["Death_Case"] = df2["Death_Case"].round(decimals = 0)

df2['First_Dose'] = df2['First_Dose'].rolling(window=14, min_periods=1).mean()
df2['First_Dose'] = df2['First_Dose'].round(decimals = 0)
 
df2['Second_Dose'] = df2['Second_Dose'].rolling(window=14, min_periods=1).mean()
df2['Second_Dose'] = df2['Second_Dose'].round(decimals = 0)

X_Death_2 = df2.drop(columns = ['Death_Case', 'First_Dose', 'Second_Dose'])
Y_Death_2 =  np.array(df2[['Death_Case']])

X_Confirmed_2 = df2.drop(columns = ['Confirmed_case','Death_Case'])
Y_Confirmed_2 =  np.array(df2[['Confirmed_case']])

def evaluate_model(y, y_predict, flg):
    if flg == 1:
        print('MAE: ', metrics.mean_absolute_error(y, y_predict))
        print('MSE: ', metrics.mean_squared_error(y, y_predict))
        print('RMSE: ', np.sqrt(metrics.mean_absolute_error(y, y_predict)))
        print('R-squared: ', metrics.r2_score(y, y_predict))
        print()
    elif flg == 2:
        print("Confusion Matrix: ")
        print(confusion_matrix(y, y_predict))
        plt.figure(figsize=(10,7))
        sns.heatmap(confusion_matrix(y, y_predict), annot=True)
        plt.xlabel('Predicted')
        plt.ylabel('Truth')
        
        print("Accuracy Score:  ",accuracy_score(y, y_predict))
        print('Precision Score: ', precision_score(y, y_predict, average=None))
        print('Recall Score:    ', recall_score(y, y_predict, average=None))
        print()
    elif flg == 3:
        RMSE = np.sqrt(metrics.mean_absolute_error(y, y_predict))
        R_squared = metrics.r2_score(y, y_predict)
        return RMSE, R_squared
    else:
        print("Invalid Flg value!")

def plot_model(x, y, x_test, y_test, model_1, model_2 = None, degree=1):
    X_seq = np.linspace(x.min(), x.max(), 100).reshape(-1,1)
    plt.figure()
    plt.scatter(x, y)
    plt.plot(X_seq, model_1.predict(X_seq), color = "black")
    
    RMSE_train, R_squared_train = evaluate_model(y, model_1.predict(x), 3)
    RMSE_test, R_squared_test = evaluate_model(y_test, model_1.predict(x_test), 3)
    
    plt.text(38100, 90, f'Degree = {degree}', fontsize = 8)
    
    plt.text(38100, 65, 'For train data: ', fontsize = 8)
    plt.text(38100, 52, f'RMSE = {round(RMSE_train,2)}', fontsize = 8)
    plt.text(38100, 38, f'R_squared = {round(R_squared_train,2)}', fontsize = 8)
    
    plt.text(38100, 15, 'For test data: ', fontsize = 8)
    plt.text(38100, 2, f'RMSE = {round(RMSE_test,2)}', fontsize = 8)
    plt.text(38100, -10, f'R_squared = {round(R_squared_test,2)}', fontsize = 8)
    
    if model_2 != None:
        plt.plot(X_seq, model_2.predict(X_seq), color = "red")

def plot_model_2(df, x, y, x_test, y_test, model_1, model_2 = None, degree=1):
    x_sec = np.linspace(x.min(), x.max(), 1000)
    
    plt.figure()
    ax1 = df.plot(kind='scatter', x='Lab_Test', y='Confirmed_case', color='r') 
    ax2 = df.plot(kind='scatter', x='First_Dose', y='Confirmed_case', color='g', ax=ax1)
    ax2 = df.plot(kind='scatter', x='Second_Dose', y='Confirmed_case', color='orange', ax=ax1)
    plt.plot(x_sec, model_1.predict(x_sec), color = "black")
    
    RMSE_train, R_squared_train = evaluate_model(y, model_1.predict(x), 3)
    RMSE_test, R_squared_test = evaluate_model(y_test, model_1.predict(x_test), 3)
    
    plt.text(38100, 90, f'Degree = {degree}', fontsize = 8)
    
    plt.text(38100, 65, 'For train data: ', fontsize = 8)
    plt.text(38100, 52, f'RMSE = {round(RMSE_train,2)}', fontsize = 8)
    plt.text(38100, 38, f'R_squared = {round(R_squared_train,2)}', fontsize = 8)
    
    plt.text(38100, 15, 'For test data: ', fontsize = 8)
    plt.text(38100, 2, f'RMSE = {round(RMSE_test,2)}', fontsize = 8)
    plt.text(38100, -10, f'R_squared = {round(R_squared_test,2)}', fontsize = 8)
    
    plt.ylim(0, 15000)
    if model_2 != None:
        plt.plot(x_sec, model_2.predict(x_sec), color = "blue")

def plot_model_3(df, x, y, x_test, y_test, model_1, model_2 = None, degree=1):
    x_sec = np.linspace(x.min(), x.max(), 1000)
    
    plt.figure()
    ax1 = df.plot(kind='scatter', x='Lab_Test', y='Death_Case', color='r') 
    ax2 = df.plot(kind='scatter', x='Confirmed_case', y='Death_Case', color='g', ax=ax1)
    plt.plot(x_sec, model_1.predict(x_sec), color = "black")
    
    RMSE_train, R_squared_train = evaluate_model(y, model_1.predict(x), 3)
    RMSE_test, R_squared_test = evaluate_model(y_test, model_1.predict(x_test), 3)
    
    plt.text(38100, 90, f'Degree = {degree}', fontsize = 8)
    
    plt.text(38100, 65, 'For train data: ', fontsize = 8)
    plt.text(38100, 52, f'RMSE = {round(RMSE_train,2)}', fontsize = 8)
    plt.text(38100, 38, f'R_squared = {round(R_squared_train,2)}', fontsize = 8)
    
    plt.text(38100, 15, 'For test data: ', fontsize = 8)
    plt.text(38100, 2, f'RMSE = {round(RMSE_test,2)}', fontsize = 8)
    plt.text(38100, -10, f'R_squared = {round(R_squared_test,2)}', fontsize = 8)
    
    if model_2 != None:
        plt.plot(x_sec, model_2.predict(x_sec), color = "blue")
        
        
def OLS(X, Y):
    X = sm.add_constant(X)
    ols_model = sm.OLS(Y,X)
    results = ols_model.fit()
    print(results.summary())
    

def Linear_Regression(df, X, Y, ratio = 0.2, flg=0):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = ratio, random_state = 0)
    linear_regression = LinearRegression()
    linear_regression.fit(X_train, Y_train)
    Y_pred_train = linear_regression.predict(X_train)
    Y_pred_test = linear_regression.predict(X_test)
    
    if flg == 0:
        if X.shape[1] == Y.shape[1]:
            plot_model(X_train, Y_train, X_test, Y_test, linear_regression)
        else:
            plot_model_3(df, X_train, Y_train, X_test, Y_test, linear_regression)
    else:
        if X.shape[1] == Y.shape[1]:
            plot_model(X_train, Y_train, X_test, Y_test, linear_regression)
        else:
            plot_model_2(df, X_train, Y_train, X_test, Y_test, linear_regression)
    
    print("For Train Dataset: ")
    evaluate_model(Y_train, Y_pred_train, 1)
    
    print("For Test Dataset: ")
    evaluate_model(Y_test, Y_pred_test, 1)
    return linear_regression
    
def Polynomial_Regression(df, X, Y, degree=2, ratio = 0.2, flg=0):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = ratio, random_state = 0)
    polynomial_regression = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    polynomial_regression.fit(X_train, Y_train)
    Y_pred_train = polynomial_regression.predict(X_train)
    Y_pred_test = polynomial_regression.predict(X_test)
    
    if flg == 0:
        if X.shape[1] == Y.shape[1]:
            plot_model(X_train, Y_train, X_test, Y_test, polynomial_regression, degree=degree)
        else:
            plot_model_3(df, X_train, Y_train, X_test, Y_test, polynomial_regression, degree=degree)
    else:
        if X.shape[1] == Y.shape[1]:
            plot_model(X_train, Y_train, X_test, Y_test, polynomial_regression, degree=degree)
        else:
            plot_model_2(df, X_train, Y_train, X_test, Y_test, polynomial_regression, degree=degree)
    
    print("For Train Dataset: ")
    evaluate_model(Y_train, Y_pred_train, 1)
    
    print("For Test Dataset: ")
    evaluate_model(Y_test, Y_pred_test, 1)
    return polynomial_regression

def Polynomial_Regression_L1(df, X, Y, degree=2, alpha = 0.5, ratio = 0.2, flg=0):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = ratio, random_state = 0)
    polynomial_regression_L1 = make_pipeline(PolynomialFeatures(degree), Lasso(alpha=alpha))
    polynomial_regression_L1.fit(X_train, Y_train)
    Y_pred_train = polynomial_regression_L1.predict(X_train)
    Y_pred_test = polynomial_regression_L1.predict(X_test)
    
    if flg == 0:
        if X.shape[1] == Y.shape[1]:
            plot_model(X_train, Y_train, X_test, Y_test, polynomial_regression_L1, degree=degree)
        else:
            plot_model_3(df, X_train, Y_train, X_test, Y_test, polynomial_regression_L1, degree=degree)
    else:
        if X.shape[1] == Y.shape[1]:
            plot_model(X_train, Y_train, X_test, Y_test, polynomial_regression_L1, degree=degree)
        else:
            plot_model_2(df, X_train, Y_train, X_test, Y_test, polynomial_regression_L1, degree=degree)
    
    
    print("For Train Dataset: ")
    evaluate_model(Y_train, Y_pred_train, 1)
    
    print("For Test Dataset: ")
    evaluate_model(Y_test, Y_pred_test, 1)
    return polynomial_regression_L1
    
def Polynomial_Regression_L2(df, X, Y, degree=2, alpha = 0.5, ratio = 0.2, flg=0):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = ratio, random_state = 0)
    polynomial_regression_L2 = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=alpha))
    polynomial_regression_L2.fit(X_train, Y_train)
    Y_pred_train = polynomial_regression_L2.predict(X_train)
    Y_pred_test = polynomial_regression_L2.predict(X_test)
    

    if flg == 0:
        if X.shape[1] == Y.shape[1]:
            plot_model(X_train, Y_train, X_test, Y_test, polynomial_regression_L2, degree=degree)
        else:
            plot_model_3(df, X_train, Y_train, X_test, Y_test, polynomial_regression_L2, degree=degree)
    else:
        if X.shape[1] == Y.shape[1]:
            plot_model(X_train, Y_train, X_test, Y_test, polynomial_regression_L2, degree=degree)
        else:
            plot_model_2(df, X_train, Y_train, X_test, Y_test, polynomial_regression_L2, degree=degree)
        
    print("For Train Dataset: ")
    evaluate_model(Y_train, Y_pred_train, 1)
    
    print("For Test Dataset: ")
    evaluate_model(Y_test, Y_pred_test, 1)
    return polynomial_regression_L2

def Lasso_Regression(df, X, Y, alpha = 0.5, ratio = 0.2, flg=0):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = ratio, random_state = 0)
    lasso = Lasso(alpha = alpha)
    lasso.fit(X_train, Y_train)
    Y_pred_train = lasso.predict(X_train)
    Y_pred_test = lasso.predict(X_test)
    
    
    if flg == 0:
        if X.shape[1] == Y.shape[1]:
            plot_model(X_train, Y_train, X_test, Y_test, lasso)
        else:
            plot_model_3(df, X_train, Y_train, X_test, Y_test, lasso)
    else:
        if X.shape[1] == Y.shape[1]:
            plot_model(X_train, Y_train, X_test, Y_test, lasso)
        else:
            plot_model_2(df, X_train, Y_train, X_test, Y_test, lasso)
    
    print("For Train Dataset: ")
    evaluate_model(Y_train, Y_pred_train, 1)
    
    print("For Test Dataset: ")
    evaluate_model(Y_test, Y_pred_test, 1)
    return lasso

def Ridge_Regression(df, X, Y, alpha = 0.5, ratio = 0.2, flg=0):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = ratio, random_state = 0)
    ridge = Ridge(alpha = alpha)
    ridge.fit(X_train, Y_train)
    Y_pred_train = ridge.predict(X_train)
    Y_pred_test = ridge.predict(X_test)
    

    if flg == 0:
        if X.shape[1] == Y.shape[1]:
            plot_model(X_train, Y_train, X_test, Y_test, ridge)
        else:
            plot_model_3(df, X_train, Y_train, X_test, Y_test, ridge)
    else:
        if X.shape[1] == Y.shape[1]:
            plot_model(X_train, Y_train, X_test, Y_test, ridge)
        else:
            plot_model_2(df, X_train, Y_train, X_test, Y_test, ridge)
    
    print("For Train Dataset: ")
    evaluate_model(Y_train, Y_pred_train, 1)
    
    print("For Test Dataset: ")
    evaluate_model(Y_test, Y_pred_test, 1)
    return ridge

def ElasticNet_Regression(df, X, Y, alpha = 0.5, l1_ratio = 0.5, ratio = 0.2, flg=0):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = ratio, random_state = 0)
    elasticNet = ElasticNet(alpha = alpha, l1_ratio=l1_ratio)
    elasticNet.fit(X_train, Y_train)
    Y_pred_train = elasticNet.predict(X_train)
    Y_pred_test = elasticNet.predict(X_test)
    
    
    if flg == 0:
        if X.shape[1] == Y.shape[1]:
            plot_model(X_train, Y_train, X_test, Y_test, elasticNet)
        else:
            plot_model_3(df, X_train, Y_train, X_test, Y_test, elasticNet)
    else:
        if X.shape[1] == Y.shape[1]:
            plot_model(X_train, Y_train, X_test, Y_test, elasticNet)
        else:
            plot_model_2(df, X_train, Y_train, X_test, Y_test, elasticNet)
    
    print("For Train Dataset: ")
    evaluate_model(Y_train, Y_pred_train, 1)
    
    print("For Test Dataset: ")
    evaluate_model(Y_test, Y_pred_test, 1)
    return elasticNet

def Linear_VS_Polynomial_Regression(df, X, Y, degree=2, ratio = 0.2, flg=0):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = ratio, random_state = 0)
    
    linear_regression = Linear_Regression(df, X,Y)
    polynomial_regression = Polynomial_Regression(df, X,Y, degree=degree)
    
    if flg == 0:
        if X.shape[1] == Y.shape[1]:
            plot_model(X_train, Y_train, linear_regression, polynomial_regression)
        else:
            plot_model_3(df, X_train, Y_train, linear_regression, polynomial_regression)
    else:
        if X.shape[1] == Y.shape[1]:
            plot_model(X_train, Y_train, linear_regression, polynomial_regression)
        else:
            plot_model_2(df, X_train, Y_train, linear_regression, polynomial_regression)
    

def Logistic_Regression(X, Y, c=10, ratio = 0.2):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = ratio, random_state = 0)
    logistic_regression = LogisticRegression(C = c)
    logistic_regression.fit(X_train, Y_train)
    Y_pred_train = logistic_regression.predict(X_train)
    Y_pred_test = logistic_regression.predict(X_test)
    
    print("------------------------Logistic_Regression------------------------------------------------")

    
    prediction_train = list(map(round,Y_pred_train))
    prediction_test = list(map(round,Y_pred_test))
    
    print("For Train Dataset: ")
    evaluate_model(Y_train, prediction_train, 2)
    
    print("For Test Dataset: ")
    evaluate_model(Y_test, prediction_test, 2)
    
    return logistic_regression


def SVM(X, Y, gamma='auto', ratio = 0.2, c=10):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = ratio, random_state = 0)
    svm_model = make_pipeline(preprocessing.StandardScaler(), SVC(kernel='linear',C=c, gamma=gamma))
    svm_model.fit(X_train, Y_train)
    
    Y_pred_train = svm_model.predict(X_train)
    Y_pred_test = svm_model.predict(X_test)
    
    
    print("------------------------SVM------------------------------------------------")

    
    prediction_train = list(map(round,Y_pred_train))
    prediction_test = list(map(round,Y_pred_test))
    
    print("For Train Dataset: ")
    evaluate_model(Y_train, prediction_train, 2)
    
    print("For Test Dataset: ")
    evaluate_model(Y_test, prediction_test, 2)
    return svm_model

"""# Classification"""

df3 = data.copy()
df3['Percentage'] = (df3['Confirmed_case'] / df3['Lab_Test'])*100
condlist = [df3['Percentage']<5, df3['Percentage']>20]
choicelist = ['Low', 'High']
df3['Risk'] = np.select(condlist, choicelist, default='Medium')

df3['Risk'].value_counts()

le = preprocessing.LabelEncoder()
for feature in df3.columns:
    unique_values = df3[feature].unique()
    example_value = unique_values[0]
    if isinstance(example_value, str):
        df3[feature] = le.fit_transform(df3[feature])

X2 = df3[['Lab_Test','Confirmed_case']]
Y2 =  np.array(df3['Risk'])

X_train, X_test, Y_train, Y_test = train_test_split(X2, Y2, test_size = 0.2, random_state = 0)

print(X2.shape, X_train.shape, X_test.shape)

pd.DataFrame(Y_test).value_counts()

Logistic_Regression(X2,Y2, c=1)

low = df3[df3.Risk == 1]
Medium = df3[df3.Risk == 2]
High = df3[df3.Risk == 0]


plt.xlabel('Lab_Test')
plt.ylabel('Confirmed_case')
plt.scatter(low['Lab_Test'], low['Confirmed_case'], color='green', marker='+')
plt.scatter(Medium['Lab_Test'], Medium['Confirmed_case'], color='blue', marker='.')
plt.scatter(High['Lab_Test'], High['Confirmed_case'], color='red', marker='d')

SVM(X2,Y2)

"""# Regression

# Predict the Death Case
"""

OLS(X_Death_2,Y_Death_2)

"""Death Case = -12.4858 + 0.0010 * Lab Test + 0.0158 * Confirmed Case"""

print("--------------------Linear_Regression--------------------")
print()

print("The original dataset: ")
print()
Linear_Regression(data,X_Death,Y_Death)

print("------------------------------")

print("The Clean dataset: ")
print()
Linear_Regression(df2,X_Death_2,Y_Death_2)

print("--------------------Polynomial_Regression--------------------")
print()

print("The original dataset: ")
print()
Polynomial_Regression(data,X_Death,Y_Death, degree=4)

print("------------------------------")

print("The Clean dataset: ")
print()
Polynomial_Regression(data,X_Death_2,Y_Death_2, degree=4)

print("------------------------------")

print("The Clean dataset: ")
print()
Polynomial_Regression(data,X_Death_2,Y_Death_2, degree=7)

print("------------------------------")

print("The Clean dataset: ")
print()
Polynomial_Regression(data,X_Death_2,Y_Death_2, degree=14)

print("--------------------Polynomial_Regression_L1--------------------")
print()

print("The original dataset: ")
print()
Polynomial_Regression_L1(data,X_Death,Y_Death, degree=7, alpha=0.7)

print("------------------------------")

print("The Clean dataset: ")
print()
Polynomial_Regression_L1(df2,X_Death_2,Y_Death_2, degree=4, alpha=0.7)

print("------------------------------")

print("The Clean dataset: ")
print()
Polynomial_Regression_L1(df2,X_Death_2,Y_Death_2, degree=7, alpha=0.7)

print("------------------------------")

print("The Clean dataset: ")
print()
Polynomial_Regression_L1(df2,X_Death_2,Y_Death_2, degree=14, alpha=0.7)

print("--------------------Polynomial_Regression_L2--------------------")
print()

print("The original dataset: ")
print()
Polynomial_Regression_L2(data,X_Death,Y_Death, degree=7)

print("------------------------------")

print("The Clean dataset: ")
print()
Polynomial_Regression_L2(df2,X_Death_2,Y_Death_2, degree=4)

print("------------------------------")

print("The Clean dataset: ")
print()
Polynomial_Regression_L2(df2,X_Death_2,Y_Death_2, degree=7)

print("------------------------------")

print("The Clean dataset: ")
print()
Polynomial_Regression_L2(df2,X_Death_2,Y_Death_2, degree=14)

print("--------------------Lasso_Regression--------------------")
print()

print("The original dataset: ")
print()
Lasso_Regression(data,X_Death,Y_Death, alpha=0.1)

print("------------------------------")

print("The Clean dataset alpha=0.1: ")
print()
Lasso_Regression(df2,X_Death_2,Y_Death_2, alpha=0.1)

print("------------------------------")

print("The Clean dataset alpha=1: ")
print()
Lasso_Regression(df2,X_Death_2,Y_Death_2, alpha=1)

print("------------------------------")

print("The Clean dataset alpha=10: ")
print()
Lasso_Regression(df2,X_Death_2,Y_Death_2, alpha=10)

print("--------------------Ridge_Regression--------------------")
print()

print("The original dataset: ")
print()
Ridge_Regression(data,X_Death,Y_Death)

print("------------------------------")

print("The Clean dataset: ")
print()
Ridge_Regression(df2,X_Death_2,Y_Death_2)

corr = data.corr() 
print(corr)
print()

#corelation analysis
plt.figure(figsize=(10,10))
sns.heatmap(corr,cbar=True,square=True,fmt='.2f',annot=True,annot_kws={'size':8}, cmap='Reds')

print("--------------------ElasticNet_Regression--------------------")
print()

print("The original dataset: ")
print()
ElasticNet_Regression(data,X_Death,Y_Death, l1_ratio=0.5)

print("------------------------------")

print("The Clean dataset l1_ratio=0.3: ")
print()
ElasticNet_Regression(df2,X_Death_2,Y_Death_2, l1_ratio=0.3)

print("------------------------------")

print("The Clean dataset l1_ratio=0.5: ")
print()
ElasticNet_Regression(df2,X_Death_2,Y_Death_2, l1_ratio=0.5)

print("------------------------------")

print("The Clean dataset l1_ratio=0.7: ")
print()
ElasticNet_Regression(df2,X_Death_2,Y_Death_2, l1_ratio=0.7)

"""# Predict the Confirme Case"""

OLS(X_Confirmed_2,Y_Confirmed_2)

"""Confirme Case = -2217.2933 + 0.3118 * Lab Test - 0.0003 * First Dose + 0.0003 * Second Dose"""

print("--------------------Linear_Regression--------------------")
print()

print("The original dataset: ")
print()
Linear_Regression(data,X_Confirmed,Y_Confirmed, flg=1)

print("------------------------------")

print("The Clean dataset: ")
print()
Linear_Regression(df2,X_Confirmed_2,Y_Confirmed_2, flg=1)

print("--------------------Polynomial_Regression--------------------")
print()

print("The original dataset: ")
print()
Polynomial_Regression(data,X_Confirmed,Y_Confirmed, degree=7,flg=1)

print("------------------------------")

print("The Clean dataset: ")
print()
Polynomial_Regression(df2,X_Confirmed_2,Y_Confirmed_2, degree=7,flg=1)

print("--------------------Polynomial_Regression_L1--------------------")
print()

print("The original dataset: ")
print()
Polynomial_Regression_L1(data,X_Confirmed,Y_Confirmed, degree=7,flg=1)

print("------------------------------")

print("The Clean dataset: ")
print()
Polynomial_Regression_L1(df2,X_Confirmed_2,Y_Confirmed_2, degree=7,flg=1)

print("--------------------Polynomial_Regression_L2--------------------")
print()

print("The original dataset: ")
print()
Polynomial_Regression_L2(data,X_Confirmed,Y_Confirmed, degree=7,flg=1)

print("------------------------------")

print("The Clean dataset: ")
print()
Polynomial_Regression_L2(df2,X_Confirmed_2,Y_Confirmed_2, degree=7,flg=1)

print("--------------------Lasso_Regression--------------------")
print()

print("The original dataset: ")
print()
Lasso_Regression(data,X_Confirmed,Y_Confirmed,flg=1)

print("------------------------------")

print("The Clean dataset: ")
print()
Lasso_Regression(df2,X_Confirmed_2,Y_Confirmed_2,flg=1)

print("--------------------Ridge_Regression--------------------")
print()

print("The original dataset: ")
print()
Ridge_Regression(data,X_Confirmed,Y_Confirmed,flg=1)

print("------------------------------")

print("The Clean dataset: ")
print()
Ridge_Regression(df2,X_Confirmed_2,Y_Confirmed_2,flg=1)

corr = data.corr() 
print(corr)
print()

#corelation analysis
plt.figure(figsize=(10,10))
sns.heatmap(corr,cbar=True,square=True,fmt='.2f',annot=True,annot_kws={'size':8}, cmap='Reds')

"""# Time Series Analysis"""

import statsmodels.graphics.tsaplots as sgt
import statsmodels.tsa.stattools as sts
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.arima_model import ARIMA
from scipy.stats.distributions import chi2

df = data.copy()
print(df.isna().sum())

df.Confirmed_case.plot(figsize=(20,5), title='Death_Case', color = "red")

df_freq = df.asfreq('d')
df_freq_2 = df_freq.drop(columns = ['Lab_Test','Death_Case', 'First_Dose', 'Second_Dose'])
df_freq_2.head(10)

def test_stationarity(timeseries):
    
    # Determing rolling statistics
    rolmean = timeseries.rolling(window=14, min_periods=1).mean()
    rolstd = timeseries.rolling(window=14, min_periods=1).std()

    # Plot rolling statistics
    orig = plt.plot(timeseries, color='blue', label = 'Original')
    mean = plt.plot(rolmean, color='red', label = 'Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Rolling Std')
    plt.show()
    
    # perform Dickey-fuller test
    print("Results of Dickey-fuller test: ")

    dftest = adfuller(timeseries, autolag='AIC')
    
    dfoutput = pd.Series(dftest[0:4], index=['Test_statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    
    print(dfoutput)

print(df_freq_2.iloc[:,0])

test_stationarity(df_freq_2.iloc[:,0])

# Seasonality

s_dec_additive = seasonal_decompose(df_freq_2, model = 'additive')
s_dec_additive.plot()

# there is no seasonality

# ACF (Direct + Indirect)

sgt.plot_acf(df_freq_2, lags=40, zero = False)
plt.title('ACF Plot', size= 24)

# PACF (Direct)

sgt.plot_pacf(df_freq_2, lags=40, zero = False, method=('ols'))
plt.title('PACF Plot', size= 24)

# ARIMA model
model = ARIMA(df_freq_2, order=(5,0,5))
result_ARIMA = model.fit(disp=-1)
plt.plot(df_freq_2)
plt.plot(result_ARIMA.fittedvalues, color='red')
plt.title('R-squared: %.4f'% metrics.r2_score(df_freq_2.Confirmed_case, result_ARIMA.fittedvalues))
print('Plotting ARIMA Model')

predict_ARIMA = pd.Series(result_ARIMA.fittedvalues, copy = True)
print(predict_ARIMA.tail())

df_freq_2.tail()

plt.plot(df_freq_2.Confirmed_case)

plt.plot(predict_ARIMA,color='red')

df_freq_2.shape

result_ARIMA.plot_predict(1,626+120)
# result_ARIMA.forecast(steps=120)

