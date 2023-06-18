# Evaluate the model on the testing data
score = model.evaluate(X_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# Make predictions on new data
new_data = np.random.random((10, 224, 224, 1))
predictions = model.predict(new_data)
print(predictions)
