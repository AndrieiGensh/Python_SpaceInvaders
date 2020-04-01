import pygame
import random
from pygame.locals import *

WHITE = (255, 255, 255)

class Life(pygame.sprite.Sprite):
    def __init__(self,position_x,position_y):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("ship.png")
        self.image=pygame.transform.scale(self.image,(23,23))
        self.rect=self.image.get_rect(topleft=(position_x,position_y))
        self.state=True

    def update(self, screen):
        screen.blit(self.image,self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,center_x,center_y,who_shoots):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("bullet.png")
        self.rect=self.image.get_rect(topleft=(center_x,center_y))
        self.master=who_shoots
        self.direction=0
        if self.master=="player":
            self.direction=-1
            print("it is players bullet")
        else:
            self.direction=1
        self.speed=10

    def update(self,screen):
        screen.blit(self.image,self.rect)
        self.rect.y+=self.direction*self.speed
        if self.direction==-1:
            if self.rect.y<=20:
                print("killed bullet")
                self.kill()
        else:
            if self.rect.y>=580:
                print("killed bullet")
                self.kill()



class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("ship.png")
        self.rect= self.image.get_rect(topleft=(370,550))
        self.movement_speed=5
        self.fire_rate=700
        self.timer=pygame.time.get_ticks()

    def update(self, pressed_keys,screen):
        if pressed_keys[pygame.K_LEFT]:
            if self.rect.x>=20:
                self.rect.x-=self.movement_speed
                screen.blit(self.image,self.rect)
        elif pressed_keys[pygame.K_RIGHT]:
            if self.rect.x<=740:
                self.rect.x+=self.movement_speed
                screen.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("enemy.png")
        self.image=pygame.transform.scale(self.image,(40,35))
        self.rect=self.image.get_rect()
        self.rect.x=370
        self.rect.y=30
        self.down_speed=30
        self.left_right_speed=30

        self.points_scored=0

        self.move_time=600
        self.timer=pygame.time.get_ticks()

        self.move_direc=1

    def update(self,current_time):
        if (current_time-self.timer) >= self.move_time:
            if self.move_direc==1:
                self.rect.x+=self.left_right_speed
                if self.rect.x>=740:
                    self.move_direc=-1
                    self.rect.y+=self.down_speed
                self.timer += self.move_time

            else:
                self.rect.x-=self.left_right_speed
                if self.rect.x<=20:
                    self.move_direc=1
                    self.rect.y+=self.down_speed
                self.timer += self.move_time

class Super_Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("sup_enemy.png")
        self.image=pygame.transform.scale(self.image,(50,35))
        self.rect=self.image.get_rect()
        self.rect.x=-70
        self.rect.y=30
        self.speed=6
        self.direction=1

        self.points_scored=500
        self.show_up_time=20000
        self.timer=pygame.time.get_ticks()

    def update(self,current_time):
        time=current_time-self.timer
        if time>=self.show_up_time:
            if self.direction==1:
                self.rect.x+=self.speed
                if self.rect.x>=800:
                    self.direction=-1
                    self.rect.x=870
                    self.timer=pygame.time.get_ticks()
            else:
                self.rect.x-=self.speed
                if self.rect.x<=-30:
                    self.rect.x=-100
                    self.direction=1
                    self.timer=pygame.time.get_ticks()

class Game(object):

    def __init__(self):
        self.player=Player()
        self.enemy=Enemy()
        self.sup_enemy=Super_Enemy()

        self.life1=Life(700,50)
        self.life2=Life(733,50)
        self.life3=Life(766,50)

        self.game_over=False

        self.clock=pygame.time.Clock()

        self.all_group = pygame.sprite.Group()
        self.player_group=pygame.sprite.Group()
        self.enemy_group=pygame.sprite.Group()
        self.bullet_group=pygame.sprite.Group()
        self.life_group=pygame.sprite.Group(self.life1,self.life2,self.life3)

        self.all_group.add(self.player)
        self.all_group.add(self.sup_enemy)
        self.all_group.add(self.enemy)
        self.all_group.add(self.life1)
        self.all_group.add(self.life2)
        self.all_group.add(self.life3)

        self.enemy_group.add(self.sup_enemy)
        self.enemy_group.add(self.enemy)
        self.player_group.add(self.player)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
               return True
            else:
                return False

    def run_game(self,screen):

        if not self.game_over:
            currentTime=pygame.time.get_ticks()

            self.pressed_keys=pygame.key.get_pressed()

            if self.pressed_keys[pygame.K_UP]:
                if (currentTime-self.player.timer)>=self.player.fire_rate and len(self.bullet_group)==0:
                    print("supposed to fire")
                    p_bullet=Bullet(self.player.rect.x+20,self.player.rect.y+5,"player")
                    self.bullet_group.add(p_bullet)
                    print("player timer before:",self.player.timer)
                    self.player.timer+=self.player.fire_rate
                    print("player timer after:",self.player.timer)
                else:
                    print("not the time")

            self.player_group.update(self.pressed_keys,screen)
            self.bullet_group.update(screen)
            self.enemy_group.update(currentTime)
            self.life_group.update(screen)

    def display(self,display_screen):

        if not self.game_over:
            self.all_group.draw(display_screen)
        pygame.display.flip()

def main():

    pygame.init()
    bg=pygame.image.load("space.png")
    bg=pygame.transform.scale(bg,(800,600))
    DISPLAY_SCREEN = pygame.display.set_mode((800, 600))

    pygame.display.set_caption("Space invaders by Andriei Gensh")

    over = False

    game_instance=Game()

    while not over:
        DISPLAY_SCREEN.blit(bg,(0,0))
        over=game_instance.process_events()

        game_instance.run_game(DISPLAY_SCREEN)

        game_instance.display(DISPLAY_SCREEN)

        game_instance.clock.tick(60)

    pygame.quit()

if __name__=="__main__":
    main()