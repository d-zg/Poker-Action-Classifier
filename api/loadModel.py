import numpy as np
import tensorflow as tf
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers


def getDict(action_features):
    # for name, column in action_features.items():
    #     dtype = column.dtype
    #     if dtype == object:
    #         dtype = tf.string
    #     else:
    #         dtype = tf.float32
    # action_features_dict = {name: np.array(value) 
    #                         for name, value in action_features.items()}
    # return action_features_dict
    inputs = {}

    for name, column in action_features.items():
        dtype = column.dtype
        if dtype == object:
            dtype = tf.string
        else:
            dtype = tf.float32
        inputs[name] = tf.keras.Input(shape =(1, ), name=name, dtype = dtype)


    action_features_dict = {name: np.array(value) 
                            for name, value in action_features.items()}

    return action_features_dict

def getPrediction(features):
    model = keras.models.load_model('./my_model')
    feature_array = np.array(features)
    feature_df = pd.DataFrame([feature_array], columns=['amountToPlay', 'previousBet', 'lastAction', 'position', 'potSize', 'stack', 'equityVsUnknown'])#.astype('amountToPlay': )
    feature_df["amountToPlay"] = pd.to_numeric(feature_df["amountToPlay"])
    feature_df["previousBet"] = pd.to_numeric(feature_df["previousBet"])
    feature_df["position"] = pd.to_numeric(feature_df["position"])
    feature_df["potSize"] = pd.to_numeric(feature_df["potSize"])
    feature_df["stack"] = pd.to_numeric(feature_df["stack"])
    feature_df["equityVsUnknown"] = pd.to_numeric(feature_df["equityVsUnknown"])
    feature_dict = getDict(feature_df)
    predictions = model.predict(feature_dict)
    actionMap = ['check', 'call', 'fold', 'raise 1/3', 'raise pot', 'raise all in']
    for prediction in predictions:
        max = 0
        current = -1
        i = 0
        for action in prediction:
            if action > max:
                max = action
                current = i 
            i = i+1
        return(actionMap[current])

print(getPrediction([233.3333333,0,'Raise pot',-10,933.3333333,1015,0.752]))

# actions_train = pd.read_csv('danielActions.csv', names=['amountToPlay', 'previousBet', 'lastAction', 'position', 'potSize', 'stack', 'equityVsUnknown', 'action'])


# feature_array = np.array([233.3333333,0,'Raise pot',-10,933.3333333,1015,0.752])
# feature_df = pd.DataFrame([feature_array], columns=['amountToPlay', 'previousBet', 'lastAction', 'position', 'potSize', 'stack', 'equityVsUnknown'])
# print(getDict(feature_df))