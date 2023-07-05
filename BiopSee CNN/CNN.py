import tensorflow as tf
from keras import layers
from keras.preprocessing.image import ImageDataGenerator
from keras.metrics import Precision, Recall
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt



#insert preprocessing code here
training_dir = '/Users/bennettye/Desktop/trainingsetimages'
validation_dir = '/Users/bennettye/Desktop/tumorTissueTests'

train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)
val_datagen = ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory(
    training_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'
)

val_data = val_datagen.flow_from_directory(
    validation_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'
)

def f1(y_true, y_pred):
    tp = tf.keras.backend.sum(tf.keras.backend.round(tf.keras.backend.clip(y_true * y_pred, 0, 1)))
    fp = tf.keras.backend.sum(tf.keras.backend.round(tf.keras.backend.clip(y_pred - y_true, 0, 1)))
    fn = tf.keras.backend.sum(tf.keras.backend.round(tf.keras.backend.clip(y_true - y_pred, 0, 1)))

    precision = tp / (tp + fp + tf.keras.backend.epsilon())
    recall = tp / (tp + fn + tf.keras.backend.epsilon())
    f1_score = 2 * precision * recall / (precision + recall + tf.keras.backend.epsilon())

    return f1_score

#create the mdoel 
model = tf.keras.Sequential([
    layers.Conv2D(32, (3,3), activation = 'relu', input_shape = (224,224,3)), #convolutional layer
    layers.Dropout(0.2), # dropout layer
    layers.BatchNormalization(), #batch normalization layer
    layers.MaxPooling2D((2,2)), # max pooling layer
    layers.Conv2D(64, (3,3), activation = 'relu'),
    layers.Dropout(0.3),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(128, (3,3), activation = 'relu'),
    layers.Dropout(0.3),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(256, (3,3), activation = 'relu'),
    layers.Dropout(0.5),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(512, (3,3), activation = 'relu'),
    layers.Dropout(0.5),
    layers.Flatten(),
    layers.Dense(128, activation = 'relu'),
    layers.Dense(1, activation = 'sigmoid')
])


earlystop_callback = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

model.compile(loss = 'binary_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001), 
                metrics=['accuracy', Precision(name = 'precision'), Recall(name = 'recall'), f1])

history = model.fit(train_data, epochs=20, validation_data=val_data, callbacks = [earlystop_callback])  # train the model

val_loss, val_accuracy, val_precision, val_recall, val_f1 = model.evaluate(val_data)  # compute validation metrics

print("Validation Loss:", val_loss)
print("Validation Accuracy:", val_accuracy)
print("Validation Precision:", val_precision)
print("Validation Recall:", val_recall)
print("Validation F1 Score:", val_f1)

# plot the training and validation accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

# plot the training and validation loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()
