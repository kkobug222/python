from tkinter import *
import tkinter as tk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import os
import pygame
import time
import datetime
import random
import math


font_path = 'C://Windows//Fonts//gulim.ttc'
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)


window = Tk()
window.title("집중호우 예측 프로그램")
window.geometry("1100x700+250+50")
window.iconbitmap('water.ico')

window.resizable(False, False)

df = pd.read_csv('data.csv', encoding='euc-kr')
df.set_index('측정 연도', inplace=True)
    

arr = df['지역']
result = []

for value in arr:
    if value not in result:
        result.append(value)


slocation = 0

def predict_paju():
    global slocation
    slocation = 0
    predict()
    
def predict_icheon():
    global slocation
    slocation = 1
    predict()
    
def predict_yang():
    global slocation
    slocation = 2
    predict()
    
def predict_suwon():
    global slocation
    slocation = 3
    predict()
    
def predict_dongdu():
    global slocation
    slocation = 4
    predict()


# ent = Entry(window, width=30)
# ent.place(x=410, y=600)
# ent.insert(0, "여기 입력")




def predict():
    
    global df
    global location
    global arr
    global view
    global outcome
    global text1
    global text2
    global text3
    global state
    # global last_year
    # global what_year
    
    if slocation == 0:
        location = '파주'
    elif slocation == 1:
        location = '이천'
    elif slocation == 2:
        location = '양평'
    elif slocation == 3:
        location = '수원'
    else:
        location = '동두천'
    
    # plt.figure(figsize=(2, 5))
    df = df[df["지역"] == location]
    last_water_amount = df.iloc[-1, -1]

    # what_year = Label(window, bg='white', text="몇년도 강수량까지 예측하실건지 입력해주세요. : ")
    # what_year.place(x=410, y=580)
    
    #years_to_predict = range(2024, last_year)
    years_to_predict = range(2024, 2051)
    
    if location == '파주':
        np.random.seed(1)
    elif location == '이천':
        np.random.seed(2)
    elif location == '양평':
        np.random.seed(3)
    elif location == '수원':
        np.random.seed(4)
    else:
        np.random.seed(5)
        
    
    features = np.random.randint(500, 1200, size=(len(years_to_predict), 2))
    predicted_rain = last_water_amount + 0.0042 * features[:, 0] + 0.0017 * features[:, 1]
    
    for year, rain  in zip(range(2024, 2051), predicted_rain):
        print(f"예측된 {location} {year}년의 강수량: {rain: .2f}mm")
    
    df = pd.DataFrame({"측정 연도": years_to_predict, "강수량": predicted_rain})
    df.set_index('측정 연도', inplace=True)

    plt.figure(figsize=(6.5, 5))
    df["강수량"].plot(color="skyblue", alpha=0.5, marker='o', markerfacecolor='blue', markersize=6)
    plt.xticks(np.arange(2022, 2051).tolist(), rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.xlabel('측정 연도', labelpad=10, loc='right', color='blue', size=10)
    #plt.ylabel('강수량', labelpad=10, loc='top', rotation=360, color='red', size=12)
    plt.grid(alpha=0.3)
    plt.title(location, size=18)
    plt.legend()
    plt.tight_layout()
    plt.savefig('view.png')
    #plt.show()
    
    view = PhotoImage(file="view.png")
    outcome = Label(window, image=view)
    outcome.place(x=400, y=47, width=656, height=491)

    rainMaxYear = df.index[df['강수량']== df['강수량'].max()].tolist()
    rainMax = round(df['강수량'].max(), 2)
    rainMean = round(df['강수량'].mean(), 2)
    print('\n')
    print(f'[2022년 ~ 2050년] {location}의 최고 강수량과 평균 강수량')
    print(f'{location}의 최고 강수량은 {rainMaxYear[0]}년도 {rainMax}mm 입니다.')
    print(f'{location}의 평균 강수량은 {rainMean}mm 입니다.')

    print('\n')
    print(f'{location}의 평균 강수량이 {rainMean}mm 일 때')
    if rainMean >= 50:
        state = '[집중호우]'
    elif rainMean >= 30:
        state = '[폭우]'
    elif rainMean >= 10:
        state = '[굵은비]'
    else:
        state = '[가랑비]'
        
        
    text1 = Label(window, bg='white', text=f'{location}의 최고 강수량은 {rainMaxYear[0]}년도 {rainMax}mm 입니다.       ')
    text2 = Label(window, bg='white', text=f'{location}의 평균 강수량은 {rainMean}mm 입니다.                 ')
    text3 = Label(window, bg='white', text=f'{location}의 평균 강수량이 {rainMean}mm 일 때 {state}상태입니다.          ')
    text1.place(x=410, y=580)
    text2.place(x=410, y=600)
    text3.place(x=410, y=620)
    
    df = pd.read_csv('data.csv', encoding='euc-kr')
    df.set_index('측정 연도', inplace=True)    


def game():
    
    global character_height
    global to_x 
    global to_y
    global enemy_rect
    global game_font
    global start_ticks

    pygame.init() # 초기화 (반드시 필요)


    # 화면 크기 설정
    screen_width = 1050
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))


    # 화면 타이틀 설정
    pygame.display.set_caption("우중전투")


    # FPS
    clock = pygame.time.Clock()


    # 배경 이미지 불러오기
    background = pygame.image.load("game_background.png")
    title = pygame.image.load("start.png")
    game_end_img = pygame.image.load("clear.png")


    #점수 불러오기
    score = 0
    WHITE = (255,255,255)
    BLACK = (0, 0, 0)
    font_01 = pygame.font.SysFont("새굴림", 35, True, False)



    # 캐릭터 이미지 불러오기
    character = pygame.image.load("front.png")
    character_info = 'front'
    character_size = character.get_rect().size # 이미지의 크기를 구해옴
    character_width = character_size[0] # 캐릭터의 가로 크기
    character_height = character_size[1] # 캐릭터의 세로 크기
    character_x_pos = (screen_width / 1.8) - (character_width / 9)
    character_y_pos = screen_height / 2.7


    # 이동할 좌표
    to_x = 0
    to_y = 0


    # 이동 속도
    character_speed = 0.6


    # 적 enemy 캐릭터
    enemy = pygame.image.load("enemy.png")
    enemy_rect = enemy.get_rect()
    enemy_size = enemy.get_rect().size # 이미지의 크기를 구해옴
    enemy_width = enemy_size[0] # 캐릭터의 가로 크기
    enemy_height = enemy_size[1] # 캐릭터의 세로 크기
    enemy_x_pos = (screen_width / 1.5) - (enemy_width / 2) # 화면 가로의 절반 크기에 해당하는 곳에 위치 (가로)
    enemy_y_pos = (screen_height / 1.3) - (enemy_height / 2) # 화면 세로 크기 가장 아래에 해당하는 곳에 위치 (세로)

    enemies = []
    enemies_speed = 6

    # 적 소환
    spawn_timer = 0
    next_time_to_spawn = random.randint(2000, 5000)


    # 폰트 정의
    game_font = pygame.font.Font(None, 40) # 폰트 객체 생성 (폰트, 크기)


    # 시작 시간
    start_ticks = pygame.time.get_ticks() # 현재 tick 을 받아옴
    

    character_to_x = 0
    character_to_y = 0


    # 캐릭터 이동 속도
    character_speed = 8
    
    
    # 무기 만들기
    L_bullet = pygame.image.load("L_bullet.png")
    R_bullet = pygame.image.load("R_bullet.png")
    U_bullet = pygame.image.load("U_bullet.png")
    D_bullet = pygame.image.load("D_bullet.png")
    bullet_size = L_bullet.get_rect().size
    bullet_size = R_bullet.get_rect().size
    bullet_size = U_bullet.get_rect().size
    bullet_size = D_bullet.get_rect().size
    bullet_width = bullet_size[0]

    # 무기는 한 번에 여러 발 발사 가능
    left_bullets = []
    right_bullets = []
    down_bullets = []
    up_bullets = []

    # 무기 이동 속도
    bullet_speed = 15

    # 무기 발사 속도 (초)
    reload_speed = 0.2
    last_shot = time.time()

    game_over_img = pygame.image.load('gameover.png')

    running = True
    SHOW_TITLE = True
    GAME_OVER = False
    GAME_END = False


    while running:
        global dt
        
        dt = clock.tick(30)
        
        # 2. 이벤트 처리 (키보드, 마우스 등)
        
        if GAME_OVER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.blit(game_over_img, (0, 0))
            pygame.display.update()
            continue

        if GAME_END:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.blit(game_end_img, (0, 0))
            text_score = font_01.render("score : " + str(score), True, BLACK)
            screen.blit(text_score, [70, 520])
            running_time = font_01.render("time : " + f"{times} sec", True, BLACK)
            screen.blit(running_time, [70, 570])
            pygame.display.update()
            continue

        
        while SHOW_TITLE & running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                screen.blit(title, (0, 0))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start = time.time()
                        SHOW_TITLE = False
                pygame.display.update()
                
        clock.get_rawtime()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: # 캐릭터를 왼쪽으로
                    character_to_x -= character_speed
                    character = pygame.image.load("left.png")
                    character_info = 'left'
                elif event.key == pygame.K_RIGHT: # 캐릭터를 오른쪽으로
                    character_to_x += character_speed
                    character = pygame.image.load("right.png")
                    character_info = 'right'
                elif event.key == pygame.K_UP: # 캐릭터를 위쪽으로
                    character_to_y -= character_speed
                    character = pygame.image.load("back.png")
                    character_info = 'up'
                elif event.key == pygame.K_DOWN: # 캐릭터를 아래쪽으로
                    character_to_y += character_speed
                    character = pygame.image.load("front.png")
                    character_info = 'down'
                elif event.key == pygame.K_SPACE: # 무기 발사
                    if time.time() - reload_speed > last_shot:
                        
                        if character_info == 'left':
                            bullet_x_pos = character_x_pos + (character_width / 9) - (bullet_width / 1.3)
                            bullet_y_pos = character_y_pos + (character_width / 1.3)
                        
                            character = pygame.image.load("gun_left.png")
                            left_bullets.append([bullet_x_pos, bullet_y_pos])
                            
                        if character_info == 'right':
                            bullet_x_pos = character_x_pos + (character_width / 1.4) - (bullet_width / 2)
                            bullet_y_pos = character_y_pos + (character_width / 1.3)
                        
                            character = pygame.image.load("gun_right.png")
                            right_bullets.append([bullet_x_pos, bullet_y_pos])
                            
                        if character_info == 'up':
                            bullet_x_pos = character_x_pos + (character_width / 2) - (bullet_width / 2)
                            bullet_y_pos = character_y_pos + (character_width / 1.3)
                            
                            character = pygame.image.load("back_attack.png")
                            up_bullets.append([bullet_x_pos, bullet_y_pos])
                            
                        if character_info == 'down':
                            bullet_x_pos = character_x_pos + (character_width / 1.3) - (bullet_width / 2)
                            bullet_y_pos = character_y_pos + (character_width / 1.5)
                            
                            character = pygame.image.load("front_attack.png")
                            down_bullets.append([bullet_x_pos, bullet_y_pos])
                        
                        last_shot = time.time()
        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    character_to_x = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    character_to_y = 0


        # 3. 게임 캐릭터 위치 정의
        character_x_pos += character_to_x

        if character_x_pos < 0:
            character_x_pos = 0
        elif character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width

        character_y_pos += character_to_y

        if character_y_pos < 0:
            character_y_pos = 0
        elif character_y_pos > screen_width - character_width:
            character_y_pos = screen_width - character_width



        # 무기 위치 조정
        # 100, 200 -> 180, 160, 140, ...
        # 500, 200 -> 180, 160, 140, ...
        right_bullets = [ [w[0] + bullet_speed, w[1]] for w in right_bullets] # 무기 위치를 오른쪽으로
        left_bullets = [ [w[0] - bullet_speed, w[1]] for w in left_bullets] # 무기 위치를 왼쪽으로
        up_bullets = [ [w[0], w[1] - bullet_speed] for w in up_bullets]
        down_bullets = [ [w[0], w[1] + bullet_speed] for w in down_bullets]

        # 천장에 닿은 무기 없애기
        right_bullets = [ [w[0], w[1]] for w in right_bullets if w[1] > 0]
        left_bullets = [ [w[0], w[1]] for w in left_bullets if w[1] > 0]
        up_bullets = [ [w[0], w[1]] for w in up_bullets if w[1] > 0]
        down_bullets = [ [w[0], w[1]] for w in down_bullets if w[1] > 0] 
    
        # 적 소환
        spawn_timer += clock.get_rawtime()
        if spawn_timer > next_time_to_spawn:
            enemies.append([(screen_width / 0.5) - (enemy_width / 2), (screen_height / 1.8) - (enemy_height / 2), math.radians(90)])
            enemies.append([(screen_width / 6.0) - (enemy_width / 2), (screen_height / 2.2) - (enemy_height / 2), math.radians(180)])
            enemies.append([(screen_width / 1.8) - (enemy_width / 2), (screen_height / 9.0) - (enemy_height / 2), math.radians(270)])
            enemies.append([(screen_width / 1.5) - (enemy_width / 2), (screen_height / 0.5) - (enemy_height / 2), math.radians(0)])
            spawn_timer = 0
            next_time_to_spawn = random.randint(1000, 2000)
        
        # 적 이동
        enemies = [ [w[0] + enemies_speed * math.cos(w[2]), w[1] + enemies_speed * math.sin(w[2]), w[2]] for w in enemies ]
        
        # 적 충돌
        n_enemies = []
        for w in enemies:
            mark_as_delete = False
            r1 = pygame.Rect(w[0], w[1], enemy_size[0], enemy_size[1])
            for i, b in enumerate(left_bullets):
                r2 = pygame.Rect(b[0], b[1], bullet_size[0], bullet_size[1])
                if r2.colliderect(r1):
                    del left_bullets[i]
                    mark_as_delete = True
                    score +=10
                    break
            for i, b in enumerate(right_bullets):
                r2 = pygame.Rect(b[0], b[1], bullet_size[0], bullet_size[1])
                if r2.colliderect(r1):
                    del right_bullets[i]
                    mark_as_delete = True
                    score +=10
                    break
                # print(r1, r2)
            for i, b in enumerate(up_bullets):
                r2 = pygame.Rect(b[0], b[1], bullet_size[0], bullet_size[1])
                if r2.colliderect(r1):
                    del up_bullets[i]
                    mark_as_delete = True
                    score +=10
                    break
            for i, b in enumerate(down_bullets):
                r2 = pygame.Rect(b[0], b[1], bullet_size[0], bullet_size[1])
                if r2.colliderect(r1):
                    del down_bullets[i]
                    mark_as_delete = True
                    score +=10
                    break
            if not mark_as_delete:
                n_enemies.append(w)
        
        enemies = n_enemies
        del n_enemies

        enemies = [[w[0], w[1], math.atan2((character_y_pos-w[1]),(character_x_pos-w[0]))] for w in enemies]

        # 사망
        for w in enemies:
            r1 = pygame.Rect(w[0], w[1], enemy_size[0], enemy_size[1])
            r2 = pygame.Rect(character_x_pos, character_y_pos, character_size[0] - 2.5, character_size[1])
            if r1.colliderect(r2):
                GAME_OVER = True
                break

        #엔딩 - 해피엔딩
        if score >= 200 :
            global short
            
            sec = time.time()-start
            times = str(datetime.timedelta(seconds=sec)) # 걸린시간 보기좋게 바꾸기
            short = times.split(".")[0] # 초 단위 까지만
            GAME_END = True
        
        # 5. 화면에 그리기
        screen.blit(background, (0, 0)) 
        text_score = font_01.render("Score : " + str(score), True, WHITE)
        screen.blit(text_score, [15, 15])

    
        for bullet_x_pos, bullet_y_pos in left_bullets:
            screen.blit(L_bullet, (bullet_x_pos, bullet_y_pos))
            
        for bullet_x_pos, bullet_y_pos in right_bullets:
            screen.blit(R_bullet, (bullet_x_pos, bullet_y_pos))
            
        for bullet_x_pos, bullet_y_pos in up_bullets:
            screen.blit(U_bullet, (bullet_x_pos, bullet_y_pos))
        


        #screen.blit(stage, (0, screen_height - stage_height))
        screen.blit(character, (character_x_pos, character_y_pos))

        for bullet_x_pos, bullet_y_pos in down_bullets:
            screen.blit(D_bullet, (bullet_x_pos, bullet_y_pos))

        
        for enemy_x_pos, enemy_y_pos, angle in enemies:
            screen.blit(enemy, (enemy_x_pos, enemy_y_pos))
        pygame.display.update()

    pygame.quit()


