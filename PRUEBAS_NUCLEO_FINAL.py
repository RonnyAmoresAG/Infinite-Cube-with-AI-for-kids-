import cv2
import numpy as np
from tensorflow.keras.models import load_model
import tkinter as tk
from PIL import Image, ImageTk
from collections import Counter

# Configuración
MODEL_PATH = 'C:/Users/Ronny Amores/Desktop/Sexto Semestre EPN/HCI/PROYECTOI/Prueba2/digits.h5'
CONFIDENCE_THRESHOLD = 0.95
CAPTURE_WIDTH = 640
CAPTURE_HEIGHT = 480
RESIZE_WIDTH = 200
RESIZE_HEIGHT = 200
PREDICTION_FRAMES = 10

# Cargar el modelo
model = load_model(MODEL_PATH)

# Función para realizar la predicción
def prediction(image, model):
    img = cv2.resize(image, (28, 28))
    img = img / 255
    img = img.reshape(1, 28, 28, 1)
    predict = model.predict(img)
    prob = np.amax(predict)
    class_index = np.argmax(predict)
    result = class_index
    if prob < CONFIDENCE_THRESHOLD:
        result = "PON BOLUDO "
        prob = 0
    return result, prob

# Lista para almacenar las últimas predicciones
last_predictions = []

# Función para actualizar la imagen en la interfaz gráfica
def update_image():
    global last_predictions
    _, frame = cap.read()
    frame_copy = frame.copy()

    bbox_size = (70, 70)#60,60
    bbox = [(int(CAPTURE_WIDTH // 2 - bbox_size[0] // 2), int(CAPTURE_HEIGHT // 2 - bbox_size[1] // 2)),
            (int(CAPTURE_WIDTH // 2 + bbox_size[0] // 2), int(CAPTURE_HEIGHT // 2 + bbox_size[1] // 2))]

    img_cropped = frame[bbox[0][1]:bbox[1][1], bbox[0][0]:bbox[1][0]]
    img_gray = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.resize(img_gray, (RESIZE_WIDTH, RESIZE_HEIGHT))

    result, probability = prediction(img_gray, model)
    last_predictions.append(result)
    if len(last_predictions) > PREDICTION_FRAMES:
        last_predictions.pop(0)
    most_common_prediction = Counter(last_predictions).most_common(1)[0][0]

    cv2.putText(frame_copy, f"Prediction: {most_common_prediction}", (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(frame_copy, "Probabilty: {:.2f}".format(probability), (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2, cv2.LINE_AA)

    color = (0, 255, 0) if probability > CONFIDENCE_THRESHOLD else (0, 0, 255)
    cv2.rectangle(frame_copy, bbox[0], bbox[1], color, 3)

    # Convertir la imagen a RGB para mostrarla en la interfaz gráfica
    frame_rgb = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)
    img_tk = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
    video_label.img_tk = img_tk
    video_label.configure(image=img_tk)

    # Llamar a esta función periódicamente para actualizar la imagen
    root.after(10, update_image)

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Handwritten Digit Recognition")
video_label = tk.Label(root)
video_label.pack()

# Inicializar la captura de video
cap = cv2.VideoCapture(2 + cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_HEIGHT)

# Llamar a la función para actualizar la imagen
update_image()

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()

# Cuando se cierra la interfaz, liberar la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows() 