import random

import pygame

import assets

WHITE = (255, 255, 255)
GREEN = (78, 255, 87)
YELLOW = (241, 255, 0)
BLUE = (80, 255, 239)
PURPLE = (203, 0, 255)
RED = (237, 28, 36)
# these are the constants that describe the direction of
# a moving object
DOWN = 1
UP = -1

FONT_NAME = pygame.font.match_font("arial")
DISPLAY_SCREEN = pygame.display.set_mode((800, 600))

"""
It is crucial to remember, that every "pygame.sprite.Sprite" child
class should define its own "self.rect" field as well as "update()"
function, so that the other pygame module functions such as draw(), 
spritecollide() etc. could work properly. For detailed information 
read the official pygame.sprite.Sprite documentation on 
https://www.pygame.org/docs/ref/sprite.html
"""


def print_message(screen, message, size, colour, x_position, y_position):
    """ Function prints out a message in a specified position on the screen
    screen - object, that pygame.display.set_mode() returns
    message - message you would like to be printed
    size - font size of the text
    colour - text colour
    x_pos, y_pos - position of the message on the screen
    """
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(message, True, colour)
    text_rectangle = text_surface.get_rect()
    text_rectangle.midtop = (x_position, y_position)
    screen.blit(text_surface, text_rectangle)


class Life(pygame.sprite.Sprite):
    """
    Player's life class.
    """

    def __init__(self, position_x, position_y):
        super().__init__()
        """
        Initializes the object.
        position_x, positions_y - obvious
        """
        self.image = assets.Assets.SHIP_IMAGE
        self.image = pygame.transform.scale(self.image, (23, 23))
        self.rect = self.image.get_rect(topleft=(position_x, position_y))
        self.state = True  # alive or not

    def update(self):
        """
        Updates the sprite on the screen
        """
        DISPLAY_SCREEN.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
    """
    Bullet class. Used by both enemies and player. Depends on
    the value of "master" field.
    """

    def __init__(self, center_x, center_y, who_shoots, speed):
        super().__init__()

        self.image = assets.Assets.LASER_IMAGE
        self.rect = self.image.get_rect(topleft=(center_x, center_y))
        self.master = who_shoots
        if self.master == "player":
            self.direction = UP
        else:
            self.direction = DOWN
        self.speed = speed

    def update(self):
        """
        Updates the position of the bullet once it was created. If it
        reaches the screen borders - it "dies"
        """
        DISPLAY_SCREEN.blit(self.image, self.rect)
        self.rect.y += self.direction * self.speed
        if self.direction == UP:
            if self.rect.y <= 20:
                self.kill()
        else:
            if self.rect.y >= 580:
                self.kill()