def quiz():
    guhyeon = Label(window, bg='white', text='구현 전입니다.          ')
    guhyeon.place(x=410, y=580)
    # print("구현 전입니다.")


def outcome_disappear():
    outcome.destroy()
    text1.destroy()
    text2.destroy()
    text3.destroy()
    intro_content.destroy()

def pre_prediction():
    big_disable_button()
    small_enable_button()
    
def intro():
    intro_content.place(x=400, y=47, width=656, height=491)

def quiz():
    global quiz_stage
    global number
    
    button1.place(x=430, y=450)
    button2.place(x=500, y=450) 
    button3.place(x=570, y=450)
    button4.place(x=640, y=450)
    
    background.config(image=quiz1)
    next.place(x=950, y=450)
    next_disable()

    input()

    if number ==4:
        success = Label(window, bg='white', text='정답입니다!          ')
        success.place(x=410, y=580)
        quiz_stage = 2
        next_enable()
    else:
        fail = Label(window, bg='white', text='오답입니다.          ')
        fail.place(x=410, y=600)
    
        
        
#     # quiz1.place(x=400, y=47, width=656, height=491)  

   
   
def one():
    global number
    number = 1
def two():
    global number
    number = 2
def three():
    global number
    number = 3
def four():
    global number
    number = 4


