
import tensorflow_gan as tfgan
import tensorflow as tf

from tensorflow.keras import layers
from tensorflow.python.keras.models import Model
import pandas as pd
import numpy as np
class_names = ['Check', 'Call', 'Raise one third pot', 'Raise pot', 'Raise all in',
               'Fold']

actions_train = pd.read_csv('danielActions.csv', names=['Amount to play', 'Previous Bet', 'Last Action', 'Position', 'Pot Size', 'Stack', 'Equity vs Unknown', 'Action'])
action_features = actions_train.copy()
action_labels = action_features.pop('Action')
# action_features = np.array(action_features)
# action_labels = np.array(action_labels)
# print(action_labels)
# print(action_features)
# actions_model = tf.keras.Sequential([
#     layers.Dense(64),
#     layers.Dense(1)
# ])

inputs = {}

for name, column in action_features.items():
    dtype = column.dtype
    if dtype == object:
        dtype = tf.string
    else:
        dtype = tf.float32
    inputs[name] = tf.keras.Input(shape =(1, ), name=name, dtype = dtype)
# print(inputs)

numeric_inputs = {name:input for name,input in inputs.items()
                  if input.dtype==tf.float32}

x = layers.Concatenate()(list(numeric_inputs.values()))
norm = layers.Normalization()
norm.adapt(np.array(actions_train[numeric_inputs.keys()]))
all_numeric_inputs = norm(x)
print("\n\n\n\n\n\n this is normalized out put: ")
print(all_numeric_inputs)

preprocessed_inputs = [all_numeric_inputs]

for name, input in inputs.items():
    if input.dtype == tf.float32:
        continue
    lookup = layers.StringLookup(vocabulary=np.unique(action_features[name]))
    one_hot = layers.CategoryEncoding(num_tokens=lookup.vocabulary_size())
    x = lookup(input)
    x = one_hot(x)
    preprocessed_inputs.append(x)

preprocessed_inputs_cat = layers.Concatenate()(preprocessed_inputs)
action_preprocessing = tf.keras.Model(inputs, preprocessed_inputs_cat)

action_features_dict = {name: np.array(value) 
                         for name, value in action_features.items()}

features_dict = {name:values[:1] for name, values in action_features_dict.items()}
print("\n\n\n\n pre pro")
print(action_preprocessing(features_dict))

def action_model(preprocessing_head, inputs):
  body = tf.keras.Sequential([
    layers.Dense(64),
    layers.Dense(1)
  ])

  preprocessed_inputs = preprocessing_head(inputs)
  result = body(preprocessed_inputs)
  model = tf.keras.Model(inputs, result)

  model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                optimizer=tf.keras.optimizers.Adam())
  return model

action_model = action_model(action_preprocessing, inputs)
action_model.fit(x=action_features_dict, y=action_labels, epochs=10)
# input_layer = layers.Input(shape=(action_features.shape[1],))
# dense_layer_1 = layers.Dense(15, activation='relu')(input_layer)
# dense_layer_2 = layers.Dense(10, activation='relu')(dense_layer_1)
# output = layers.Dense(6, activation='softmax')(dense_layer_2)

# model = Model(inputs=input_layer, outputs=output)
# model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])
# [print(i.shape, i.dtype) for i in model.inputs]
# [print(o.shape, o.dtype) for o in model.outputs]
# history = model.fit(action_features, action_labels, epochs=10)
def input_fn(mode, params):
    assert 'batch_size' in params
    assert 'noise_dims' in params
    bs = params['batch_size']
    nd = params['noise_dims']
    split = 'train' if mode == tf.estimator.ModeKeys.TRAIN else 'test'
    shuffle = (mode == tf.estimator.ModeKeys.TRAIN)
    just_noise = (mode == tf.estimator.ModeKeys.PREDICT)
    noise_ds = (tf.data.Dataset.from_tensors(0).repeat()
        .map(lambda _: tf.random.normal([bs, nd])))