class Player(pygame.sprite.Sprite):
    """
    Implements player class.
    A player is basically a ship that moves, shoots and scores points
    for killing enemies
    """

    def __init__(self):
        """
        image - player's ship image
        rectangle - sprite dimensions
        movement_speed - how fast a player can move. Defines the distance
                                (in pixels) that a ship can travel at once
        fire_rate - minimum delay before firing
        timer - serves as a timer (works in pair with the fire_rate field)
        """
        super().__init__()

        self.image = assets.Assets.PLAYER_IMAGE
        self.rect = self.image.get_rect(topleft=(370, 550))
        self.movement_speed = 5
        self.fire_rate = 100
        self.timer = pygame.time.get_ticks()

    def reset_position(self):
        """
        Resets players position on the screen
        """
        self.rect.x = 370
        self.rect.y = 550

    def update(self, pressed_keys):
        """
        Updates players position and prevents it from crossing the
        screen borders
        :param pressed_keys: obvious, the keys that are currently pressed
        """
        if pressed_keys[pygame.K_LEFT]:
            if self.rect.x >= 20:
                self.rect.x -= self.movement_speed
                DISPLAY_SCREEN.blit(self.image, self.rect)
        elif pressed_keys[pygame.K_RIGHT]:
            if self.rect.x <= 740:
                self.rect.x += self.movement_speed
                DISPLAY_SCREEN.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    """
    Implements an enemy class. It can move, shoot, and be killed
    """
    # timer that every enemy shares, a necessary evil
    timer = pygame.time.get_ticks()

    def __init__(self, row, column):
        """
        Initializes the enemy object. Sets its position on the screen
        (depends on the row and the column),
        image and so on
        :param row: what row is an enemy in
        :param column: what column is an enemy in
        """
        super().__init__()
        if row == 0:
            self.image = assets.Assets.ENEMY_1_IMAGE
            self.images = assets.Assets.ENEMY_1_ANIMATION
            self.death_image = assets.Assets.ENEMY_1_DEATH
        elif row == 2:
            self.image = assets.Assets.ENEMY_2_IMAGE
            self.images = assets.Assets.ENEMY_2_ANIMATION
            self.death_image = assets.Assets.ENEMY_2_DEATH
        else:
            self.image = assets.Assets.ENEMY_3_IMAGE
            self.images = assets.Assets.ENEMY_3_ANIMATION
            self.death_image = assets.Assets.ENEMY_3_DEATH
        self.image = pygame.transform.scale(self.image, (40, 35))
        self.rect = self.image.get_rect()
        self.rect.x = 35 + 60 * column
        self.rect.y = 30 + 75 * row
        self.row = row
        self.column = column
        self.points_scored = 50

    def update(self):
        """
        Updates enemy o the screen
        """
        DISPLAY_SCREEN.blit(self.image, self.rect)


class EnemyGroup(pygame.sprite.Group):
    """
    Implements an enemy group. useful way of managing
    many enemies at once
    """

    def __init__(self):
        """
        Initializes the enemy group, which basically consists
        of many other enemies.
        Sets their's positions, general fire rate, movement
        speed and so on
        """
        super().__init__()
        self.rows = 3
        self.columns = 10
        # useful to now how many enemies are still alive
        self.alive_enemies_count = self.rows * self.columns
        # alive enemies indexes( actually coded in a very simple way)
        self.alive_indexes = [x for x in range(0, 30, 1)]
        # the actual enemies list
        self.enemies_list = [[None for _ in range(self.columns)]
                             for _ in range(self.rows)]
        self.right_column_index = 9
        self.left_column_index = 0
        self.direction = DOWN
        self.fire_rate = 3000
        # different bullets speeds to chose from
        self.bullet_speeds = [7, 10, 12, 15]

        self.down_speed = 30
        self.left_right_speed = 30
        self.move_time = 600

        self.frame_counter = 0

        self.move_timer = pygame.time.get_ticks()
        self.timer = pygame.time.get_ticks()
        self.delay_timer = pygame.time.get_ticks()

    def reset_group_parameters(self):
        """
        Resets the group totally.
        """
        self.rows = 3
        self.columns = 10
        self.alive_enemies_count = self.rows * self.columns
        self.alive_indexes = [x for x in range(0, 30, 1)]
        self.enemies_list = [[None for _ in range(self.columns)]
                             for _ in range(self.rows)]
        self.right_column_index = 9
        self.left_column_index = 0
        self.direction = DOWN
        self.left_right_speed = 30
        self.move_time = 600

    def level_changes(self, current_level):
        """
        Changes enemies characteristics depending on the current level
        of hte game
        :param current_level: game level
        """
        self.move_time -= current_level * 20

    def check_border_columns(self):
        """
        Important function. Checks whether or not the enemy group
        has reached the borders of the screen. Also determines
        the very left and very right enemies column, so it would
        be easier to check, if the group has crossed the screen
        borders or not. This function is called every time any
        enemy dies
        """
        if self.alive_enemies_count == 0:
            return
        any_left = False
        any_right = False
        found_left = False
        found_right = False
        for i in range(0, self.rows):
            if self.enemies_list[i][self.left_column_index] is not None:
                any_left = True
                break
        if not any_left:
            for column in range(self.left_column_index,
                                self.right_column_index + 1):
                if found_left:
                    break
                for row in range(0, self.rows):
                    if isinstance(self.enemies_list[row][column], Enemy):
                        self.left_column_index = column
                        found_left = True
                        break

        for i in range(0, self.rows):
            if self.enemies_list[i][self.right_column_index] is not None:
                any_right = True
                break
        if not any_right:
            for column in range(self.right_column_index,
                                self.left_column_index - 1, -1):
                if found_right:
                    break
                for row in range(0, self.rows):
                    if isinstance(self.enemies_list[row][column], Enemy):
                        self.right_column_index = column
                        found_right = True
                        break

    def add_internal(self, *sprite):
        """
        Overridden sprite class function. Defines the way an enemy
        should be added
        :param sprite: basically it is an enemy object that is about
         to be added
        """
        super().add_internal(*sprite)
        for new_sprite in sprite:
            self.enemies_list[new_sprite.row][new_sprite.column] = new_sprite

    def remove_internal(self, *sprite):
        """
        Overridden sprite class function. Defines the way an enemy
        should be deleted
        :param sprite: basically it is an enemy that is killed but not
        yet deleted from the group
        """
        super().remove_internal(*sprite)
        for new_sprite in sprite:
            self.enemies_list[new_sprite.row][new_sprite.column] = None
            self.alive_indexes.remove((new_sprite.row * 10 + new_sprite.column))
            self.alive_enemies_count -= 1
            self.check_border_columns()

    def update(self):
        """
        Updated each enemies position if it is the right time
        """
        self.move_time = 600 - (30 - self.alive_enemies_count) * 15

        current_time = pygame.time.get_ticks()
        if current_time - self.move_timer >= self.move_time:
            self.frame_counter = (self.frame_counter + 1) % 2
            for enemy in self:
                enemy.rect.x += self.direction * self.left_right_speed
                enemy.image = enemy.images[self.frame_counter]
            if self.direction == DOWN:
                for row in range(0, self.rows):
                    if isinstance(self.enemies_list[row][self.right_column_index], Enemy):
                        if self.enemies_list[row][self.right_column_index].rect.x >= 725:
                            self.direction = UP
                            for enemy in self:
                                enemy.rect.y += self.down_speed
                        break
            else:
                for row in range(0, self.rows):
                    if isinstance(self.enemies_list[row][self.left_column_index], Enemy):
                        if self.enemies_list[row][self.left_column_index].rect.x <= 35:
                            self.direction = DOWN
                            for enemy in self:
                                enemy.rect.y += self.down_speed
                        break

            for enemy in self:
                enemy.update()
            self.move_timer = pygame.time.get_ticks()


