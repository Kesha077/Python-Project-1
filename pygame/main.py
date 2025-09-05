import pygame

image_path = '/data/data/org.test.MisterMario/files/app/'

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1280, 720)) #flags=pygame.NOFRAME
pygame.display.set_caption("Mister-Mario and Ghosts")
icon = pygame.image.load(image_path + 'images/mister_mario.png').convert_alpha()
pygame.display.set_icon(icon)



bg = pygame.image.load(image_path + 'images/Game_Background_190.png').convert_alpha()
#Players
walk_right=[
    pygame.image.load(image_path + 'images/player_right_s/player_right1.png').convert_alpha(),
    pygame.image.load(image_path + 'images/player_right_s/player_right2.png').convert_alpha(),
    pygame.image.load(image_path + 'images/player_right_s/player_right3.png').convert_alpha(),
    pygame.image.load(image_path + 'images/player_right_s/player_right4.png').convert_alpha(),
    pygame.image.load(image_path + 'images/player_right_s/player_right5.png').convert_alpha(),
]

walk_left=[
    pygame.image.load(image_path + 'images/player_left_c/player_left_1.png').convert_alpha(),
    pygame.image.load(image_path + 'images/player_left_c/player_left_2.png').convert_alpha(),
    pygame.image.load(image_path + 'images/player_left_c/player_left_3.png').convert_alpha(),
    pygame.image.load(image_path + 'images/player_left_c/player_left_4.png').convert_alpha(),
    pygame.image.load(image_path + 'images/player_left_c/player_left_5.png').convert_alpha(),
]

ghost1 = pygame.image.load(image_path + 'images/ghost1.png').convert_alpha()
ghost1_list_in_game=[]

player_animation=0
bg_x=0

player_speed=12
player_x=250

player_y=400
is_jump=False
jump_count=11

ghost1_timer=pygame.USEREVENT
pygame.time.set_timer(ghost1_timer, 4500)

label = pygame.font.Font(image_path + 'fonts/Roboto-Black.ttf', 80)
lose_label=label.render("GAME OVER!!!", False, (0,0,0))
restart_label=label.render("Restart Play...", False, (0, 213, 255))
restart_label_rect = restart_label.get_rect(topleft=(360, 450))


bullet=pygame.image.load(image_path + 'images/bullet1.png').convert_alpha()
bullets=[]
bullets_left=5

gameplay=True

bg_sound = pygame.mixer.Sound(image_path + 'sounds/bg_sound.mp3')
bg_sound.play()

running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x+1280, 0))

    if gameplay:

        player_rect=walk_left[0].get_rect(topleft=(player_x, player_y))

        if ghost1_list_in_game:
            for (i, el) in enumerate(ghost1_list_in_game):
                screen.blit(ghost1, el)
                el.x -= 12

                if el.x < -12:
                    ghost1_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay=False


        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_animation], (player_x, player_y))
        else:
            screen.blit(walk_right[player_animation], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 1000:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_UP]:
                is_jump=True
        else:
            if jump_count >= -11:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump=False
                jump_count = 11



        if player_animation == 2:
            player_animation = 0
        else:
            player_animation += 1

        bg_x -= 2
        if bg_x == -1280:
            bg_x = 0

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 5

                if el.x >1290:
                    bullets.pop(i)

                if ghost1_list_in_game:
                    for (index, ghost_el) in enumerate(ghost1_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost1_list_in_game.pop(index)
                            bullets.pop(i)

    else:
        screen.fill((209, 13, 16))
        screen.blit(lose_label, (350, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse=pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay=True
            player_x=250
            ghost1_list_in_game.clear()
            bullets.clear()
            bullets_left=5


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost1_timer:
            ghost1_list_in_game.append(ghost1.get_rect(topleft=(1281, 535)))
        if gameplay and event.type==pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 150, player_y + 140)))
            bullets_left-=1

    clock.tick(15)