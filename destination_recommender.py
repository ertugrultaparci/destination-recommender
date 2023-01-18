import numpy as np
import pandas as pd

import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing

from keras.utils import np_utils
from keras.models import model_from_json
from keras import backend as K

from numpy import argmax

from read_data import read_data

dataframe = read_data('newdata.csv')

# Encode the dataset:
dataset = dataframe.values

# categories and columns to be encoded
name = dataset[:,0]
mail = dataset[:,1]
orig = dataset[:,2]

# label column to be encoded:
dest = dataset[:,3]

def feature_encoder(feature):
    encoder = preprocessing.LabelEncoder()
    encoder.fit(feature)

    return encoder

encoder_name = feature_encoder(name)
encoder_mail = feature_encoder(mail)
encoder_orig = feature_encoder(orig)
encoder_dest = feature_encoder(dest)

# encode name values as integers
encoder_name = feature_encoder(name)
encoded_name = encoder_name.transform(name)

# encode mail values as integers
encoder_mail = feature_encoder(mail)
encoded_mail = encoder_mail.transform(mail)

# encode orig values as integers
encoder_orig = feature_encoder(orig)
encoded_orig = encoder_orig.transform(orig)

# encode dest values as integers
encoder_dest = feature_encoder(dest)
encoded_dest = encoder_dest.transform(dest)

# Create a dataframe with embedded columns:
new_dataframe = pd.DataFrame()

new_dataframe['0'] = encoded_name
new_dataframe['1'] = encoded_mail
new_dataframe['2'] = encoded_orig

new_dataframe_y = pd.DataFrame()
new_dataframe_y['Dest'] = encoded_dest

#output size:
output_size = new_dataframe_y.Dest.unique().size

X = new_dataframe
y = new_dataframe_y

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2 - Model Building

yhot_train = np_utils.to_categorical(y_train)
yhot_test = np_utils.to_categorical(y_test)

def run(text_input):  
    K.clear_session()
    f = open("model_architecture.json",'r+')
    json_string = f.read()
    f.close()
    model = model_from_json(json_string)

    model.load_weights('model_weights.h5')
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    predict_x = model.predict(text_input)
    pred = np.argmax(predict_x, axis=1)
    
    ans = encoder_dest.inverse_transform(pred)

    return ans[0]
    K.clear_session()