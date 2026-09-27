from pathlib import Path

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def decode_image(path: tf.Tensor, label: tf.Tensor, image_size: int):
    """Decode PNG and composite transparency onto white, like the classical pipeline."""
    rgba = tf.io.decode_png(tf.io.read_file(path), channels=4)
    rgba = tf.cast(rgba, tf.float32) / 255.0
    alpha = rgba[..., 3:4]
    rgb = rgba[..., :3] * alpha + (1.0 - alpha)
    rgb = tf.image.resize(rgb, (image_size, image_size), antialias=True)
    return rgb, label


def make_dataset(
    paths: list[Path], labels, image_size: int, batch_size: int,
    training: bool = False, seed: int = 42,
) -> tf.data.Dataset:
    dataset = tf.data.Dataset.from_tensor_slices(([str(path) for path in paths], labels))
    if training:
        dataset = dataset.shuffle(len(paths), seed=seed, reshuffle_each_iteration=True)
    dataset = dataset.map(
        lambda path, label: decode_image(path, label, image_size),
        num_parallel_calls=tf.data.AUTOTUNE,
    )
    return dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)


def build_lenet(image_size: int, class_count: int, learning_rate: float) -> keras.Model:
    """A modernised LeNet-style CNN using concepts from CM-CV2/CM-CV3."""
    augmentation = keras.Sequential([
        layers.RandomRotation(0.04),
        layers.RandomTranslation(0.06, 0.06),
        layers.RandomContrast(0.10),
    ], name="data_augmentation")
    inputs = keras.Input((image_size, image_size, 3))
    x = augmentation(inputs)
    x = layers.Conv2D(32, 5, padding="same", activation="relu")(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(64, 3, padding="same", activation="relu")(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(128, 3, padding="same", activation="relu")(x)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.35)(x)
    outputs = layers.Dense(class_count, activation="softmax")(x)
    model = keras.Model(inputs, outputs, name="emoji_lenet")
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model
