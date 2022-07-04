
from re import I
from sklearn.preprocessing import LabelEncoder
import tensorflow_gan as tfgan
import tensorflow as tf
from keras.utils import np_utils
from tensorflow.keras import layers
from tensorflow.python.keras.models import Model
import pandas as pd
import numpy as np
class_names = ['Check', 'Call', 'Raise one third pot', 'Raise pot', 'Raise all in',
               'Fold']

# reading csv and converting to pandas dataframe
actions_train = pd.read_csv('danielActions.csv', names=['amountToPlay', 'previousBet', 'lastAction', 'position', 'potSize', 'stack', 'equityVsUnknown', 'action'])
action_features = actions_train.copy()

# separating labels
action_labels = action_features.pop('action')

# making categorical var out of labels
action_labels = np_utils.to_categorical(action_labels)

# same with test data
actions_test = pd.read_csv('actionsTest.csv', names=['amountToPlay', 'previousBet', 'lastAction', 'position', 'potSize', 'stack', 'equityVsUnknown', 'action'])
test_features = actions_test.copy()
test_labels = test_features.pop('action')
encoder = LabelEncoder() # encoder is here bc test data uses strings to describe actions, training data is converted to numbers
encoder.fit(test_labels)
encoded_labels = encoder.transform(test_labels)
final_test_labels = np_utils.to_categorical(encoded_labels)


def getFeaturesDict(action_features):
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


    # 0 is for check, 1 call, 2 fold, 3 raise 1/3rd pot, 4 raise pot, 5 all in
    for name, input in inputs.items():
        if input.dtype == tf.float32:
            continue
        lookup = layers.StringLookup(vocabulary=np.unique(action_features[name]))
        one_hot = layers.CategoryEncoding(num_tokens=lookup.vocabulary_size())
        x = lookup(input)
        x = one_hot(x)
        preprocessed_inputs.append(x)

    action_features_dict = {name: np.array(value) 
                            for name, value in action_features.items()}

    return action_features_dict

test_features_dict = getFeaturesDict(test_features)

# embedding transformations into the model
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

# using tf normalization proprocessing for each numeric field
# amounttoplay, previousbet, position, stack, equityvsunknown
numeric_inputs = {name:input for name,input in inputs.items()
                  if input.dtype==tf.float32}

x = layers.Concatenate()(list(numeric_inputs.values()))
norm = layers.Normalization()
norm.adapt(np.array(actions_train[numeric_inputs.keys()]))
all_numeric_inputs = norm(x)
print("\n\n\n\n\n\n this is normalized out put: ")
print(all_numeric_inputs)

# collecting for future concacatenation 
preprocessed_inputs = [all_numeric_inputs]

# using StringLookup to map strings to an index in a vocabulary based on dif strings 
# using index, generate one hot vector 
for name, input in inputs.items():
    if input.dtype == tf.float32:
        continue
    lookup = layers.StringLookup(vocabulary=np.unique(action_features[name]))
    one_hot = layers.CategoryEncoding(num_tokens=lookup.vocabulary_size())
    x = lookup(input)
    x = one_hot(x)
    preprocessed_inputs.append(x)

# concatenate the normalized and categorized inputs & build a model based on those
# see model.png to see what it does to our data
preprocessed_inputs_cat = layers.Concatenate()(preprocessed_inputs)
action_preprocessing = tf.keras.Model(inputs, preprocessed_inputs_cat)

# now we'll actually run our data through the model
action_features_dict = {name: np.array(value) 
                         for name, value in action_features.items()}

features_dict = {name:values for name, values in action_features_dict.items()}
print("\n\n\n\n pre pro")
print(action_features_dict)
print("\n\n\n\n this")
print(action_labels)

def action_model(preprocessing_head, inputs): # takes the model we constructed before
  body = tf.keras.Sequential([
    layers.Dense(32, activation=tf.nn.relu),
    tf.keras.layers.Dense(6, activation=tf.nn.softmax)
  ])

  preprocessed_inputs = preprocessing_head(inputs) # here is where our data gets preprocessed
  result = body(preprocessed_inputs)
  model = tf.keras.Model(inputs, result)

  model.compile(loss='categorical_crossentropy',
                optimizer=tf.keras.optimizers.Adam(), metrics=['accuracy'])
  return model

ourModel = action_model(action_preprocessing, inputs)
history = ourModel.fit(x=action_features_dict, y=action_labels, epochs=100) # handles normalization and feature value indexing on its own! don't need to preprocess

print("\n\n\nhistory: ")
print(history.history)



result = ourModel.evaluate(test_features_dict, final_test_labels, batch_size= 86, verbose=2)
print("test loss, test acc:", result)

# print("gen predictions for 3 samples")
# predictions = ourModel.predict(action_features_dict)
# print("leng: ", len(predictions))

# actionMap = ['check', 'call', 'fold', 'raise 1/3', 'raise pot', 'raise all in']
# for prediction in predictions:
#     max = 0
#     current = -1
#     i = 0
#     for action in prediction:
#         if action > max:
#             max = action
#             current = i 
#         i = i+1
#     print(actionMap[current])

# print("\n\n\n\n\n\n")

ourModel.save('my_model')