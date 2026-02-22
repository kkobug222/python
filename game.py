import os
import pygame
import time
import datetime
import random
import math

pygame.init() # 초기화 (반드시 필요)


# 화면 크기 설정
screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))


# 화면 타이틀 설정
pygame.display.set_caption("일제강점기 게임")


# FPS
clock = pygame.time.Clock()


# 배경 이미지 불러오기
background = pygame.image.load("background.png")
title = pygame.image.load("title.png")
game_end_img = pygame.image.load("clear1.png")


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
enemy_x_pos = (screen_width / 1.3) - (enemy_width / 2) # 화면 가로의 절반 크기에 해당하는 곳에 위치 (가로)
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
character_speed = 7
   
   
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
        text_score = font_01.render("점수 : " + str(score), True, BLACK)
        screen.blit(text_score, [70, 520])
        running_time = font_01.render("소요시간 : " + f"{times} sec", True, BLACK)
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
                        bullet_y_pos = character_y_pos + (character_width / 3.2)
                    
                        character = pygame.image.load("gun_left.png")
                        left_bullets.append([bullet_x_pos, bullet_y_pos])
                        
                    if character_info == 'right':
                        bullet_x_pos = character_x_pos + (character_width / 1.4) - (bullet_width / 2)
                        bullet_y_pos = character_y_pos + (character_width / 3.3)
                    
                        character = pygame.image.load("gun_right.png")
                        right_bullets.append([bullet_x_pos, bullet_y_pos])
                        
                    if character_info == 'up':
                        bullet_x_pos = character_x_pos + (character_width / 2) - (bullet_width / 2)
                        bullet_y_pos = character_y_pos + (character_width / 1.3)
                        
                        character = pygame.image.load("back.png")
                        up_bullets.append([bullet_x_pos, bullet_y_pos])
                        
                    if character_info == 'down':
                        bullet_x_pos = character_x_pos + (character_width / 1.95) - (bullet_width / 2)
                        bullet_y_pos = character_y_pos + (character_width / 1.3)
                        
                        character = pygame.image.load("front.png")
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
        r2 = pygame.Rect(character_x_pos, character_y_pos, character_size[0], character_size[1])
        if r1.colliderect(r2):
            GAME_OVER = True
            break

    #엔딩 - 해피엔딩
    if score >= 500 :
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
    
    for bullet_x_pos, bullet_y_pos in down_bullets:
        screen.blit(D_bullet, (bullet_x_pos, bullet_y_pos))


    #screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    for enemy_x_pos, enemy_y_pos, angle in enemies:
        screen.blit(enemy, (enemy_x_pos, enemy_y_pos))
    pygame.display.update()

pygame.quit()
