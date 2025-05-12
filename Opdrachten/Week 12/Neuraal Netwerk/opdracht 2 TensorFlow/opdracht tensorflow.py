
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
tf.random.set_seed(100)

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

df = sns.load_dataset('mpg')
print(df.shape)
df.describe(include='all')

df['horsepower'].fillna(df['horsepower'].median(), inplace=True)
df = df.drop(['name'], axis=1)
df = pd.get_dummies(df, columns=['cylinders'], drop_first=True, prefix='Cylinder')
df = pd.get_dummies(df, columns=['model_year'], drop_first=True, prefix='Year')
df = pd.get_dummies(df, columns=['origin'], drop_first=True, prefix='Origin')
df.head()


target_variable = ['mpg']
predictors = list(set(list(df.columns))-set(target_variable))
df[predictors] = df[predictors]/df[predictors].max()
df.describe()

X = df[predictors].values
y = df[target_variable].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=100)


print(X_train.shape); print(X_test.shape)


# define model
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(32, input_shape = (X_train.shape[1],), activation = 'relu'))
model.add(tf.keras.layers.Dense(16, activation= "relu"))
model.add(tf.keras.layers.Dense(8, activation= "relu"))
model.add(tf.keras.layers.Dense(4, activation= "relu"))
model.add(tf.keras.layers.Dense(1))


optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)
model.compile(loss = 'mae', metrics = ['mae'], optimizer = optimizer)

model.fit(X_train, y_train, epochs=50)

print(model.evaluate(X_train, y_train))

print(model.evaluate(X_test, y_test))

from sklearn.metrics import r2_score
pred_train = model.predict(X_train)
r2_score(y_train, pred_train)

pred_test = model.predict(X_test)
r2_score(y_test, pred_test)