class SuperEnemy(pygame.sprite.Sprite):
    """
    Super enemy class. Moves faster then any enemy, when
    killed by player -gives additional points
    """

    def __init__(self):
        """
        Initializes the SuperEnemy class with an image, speed,
        position and so on.
        No arguments needed to be passed
        """
        super().__init__()

        self.image = assets.Assets.MYSTERY_IMAGE
        self.image = pygame.transform.scale(self.image, (50, 35))
        self.rect = self.image.get_rect()
        self.rect.x = -70
        self.rect.y = 30
        self.speed = 6
        self.direction = DOWN

        self.points_scored = 500
        self.show_up_time = 20000
        self.timer = pygame.time.get_ticks()

    def update(self, current_time):
        """
        Updates Superenemy's position on the screen
        :param current_time: Current time of the game. Is
        used along with a timer class field to define, if
        a superenemy is allowed to move
        """
        time = current_time - self.timer
        if time >= self.show_up_time:
            assets.Assets.MYSTERY_SOUND.play()
            if self.direction == DOWN:
                self.rect.x += self.speed
                if self.rect.x >= 800:
                    self.direction = UP
                    self.rect.x = 870
                    self.timer = pygame.time.get_ticks()
            else:
                self.rect.x -= self.speed
                if self.rect.x <= -30:
                    self.rect.x = -100
                    self.direction = DOWN
                    self.timer = pygame.time.get_ticks()


