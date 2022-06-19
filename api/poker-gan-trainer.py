
from re import I
import tensorflow_gan as tfgan
import tensorflow as tf
from keras.utils import np_utils
from tensorflow.keras import layers
from tensorflow.python.keras.models import Model
import pandas as pd
import numpy as np
class_names = ['Check', 'Call', 'Raise one third pot', 'Raise pot', 'Raise all in',
               'Fold']

actions_train = pd.read_csv('danielActions.csv', names=['Amount to play', 'Previous Bet', 'Last Action', 'Position', 'Pot Size', 'Stack', 'Equity vs Unknown', 'Action'])
action_features = actions_train.copy()
action_labels = action_features.pop('Action')
action_labels = np_utils.to_categorical(action_labels)
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

print("\n\n\n\n\n\n these are inputs")
print(inputs)

numeric_inputs = {name:input for name,input in inputs.items()
                  if input.dtype==tf.float32}

x = layers.Concatenate()(list(numeric_inputs.values()))
norm = layers.Normalization()
norm.adapt(np.array(actions_train[numeric_inputs.keys()]))
all_numeric_inputs = norm(x)
print("\n\n\n\n\n\n this is normalized out put: ")
print(all_numeric_inputs)

preprocessed_inputs = [all_numeric_inputs]


#0 is for check, 1 call, 2 fold, 3 raise 1/3rd pot, 4 raise pot, 5 all in
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

features_dict = {name:values for name, values in action_features_dict.items()}
print("\n\n\n\n pre pro")
print(action_features_dict)
print("\n\n\n\n this")
print(action_labels)

def action_model(preprocessing_head, inputs):
  body = tf.keras.Sequential([
    layers.Dense(8, activation=tf.nn.relu),
    layers.Dense(4, activation=tf.nn.relu),
    tf.keras.layers.Dense(6, activation=tf.nn.softmax)
  ])

  preprocessed_inputs = preprocessing_head(inputs)
  result = body(preprocessed_inputs)
  model = tf.keras.Model(inputs, result)

  model.compile(loss='categorical_crossentropy',
                optimizer=tf.keras.optimizers.Adam(), metrics=['accuracy'])
  return model

ourModel = action_model(action_preprocessing, inputs)
history = ourModel.fit(x=action_features_dict, y=action_labels, epochs=15)

print("\n\n\nhistory: ")
print(history.history)
# action_model.save('test')


result = ourModel.evaluate(action_features_dict, action_labels, batch_size= 105, verbose=2)
print("test loss, test acc:", result)

print("gen predictions for 3 samples")
predictions = ourModel.predict(action_features_dict)
print("leng: ", len(predictions))

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
    print(actionMap[current])

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