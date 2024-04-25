import tensorflow as tf
import matplotlib as plt

mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(265, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

epocas_hist = model.fit(x_train, y_train, epochs=3, validation_split=0.2)

import pandas as pd

df_historico = pd.DataFrame(epocas_hist.history)
df_historico.info()

test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'Teste acurácia: {test_acc:.3f}\nTeste loss: {test_loss:0.3f}')

model.save('mnist_mlp_model.h5')
