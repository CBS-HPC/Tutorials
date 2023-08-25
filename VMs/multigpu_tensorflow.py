
import tensorflow as tf
from tensorflow import keras
import os

# Define Model
def get_compiled_model():
    # Make a simple 2-layer densely-connected neural network.
    inputs = keras.Input(shape=(784,))
    x = keras.layers.Dense(256, activation="relu")(inputs)
    x = keras.layers.Dense(256, activation="relu")(x)
    outputs = keras.layers.Dense(10)(x)
    model = keras.Model(inputs, outputs)
    model.compile(
        optimizer=keras.optimizers.Adam(),
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=[keras.metrics.SparseCategoricalAccuracy()],
    )
    return model

# Define data
def get_dataset():
    batch_size = 32
    num_val_samples = 10000

    # Return the MNIST dataset in the form of a `tf.data.Dataset`.
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    # Preprocess the data (these are Numpy arrays)
    x_train = x_train.reshape(-1, 784).astype("float32") / 255
    x_test = x_test.reshape(-1, 784).astype("float32") / 255
    y_train = y_train.astype("float32")
    y_test = y_test.astype("float32")

    # Reserve num_val_samples samples for validation
    x_val = x_train[-num_val_samples:]
    y_val = y_train[-num_val_samples:]
    x_train = x_train[:-num_val_samples]
    y_train = y_train[:-num_val_samples]
    return (
        tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(batch_size),
        tf.data.Dataset.from_tensor_slices((x_val, y_val)).batch(batch_size),
        tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(batch_size),
    )

# Prepare a directory to store all the checkpoints.
checkpoint_dir = "./ckpt"
if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)

def make_or_restore_model():
    # Either restore the latest model, or create a fresh one
    # if there is no checkpoint available.
    checkpoints = [checkpoint_dir + "/" + name for name in os.listdir(checkpoint_dir)]
    if checkpoints:
        latest_checkpoint = max(checkpoints, key=os.path.getctime)
        print("Restoring from", latest_checkpoint)
        return keras.models.load_model(latest_checkpoint)
    print("Creating a new model")
    return get_compiled_model()

def run_training(total_epochs=1, n_gpu=None,save_every=None):
    
    # Create a MirroredStrategy.

    gpu_devices = tf.config.experimental.list_physical_devices('GPU')
    if n_gpu is not None:
         # Get a list of all available GPU devices
        gpu_devices = tf.config.experimental.list_physical_devices('GPU')

        if n_gpu is None:
            gpu_devices_to_use = ["/device:GPU:{}".format(i) for i in range(len(gpu_devices))]
        else:
            gpu_devices_to_use = ["/device:GPU:{}".format(i) for i in range(n_gpu)]

        strategy = tf.distribute.MirroredStrategy(devices=gpu_devices_to_use)
    else: 
        strategy = tf.distribute.MirroredStrategy()

    # Open a strategy scope and create/restore the model
    with strategy.scope():
        model = make_or_restore_model()

    if save_every is None:
        save_every = "epoch"  # Default to saving checkpoints every epoch

    callbacks = [
        # This callback saves a SavedModel every epoch
        # We include the current epoch in the folder name.
        keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_dir + "/ckpt-{epoch}", save_freq=save_every
        )
    ]
    
    # Load data
    train_dataset, val_dataset, test_dataset = get_dataset()

    # Train Model
    model.fit(
        train_dataset,
        epochs=total_epochs,
        callbacks=callbacks,
        validation_data=val_dataset,
        verbose=2,
    )

    # Test the model on all available devices.
    model.evaluate(test_dataset)

    # Save the entire model as a `.keras` zip archive.
    model.save('final_model.keras')

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='simple distributed training job')
    parser.add_argument('total_epochs', type=int, help='Total epochs to train the model')
    parser.add_argument('--n_gpu', type=int, default=None, help='Number of GPUs to use')
    #parser.add_argument('--save_every', type=int, default=None, help='Save checkpoints every N epochs or "epoch" (default: epoch)')
    args = parser.parse_args()
    
    # Running the first time creates the model
    run_training(total_epochs=args.total_epochs, n_gpu=args.n_gpu)