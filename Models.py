import keras
from keras import backend as K
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Activation, Flatten, Input, Lambda, Reshape
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization, Cropping2D
from keras.layers import Input, UpSampling2D, concatenate

def get_denoise_model(shape):
    inputs = Input(shape)

    ## Encoder starts
    conv1 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(inputs)
    conv2 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = Conv2D(32, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool1)
    conv4 = Conv2D(32, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv3)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv4)

    conv5 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool2)
    conv6 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv5)
    pool3 = MaxPooling2D(pool_size=(2, 2))(conv6)

    conv7 = Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool3)
    conv8 = Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv7)
    # pool4 = MaxPooling2D(pool_size=(2, 2))(conv8)

    ## Bottleneck
    # conv9 = Conv2D(1024, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool4)
    # conv10 = Conv2D(1024, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv9)

    ## Now the decoder starts
    # up1 = Conv2D(512, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(conv10))
    # merge1 = concatenate([conv8,up1], axis = -1)
    # conv11 = Conv2D(512, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge1)
    # conv12 = Conv2D(512, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv11)

    up2 = Conv2D(64, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv7))
    merge2 = concatenate([conv6, up2], axis=-1)
    conv13 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge2)
    conv14 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv13)

    up3 = Conv2D(32, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv14))
    merge3 = concatenate([conv4, up3], axis=-1)
    conv15 = Conv2D(32, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge3)
    conv16 = Conv2D(32, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv15)

    up4 = Conv2D(16, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv16))
    merge4 = concatenate([conv2, up4], axis=-1)
    conv17 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge4)
    conv18 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv17)

    conv19 = Conv2D(1, 3, padding='same')(conv18)  ####different

    U_net = Model(inputs=inputs, outputs=conv19)

    return U_net


def get_baseline_model(shape):
    inputs = Input(shape)

    ## Encoder starts
    conv1 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(inputs)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

    ## Bottleneck
    conv2 = Conv2D(32, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool1)

    ## Now the decoder starts
    up3 = Conv2D(64, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv2))
    merge3 = concatenate([conv1, up3], axis=-1)
    conv3 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge3)

    conv4 = Conv2D(1, 3, padding='same')(conv3)

    baseline_net = Model(inputs=inputs, outputs=conv4)

    return baseline_net


def get_full_model(shape):
    inputs = Input(shape)

    ## Encoder starts
    conv1 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(inputs)
    conv2 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = Conv2D(32, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool1)
    conv4 = Conv2D(32, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv3)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv4)

    conv5 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool2)
    conv6 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv5)
    pool3 = MaxPooling2D(pool_size=(2, 2))(conv6)

    conv7 = Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool3)
    conv8 = Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv7)
    pool4 = MaxPooling2D(pool_size=(2, 2))(conv8)

    # Bottleneck
    conv9 = Conv2D(1024, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool4)
    conv10 = Conv2D(1024, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv9)

    # Now the decoder starts
    up1 = Conv2D(512, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv10))
    merge1 = concatenate([conv8, up1], axis=-1)
    conv11 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge1)
    conv12 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv11)

    up2 = Conv2D(64, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv12))
    merge2 = concatenate([conv6, up2], axis=-1)
    conv13 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge2)
    conv14 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv13)

    up3 = Conv2D(32, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv14))
    merge3 = concatenate([conv4, up3], axis=-1)
    conv15 = Conv2D(32, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge3)
    conv16 = Conv2D(32, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv15)

    up4 = Conv2D(16, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv16))
    merge4 = concatenate([conv2, up4], axis=-1)
    conv17 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge4)
    conv18 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv17)

    conv19 = Conv2D(1, 3, padding='same')(conv18)  ####different

    U_net = Model(inputs=inputs, outputs=conv19)

    return U_net


