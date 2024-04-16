"""
Training the faces.
Here we are fetching the data from kaggle dataset.
link : https://www.kaggle.com/datasets/msambare/fer2013

Libraries used here are :
1. Keras
2. Tensorflow
3. numpy
4. opencv2
5. tkinter
"""

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
from keras.optimizers import Adam
from keras.models import model_from_json
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# from docx import Document

# Initializing image data generator with rescaling
train_data_gen = ImageDataGenerator(rescale=1./255)
validation_data_gen = ImageDataGenerator(rescale=1./255)

"""
Image preprocessing using image data generator
"""
#Preprocessing all the training images
train_generator = train_data_gen.flow_from_directory(
    'Data/train',
    target_size=(48, 48),
    batch_size=64,
    color_mode="grayscale",
    class_mode='categorical'
)

#Preprocessing all the testing images
validation_generator = validation_data_gen.flow_from_directory(
    'Data/test',
    target_size=(48, 48),
    batch_size=64,
    color_mode="grayscale",
    class_mode='categorical'
)

#create model structure
"""
To avoid overfitting use dropout
"""
emotion_model = Sequential()

emotion_model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
emotion_model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Dropout(0.25))

emotion_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Dropout(0.25))

emotion_model.add(Flatten())
emotion_model.add(Dense(1024, activation='relu'))
emotion_model.add(Dropout(0.25))
emotion_model.add(Dense(7, activation='softmax'))

emotion_model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=0.0001, decay=1e-6), metrics=['accuracy'])

#Train the neural network/model
emotion_model_info = emotion_model.fit_generator(
    train_generator,
    steps_per_epoch=28709 // 64,
    epochs=100,
    validation_data=validation_generator,
    validation_steps=7178 // 64
)

# Evaluate the model on the test
# test_loss, test_accuracy = emotion_model.evaluate(validation_generator)
# Print the test accuracy
# print("Test Accuracy: {:.2f}%".format(test_accuracy * 100))

#save model structure in jason file
model_json = emotion_model.to_json()
with open("Model/emotional_model.json", "w") as json_file:
    json_file.write(model_json)

# Save trained model weight in .h5 file
emotion_model.save_weights('emotional_model.h5')

# Evalute model on test data
loss, accuracy = emotion_model.evaluate(validation_generator, steps=7178 // 64)
print("Accuracy on test data: {:.2f}%".format(accuracy * 100))
print("Loss on test data: {:.4f}".format(loss))

# Get training loss and accuracy
training_loss = emotion_model_info.history['loss']
training_accuracy = emotion_model_info.history['accuracy']

# Print training loss and accuracy
print("Training Loss: {:.4f}".format(training_loss[-1]))
print("Training Accuracy: {:.2f}%".format(training_accuracy[-1] * 100))

# Save metrics to a Word document
# doc = Document()
# doc.add_heading('Model Metrics', 0)
#
# # Training metrics
# doc.add_heading('Training Metrics', level=1)
# doc.add_paragraph("Final Training Loss: {:.4f}".format(training_loss[-1]))
# doc.add_paragraph("Final Training Accuracy: {:.2f}%".format(training_accuracy[-1] * 100))
#
# # Testing metrics
# doc.add_heading('Testing Metrics', level=1)
# doc.add_paragraph("Test Loss: {:.4f}".format(loss))
# doc.add_paragraph("Test Accuracy: {:.2f}%".format(accuracy * 100))
#
# # Save document
# doc.save('model_metrics.docx')
# print("Model metrics saved to 'model_metrics.docx'")

# Confusion Matrix and Classification Report
# Generate predictions for the test data
y_pred = np.argmax(emotion_model.predict(validation_generator), axis=-1)
y_true = validation_generator.classes

# Generate confusion Matrix
conf_mat = confusion_matrix(y_true, y_pred)

# Plot confusion matrix
plt.figure(figsize=(8, 8))
sns.heatmap(conf_mat, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=train_generator.class_indices,
            yticklabels=train_generator.class_indices)
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()

# Save confusion matrix as an image
plt.savefig('/Users/mohit/PycharmProjects/Emotion_detection/confusion_matrix.png')
plt.close()

# Print classification report
class_labels = list(train_generator.class_indices.keys())
cls_report = classification_report(y_true, y_pred, target_names=class_labels)
print("Classification Report : \n", cls_report)

# Save classification report to a text file
with open('/Users/mohit/PycharmProjects/Emotion_detection/classification_report.txt', 'w') as report_file:
    report_file.write(cls_report)

# To Test the model and print the accuracy

# # Load model structure from json file
# with open('Model/emotional_model.json', 'r') as json_file:
#     loaded_model_json = json_file.read()
#
# model = model_from_json(loaded_model_json)
#
# # Load weights into the new model
# model.load_weights('emotional_model.h5')
#
# # Compile the model before evolution
# model.compile(
#     loss='categorical_crossentropy',
#     optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=0.0001, decay=1e-6),
#     metrics=['accuracy']
# )
#
# # Evaluate model
# loss, accuracy = model.evaluate(validation_generator, steps= 7178 // 64)
# print("Accuracy on test data is: ", accuracy)
#
# # Get training loss and accuracy
# loss = emotion_model_info.history['loss']
# accuracy = emotion_model_info.history['accuracy']
#
# print("Training Loss is: ", loss)
# print("Training Accuracy is: ", accuracy)