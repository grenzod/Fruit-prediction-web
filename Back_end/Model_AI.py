import matplotlib.pyplot as plt
import os
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Flatten, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Đường dẫn đến thư mục dữ liệu
data_dir = 'C:/Users/TIN/OneDrive/Desktop/BigData/data/Train and Test'
image_paths = []
labels = []

# Lấy đường dẫn đến hình ảnh và nhãn tương ứng
for root, dirs, files in os.walk(data_dir):
    for filename in files:
        if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
            image_path = os.path.join(root, filename)
            image_paths.append(image_path)

            # Lấy tên thư mục chứa tệp hình ảnh làm nhãn
            folder_name = os.path.basename(root)
            if folder_name in ['apple', 'avocado', 'banana', 'cherry', 'kiwi', 'mango', 'orange', 'pineapple',
                               'strawberries', 'watermelon']:
                labels.append(folder_name)
            else:
                labels.append('unknown')

# Load mô hình VGG16 đã được huấn luyện trên ImageNet, không bao gồm các lớp fully connected
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Thêm các lớp fully connected trên mô hình VGG16
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation='relu')(x)
predictions = Dense(len(set(labels)), activation='softmax')(x)

# Tạo mô hình hoàn chỉnh
model = Model(inputs=base_model.input, outputs=predictions)

# Đóng băng các lớp của base_model để không huấn luyện lại
for layer in base_model.layers:
    layer.trainable = False

# Compile mô hình
model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Chuyển nhãn từ tên sang số
label_to_index = {label: idx for idx, label in enumerate(sorted(set(labels)))}
y_numeric = np.array([label_to_index[label] for label in labels])

# Trích xuất đặc trưng
X = np.array([preprocess_input(
    img_to_array(
        load_img(img, target_size=(224, 224)))) for img in image_paths])

# Chia tập dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y_numeric, test_size=0.2, random_state=42)

# Huấn luyện mô hình
history = model.fit(X_train, y_train, epochs=5, batch_size=32, validation_data=(X_test, y_test))
model.save('vgg16_fruit_classifier.h5')

# Dự đoán trên tập kiểm tra
y_pared = np.argmax(model.predict(X_test), axis=1)

# Đánh giá mô hình
print(classification_report(y_test, y_pared, target_names=sorted(set(labels))))
print(confusion_matrix(y_test, y_pared))

plt.figure(figsize=(8, 6))
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
