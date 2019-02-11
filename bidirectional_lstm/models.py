import os

from keras import Sequential, Input, Model
from keras.callbacks import ModelCheckpoint
from keras.layers import Bidirectional, LSTM, Permute, Reshape, Dense, Concatenate, concatenate, BatchNormalization
from keras.optimizers import Adam
from keras.utils import plot_model
from utils.images import create_dataset, Dataset

batch_size = 4
rows = 90
cols = 90
channels = 27
classes = 21
hidden_size = 40


def build_model(rows, cols, channels):
    input_x = Input(shape=(rows, cols, channels))
    x = Reshape((rows * cols, channels))(input_x)
    x = LSTM(hidden_size, return_sequences=True)(x)
    x = Reshape((rows, cols, hidden_size))(x)
    x = Permute((2, 1, 3))(x)
    x = Reshape((rows * cols, hidden_size))(x)
    x = LSTM(hidden_size, return_sequences=True)(x)
    x = Dense(hidden_size, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Reshape((rows, cols, hidden_size))(x)

    input_xv = Input(shape=(rows, cols, channels))
    xv = Reshape((rows * cols, channels))(input_xv)
    xv = LSTM(hidden_size, return_sequences=True)(xv)
    xv = Reshape((rows, cols, hidden_size))(xv)
    xv = Permute((2, 1, 3))(xv)
    xv = Reshape((rows * cols, hidden_size))(xv)
    xv = LSTM(hidden_size, return_sequences=True)(xv)
    xv = Dense(hidden_size, activation='relu')(xv)
    xv = BatchNormalization()(xv)
    xv = Reshape((rows, cols, hidden_size))(xv)

    input_xh = Input(shape=(rows, cols, channels))
    xh = Reshape((rows * cols, channels))(input_xh)
    xh = LSTM(hidden_size, return_sequences=True)(xh)
    xh = Reshape((rows, cols, hidden_size))(xh)
    xh = Permute((2, 1, 3))(xh)
    xh = Reshape((rows * cols, hidden_size))(xh)
    xh = LSTM(hidden_size, return_sequences=True)(xh)
    xh = Dense(hidden_size, activation='relu')(xh)
    xh = BatchNormalization()(xh)
    xh = Reshape((rows, cols, hidden_size))(xh)

    input_xvh = Input(shape=(rows, cols, channels))
    xvh = Reshape((rows * cols, channels))(input_xvh)
    xvh = LSTM(hidden_size, return_sequences=True)(xvh)
    xvh = Reshape((rows, cols, hidden_size))(xvh)
    xvh = Permute((2, 1, 3))(xvh)
    xvh = Reshape((rows * cols, hidden_size))(xvh)
    xvh = LSTM(hidden_size, return_sequences=True)(xvh)
    xvh = Dense(hidden_size, activation='relu')(xvh)
    xvh = BatchNormalization()(xvh)
    xvh = Reshape((rows, cols, hidden_size))(xvh)

    merge_layer = concatenate([x, xv, xh, xvh])
    dense = Dense(classes, activation='softmax')(merge_layer)

    model = Model(inputs=[input_x, input_xv, input_xh, input_xvh], outputs=[dense])
    return model


if __name__ == '__main__':
    model = build_model(rows, cols, channels)
    optimizer = Adam(lr=10e-4)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])


    plot_model(model)

    # callbacks = [ModelCheckpoint(os.path.join('/home/pseweryn/Projects/multidimensional_lstm/repository/models', 'weights.{epoch:02d}-{val_loss:.4f}.hdf5'),
    #                              save_best_only=True)]

    # directory_voc_dataset = '/home/pseweryn/Repositories/VOCdevkit/VOC2012'


    # dataset = Dataset(directory_voc_dataset, subsets=['train', 'val'], image_shape=(rows * 3, cols * 3))
    # X, y = dataset.create_patches('train', how_many_images=-1)
    # print(X.shape)
    # print(y.shape)
    # print('dataset created')
    # model.fit(x=[X[:, 0], X[:, 1], X[:, 2], X[:, 3]], y=y, batch_size=batch_size, epochs=5, verbose=1)