def next_disable():
    next.config(state=tk.DISABLED)
    
def next_enable():
    next.config(state=tk.NORMAL)

def confirm():
    big_enable_button()
    small_disable_button()
    outcome_disappear()


def next():
    pass

# def next():
#     if quiz_stage == 2:
#         background.config(image=quiz2)
#     elif quiz_stage == 3:
#         background.config(image=quiz3)
#     elif quiz_stage == 4:
#         background.config(image=quiz4)
#     elif quiz_stage == 5:
#         background.config(image=quiz5)
#     elif quiz_stage == 6:
#         background.config(image=quiz6)
        
#     quiz_stage =+ 1
        

def big_disable_button():
    prediction.config(state=tk.DISABLED)
def big_enable_button():
    prediction.config(state=tk.NORMAL)
    
def small_disable_button():
    paju.config(state=tk.DISABLED)
    icheon.config(state=tk.DISABLED)
    yang.config(state=tk.DISABLED)
    suwon.config(state=tk.DISABLED)
    dongdu.config(state=tk.DISABLED)
def small_enable_button():
    paju.config(state=tk.NORMAL)
    icheon.config(state=tk.NORMAL)
    yang.config(state=tk.NORMAL)
    suwon.config(state=tk.NORMAL)
    dongdu.config(state=tk.NORMAL)



    
