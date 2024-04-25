import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

model = tf.keras.models.load_model('mnist_mlp_model.h5')


def load_and_prepare_image(filepath):
    img = image.load_img(filepath, color_mode='grayscale', target_size=(28, 28))
    img = image.img_to_array(img)
    img = img.reshape(1, 28, 28)
    img = img.astype('float32')
    img /= 255.0
    return img


filepath = 'teste.png'

img = load_and_prepare_image(filepath)
predictions = model.predict(img)
predicted_digit = np.argmax(predictions)

plt.imshow(img.reshape(28, 28), cmap='gray')
plt.title(f'Previsão: {predicted_digit}')
plt.show()
