# Import necessary libraries
import numpy as np
from tensorflow import keras
from sklearn.model_selection import train_test_split
from preprocess_Data import preprocessed_images
from label_Images import labels

# Set the input data and labels
X = preprocessed_images
y = labels

# Split the data into a training set and a testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert the labels to categorical values
num_classes = len(np.unique(y))

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# Print the shape of the training and testing sets
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)
