import pygame
import random
from pygame.locals import *

WHITE = (255, 255, 255)
GREEN = (78, 255, 87)
YELLOW = (241, 255, 0)
BLUE = (80, 255, 239)
PURPLE = (203, 0, 255)
RED = (237, 28, 36)
FONT = "font.ttf"


class Text(object):
    def __init__(self,text,t_font,size,colour,x,y):
        self.font = pygame.font.Font(t_font, size)
        self.surface = self.font.render(text, True, colour)
        self.rect = self.surface.get_rect(topleft=(x, y))

    def show(self,screen):
        screen.blit(self.surface,self.rect)

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
    def __init__(self,center_x,center_y,who_shoots,speed):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("bullet.png")
        self.rect=self.image.get_rect(topleft=(center_x,center_y))
        self.master=who_shoots
        self.direction=0
        if self.master=="player":
            self.direction=-1
        else:
            self.direction=1
        self.speed=speed

    def update(self,screen):
        screen.blit(self.image,self.rect)
        self.rect.y+=self.direction*self.speed
        if self.direction==-1:
            if self.rect.y<=20:
                self.kill()
        else:
            if self.rect.y>=580:
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
    timer=pygame.time.get_ticks()

    def __init__(self,row,column):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("enemy.png")
        self.image=pygame.transform.scale(self.image,(40,35))
        self.rect=self.image.get_rect()
        self.rect.x=35+60*column
        self.rect.y=30+75*row
        self.row=row
        self.column=column
        self.points_scored=50

    def update(self,screen):
        screen.blit(self.image,self.rect)


class EnemyGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.rows=3
        self.columns=10
        self.alive_enemies_count=self.rows*self.columns
        self.alive_indexes=[x for x in range(0,30,1)]
        self.enemies_list=[[None for j in range(self.columns)]for i in range(self.rows)]
        self.right_column_index=9
        self.left_column_index=0
        self.direction=1
        self.fire_rate=3000
        self.bullet_speeds=[7,10,12,15]

        self.down_speed=30
        self.left_right_speed=30
        self.move_time=600

        self.move_timer=pygame.time.get_ticks()
        self.timer=pygame.time.get_ticks()
        self.delay_timer=pygame.time.get_ticks()

    def add_internal(self, *sprite):
        super(EnemyGroup,self).add_internal(*sprite)
        for spr in sprite:
            self.enemies_list[spr.row][spr.column]=spr

    def remove_internal(self, *sprite):
        super(EnemyGroup, self).remove_internal(*sprite)
        for spr in sprite:
            self.enemies_list[spr.row][spr.column]=None
            self.alive_indexes.remove(spr.row*10+spr.column)

    def update(self,screen):
        current_time=pygame.time.get_ticks()
        if current_time-self.move_timer>=self.move_time:
            for enemy in self:
                enemy.rect.x += self.direction * self.left_right_speed
            if self.direction==1:
                if self.enemies_list[0][self.right_column_index].rect.x>=725:
                    self.direction=-1
                    for enemy in self:
                        enemy.rect.y+=self.down_speed
            else:
                if self.enemies_list[0][self.left_column_index].rect.x<=35:
                    self.direction=1
                    for enemy in self:
                        enemy.rect.y += self.down_speed
            for enemy in self:
                enemy.update(screen)
            self.move_timer=pygame.time.get_ticks()



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

        self.score=0;

        self.player=Player()
        #self.enemy=Enemy()
        self.sup_enemy=Super_Enemy()
        self.enemies=EnemyGroup()

        self.life1=Life(700,50)
        self.life2=Life(733,50)
        self.life3=Life(766,50)

        self.game_over=False

        self.secret_iterator=0

        self.clock=pygame.time.Clock()
        self.fps=60

        for i in range(self.enemies.rows):
            for j in range(self.enemies.columns):
                new_enemy = Enemy(i,j)
                self.enemies.add(new_enemy)


        self.all_group = pygame.sprite.Group()
        self.player_group=pygame.sprite.Group()
        self.sup_enemy_group=pygame.sprite.Group()
        self.bullet_group=pygame.sprite.Group()
        self.enemy_bullets_group=pygame.sprite.Group()
        self.life_group=pygame.sprite.Group(self.life1,self.life2,self.life3)

        self.all_group.add(self.player)
        self.all_group.add(self.sup_enemy)
        self.all_group.add(self.enemies)
        self.all_group.add(self.life1)
        self.all_group.add(self.life2)
        self.all_group.add(self.life3)

        self.sup_enemy_group.add(self.sup_enemy)
        self.player_group.add(self.player)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
               return True
            else:
                return False

    def collisions(self,screen):
        for en in pygame.sprite.groupcollide(self.enemies,self.bullet_group,True,True).keys():
            mes = Text(str(en.points_scored),FONT,20,PURPLE,en.rect.x,en.rect.y)
            mes.show(screen)
            self.score+=en.points_scored

        for pl in pygame.sprite.groupcollide(self.player_group,self.enemy_bullets_group,False,True).keys():
            if self.life1.alive():
                self.life1.kill()
            elif self.life2.alive():
                self.life2.kill()
            elif self.life3.alive():
                self.life3.kill()
                mes = Text("Game Over!!!",FONT,50,RED,400,400)
                mes.show(screen)
                pl.kill()
                self.game_over=True

        for sup in pygame.sprite.groupcollide(self.sup_enemy_group,self.bullet_group,True,True).keys():
            mes = Text(str(sup.points_scored), FONT, 50, BLUE, 400, 400)
            mes.show(screen)

    def run_game(self,screen):

        if not self.game_over:
            currentTime=pygame.time.get_ticks()

            self.pressed_keys=pygame.key.get_pressed()

            if self.pressed_keys[pygame.K_UP]:
                if (currentTime-self.player.timer)>=self.player.fire_rate and len(self.bullet_group)==0:
                    p_bullet=Bullet(self.player.rect.x+20,self.player.rect.y+5,"player",10)
                    self.bullet_group.add(p_bullet)
                    self.player.timer+=self.player.fire_rate
                else:
                    pass

            current_Time=pygame.time.get_ticks()
            if (current_Time - self.enemies.timer )>= self.enemies.fire_rate and len(self.enemy_bullets_group)==0:
                how_many_should_fire = random.randint(4, 8)
                list_of_firing_enemies = random.sample(self.enemies.alive_indexes, how_many_should_fire)
                for enemy_index in list_of_firing_enemies:
                    r=enemy_index//10
                    c=enemy_index%10
                    random_speed=random.choice(self.enemies.bullet_speeds)
                    enemy_bullet=Bullet(self.enemies.enemies_list[r][c].rect.x+20,self.enemies.enemies_list[r][c].rect.y+5,"enemy",random_speed)
                    self.enemy_bullets_group.add(enemy_bullet)
                self.enemies.timer+=self.enemies.fire_rate


            self.player_group.update(self.pressed_keys,screen)
            self.bullet_group.update(screen)
            self.enemy_bullets_group.update(screen)
            self.sup_enemy_group.update(currentTime)
            self.enemies.update(screen)
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

        game_instance.collisions(DISPLAY_SCREEN)

        game_instance.display(DISPLAY_SCREEN)

        game_instance.clock.tick(game_instance.fps)

    pygame.quit()

if __name__=="__main__":
    main()