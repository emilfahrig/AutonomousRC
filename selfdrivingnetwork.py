from keras.models import Model
from keras.layers import Conv2D, Dense, Flatten, Input, Dropout, MaxPool2D, Concatenate, BatchNormalization
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
import matplotlib.pyplot as plt
import os
import tensorflow as tf


def define_model():
    # define input layer size of Convolutional Neural Network
    input_image_array = Input((150, 100, 3))

    conv_layer_1 = (Conv2D(128, (16, 16), kernel_initializer='he_uniform', activation='relu', input_shape=(150, 100)))(input_image_array)
    conv_dropout_1 = (Dropout(0.15))(conv_layer_1)
    conv_max_pool_1 = (MaxPool2D((6, 6), strides=3))(conv_dropout_1)
    conv_layer_2 = (Conv2D(64, (9, 9), strides=2, kernel_initializer='he_uniform', activation='relu'))(conv_max_pool_1)
    conv_dropout_2 = (Dropout(0.15))(conv_layer_2)
    conv_max_pool_2 = (MaxPool2D((4, 4), strides=2))(conv_dropout_2)
    conv_layer_3 = (Conv2D(32, (3, 3), strides=2, kernel_initializer='he_uniform', activation='relu'))(conv_max_pool_2)
    conv_batchnormalize = BatchNormalization()(conv_layer_3)
    flatten_layer = (Flatten())(conv_batchnormalize)

    dense_layer_1 = (Dense(128, kernel_initializer='he_uniform', activation='relu'))(flatten_layer)
    dense_dropout_1 = (Dropout(0.15))(dense_layer_1)
    dense_layer_2 = (Dense(64, kernel_initializer='he_uniform', activation='relu'))(dense_dropout_1)
    dense_dropout_2 = (Dropout(0.15))(dense_layer_2)
    dense_layer_3 = (Dense(32, kernel_initializer='he_uniform', activation='relu'))(dense_dropout_2)
    dense_dropout_3 = (Dropout(0.2))(dense_layer_3)
    dense_layer_4 = (Dense(16, kernel_initializer='he_uniform', activation='relu'))(dense_dropout_3)
    dense_dropout_4 = (Dropout(0.2))(dense_layer_4)
    dense_layer_5 = (Dense(3, activation='softmax'))(dense_dropout_4)

    model = Model(inputs=[input_image_array], outputs=[dense_layer_5])
    optimization = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7)
    model.compile(optimizer=optimization, loss='categorical_crossentropy', metrics=['accuracy'])

    return model


def load_model_improve():
    model = load_model('self_driveplease.h5')

    image_data = ImageDataGenerator(rescale=(1.0/255.0), height_shift_range=0.1, width_shift_range=0.1)
    train_data = image_data.flow_from_directory("C:/Users/emilx/PycharmProjects/AutonoCar/TRAINIMPROVETEST",
                                                class_mode="categorical", batch_size=16, target_size=(150, 100))
    test_data = image_data.flow_from_directory("C:/Users/emilx/PycharmProjects/AutonoCar/testing",
                                              class_mode="categorical", batch_size=16, target_size=(150, 100))
    history = model.fit_generator(train_data, validation_data=test_data, epochs=20, shuffle=True, verbose=1)
    model.save('self_driveplease_improved.h5')

    _, acc = model.evaluate_generator(test_data, steps=len(test_data), verbose=0)
    print('> %.3f' % (acc * 100.0))

    plt.plot(history.history['accuracy'])
    plt.show()


load_model_improve()



