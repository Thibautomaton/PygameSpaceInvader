# This is a sample Python script.
import sys
from json.encoder import py_encode_basestring_ascii

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
import random

pygame.init()

WIDTH = 1450
HEIGHT = 720

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aliens attack")

class Game():
    def __init__(self, player, alien_group, alien_bullet_group, player_bullet_group):

        self.player = player
        self.alien_group = alien_group
        self.alien_bullet_group = alien_bullet_group
        self.player_bullet_group = player_bullet_group

        self.score =0
        self.round_number =5


        self.font = pygame.font.Font("Super Dream.ttf", 24)

        self.start_new_round()

    def update(self):
        self.shift_aliens()
        self.check_collisions()
        self.check_round_completion()

    def draw(self):
        WHITE=(255, 255, 255)

        score_text = self.font.render("Score " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft= (20,10)

        round_text = self.font.render(f"Current Round {self.round_number}", True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.centerx = WIDTH//2
        round_rect.top=10

        lives_text = self.font.render(f"Lives {self.player.lives}", True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topright = (WIDTH-20, 10)

        display_surface.blit(score_text, score_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(lives_text, lives_rect)
        pygame.draw.line(display_surface, WHITE, (0, 60), (WIDTH, 60))


    def start_new_round(self):
        for i in range (11):
            for j in range(5):
                alien = Alien(64+i*48, 64 + j*48, self.round_number, self.alien_bullet_group)
                self.alien_group.add(alien)

        self.pause_game(f"Are you ready ? round {self.round_number}", "Press Enter to continue")

    def shift_aliens(self):
        shift = False
        for alien in self.alien_group.sprites():
            if alien.rect.left<=0 or alien.rect.right>=WIDTH:
                shift= True

        if shift:
            breach = False
            for alien in self.alien_group.sprites():
                alien.rect.y += 10*self.round_number

                alien.direction*=-1

                if alien.rect.bottom>=HEIGHT-100:
                    breach=True

            if breach:
                self.player.lives-=1
                self.check_game_status("Alien breached the line", "Press Enter to continue<Enter>")


    def check_collisions(self):
        if (pygame.sprite.spritecollide(self.player, self.alien_bullet_group, True)):
            self.player.lives -=1
            self.player.reset()
            self.check_game_status("You were hit continue ?", "Press ENter to continue")

        elif (pygame.sprite.groupcollide(self.alien_group, self.player_bullet_group, True, True)):
            self.score +=10

    def check_round_completion(self):
        if not alien_group:
            self.score+=100*self.round_number
            self.round_number+=1
            self.start_new_round()


    def check_game_status(self, main_text, sub_text):

        self.player_bullet_group.empty()
        self.alien_bullet_group.empty()
        self.player.reset()
        for alien in alien_group:
            alien.reset()

        if self.player.lives<=0:
            self.reset_game()
        else:
            self.pause_game(main_text, sub_text)


    def reset_game(self):

        self.pause_game(f"Final score is {self.score}", "Press Enter to play again")
        self.player.lives = 5
        self.round_number = 1
        self.score = 0

        self.alien_group.empty()
        self.alien_bullet_group.empty()
        self.player_bullet_group.empty()

        self.start_new_round()


    def pause_game(self,main_text, sub_text):
        WHITE=(255, 255, 255)
        main_text = self.font.render(main_text, True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WIDTH//2, HEIGHT//2)

        sub_text = self.font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WIDTH//2, HEIGHT//2+100)

        display_surface.fill((0,0,0))
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)

        pygame.display.update()

        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        is_paused=False
                elif event.type==pygame.QUIT:
                    running =False
                    exit(0)

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity, bullet_group):
        super().__init__()
        self.image=pygame.image.load("alien.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.bullet_group = bullet_group

        self.startx = x
        self.starty = y

        self.direction=1

        self.velocity = velocity

    def update(self):
        self.rect.x += self.direction*self.velocity
        if random.randint(0, 1000)>999 and len(self.bullet_group)<3:
            self.fire()

    def fire(self):
        AlienBullet(self.rect.centerx, self.rect.bottom, self.bullet_group)

    def reset(self):
        self.rect.topleft = (self.startx, self.starty)



class Player(pygame.sprite.Sprite):
    def __init__(self,bullet_group):
        super().__init__()
        self.image = pygame.image.load("shuttle.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH//2
        self.rect.bottom = HEIGHT-10

        self.bullet_group = bullet_group

        self.velocity = 8

        self.lives=5

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x +=self.velocity
        elif keys[pygame.K_LEFT]:
            self.rect.x -=self.velocity

    def fire(self):
        PlayerBullet(self.rect.centerx, self.rect.top, self.bullet_group)

    def reset(self):
        self.rect.centerx = WIDTH//2

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_group):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("laser_green.png"), (8, 32))
        self.rect = self.image.get_rect()
        self.rect.centerx=x
        self.rect.bottom = y

        self.velocity = 5

        bullet_group.add(self)


    def update(self):
        self.rect.y -= self.velocity

        if self.rect.bottom<=0:
            self.kill()


class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_group):
        super().__init__()
        self.image= pygame.transform.scale(pygame.image.load("laser_red.png"), (8, 32))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y

        self.velocity = 8

        bullet_group.add(self)

    def update(self):
        self.rect.y += self.velocity

        if self.rect.top>=HEIGHT:
            self.kill()




player_bullet_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()

player_group = pygame.sprite.Group()
my_player = Player(player_bullet_group)
player_group.add(my_player)

alien_group = pygame.sprite.Group()
# for i in range(10):
#     alien = Alien(64+64*i, 100, 2, alien_bullet_group)
#     alien_group.add(alien)


the_game = Game(my_player, alien_group, alien_bullet_group, player_bullet_group)

clock = pygame.time.Clock()

TARGET_FPS = 60
running= True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False
            exit(0)
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                if len(player_bullet_group)<3:
                    my_player.fire()

    display_surface.fill((0,0,0))

    player_group.update()
    player_group.draw(display_surface)

    player_bullet_group.update()
    player_bullet_group.draw(display_surface)

    alien_group.update()
    alien_group.draw(display_surface)

    alien_bullet_group.update()
    alien_bullet_group.draw(display_surface)

    the_game.update()
    the_game.draw()

    pygame.display.update()
    clock.tick(TARGET_FPS)

pygame.quit()




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
