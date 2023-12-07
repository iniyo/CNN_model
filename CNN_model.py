import keras
import numpy as np
import matplotlib.pyplot as plt

train_images, test_images, train_labels, test_labels = np.load('C:\\Users\\iniyo\\Desktop\\face_Datasets\\learning_dataset=128.npy', allow_pickle = True) 
# 데이터 전처리
train_images, test_images = train_images / 255, test_images / 255

model = keras.models.Sequential([
    keras.layers.Conv2D(input_shape = (128, 128, 3),
                        kernel_size = (3,3), padding ='same',
                        filters = 64, activation= 'relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2, padding='same'),
    keras.layers.Conv2D(kernel_size = (3,3), padding ='same',
                        filters = 128),
    keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2, padding='same'),
    keras.layers.Conv2D(kernel_size = (3,3), padding ='same',
                        filters = 256),
    keras.layers.Conv2D(kernel_size = (3,3), padding ='same',
                        filters = 256),
    keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2, padding='same'),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation = 'relu'),
    keras.layers.Dropout(.5),
    keras.layers.Dense(32, activation= 'relu'),
    keras.layers.Dropout(.5),
    keras.layers.Dense(1, activation='sigmoid'),
])

model.compile(optimizer='sgd', loss ='binary_crossentropy', metrics = ['accuracy'], run_eagerly=True) # 이진 분류이므로 
# 교차 검증법을 통한 model 학습
history = model.fit(train_images, train_labels, epochs = 50, verbose=1, validation_split=0.25)

plt.plot(history.history['accuracy'], 'b-')
plt.plot(history.history['val_accuracy'], 'r--')
plt.plot(history.history['loss'], 'g-')
plt.plot(history.history['val_loss'], 'k--')
plt.show()

# model save 경로
model.save('C:\\Users\\iniyo\\Desktop\\CNN_model\\CNN_model.h5')
# test_images, test_labels로 정확도 평가
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)

print(test_loss)
print(test_acc)
pre = model.predict(test_images[:10])
print('예측값 :', pre)
print('실제값 :', test_labels[:10])

for i, vl in enumerate(pre):
    if vl < 0.5:
        plt.figure()
        plt.imshow(test_images[i,:,:])
        plt.title('warm')
        plt.axis('off')
        plt.show()
        if i == 10: break
    else :
        plt.figure()
        plt.imshow(test_images[i,:,:])
        plt.title('cool')
        plt.axis('off')
        plt.show()
        if i == 10: break