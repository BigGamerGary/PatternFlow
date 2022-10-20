from pkgutil import get_data
import numpy as np
import tensorflow as tf
import tensorflow.keras.utils
from tensorflow.keras.preprocessing.image import array_to_img
from tensorflow.keras.preprocessing.image import img_to_array
import matplotlib.pyplot as plt
     
def scaling(input_image):
    input_image = input_image / 255.0
    return input_image

def process_input(input, input_size):
    input = tf.image.rgb_to_yuv(input)
    last_dimension_axis = len(input.shape) - 1
    y, _ ,_ = tf.split(input, 3, axis=last_dimension_axis)
    return tf.image.resize(y, [input_size, input_size], method="area")

def process_target(input):
    input = tf.image.rgb_to_yuv(input)
    last_dimension_axis = len(input.shape) - 1
    y, _ ,_ = tf.split(input, 3, axis=last_dimension_axis)
    return y

"""
Retrieves the datasets from the folder for use by the algorithm

@return the three datasets for training, validation, and testing

"""
def get_datasets(train_path, test_path, batch_size, upscale_factor, crop_size):
    input_size = crop_size // upscale_factor
    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_path, 
        batch_size = batch_size,
        image_size=(crop_size, crop_size),
        label_mode = None,
        validation_split = 0.1,
        seed = 123,
        subset = "training")
    
    val_ds = tf.keras.utils.image_dataset_from_directory(
        train_path, 
        batch_size = batch_size,
        image_size=(crop_size, crop_size),
        label_mode = None,
        validation_split = 0.1,
        seed = 123,
        subset = "validation")

    test_ds = tf.keras.utils.image_dataset_from_directory(test_path, label_mode = None)

    train_ds = train_ds.map(scaling)
    val_ds = val_ds.map(scaling)

    train_ds = train_ds.map(
        lambda x: (process_input(x, input_size), process_target(x))
    )
    val_ds = val_ds.map(
    lambda x: (process_input(x, input_size), process_target(x))
    )
    return train_ds, val_ds, test_ds



def main():
    train_path = "dataset\\train"
    test_path = "dataset\\test"

    train_ds, val_ds, test_ds = get_datasets(train_path, test_path, 8, 4, 200)

    for batch in train_ds.take(1):
        plt.imshow(array_to_img(batch[0][0]))
        plt.show()
        plt.imshow(array_to_img(batch[1][0]))
        plt.show()

if __name__ == "__main__":
    main()