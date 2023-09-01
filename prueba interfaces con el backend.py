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

confirm_button = pygame.Rect(200, 415, 110, 40)
reset_button = pygame.Rect(330, 415, 110, 40)
confirm_button = pygame.Rect(200, 415, 110, 40)
reset_button = pygame.Rect(330, 415, 110, 40)

## page 2 
def three_choose_from_six():
    global numero_aleatorio
    win.fill((59, 89, 152))
    win.blit(font_2.render('Please choose the number below -interfaz :', False, (212, 216, 232)), (140, 50))
    
    
    subprocess.Popen(["python", "C:/Users/Ronny Amores/Desktop/Sexto Semestre EPN/HCI/PROYECTOI/Proyeto_Final_HCI/Infinite-Cube-with-AI-for-kids-/PRUEBAS_NUCLEO_FINAL.py"])

    pygame.draw.rect(win, (148, 148, 148), (270, 85, 100, 160))
    pygame.draw.rect(win, (242, 242, 242), (235, 275, 80, 120))
    pygame.draw.rect(win, (176, 188, 213), (230, 270, 80, 120))
    
    en_char_2_x = 247
    en_char_2_x = adj_en_char2(numero_aleatorio, en_char_2_x)
    win.blit(font_7.render(numero_aleatorio, False, (255, 255, 255)), (en_char_2_x, 270))

    pygame.draw.rect(win, (255, 255, 255), (200, 415, 110, 40))
    win.blit(font_4.render('Confirm', False, (59, 89, 152)), (220, 422))
    pygame.draw.rect(win, (255, 255, 255), (330, 415, 110, 40))
    win.blit(font_4.render('Reset', False, (59, 89, 152)), (360, 422))
    win.blit(font_2.render('Mark : '+str(mark), False, (212, 216, 232)), (510, 10))
    win.blit(font_2.render('Life : '+str(life), False, (212, 216, 232)), (20, 10))   


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
                position = 0
                choose_ans = []
                if len(correct_ans) == 3:
                    numero_aleatorio = show_card_three()
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
                    if choose_ans == correct_ans:
                        mark += 10
                        page = 3
                        delay = 1
                        correct_match()
                    else:
                        life -= 1
                        word_one_idx = 0
                        word_two_idx = 0
                        word_three_idx = 0
                        word_four_idx = 0
                        word_five_idx = 0
                        word_six_idx = 0
                        position = 0
                        choose_ans = []
                        if len(correct_ans) == 3:
                           numero_aleatorio = show_card_three()
                           three_choose_from_six(numero_aleatorio)
                        
            if (reset_button.collidepoint(mouse_pos)) & (page == 2):
                if len(correct_ans) == 3:
                    numero_aleatorio = show_card_three()
                    three_choose_from_six(numero_aleatorio)
               
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
