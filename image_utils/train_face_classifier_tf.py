from __future__ import absolute_import, division, print_function

import argparse
import os
import tensorflow as tf
print("TensorFlow version is ", tf.__version__)

import numpy as np


image_size = 160 # All images will be resized to 160x160
IMG_SHAPE = (image_size, image_size, 3)
batch_size = 32
epochs = 100
# Fine tune from this layer onwards
fine_tune_at = 0


def main(base_dir, output_dir):
	train_dir = os.path.join(base_dir, 'training')
	validation_dir = os.path.join(base_dir, 'validation')

	train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                rescale=1./255, horizontal_flip=True)
	validation_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

	# Flow training images in batches of 20 using train_datagen generator
	train_generator = train_datagen.flow_from_directory(
                train_dir,  # Source directory for the training images
                target_size=(image_size, image_size),  
                batch_size=batch_size,
                shuffle=True,
                # Since we use binary_crossentropy loss, we need binary labels
                class_mode='categorical')

	# Flow validation images in batches of 20 using test_datagen generator
	validation_generator = validation_datagen.flow_from_directory(
                validation_dir, # Source directory for the validation images
                target_size=(image_size, image_size),
                batch_size=batch_size,
                class_mode='categorical')
	# Create the base model from the pre-trained model MobileNet V2

	base_model = tf.keras.applications.ResNet50(input_shape=IMG_SHAPE,
                                               include_top=False, 
                                               weights='imagenet')
	# Let's take a look to see how many layers are in the base model
	print("Number of layers in the base model: ", len(base_model.layers))


	# Freeze all the layers before the `fine_tune_at` layer
	for layer in base_model.layers[:fine_tune_at]:
		layer.trainable =  False

	print(validation_generator.class_indices)
	model = tf.keras.Sequential([
		 base_model,
		 tf.keras.layers.GlobalAveragePooling2D(),
		 tf.keras.layers.Dense(2048, activation='relu'),
		 tf.keras.layers.Dense(2048, activation='relu'),
		 tf.keras.layers.Dense(len(validation_generator.class_indices), activation='softmax')
	])
	checkpoint_path = os.path.join(output_dir, "training_1", "cp.ckpt")
	checkpoint_dir = os.path.dirname(checkpoint_path)
	latest = tf.train.latest_checkpoint(checkpoint_dir)

	if latest is not None:
		model.load_weights(latest)

	model.compile(optimizer="adam", 
              loss='categorical_crossentropy', 
              metrics=['accuracy'])

	cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, 
                                                 save_weights_only=True,
                                                 verbose=1)
	early = tf.keras.callbacks.EarlyStopping(monitor="val_acc", mode="max", patience=30)
	reduce_on_plateau = tf.keras.callbacks.ReduceLROnPlateau(monitor="val_acc", mode="max", factor=0.1, patience=3)
	steps_per_epoch = train_generator.n // train_generator.batch_size
	validation_steps = validation_generator.n // validation_generator.batch_size
	history = model.fit_generator(train_generator, 
                              steps_per_epoch = steps_per_epoch,
                              epochs=epochs, 
                              workers=4,
                              validation_data=validation_generator, 
                              validation_steps=validation_steps,
                              callbacks=[cp_callback, early, reduce_on_plateau])
	model_path = os.path.join(output_dir, "model.h5")
	model.save(model_path)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--base-dir', dest='base_dir', help='Image base dir')
	parser.add_argument('--output-dir', dest='output_dir', help='Destination directory')
	args = parser.parse_args()
	main(args.base_dir, args.output_dir)