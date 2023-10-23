import pygame
import random
import math
import pygame.mixer

pygame.init()
pygame.mixer.init()

background_music = pygame.mixer.Sound('data/music.mp3')
background_music_menu = pygame.mixer.Sound('data/menu_music.mp3')

menu_img = pygame.image.load('data/menu.png')

game_over = False
new_game = False

points = 0
max_points_level1 = 10
max_points_level2 = 10
max_points_level3 = 3
font = pygame.font.Font(pygame.font.get_default_font(), 25)



screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

pygame.display.set_caption(' Space Invaders ')


ship_1 = pygame.image.load('data/ship.png')
ship_x = 260
ship_y = 300
ship_speed = 5

ship_2 = pygame.image.load('data/ship_2.png')
ship_option_texts = ["", "Ship 1", "Ship 2"]
ship_option_selected = 1
ship_menu_mode = False

ship = ship_1

ship_images = [
    pygame.image.load('data/ship.png'),
    pygame.image.load('data/ship_2.png'),
]

background_img = pygame.image.load('data/background.jpg')
alien_img = pygame.image.load('data/alien.png')
alien_2_img = pygame.image.load('data/alien_2.png')

aliens = []
alien_bullet_img = pygame.image.load('data/bomb.png')
alien_bullets = []
alien_bullet_speed = 3
alien_bullet_state = "fire"
active_alien_bullets = []


alien_bullet_timer = 0
alien_bullet_interval = 10000

menu_text = ["Select level: ", "Level 1", "Level 2", "Level 3", "Select ship"]
menu_selected = 1
menu_color_inactive = pygame.Color("white")
menu_color_active = pygame.Color("lime")

current_max_points = max_points_level1

heart_img = pygame.image.load('data/heart.png')
heart_x = 10
heart_y = 30
heart_width = heart_img.get_width()
heart_height = heart_img.get_height()

life = 3
life_lost = False
life_lost_interval = 2000

def draw_menu():
  for i, text in enumerate(menu_text):
        color = menu_color_active if i == menu_selected else menu_color_inactive
        text_render = font.render(text, True, color)
        screen.blit(text_render, (200, 200 + i * 30))

def draw_choosing_ship():
      for i, text in enumerate(ship_option_texts):
        color = menu_color_active if i == ship_option_selected else menu_color_inactive
        text_render = font.render(text, True, color)
        screen.blit(text_render, (-30 + i* 200, 150))
        if i == 1:
          ship_1 = pygame.image.load('data/ship.png')
          screen.blit(ship_1, (180, 190))
        elif i == 2:
          ship_2 = pygame.image.load('data/ship_2.png') 
          screen.blit(ship_2, (380, 190))

def create_alien():
  x = random.randint(0, 600)
  y = random.randint(50, 100)
  speed = random.choice([-5, 5])
  return [x, y, speed]

for i in range(5):
  aliens.append(create_alien())


bullet_img = pygame.image.load('data/bullet.png')
bullet_x = -100
bullet_y = -100
bullet_speed = 12
bullet_state = "ready"

bullet_2_img = pygame.image.load('data/bullet.png')
bullet_2_x = -100
bullet_y = -100
bullet_2_speed = 20
bullet_2_state = "ready"

def fire_bullet(x,y):
  global bullet_state
  bullet_state = "fire"
  screen.blit(bullet_img, (x + 10, y + 10))



def is_collision(alien_x, alien_y, bullet_x, bullet_y):
  distance = math.sqrt(math.pow(alien_x - bullet_x, 2) + math.pow(alien_y - bullet_y, 2))
  if distance < 25:
    return True
  return False

def create_boss():
  x = 300
  y = 100
  angle = 0
  radius = 100
  speed = 6
  return [x, y, angle, radius, speed]