class Game(object):
    """
    Main game class. Supervises every game element:
    creates instances of need classes, applies game
    logic, supervises possible events
    """

    def __init__(self):
        """
        Initialization function. Sets all needed fields (mostly
        to None value). Not every field is initialized with a
        certain value immediately, mostly it is just a
        "declaration" of a field rather then its definition.
        """

        self.score = 0  # points that player can score
        self.level = 0  # current game level
        self.pressed_keys = None  # list of currently pressed keys
        # loads a needed background image
        self.background = assets.Assets.BACK_GROUND
        self.background = pygame.transform.scale(self.background,
                                                 (800, 600))
        self.dim_screen = pygame.Surface(DISPLAY_SCREEN.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        self.player = None
        self.super_enemy = None
        self.enemies = None

        self.life1 = None
        self.life2 = None
        self.life3 = None

        # declaration of all the necessary sprite groups
        # (as empty for now)

        self.all_group = None
        self.life_group = None
        self.player_group = None
        self.super_enemy_group = None
        self.bullet_group = None
        self.enemy_bullets_group = None

        # so called "ruling" boolean fields. Define if the game is
        # started, if it is to be continued and so on

        self.game_over = False
        self.over_screen = False
        self.new_game = True
        self.next_level = True
        self.restart_game = False
        self.paused = False

        self.clock = pygame.time.Clock()  # ingame clock
        self.fps = 60  # game frames per second

    def reset(self, option):
        """
        Resets everything that should be reset.
        What exactly should be reset defines the option argument
        :param option: Defines the reset mode. If the reset is
        of a "new_game_reset" kind, then nearly every group is
        reset in order to start a new game. If the reset is of a
        "next_level_reset" kind, then only several sprite groups
        are reset in order to clear previous level and to start
        a new one.
        """
        if option == "new_game_reset":
            self.player_group.empty()
            self.enemy_bullets_group.empty()
            self.enemies.empty()
            self.enemies = EnemyGroup()
            self.super_enemy_group.empty()
            self.bullet_group.empty()
            self.life_group.empty()
            self.all_group.empty()
            self.enemies.reset_group_parameters()
            pygame.display.flip()
        elif option == "next_level_reset":
            self.enemies.empty()
            self.enemies = EnemyGroup()
            self.enemies.reset_group_parameters()
            self.bullet_group.empty()
            self.enemy_bullets_group.empty()
            self.super_enemy_group.empty()
            pygame.display.flip()

    def init_new_game(self):
        """
        __init__ method was a "declaration", this is the
        "definition" of class fields. It is called upon
        only if the game is to start. Otherwise there is no
        need to initialize variables and class fields.
        """
        self.enemies = EnemyGroup()

        self.all_group = pygame.sprite.Group()
        self.life_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.super_enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_bullets_group = pygame.sprite.Group()

    def create_enemies(self):
        """
        Creates enemies matrix on the screen.
        Called upon every time a new game or a new level starts
        """

        for i in range(self.enemies.rows):
            for j in range(self.enemies.columns):
                new_enemy = Enemy(i, j)
                self.enemies.add(new_enemy)

    def create_level(self, option):

        """
        Creates a new game level. Option argument defines the
        behavior and the kind of this new level.
        :param option: If "new_game" - a new player and new enemies
        are created, but before a suitable reset method is called upon
        to prepare everything. If "next_level" - a player is not being
        reset (he/she remains untouched with all the remaining lifes),
        however enemies are being reset and a suitable reset method
        is called upon
        """

        if option == "new_game":
            self.reset("new_game_reset")

            self.player = Player()
            self.super_enemy = SuperEnemy()

            self.create_enemies()
            self.enemies.level_changes(self.level)

            self.life1 = Life(700, 50)
            self.life2 = Life(733, 50)
            self.life3 = Life(766, 50)

            self.life_group.add(self.life1, self.life2, self.life3)
            self.player_group.add(self.player)
            self.super_enemy_group.add(self.super_enemy)
            self.all_group.add(self.player, self.enemies, self.super_enemy,
                               self.life1, self.life2, self.life3)

        elif option == "next_level":
            self.reset("next_level_reset")
            self.player.reset_position()
            self.create_enemies()
            self.enemies.level_changes(self.level)

            self.super_enemy_group.add(self.super_enemy)
            self.all_group.add(self.enemies)

    def update_all(self):
        """
        Updates sprites in all the groups
        """
        current_time = pygame.time.get_ticks()
        self.player_group.update(self.pressed_keys)
        self.bullet_group.update()
        self.enemy_bullets_group.update()
        self.super_enemy_group.update(current_time)
        self.enemies.update()
        self.life_group.update()

    def pause_screen(self):
        """
        Creates a new screen with a message that informs about a pause
        of thr game. The game is paused and will remain so unless
        player pressed any key
        """
        DISPLAY_SCREEN.blit(self.dim_screen, (0, 0))
        print_message(DISPLAY_SCREEN, "Paused", 40, GREEN, 400, 300)
        pygame.display.flip()
        wait = True
        while wait:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = False
                        wait = False

    def new_level_screen(self):
        """
        Creates a new screen with a message that informs about a start
        of a new level. The game is paused and will remain so unless
        player pressed any key
        """
        DISPLAY_SCREEN.blit(self.background, (0, 0))
        print_message(DISPLAY_SCREEN, "LEVEL " + str(self.level), 40,
                      GREEN, 400, 150)
        print_message(DISPLAY_SCREEN, "Press any key to start", 30,
                      GREEN, 400, 300)
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
        """
        Creates a new screen with a message that informs about
        a "game over". The game is paused and will remain so
        unless player pressed any key
        """
        DISPLAY_SCREEN.blit(self.background, (0, 0))
        print_message(DISPLAY_SCREEN, "GAME OVER!", 40, RED, 400, 150)
        print_message(DISPLAY_SCREEN, "Press any key to start a new game",
                      30, RED, 400, 300)
        pygame.display.flip()
        wait = True
        while wait:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    wait = False
                    self.restart_game = True
                    self.over_screen = False
                    self.game_over = False

    def new_game_screen(self):
        """
        Creates a new screen with a message that informs about a start
        of a new game. The game is paused and will remain so unless
        player pressed any key
        """
        DISPLAY_SCREEN.blit(self.background, (0, 0))
        print_message(DISPLAY_SCREEN, "WELCOME TO SPACE INVADERS", 40,
                      RED, 400, 150)
        print_message(DISPLAY_SCREEN, "Press any key to start a new game", 30,
                      RED, 400, 300)
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
        """
        Prints a score on the screen
        """
        print_message(DISPLAY_SCREEN, "SCORE: {0}".format(self.score), 15,
                      GREEN, 40, 20)
        pygame.display.flip()

    def process_events(self):
        """
        Handles necessary game events
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                return False

    def execute_logic(self):
        """
        Most important part of the game class. Runs the game logic,
        manages sprite groups and so on
        """
        current_time = pygame.time.get_ticks()
        self.pressed_keys = pygame.key.get_pressed()
        if self.pressed_keys[pygame.K_UP]:
            if ((current_time - self.player.timer) >=
                    self.player.fire_rate and len(self.bullet_group) == 0):
                player_bullet = Bullet(self.player.rect.x + 20,
                                       self.player.rect.y + 5, "player", 20)
                self.bullet_group.add(player_bullet)
                assets.Assets.SHOOT_SOUND.play()
                self.player.timer += self.player.fire_rate
            else:
                pass

        current_time = pygame.time.get_ticks()
        if ((current_time - self.enemies.timer) >= self.enemies.fire_rate
                and len(self.enemy_bullets_group) == 0):
            if 8 >= self.enemies.alive_enemies_count > 4:
                how_many_should_fire = 5
            elif (self.enemies.alive_enemies_count <= 4 and
                  self.enemies.alive_enemies_count != 0):
                how_many_should_fire = self.enemies.alive_enemies_count - 1
            elif self.enemies.alive_enemies_count == 0:
                how_many_should_fire = 0
            else:
                how_many_should_fire = random.randint(4, 8)

            list_of_firing_enemies = random.sample(self.enemies.alive_indexes,
                                                   how_many_should_fire)

            for enemy_index in list_of_firing_enemies:
                row = enemy_index // 10
                column = enemy_index % 10
                random_speed = random.choice(self.enemies.bullet_speeds)
                enemy_bullet = Bullet(self.enemies.enemies_list[row][column].rect.x + 20,
                                      self.enemies.enemies_list[row][column].rect.y + 5,
                                      "enemy", random_speed)
                self.enemy_bullets_group.add(enemy_bullet)
            assets.Assets.ENEMY_SHOOT_SOUND.play()
            self.enemies.timer = current_time

    def check_enemies_positions(self):
        """
        Checks if any of the enemies has crossed "the line". If
        the enemy's y coordinate is greater or equal to 510
        (basically the lower gamescreen border) - it means, that
        player has failed to protect the Earth from the invaders
        and the game ends
        """
        for enemy in self.enemies:
            if enemy.rect.y >= 510:
                self.player.kill()
                self.score = 0
                self.over_screen = True
                break

    def collisions(self):
        """
        Checks for the possible collisions of different sprites
        and manages their "deaths"
        """
        for enemy in pygame.sprite.groupcollide(self.enemies,
                                                self.bullet_group, False, True).keys():
            self.score += enemy.points_scored
            assets.Assets.DEATH_SOUND.play()
            enemy.image = enemy.death_image
            enemy.update()
            enemy.kill()

        for player in pygame.sprite.groupcollide(self.player_group,
                                                 self.enemy_bullets_group, False, True).keys():
            if self.life1.alive():
                self.life1.kill()
            elif self.life2.alive():
                self.life2.kill()
            elif self.life3.alive():
                self.life3.kill()
                player.kill()
                self.over_screen = True
                self.score = 0

        for super_enemy in pygame.sprite.groupcollide(self.super_enemy_group,
                                                      self.bullet_group, True, True).keys():
            super_enemy = SuperEnemy()
            self.all_group.add(super_enemy)
            self.score += 200
            self.super_enemy_group.add(super_enemy)

    def run_game(self):
        """Basically a place where everything comes together"""

        if self.new_game:
            self.init_new_game()
            self.new_game_screen()
            self.new_level_screen()
            self.create_level("new_game")
            self.level = 0
            self.next_level = False
            self.new_game = False

        if self.restart_game:
            self.new_level_screen()
            self.level = 0
            self.create_level("new_game")
            self.next_level = False
            self.restart_game = False

        if self.over_screen:
            self.level = 0
            self.game_over = True
            self.reset("new_game_reset")
            self.game_over_screen()

        if self.next_level:
            self.new_level_screen()
            self.create_level("next_level")
            self.next_level = False

        if self.paused:
            self.pause_screen()

        if not self.game_over:
            if not self.paused:
                self.execute_logic()
                self.collisions()
                self.update_all()
                self.check_enemies_positions()
                if self.enemies.alive_enemies_count == 0 and \
                        self.player.alive():
                    self.next_level = True
                    self.level += 1

    def display(self):
        """
        Displays sprites on the screen
        """

        if not self.game_over:
            self.all_group.draw(DISPLAY_SCREEN)
            self.view_score()
        pygame.display.flip()


def main():
    """
    Main function. Creates the instance of the game, sets
    the DISPLAY variable.
    """
    pygame.init()
    assets.Assets.load()
    back_ground = pygame.transform.scale(assets.Assets.BACK_GROUND, (800, 600))
    pygame.display.set_caption("Space invaders by Andriei Gensh")
    DISPLAY_SCREEN.blit(back_ground, (0, 0))
    over = False
    game_instance = Game()

    while not over:
        DISPLAY_SCREEN.blit(back_ground, (0, 0))
        over = game_instance.process_events()
        game_instance.run_game()
        game_instance.display()
        game_instance.clock.tick(game_instance.fps)
    pygame.quit()


if __name__ == "__main__":
    main()
