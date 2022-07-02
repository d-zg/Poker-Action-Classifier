import tensorflow as tf


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


    #0 is for check, 1 call, 2 fold, 3 raise 1/3rd pot, 4 raise pot, 5 all in
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