boss_img = pygame.image.load('data/boss.png')
boss_health = 20
boss_attack_interval = 2000
boss_bullet_img = pygame.image.load('data/boss_bullet.png')
boss_bullet_speed = 5
boss_bullet_cooldown = 5
boss_bullet_timer = 0
boss_bullets = []
boss_state = "circle"
boss_horizontal_speed = 7
boss_horizontal_direction = 1
boss_horizontal_x = 100
boss_weapon_img = pygame.image.load('data/boss_weapon.png')

select_ship = pygame.image.load('data/select ship.png')

menu_mode = True
level = 0
boss = create_boss()
running = True
while running:
  current_time = pygame.time.get_ticks()
  current_time_attack_boss = pygame.time.get_ticks()
  while menu_mode == True:
    background_music.stop()
    background_music_menu.play(-1)
    background_music_menu.set_volume(0.05) 
    screen.blit(menu_img, (0, 0))
    draw_menu()
    pygame.display.flip()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          menu_selected = max(1, menu_selected - 1)
        if event.key == pygame.K_DOWN:
          menu_selected = min(len(menu_text) - 1, menu_selected + 1)
        if event.key == pygame.K_RETURN:
          if menu_selected == 1:
            level = 1
            current_max_points = max_points_level1
            menu_mode = False
          elif menu_selected == 2:
            level = 2
            current_max_points = max_points_level2
            menu_mode = False
          elif menu_selected == 3:
            level = 3
            current_max_points = max_points_level3
            aliens = []
            menu_mode = False
            background_music_menu.stop()
            background_music.play(-1)
            background_music.set_volume(0.2) 
          elif menu_selected == 4:
            menu_mode = False
            ship_menu_mode = True
            
  while ship_menu_mode == True:
    screen.blit(select_ship, (0,0))
    draw_choosing_ship()
    pygame.display.flip()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          ship_option_selected = max(1, ship_option_selected - 1)
        if event.key == pygame.K_RIGHT:
          ship_option_selected = min(len(ship_option_texts) - 1, ship_option_selected + 1)
        if event.key == pygame.K_RETURN:
          if ship_option_selected == 1:
            ship = ship_1
            menu_mode = True
            ship_menu_mode = False
          if ship_option_selected == 2:
            ship = ship_2
            menu_mode = True
            ship_menu_mode = False
          else:
            selected_ship_image = ship_images[ship_option_selected - 1]
 

              
  
  clock.tick(30)
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE and bullet_state == 'ready':
        bullet_x = ship_x
        bullet_y = ship_y
        fire_bullet(bullet_x, bullet_y)
        if ship == ship_2:
          bullet_2_x = ship_x + 30
          bullet_2_y = ship_y



  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT]:
    ship_x -= ship_speed
  if keys[pygame.K_RIGHT]:
    ship_x += ship_speed
  if keys[pygame.K_UP]:
    ship_y -= ship_speed
  if keys[pygame.K_DOWN]:
    ship_y += ship_speed
  
  ship_x = max(0, min(ship_x, 540 - ship.get_width()))
  ship_y = max(0, min(ship_y, 400 - ship.get_height()))
  
  screen.blit(background_img, (0, 0))

  if ship == ship_2:
    ship_speed = 7
    bullet_speed = 20
  
  if ship == ship_1:
    ship_speed = 5
    bullet_speed = 12
  
  if level == 3:
    if boss_state == "circle":
      angle_rad = math.radians(boss[2])
      boss_x = 440 // 2 + int(boss[3] * math.cos(angle_rad))
      boss_y = 100 // 2 + int(boss[3] * math.sin(angle_rad))
      screen.blit(boss_img, (int(boss_x), int(boss_y)))
      boss[2] += boss[4]
      if boss[2] >= 360:
          boss[2] = boss[2] - 360
      boss_bullet_timer += 1
      if boss_bullet_timer >= boss_bullet_cooldown:
        boss_bullet_timer = 0
        boss_bullet_angle = random.uniform(0, 360)
        boss_bullet_x = boss_x + int(boss[3] * math.cos(math.radians(boss_bullet_angle)))
        boss_bullet_y = boss_y + int(boss[3] * math.sin(math.radians(boss_bullet_angle)))
        boss_bullets.append([boss_bullet_x, boss_bullet_y, boss_bullet_angle])
      for boss_bullet in boss_bullets:
        boss_bullet_angle_rad = math.radians(boss_bullet[2])
        boss_bullet[0] += int(boss_bullet_speed * math.cos(boss_bullet_angle_rad))
        boss_bullet[1] += int(boss_bullet_speed * math.sin(boss_bullet_angle_rad))
        if boss_bullet[0] < 0 or boss_bullet[0] > 400 or boss_bullet[1] < 0 or boss_bullet[1] > 600:
              boss_bullets.remove(boss_bullet)
      for boss_bullet in boss_bullets:
        screen.blit(boss_bullet_img, (int(boss_bullet[0]), int(boss_bullet[1])))
      for boss_bullet in boss_bullets:
        collision_ship_boss = is_collision(boss_bullet[0], boss_bullet[1], ship_x, ship_y)
        if collision_ship_boss == True:
          if life_lost == False and (life_lost_interval - current_time <=0):
            life -= 1
            life_lost = True
            life_lost_interval = current_time + 1000
            life_lost = False
            if life <=0:        
              game_over = True
              break
    elif boss_state == "horizontal movement":
      boss_horizontal_x += boss_horizontal_speed * boss_horizontal_direction
      if boss_horizontal_x <= 0 or boss_horizontal_x >= 400:
        boss_horizontal_direction *= -1
      boss_x = boss_horizontal_x
      boss_y = 50
      screen.blit(boss_img, (int(boss_x), int(boss_y)))
      screen.blit(boss_weapon_img, (int(boss_x) + 30, int(boss_y) + 100))
      for boss_bullet in boss_bullets:
        boss_weapon_x = boss_x + 30
        boss_weapon_y = boss_y + 100
        boss_weapon_width = boss_weapon_img.get_width()
        boss_weapon_height = boss_weapon_img.get_height()
        if (boss_weapon_x < ship_x + ship.get_width() and 
        boss_weapon_x + boss_weapon_width > ship_x and
        boss_weapon_y < ship_y + ship.get_height() and
        boss_weapon_y + boss_weapon_height > ship_y):
          if life_lost == False and (life_lost_interval - current_time <=0):
            life -= 1
            life_lost = True
            life_lost_interval = current_time + 1000
            life_lost = False
            if life <=0:        
              game_over = True
              break
    if random.randint(0,500) < 10:
      if boss_state == "circle":
        boss_state = "horizontal movement"
      else:
        boss_state = "circle"
    collision = is_collision(boss_x, boss_y, bullet_x, bullet_y)
    if collision == True:
      points += 1
      bullet_state = "ready"
      bullet_x = -100
      bullet_y = - 100
      boss_health -= 1
      if ship == ship_2:
        bullet_2_state = "ready"
        bullet_2_x = -100
        bullet_2_y = - 100



  if level == 1 or level == 2:
    for alien in aliens:
        alien[0] += alien[2]
        if alien[0] > 600:
            alien[0] = 0
            alien[1] += 10 
        elif alien[0] < 0:
            alien[0] = 600
            alien[1] += 40 
        elif alien[1] > 450:
            alien[0] = 0
            alien[1] = 0
        if level == 1:
            screen.blit(alien_img, (alien[0], alien[1]))
        if level == 2:
            screen.blit(alien_2_img, (alien[0], alien[1]))
        if level == 2:
          if random.randint(0,100) == 0:
              alien_bullets.append([alien[0] + alien_2_img.get_width() // 2, alien[1], "fire"])
        if level == 2:
          alien_bullet_timer += clock.get_time()
          if alien_bullet_timer >= alien_bullet_interval:
            alien_bullets.append([alien[0] + alien_2_img.get_width() // 2, alien[1], "fire"])
            alien_bullet_timer = 0  
          for alien_bullet in alien_bullets:
              if alien_bullet_state == "fire":
                  alien_bullet[1] += alien_bullet_speed
                  if alien_bullet[1] > 400:
                      alien_bullet_state = "fire"
              if alien_bullet_state == "ready":
                  alien_bullet[0] = -100
                  alien_bullet[1] = -100  
              if alien_bullet_state == "fire":
                  screen.blit(alien_bullet_img, (alien_bullet[0], alien_bullet[1]))   
  
  if bullet_state == "fire":
    fire_bullet(bullet_x, bullet_y)
    bullet_y -= bullet_speed
    if ship == ship_2:
      fire_bullet(bullet_2_x, bullet_2_y)
      bullet_2_y -= bullet_2_speed

  if bullet_y < 0:
    bullet_state = "ready"
    bullet_x = -100
    bullet_y = -100
    if ship == ship_2:
      bullet_2_state = "ready"
      bullet_2_x = -100
      bullet_2_y = -100
  
  for alien in aliens:
    collision = is_collision(alien[0], alien[1], bullet_x, bullet_y)
    if collision:
      points += 1
      bullet_state = "ready"
      bullet_x = -100
      bullet_y = -100
      if ship == ship_2:
        bullet_2_state = "ready"
        bullet_2_x = -100
        bullet_2_y = -100
      aliens.remove(alien)
      aliens.append(create_alien())
    for alien_bullet in alien_bullets:
      collision_ship_alien = is_collision(alien_bullet[0], alien_bullet[1], ship_x, ship_y)
      if collision_ship_alien == True:        
        if life_lost == False and (life_lost_interval - current_time <=0):
          life -= 1
          life_lost = True
          life_lost_interval = current_time + 10002
          life_lost = False
          if life <=0:        
            game_over = True
            break

  if points >= current_max_points:
    game_over = True
  
  for alien in aliens:
    collision_ship = is_collision(alien[0], alien[1], ship_x, ship_y)
    if collision_ship  == True:
      if life_lost  == False and (life_lost_interval - current_time <= 0):
        life -= 1
        life_lost = True
        life_lost_interval = current_time + 1000
        life_lost = False
        if life <=0:
          game_over = True
          break
    for alien_bullet in alien_bullets:
      collision_ship_alien = is_collision(alien_bullet[0], alien_bullet[1], ship_x, ship_y)

  if points >= current_max_points:
    game_over == True
      
  if game_over == True:
    if keys[pygame.K_RETURN]:
      new_game = True
    if keys[pygame.K_ESCAPE]:
      new_game = True
      menu_mode = True
    if points >= current_max_points:
      text = ["You win! Press Enter to play again", "Esc to return to menu."]
      aliens = []
      bullet_x = -100
      bullet_y = -100
      if ship == ship_2:
        bullet_2_x = -100
        bullet_2_y = -100
      screen.fill((0,0,0))
    else:
      text = ["Game over. Press Enter to play again", "Esc to return to menu."]
      alleins = []
      bullet_x = -100
      bullet_y = -100
      bullet_2_x = -100
      bullet_2_y = -100
      screen.fill((0,0,0))
    text_renders = [font.render(line, True, "white") for line in text]
    text_height = sum(render.get_height() for render in text_renders)
    text_y = 200 - text_height // 2
    for text_render in text_renders:
        text_width = text_render.get_width()
        screen.blit(text_render, (300 - text_width // 2, text_y))
        text_y += text_render.get_height()



  for i in range(life):
    screen.blit(heart_img, (heart_x + i * (heart_width + 10), heart_y))

  
  text = "Points: " + str(points)
  text_render = font.render(text, True, "white")
  screen.blit(text_render, (10,10))

  if new_game == True:
    game_over = False
    aliens = []
    for i in range(5):
      aliens.append(create_alien())
    points = 0
    ship_x = 260
    ship_y = 300
    bullet_x = -100
    bullet_y = -100
    if ship == ship_2:
      bullet_2_x = -100
      bullet_2_y = -100
    bullet_state = "ready"
    life = 3
    life_lost = False 
    new_game = False

  

  screen.blit(ship, (ship_x, ship_y))

  pygame.display.flip()

  clock.tick(60)
  

pygame.quit()