#배경버튼
back = PhotoImage(file="background.png")
background = Label(window, image=back)
background.pack()

background.place(relx=.5, rely=.5, anchor="center")
background.lower()


photo_button1 = PhotoImage(file="button1.png")
button1 = Button(window, image=photo_button1, command=one, relief=SOLID)
photo_button2 = PhotoImage(file="button2.png")
button2 = Button(window, image=photo_button2, command=two, relief=SOLID)    
photo_button3 = PhotoImage(file="button3.png")
button3 = Button(window, image=photo_button3, command=three, relief=SOLID)
photo_button4 = PhotoImage(file="button4.png")
button4 = Button(window, image=photo_button4, command=four, relief=SOLID)

#큰버튼
photo_prediction = PhotoImage(file="predict.png")
prediction = Button(window, image=photo_prediction, command=pre_prediction, relief=SOLID)
prediction.place(x=40, y=320) 

photo_intro = PhotoImage(file="intro.png")
intro = Button(window, image=photo_intro, command=intro, relief=SOLID)
intro.place(x=40, y=230) 

photo_game = PhotoImage(file="game.png")
button_game = Button(window, image=photo_game, command=game, relief=SOLID)
button_game.place(x=40, y=500)

photo_intro_content = PhotoImage(file="intro_content.png")
intro_content = Label(window, image=photo_intro_content)

