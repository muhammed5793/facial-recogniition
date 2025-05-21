import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import os

# Paths to your training and validation directories
train_dir = 'data/training'

val_dir = 'data/validation'

def get_number_of_classes():
    classes_path = os.path.join(os.curdir, 'data/training')    
    folder_names = [f for f in os.listdir(classes_path) if os.path.isdir(os.path.join(classes_path, f))]
    return len(folder_names)

def train_ai():
    train_datagen = ImageDataGenerator(
    rescale=1.0/255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
    )

    val_datagen = ImageDataGenerator(rescale=1.0/255)

    # Data Generators
    train_generator = train_datagen.flow_from_directory(
        train_dir, 
        target_size=(150, 150), 
        batch_size=16, 
        class_mode='categorical'
    )

    val_generator = val_datagen.flow_from_directory(
        val_dir, 
        target_size=(150, 150), 
        batch_size=16, 
        class_mode='categorical'
    )

   
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(150, 150, 3))
    base_model.trainable = False  

    num_class = get_number_of_classes()
    print("Total Number of class", num_class)
    # Build the Model
    model = Sequential([
        base_model,
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_class, activation='softmax')  # Adjust for 4 classes
    ])

    # Compile the Model with Lower Learning Rate
    model.compile(
        optimizer=Adam(learning_rate=0.0001), 
        loss='categorical_crossentropy', 
        metrics=['accuracy']
    )

    # Add Early Stopping
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    # Train the Model
    history = model.fit(
        train_generator, 
        validation_data=val_generator, 
        epochs=10,
        callbacks=[early_stopping]
    )

    # Save the Trained Model
    model.save('model.h5')
    print("Model training completed and saved.")