def get_denoise_model_5x2(shape):
    inputs = Input(shape)

    ## Encoder starts
    #   conv1 = Conv2D(16, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(inputs)
    #   conv2 = Conv2D(16, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv1)
    #   pool1 = MaxPooling2D(pool_size=(2, 2))(conv2)

    #   conv3= Conv2D(32, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool1)
    #   conv4= Conv2D(32, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv3)
    #   pool2 = MaxPooling2D(pool_size=(2, 2))(conv4)

    #   conv5= Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool2)
    #   conv6= Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv5)
    #   pool3 = MaxPooling2D(pool_size=(2, 2))(conv6)

    conv7 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(inputs)
    conv8 = Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv7)
    # pool4 = MaxPooling2D(pool_size=(2, 2))(conv8)

    ## Bottleneck
    # conv9 = Conv2D(1024, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool4)
    # conv10 = Conv2D(1024, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv9)

    ## Now the decoder starts
    up1 = Conv2D(128, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv8))
    # merge1 = concatenate([conv8,up1], axis = -1)
    conv11 = Conv2D(128, [3, 3], activation='relu', padding='same', kernel_initializer='he_normal')(up1)
    conv12 = Conv2D(128, [3, 3], activation='relu', padding='valid', kernel_initializer='he_normal')(conv11)

    up2 = Conv2D(64, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv12))
    #   merge2 = concatenate([conv6,up2], axis = -1)
    conv13 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(up2)
    conv14 = Conv2D(64, 3, strides=(2, 1), activation='relu', padding='same', kernel_initializer='he_normal')(conv13)

    up3 = Conv2D(32, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv14))
    #   merge3 = concatenate([conv4,up3], axis = -1)
    conv15 = Conv2D(32, 3, activation='relu', padding='same', kernel_initializer='he_normal')(up3)
    conv16 = Conv2D(32, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv15)

    up4 = Conv2D(16, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv16))
    #   merge4 = concatenate([conv2,up4], axis = -1)
    conv17 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(up4)
    conv18 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv17)

    up5 = Conv2D(16, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv18))
    #   merge4 = concatenate([conv2,up4], axis = -1)
    conv19 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(up5)
    conv20 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv19)

    up6 = Conv2D(16, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(1, 2))(conv20))
    #   merge4 = concatenate([conv2,up4], axis = -1)
    conv21 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(up6)
    conv22 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv21)

    conv23 = Conv2D(1, 3, padding='same')(conv22)  ####different

    U_net = Model(inputs=inputs, outputs=conv23)

    return U_net

def get_denoise_model_5x6(shape):
    inputs = Input(shape)

    ## Encoder starts
    #   conv1 = Conv2D(16, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(inputs)
    #   conv2 = Conv2D(16, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv1)
    #   pool1 = MaxPooling2D(pool_size=(2, 2))(conv2)

    #   conv3= Conv2D(32, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool1)
    #   conv4= Conv2D(32, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv3)
    #   pool2 = MaxPooling2D(pool_size=(2, 2))(conv4)

    #   conv5= Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool2)
    #   conv6= Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv5)
    #   pool3 = MaxPooling2D(pool_size=(2, 2))(conv6)

    conv7 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(inputs)
    conv8 = Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv7)
    # pool4 = MaxPooling2D(pool_size=(2, 2))(conv8)

    ## Bottleneck
    # conv9 = Conv2D(1024, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool4)
    # conv10 = Conv2D(1024, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv9)

    ## Now the decoder starts
    up1 = Conv2D(128, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv8))
    # merge1 = concatenate([conv8,up1], axis = -1)
    conv11 = Conv2D(128, [3, 5], activation='relu', padding='same', kernel_initializer='he_normal')(up1)
    conv12 = Conv2D(128, [3, 5], activation='relu', padding='valid', kernel_initializer='he_normal')(conv11)

    up2 = Conv2D(64, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv12))
    #   merge2 = concatenate([conv6,up2], axis = -1)
    conv13 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(up2)
    conv14 = Conv2D(64, 3, strides=(2, 2), activation='relu', padding='same', kernel_initializer='he_normal')(conv13)

    up3 = Conv2D(32, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv14))
    #   merge3 = concatenate([conv4,up3], axis = -1)
    conv15 = Conv2D(32, 3, activation='relu', padding='same', kernel_initializer='he_normal')(up3)
    conv16 = Conv2D(32, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv15)

    up4 = Conv2D(16, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv16))
    #   merge4 = concatenate([conv2,up4], axis = -1)
    conv17 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(up4)
    conv18 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv17)

    up5 = Conv2D(16, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv18))
    #   merge4 = concatenate([conv2,up4], axis = -1)
    conv19 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(up5)
    conv20 = Conv2D(16, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv19)

    #   up6 = Conv2D(16, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (1,2))(conv20))
    # #   merge4 = concatenate([conv2,up4], axis = -1)
    #   conv21 = Conv2D(16, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(up6)
    #   conv22 = Conv2D(16, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv21)

    conv21 = Conv2D(1, 3, padding='same')(conv20)  ####different

    U_net = Model(inputs=inputs, outputs=conv21)

    return U_net