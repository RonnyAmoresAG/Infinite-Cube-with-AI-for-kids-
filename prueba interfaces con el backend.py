# Import Libraries
import re
import nltk
import pandas as pd
import pygame
from pygame import mixer
import os
import string
import random
from PIL import Image
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from collections import Counter
import subprocess
import threading
import time
import traceback

###
from PIL import Image, ImageTk
from collections import Counter

# Configuración ojo
MODEL_PATH = 'C:/Users/Ronny Amores/Desktop/Sexto Semestre EPN/HCI/PROYECTOI/Prueba2/digits.h5'
CONFIDENCE_THRESHOLD = 0.95
CAPTURE_WIDTH = 640
CAPTURE_HEIGHT = 480
RESIZE_WIDTH = 200
RESIZE_HEIGHT = 200
PREDICTION_FRAMES = 15 #10

lock = threading.Lock()
predicted_number = None
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
        result = None
        prob = 0
    return result, prob

# Lista para almacenar las últimas predicciones
last_predictions = []
root = None
video_label = None 
# Función para actualizar la imagen en la interfaz gráfica
def update_image():
    global last_predictions
    global cap
    global predicted_number

    _, frame = cap.read()
    frame_copy = frame.copy()

    bbox_size = (70, 70)
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
    predicted_number = most_common_prediction

    cv2.putText(frame_copy, f"Prediction: {most_common_prediction}", (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(frame_copy, "Probabilty: {:.2f}".format(probability), (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2, cv2.LINE_AA)

    color = (0, 255, 0) if probability > CONFIDENCE_THRESHOLD else (0, 0, 255)
    cv2.rectangle(frame_copy, bbox[0], bbox[1], color, 3)

    # Mostrar la imagen con OpenCV
    cv2.imshow("Handwritten Digit Recognition", frame_copy)
    cv2.waitKey(1)

def run_digit_recognition_gui():
    global cap
    try:
        # Inicializar la captura de video
        cap = cv2.VideoCapture(2 + cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_HEIGHT)

        while predicted_number is None:
            update_image()

    except Exception as e:
        print("Error en run_digit_recognition_gui:")
        print(traceback.format_exc())
    finally:
        cap.release()
        cv2.destroyAllWindows()


####
pygame.init()
win = pygame.display.set_mode((640, 480))
pygame.display.set_caption("CUBERSE ")

mixer.init()

pygame.font.init()
font_1 = pygame.font.SysFont('impact', 55)
font_2 = pygame.font.SysFont('Arial', 25)
font_3 = pygame.font.SysFont('roboto', 30)
font_4 = pygame.font.SysFont('Arial', 20)
font_5 = pygame.font.SysFont('impact', 25)
font_6 = pygame.font.SysFont('impact', 120)
font_7 = pygame.font.SysFont('impact', 90)

clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)

#############
# Main Page #
#############

page = 0

# Background
win.fill((59, 89, 152))  # title
pygame.draw.rect(win, (117, 138, 182), (0, 200, 640, 110))  # word length
pygame.draw.rect(win, (176, 188, 213), (0, 310, 640, 110))  # time limit
pygame.draw.rect(win, (235, 238, 244), (0, 420, 640, 60))  # game start

# Title
win.blit(font_1.render('CUBERSE', False,(242, 242, 242)),(215, 45))
win.blit(font_2.render('HCI 2023A', False, (212, 216, 232)), (350, 135))

# Word Length
word_length = 3
win.blit(font_3.render('CHOOSE DIFFICULTY', False, (212, 216, 232)), (150, 210))

pygame.draw.rect(win, (59, 89, 152), (170, 250, 85, 40))
word_length_button_three = pygame.Rect(170, 250, 85, 40)
win.blit(font_4.render('Easy', False, (255, 255, 255)), (185, 257))

pygame.draw.rect(win, (255, 255, 255), (270, 250, 85, 40))
word_length_button_four = pygame.Rect(270, 250, 85, 40)
win.blit(font_4.render('Medium', False, (59, 89, 152)), (292, 257))

pygame.draw.rect(win, (255, 255, 255), (370, 250, 85, 40))
word_length_button_random = pygame.Rect(370, 250, 85, 40)
win.blit(font_4.render('Hard', False, (59, 89, 152)), (375, 257))

# Time Limit
time_limit = 3
win.blit(font_3.render('CHOOSE TIME LIMIT', False, (212, 216, 232)), (180, 320))

pygame.draw.rect(win, (59, 89, 152), (170, 360, 85, 40))
time_limit_button_three = pygame.Rect(170, 360, 85, 40)
win.blit(font_4.render('Three', False, (255, 255, 255)), (185, 367))

pygame.draw.rect(win, (255, 255, 255), (270, 360, 85, 40))
time_limit_button_five = pygame.Rect(270, 360, 85, 40)
win.blit(font_4.render('Five', False, (59, 89, 152)), (292, 367))

pygame.draw.rect(win, (255, 255, 255), (370, 360, 85, 40))
time_limit_button_ten = pygame.Rect(370, 360, 85, 40)
win.blit(font_4.render('Eight', False, (59, 89, 152)), (390, 367))
         
# Game Start
win.blit(font_5.render('GAME Start !!!', False, (59, 89, 152)), (247, 433))
game_start_button = pygame.Rect(0, 420, 640, 60)

# Action
def word_length_button_three_pressed():
    pygame.draw.rect(win, (117, 138, 182), (0, 200, 640, 110))
    win.blit(font_3.render('CHOOSE DIFFICULTY', False, (212, 216, 232)), (150, 210))
    pygame.draw.rect(win, (59, 89, 152), (170, 250, 85, 40))
    win.blit(font_4.render('Easy', False, (255, 255, 255)), (185, 257))
    pygame.draw.rect(win, (255, 255, 255), (270, 250, 85, 40))
    win.blit(font_4.render('Medium', False, (59, 89, 152)), (292, 257))
    pygame.draw.rect(win, (255, 255, 255), (370, 250, 85, 40))
    win.blit(font_4.render('Hard', False, (59, 89, 152)), (375, 257))


def word_length_button_four_pressed():
    pygame.draw.rect(win, (117, 138, 182), (0, 200, 640, 110))
    win.blit(font_3.render('CHOOSE DIFFICULTY', False, (212, 216, 232)), (150, 210))
    pygame.draw.rect(win, (255, 255, 255), (170, 250, 85, 40))
    win.blit(font_4.render('Easy', False, (59, 89, 152)), (185, 257))
    pygame.draw.rect(win, (59, 89, 152), (270, 250, 85, 40))
    win.blit(font_4.render('Medium', False, (255, 255, 255)), (292, 257))
    pygame.draw.rect(win, (255, 255, 255), (370, 250, 85, 40))
    win.blit(font_4.render('Hard', False, (59, 89, 152)), (375, 257))


def word_length_button_random_pressed():
    pygame.draw.rect(win, (117, 138, 182), (0, 200, 640, 110))
    win.blit(font_3.render('CHOOSE DIFFICULTY', False, (212, 216, 232)), (150, 210))
    pygame.draw.rect(win, (255, 255, 255), (170, 250, 85, 40))
    win.blit(font_4.render('Easy', False, (59, 89, 152)), (185, 257))
    pygame.draw.rect(win, (255, 255, 255), (270, 250, 85, 40))
    win.blit(font_4.render('Medium', False, (59, 89, 152)), (292, 257))
    pygame.draw.rect(win, (59, 89, 152), (370, 250, 85, 40))
    win.blit(font_4.render('Hard', False, (255, 255, 255)), (375, 257))


def time_limit_button_three_pressed():
    pygame.draw.rect(win, (176, 188, 213), (0, 310, 640, 110))
    win.blit(font_3.render('CHOOSE TIME LIMIT', False, (212, 216, 232)), (180, 320))
    pygame.draw.rect(win, (59, 89, 152), (170, 360, 85, 40))
    win.blit(font_4.render('Three', False, (255, 255, 255)), (185, 367))
    pygame.draw.rect(win, (255, 255, 255), (270, 360, 85, 40))
    win.blit(font_4.render('Five', False, (59, 89, 152)), (292, 367))
    pygame.draw.rect(win, (255, 255, 255), (370, 360, 85, 40))
    win.blit(font_4.render('Eight', False, (59, 89, 152)), (390, 367))


def time_limit_button_five_pressed():
    pygame.draw.rect(win, (176, 188, 213), (0, 310, 640, 110))
    win.blit(font_3.render('CHOOSE TIME LIMIT', False, (212, 216, 232)), (180, 320))
    pygame.draw.rect(win, (255, 255, 255), (170, 360, 85, 40))
    win.blit(font_4.render('Three', False, (59, 89, 152)), (185, 367))
    pygame.draw.rect(win, (59, 89, 152), (270, 360, 85, 40))
    win.blit(font_4.render('Five', False, (255, 255, 255)), (292, 367))
    pygame.draw.rect(win, (255, 255, 255), (370, 360, 85, 40))
    win.blit(font_4.render('Eight', False, (59, 89, 152)), (390, 367))


def time_limit_button_eight_pressed():
    pygame.draw.rect(win, (176, 188, 213), (0, 310, 640, 110))
    win.blit(font_3.render('CHOOSE TIME LIMIT', False, (212, 216, 232)), (180, 320))
    pygame.draw.rect(win, (255, 255, 255), (170, 360, 85, 40))
    win.blit(font_4.render('Three', False, (59, 89, 152)), (185, 367))
    pygame.draw.rect(win, (255, 255, 255), (270, 360, 85, 40))
    win.blit(font_4.render('Five', False, (59, 89, 152)), (292, 367))
    pygame.draw.rect(win, (59, 89, 152), (370, 360, 85, 40))
    win.blit(font_4.render('Eight', False, (255, 255, 255)), (390, 367))


##############
# Game Start #
##############

# Game Set Up

life = 3
numero_aleatorio = None


def adj_en_char(en_char, en_char_x):
    
    return en_char_x


def adj_en_char2(en_char, en_char_x):
    
    return en_char_x


def correct(): 
    win.fill((59, 89, 152))
    win.blit(font_1.render('CORRECTO', False, (242, 242, 242)), (215, 55))
    win.blit(font_1.render('Lo hiciste genial :D', False, (242, 242, 242)), (145, 120))

def incorrect():
    win.fill((59, 89, 152))
    win.blit(font_1.render('INCORRECTO', False, (242, 242, 242)), (215, 55))
    win.blit(font_1.render('Perdiste una vida :C', False, (242, 242, 242)), (145, 120))

    

def show_card_three():
    global numero_aleatorio
    win.fill((59, 89, 152))
    win.blit(font_1.render('Time', False, (242, 242, 242)), (215, 55))
    win.blit(font_1.render('Countdown', False, (242, 242, 242)), (145, 120))
    win.blit(font_2.render('Remember the number below :', False, (212, 216, 232)), (155, 235))
    pygame.draw.rect(win, (242, 242, 242), (280, 280, 100, 160))
    pygame.draw.rect(win, (176, 188, 213), (270, 270, 100, 160))
    # Genera un número aleatorio
    if numero_aleatorio is None:
        numero_aleatorio = str(random.randint(1, 9))

    en_char_1_x = 290
    en_char_1_x = adj_en_char(numero_aleatorio, en_char_1_x)
    win.blit(font_6.render(numero_aleatorio, False, (255, 255, 255)), (en_char_1_x, 270))
    return numero_aleatorio

##
## page 2
# 

confirm_button = pygame.Rect(200, 415, 110, 40)
reset_button = pygame.Rect(330, 415, 110, 40)

def three_choose_from_six():
    global numero_aleatorio
    global predicted_number
    
    
    win.fill((59, 89, 152))
    win.blit(font_2.render('Please choose the number below -interfaz :', False, (212, 216, 232)), (140, 50))
    
    threading.Thread(target=run_digit_recognition_gui).start()
    
    #subprocess.Popen(["python", "C:/Users/Ronny Amores/Desktop/Sexto Semestre EPN/HCI/PROYECTOI/Proyeto_Final_HCI/Infinite-Cube-with-AI-for-kids-/PRUEBAS_NUCLEO_FINAL.py"])
    
    pygame.draw.rect(win, (148, 148, 148), (270, 85, 100, 160))
    pygame.draw.rect(win, (242, 242, 242), (235, 275, 80, 120))
    pygame.draw.rect(win, (176, 188, 213), (230, 270, 80, 120))
    
    while predicted_number is None:
        time.sleep(0.1)
    en_char_2_x = 247
    if predicted_number is not None:
        en_char_2_x = adj_en_char2(str(predicted_number), en_char_2_x)
        win.blit(font_7.render(str(predicted_number), False, (255, 255, 255)), (en_char_2_x, 270))
    else:
        win.blit(font_7.render("Waiting...", False, (255, 255, 255)), (en_char_2_x, 270))

    pygame.draw.rect(win, (255, 255, 255), (200, 415, 110, 40))
    win.blit(font_4.render('Confirm', False, (59, 89, 152)), (220, 422))
    pygame.draw.rect(win, (255, 255, 255), (330, 415, 110, 40))
    win.blit(font_4.render('Reset', False, (59, 89, 152)), (360, 422))
    win.blit(font_2.render('Mark : '+str(mark), False, (212, 216, 232)), (510, 10))
    win.blit(font_2.render('Life : '+str(life), False, (212, 216, 232)), (20, 10))   



####
def reset_detection():
    try:
        global predicted_number
        global cap
        
        # Libera la cámara
        cap.release()
        # Pequeño retraso para asegurarnos de que la cámara se libere correctamente
        time.sleep(1)
        
        # Vuelve a inicializar la cámara
        cap = cv2.VideoCapture(2 + cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_HEIGHT)
        
        # Reinicia la predicción
        with lock:
            predicted_number = None
        
        # Muestra nuevamente la ventana con el número a predecir
        numero_aleatorio = show_card_three()
        three_choose_from_six()
        pygame.display.update()  # Actualiza la pantalla
    except Exception as e:
        print("Error en reset_detection:")
        print(traceback.format_exc())




def word_one_button_pressed():
    pygame.draw.rect(win, (100, 100, 100), (30, 270, 80, 120))

def word_two_button_pressed():
    pygame.draw.rect(win, (100, 100, 100), (130, 270, 80, 120))

def word_three_button_pressed():
    pygame.draw.rect(win, (100, 100, 100), (230, 270, 80, 120))

def word_four_button_pressed():
    pygame.draw.rect(win, (100, 100, 100), (330, 270, 80, 120))

def word_five_button_pressed():
    pygame.draw.rect(win, (100, 100, 100), (430, 270, 80, 120))

def word_six_button_pressed():
    pygame.draw.rect(win, (100, 100, 100), (530, 270, 80, 120))

correct_ans = [1,2,3]

next_button = pygame.Rect(0, 420, 640, 60)
music_three_button = pygame.Rect(60, 314, 80, 80)
music_four_button = pygame.Rect(30, 314, 80, 80)
restart_button = pygame.Rect(200, 265, 110, 40)
quit_button = pygame.Rect(330, 265, 110, 40)

def game_over():
    win.fill((59, 89, 152))
    win.blit(font_6.render('Game Over', False, (212, 216, 232)), (50, 10))
    win.blit(font_1.render('Total Mark', False, (212, 216, 232)), (130, 160))
    win.blit(font_1.render(str(mark), False, (212, 216, 232)), (430, 160))
    pygame.draw.rect(win, (255, 255, 255), (200, 265, 110, 40))
    win.blit(font_4.render('Restart', False, (59, 89, 152)), (220, 272))
    pygame.draw.rect(win, (255, 255, 255), (330, 265, 110, 40))
    win.blit(font_4.render('Quit', False, (59, 89, 152)), (365, 272))

def restart():
    # Background
    win.fill((59, 89, 152))  # title
    pygame.draw.rect(win, (117, 138, 182), (0, 200, 640, 110))  # word length
    pygame.draw.rect(win, (176, 188, 213), (0, 310, 640, 110))  # time limit
    pygame.draw.rect(win, (235, 238, 244), (0, 420, 640, 60))  # game start
    # Title
    win.blit(font_1.render('CUBERSE', False, (242, 242, 242)), (215, 45))
    win.blit(font_2.render('HCI 2023A', False, (212, 216, 232)), (350, 135))
    # Word Length
    win.blit(font_3.render('CHOOSE DIFFICULTY', False, (212, 216, 232)), (150, 210))
    pygame.draw.rect(win, (59, 89, 152), (170, 250, 85, 40))
    win.blit(font_4.render('Easy', False, (255, 255, 255)), (185, 257))
    pygame.draw.rect(win, (255, 255, 255), (270, 250, 85, 40))
    win.blit(font_4.render('Medium', False, (59, 89, 152)), (292, 257))
    pygame.draw.rect(win, (255, 255, 255), (370, 250, 85, 40))
    win.blit(font_4.render('Hard', False, (59, 89, 152)), (375, 257))

    # Time Limit
    win.blit(font_3.render('CHOOSE TIME LIMIT', False, (212, 216, 232)), (180, 320))
    pygame.draw.rect(win, (59, 89, 152), (170, 360, 85, 40))
    win.blit(font_4.render('Three', False, (255, 255, 255)), (185, 367))
    pygame.draw.rect(win, (255, 255, 255), (270, 360, 85, 40))
    win.blit(font_4.render('Five', False, (59, 89, 152)), (292, 367))
    pygame.draw.rect(win, (255, 255, 255), (370, 360, 85, 40))
    win.blit(font_4.render('Eight', False, (59, 89, 152)), (390, 367))

    # Game Start
    win.blit(font_5.render('Game Start !!!', False, (59, 89, 152)), (247, 433))
#---------------------------------

run = True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if life == 0:
            page = 4
            game_over()

        if page == 1:
            show_card_three()  # Mueve esta línea aquí
            if event.type == pygame.USEREVENT:
                time_count -= 1
            time_text = int(time_count)
            if time_text > time_limit:
                time_text = time_limit
            pygame.draw.rect(win, (59, 89, 152), (420, 50, 100, 160))
            win.blit(font_6.render(str(time_text), True, (242, 242, 242)), (440, 50))
            pygame.display.flip()
            clock.tick(60)
            if time_count <= 0:
                page = 2
                if len(correct_ans) == 3:
                    three_choose_from_six()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if (word_length_button_three.collidepoint(mouse_pos)) & (page == 0):
                word_length = 3
                word_length_button_three_pressed()
            if (word_length_button_four.collidepoint(mouse_pos)) & (page == 0):
                word_length = 4
                word_length_button_four_pressed()
            if (word_length_button_random.collidepoint(mouse_pos)) & (page == 0):
                word_length = 5
                word_length_button_random_pressed()

            if (time_limit_button_three.collidepoint(mouse_pos)) & (page == 0):
                time_limit = 3
                time_limit_button_three_pressed()
            if (time_limit_button_five.collidepoint(mouse_pos)) & (page == 0):
                time_limit = 5
                time_limit_button_five_pressed()
            if (time_limit_button_ten.collidepoint(mouse_pos)) & (page == 0):
                time_limit = 8
                time_limit_button_eight_pressed()

            if (game_start_button.collidepoint(mouse_pos)) & (page == 0):       
                page = 1
                time_count = time_limit + 1
                if len(correct_ans) == 3:
                    show_card_three()
                idx = 0
                mark = 0

            if (confirm_button.collidepoint(mouse_pos)) & (page == 2):
                    if str(predicted_number) == numero_aleatorio:
                        mark += 10
                        correct()
                        pygame.display.update()
                        pygame.time.wait(2000)  
                    else:
                        life -= 1
                        incorrect()
                        pygame.display.update()
                        pygame.time.wait(2000)  # Mostrar la pantalla "incorrect" durante 2 segundos

                    page = 1
                    time_count = time_limit + 2
                    numero_aleatorio = None
                    predicted_number = None
                    pygame.display.update()
                        
            if (reset_button.collidepoint(mouse_pos)) & (page == 2):
                reset_detection()
                
               
            if (restart_button.collidepoint(mouse_pos)) & (page == 4):
                page = 0
                life = 3
                word_length = 3
                time_limit = 3
                restart()

            if (quit_button.collidepoint(mouse_pos)) & (page == 4):
                run = False

    pygame.display.update()
pygame.quit()
