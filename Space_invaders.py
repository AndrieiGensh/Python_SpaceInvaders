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

f_name = pygame.font.match_font("arial")
DISPLAY_SCREEN = pygame.display.set_mode((800, 600))

def print_mes(screen,message,size,colour,x_pos,y_pos):
    font = pygame.font.Font(f_name,size)
    text_sur = font.render(message,True,colour)
    text_rect = text_sur.get_rect()
    text_rect.midtop = (x_pos,y_pos)
    screen.blit(text_sur,text_rect)

class Life(pygame.sprite.Sprite):
    def __init__(self,position_x,position_y):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("ship.png")
        self.image=pygame.transform.scale(self.image,(23,23))
        self.rect=self.image.get_rect(topleft=(position_x,position_y))
        self.state=True

    def update(self):
        DISPLAY_SCREEN.blit(self.image,self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,center_x,center_y,who_shoots,speed):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.image.load("laser.png")
        self.rect=self.image.get_rect(topleft=(center_x,center_y))
        self.master=who_shoots
        self.direction=0
        if self.master=="player":
            self.direction=-1
        else:
            self.direction=1
        self.speed=speed

    def update(self):
        DISPLAY_SCREEN.blit(self.image,self.rect)
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
        self.fire_rate=100
        self.timer=pygame.time.get_ticks()

    def reset_position(self):
        self.rect.x=370
        self.rect.y=550

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_LEFT]:
            if self.rect.x>=20:
                self.rect.x-=self.movement_speed
                DISPLAY_SCREEN.blit(self.image,self.rect)
        elif pressed_keys[pygame.K_RIGHT]:
            if self.rect.x<=740:
                self.rect.x+=self.movement_speed
                DISPLAY_SCREEN.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    timer=pygame.time.get_ticks()

    def __init__(self,row,column):
        pygame.sprite.Sprite.__init__(self)
        if row==0:
            self.image=pygame.image.load("enemy.png")
        elif row==2:
            self.image=pygame.image.load("enemy2.png")
        else:
            self.image=pygame.image.load("enemy3.png")
        self.image=pygame.transform.scale(self.image,(40,35))
        self.rect=self.image.get_rect()
        self.rect.x=35+60*column
        self.rect.y=30+75*row
        self.row=row
        self.column=column
        self.points_scored=50

    def update(self):
        DISPLAY_SCREEN.blit(self.image,self.rect)


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

    def reset_group_params(self):
        self.rows = 3
        self.columns = 10
        self.alive_enemies_count = self.rows * self.columns
        self.alive_indexes = [x for x in range(0, 30, 1)]
        self.enemies_list = [[None for j in range(self.columns)] for i in range(self.rows)]
        self.right_column_index = 9
        self.left_column_index = 0
        self.direction = 1
        self.left_right_speed=30

    def level_changes(self,current_level):
        self.move_time-=current_level*20

    def check_border_columns(self):
        if self.alive_enemies_count==0:
            return
        any_left=False
        any_right=False
        found_left=False
        found_right=False
        for i in range(0,self.rows):
            if self.enemies_list[i][self.left_column_index] is not None:
                any_left=True
                break
        if not any_left:
            print("left missing")
            for col in range(self.left_column_index,self.right_column_index+1):
                if found_left:
                    break
                for row in range(0,self.rows):
                    if isinstance(self.enemies_list[row][col],Enemy):
                        self.left_column_index=col
                        found_left=True
                        break

        for i in range(0, self.rows):
            if self.enemies_list[i][self.right_column_index] is not None:
                any_right = True
                break
        if not any_right:
            print("right missing")
            print(range(self.right_column_index,self.left_column_index))
            for col2 in range(self.right_column_index,self.left_column_index-1,-1):
                if found_right:
                    break
                for row2 in range(0,self.rows):
                    if isinstance(self.enemies_list[row2][col2],Enemy):
                        self.right_column_index=col2
                        print("new righjt =",self.right_column_index)
                        found_right=True
                        break

        print("left=",self.left_column_index)
        print("right=",self.right_column_index)

    def add_internal(self, *sprite):
        super(EnemyGroup,self).add_internal(*sprite)
        for spr in sprite:
            self.enemies_list[spr.row][spr.column]=spr

    def remove_internal(self, *sprite):
        super(EnemyGroup, self).remove_internal(*sprite)
        for spr in sprite:
            self.enemies_list[spr.row][spr.column]=None
            self.alive_indexes.remove((spr.row*10+spr.column))
            self.alive_enemies_count-=1
            self.check_border_columns()

    def update(self):

        current_time=pygame.time.get_ticks()
        if current_time-self.move_timer>=self.move_time:
            for enemy in self:
                enemy.rect.x += self.direction * self.left_right_speed
            if self.direction==1:
                for row in range(0,self.rows):
                    if isinstance(self.enemies_list[row][self.right_column_index],Enemy):
                        if self.enemies_list[row][self.right_column_index].rect.x>=725:
                            self.direction=-1
                            for enemy in self:
                                enemy.rect.y+=self.down_speed
                        break
            else:
                for row in range(0,self.rows):
                    if isinstance(self.enemies_list[row][self.left_column_index],Enemy):
                        if self.enemies_list[row][self.left_column_index].rect.x<=35:
                            self.direction=1
                            for enemy in self:
                                enemy.rect.y += self.down_speed
                        break

            for enemy in self:
                enemy.update()
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
            pygame.mixer.Sound("mystery.wav").play()
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

        self.score=0

        self.level=0

        self.background=pygame.image.load("space.png")
        self.background=pygame.transform.scale(self.background,(800,600))

        self.player = None
        self.sup_enemy = None
        self.enemies = None

        self.life1 = None
        self.life2 = None
        self.life3 = None

        self.all_group = None
        self.life_group = None
        self.player_group = None
        self.sup_enemy_group = None
        self.bullet_group = None
        self.enemy_bullets_group = None

        self.game_over=False
        self.over_screen=False
        self.new_game=True
        self.next_level=True
        self.restart_game=False

        self.secret_iterator=0

        self.clock=pygame.time.Clock()
        self.fps=60

    def reset(self,option):
        if option=="new_game_reset":
            self.player_group.empty()
            self.enemy_bullets_group.empty()
            self.enemies.empty()
            self.enemies = EnemyGroup()
            self.sup_enemy_group.empty()
            self.bullet_group.empty()
            self.life_group.empty()
            self.all_group.empty()
            self.enemies.reset_group_params()
        elif option=="next_level_reset":
            self.enemies.empty()
            self.enemies = EnemyGroup()
            self.enemies.reset_group_params()
            self.bullet_group.empty()
            self.enemy_bullets_group.empty()
            self.sup_enemy_group.empty()

    def init_new_game(self):
        self.player=None
        self.sup_enemy=None
        self.enemies=EnemyGroup()

        self.life1 = None
        self.life2 = None
        self.life3 = None

        self.all_group=pygame.sprite.Group()
        self.life_group=pygame.sprite.Group()
        self.player_group=pygame.sprite.Group()
        self.sup_enemy_group=pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_bullets_group = pygame.sprite.Group()

    def create_enemies(self):

        for i in range(self.enemies.rows):
            for j in range(self.enemies.columns):
                new_enemy = Enemy(i, j)
                self.enemies.add(new_enemy)

    def create_level(self,option):
        if option=="new_game":
            self.reset("new_game_reset")

            self.player=Player()
            self.sup_enemy=Super_Enemy()

            self.create_enemies()
            self.enemies.level_changes(self.level)

            self.life1 = Life(700, 50)
            self.life2 = Life(733, 50)
            self.life3 = Life(766, 50)

            self.life_group.add(self.life1,self.life2,self.life3)
            self.player_group.add(self.player)
            self.sup_enemy_group.add(self.sup_enemy)
            self.all_group.add(self.player,self.enemies,self.sup_enemy,self.life1,self.life2,self.life3)

        elif option=="next_level":
            self.reset("next_level_reset")
            self.player.reset_position()
            self.create_enemies()
            self.enemies.level_changes(self.level)

            self.sup_enemy_group.add(self.sup_enemy)
            self.all_group.add(self.enemies)

    def update_all(self):
        currentTime = pygame.time.get_ticks()
        self.player_group.update(self.pressed_keys)
        self.bullet_group.update()
        self.enemy_bullets_group.update()
        self.sup_enemy_group.update(currentTime)
        self.enemies.update()
        self.life_group.update()

    def new_level_screen(self):
        DISPLAY_SCREEN.blit(self.background, (0, 0))
        print_mes(DISPLAY_SCREEN,"LEVEL "+str(self.level),40,GREEN,400,150)
        print_mes(DISPLAY_SCREEN,"Press any key to start",30,GREEN,400,300)
        pygame.display.flip()
        wait = True
        while wait:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    wait = False

    def game_over_screen(self):
        DISPLAY_SCREEN.blit(self.background, (0, 0))
        print_mes(DISPLAY_SCREEN,"GAME OVER!",40,RED,400,150)
        print_mes(DISPLAY_SCREEN,"Pess any key to start a new game",30,RED,400,300)
        pygame.display.flip()
        wait=True
        while wait:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    wait=False
                    self.restart_game=True
                    self.over_screen=False
                    self.game_over=False

    def new_game_screen(self):
        DISPLAY_SCREEN.blit(self.background,(0,0))
        print_mes(DISPLAY_SCREEN, "WELCOME TO SPACE INVADERS", 40, RED, 400, 150)
        print_mes(DISPLAY_SCREEN, "Press any key to start a new game", 30, RED, 400, 300)
        pygame.display.flip()
        wait = True
        while wait:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    wait = False

    def view_score(self):
        print_mes(DISPLAY_SCREEN,"SCORE: {0}".format(self.score),15,GREEN,40,20)
        pygame.display.flip()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
               return True
            else:
                return False

    def execute_logic(self):
        currentTime = pygame.time.get_ticks()

        self.pressed_keys = pygame.key.get_pressed()

        if self.pressed_keys[pygame.K_UP]:
            if (currentTime - self.player.timer) >= self.player.fire_rate and len(self.bullet_group) == 0:
                p_bullet = Bullet(self.player.rect.x + 20, self.player.rect.y + 5, "player", 20)
                self.bullet_group.add(p_bullet)
                pygame.mixer.Sound("shoot.wav").play()
                self.player.timer += self.player.fire_rate
            else:
                pass

        current_Time = pygame.time.get_ticks()
        if (current_Time - self.enemies.timer) >= self.enemies.fire_rate and len(self.enemy_bullets_group) == 0:
            print(self.enemies.alive_indexes)
            if self.enemies.alive_enemies_count<=8 and self.enemies.alive_enemies_count>4:
                how_many_should_fire=5
            elif self.enemies.alive_enemies_count <= 4 and self.enemies.alive_enemies_count != 0:
                how_many_should_fire = self.enemies.alive_enemies_count - 1
            elif self.enemies.alive_enemies_count == 0:
                how_many_should_fire = 0
            else:
                how_many_should_fire = random.randint(4, 8)
            print("shpild fire=", how_many_should_fire)
            print(self.enemies.alive_enemies_count)
            list_of_firing_enemies = random.sample(self.enemies.alive_indexes, how_many_should_fire)
            for enemy_index in list_of_firing_enemies:
                r = enemy_index // 10
                c = enemy_index % 10
                random_speed = random.choice(self.enemies.bullet_speeds)
                enemy_bullet = Bullet(self.enemies.enemies_list[r][c].rect.x + 20,
                                      self.enemies.enemies_list[r][c].rect.y + 5, "enemy", random_speed)
                self.enemy_bullets_group.add(enemy_bullet)
            pygame.mixer.Sound("shoot2.wav").play()
            self.enemies.timer += self.enemies.fire_rate

    def collisions(self):
        for en in pygame.sprite.groupcollide(self.enemies,self.bullet_group,True,True).keys():
            self.score+=en.points_scored
            pygame.mixer.Sound("invaderkilled.wav").play()

        for pl in pygame.sprite.groupcollide(self.player_group,self.enemy_bullets_group,False,True).keys():
            if self.life1.alive():
                self.life1.kill()
            elif self.life2.alive():
                self.life2.kill()
            elif self.life3.alive():
                self.life3.kill()
                pl.kill()
                self.over_screen=True
                self.score = 0

        for sup in pygame.sprite.groupcollide(self.sup_enemy_group,self.bullet_group,True,True).keys():
            sup=Super_Enemy()
            self.all_group.add(sup)
            self.score+=200
            self.sup_enemy_group.add(sup)

    def run_game(self):

        if self.new_game:
            self.init_new_game()
            self.new_game_screen()

            self.new_level_screen()
            self.create_level("new_game")

            self.level=0

            self.next_level=False
            self.new_game=False

        if self.restart_game:
            #self.reset("new_game_reset")
            self.new_level_screen()
            self.level=0
            self.create_level("new_game")
            self.next_level=False
            self.restart_game=False

        if self.over_screen:
            self.level=0
            self.game_over=True
            self.game_over_screen()

        if self.next_level:
            #self.reset("next_level_reset")
            self.new_level_screen()
            self.create_level("next_level")
            self.next_level=False

        if not self.game_over:

            self.execute_logic()

            self.collisions()

            self.update_all()

            if self.enemies.alive_enemies_count==0 and self.player.alive():
                self.next_level=True
                self.level+=1

    def display(self):

        if not self.game_over:
            self.all_group.draw(DISPLAY_SCREEN)
            self.view_score()
        pygame.display.flip()

def main():

    pygame.init()
    bg=pygame.image.load("space.png")
    bg=pygame.transform.scale(bg,(800,600))
    pygame.display.set_caption("Space invaders by Andriei Gensh")
    DISPLAY_SCREEN.blit(bg, (0, 0))
    over = False

    game_instance=Game()

    while not over:
        DISPLAY_SCREEN.blit(bg,(0,0))
        over=game_instance.process_events()

        game_instance.run_game()

        game_instance.display()

        game_instance.clock.tick(game_instance.fps)

    pygame.quit()

if __name__=="__main__":
    main()