photo_okay = PhotoImage(file="okay.png")
okay = Button(window, image=photo_okay, command=confirm, relief=SOLID)
okay.place(x=920, y=578)

photo_quiz = PhotoImage(file="quiz.png")
quiz = Button(window, image=photo_quiz, command=quiz, relief=SOLID)
quiz.place(x=40, y=410)

quiz1 = PhotoImage(file="quiz_1.png")
quiz2 = PhotoImage(file="quiz_2.png")
quiz3 = PhotoImage(file="quiz_3.png")
quiz4 = PhotoImage(file="quiz_4.png")
quiz5 = PhotoImage(file="quiz_5.png")
quiz6 = PhotoImage(file="quiz_6.png")

photo_next = PhotoImage(file="button_next.png")
next = Button(window, image=photo_next, command=next, relief=SOLID)



#새끼버튼
photo_paju = PhotoImage(file="paju.png")
paju = Button(window, image=photo_paju, command=predict_paju, relief=SOLID)
paju.place(x=210, y=230)

photo_icheon = PhotoImage(file="icheon.png")
icheon = Button(window, image=photo_icheon, command=predict_icheon, relief=SOLID)
icheon.place(x=210, y=320)

photo_yang = PhotoImage(file="yang.png")
yang = Button(window, image=photo_yang, command=predict_yang, relief=SOLID)
yang.place(x=210, y=410)

photo_suwon = PhotoImage(file="suwon.png")
suwon = Button(window, image=photo_suwon, command=predict_suwon, relief=SOLID)
suwon.place(x=210, y=500)

photo_dongdu = PhotoImage(file="dongdu.png")
dongdu = Button(window, image=photo_dongdu, command=predict_dongdu, relief=SOLID)
dongdu.place(x=210, y=590)


if prediction["state"] == "disabled":
    small_enable_button()
else:
    small_disable_button()
    


window.mainloop()
