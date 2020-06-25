import pygame


class Assets:
    """
    This class is used to load all the necessary images,
    sound and so one at once, so there would be no
    need to load them manually every time
    """

    @staticmethod
    def load():
        """
        This is a loading method itself.
        The method is static so that we do not need to create an
        object of this class in order to get access to the loaded data
        """
        # initialize pygame here so that you don`t need to do
        # it every time in every module you are using this file
        pygame.init()
        # ships images loaded here
        Assets.PLAYER_IMAGE = pygame.image.load("images/ship.png")
        Assets.SHIP_IMAGE = pygame.image.load("images/ship.png")
        Assets.LASER_IMAGE = pygame.image.load("images/laser.png")
        Assets.MYSTERY_IMAGE = pygame.transform.scale(
            pygame.image.load("images/sup_enemy.png"), (50, 35))
        # enemy one (purple) images and animation loaded here
        Assets.ENEMY_1_IMAGE = pygame.image.load("images/enemy1.png")
        Assets.ENEMY_1_ANIMATION = [pygame.transform.scale(
            pygame.image.load("images/enemy1.png"), (40, 35)),
            pygame.transform.scale(pygame.image.load("images/enemy1_2.png"), (40, 35))]
        Assets.ENEMY_1_DEATH = pygame.transform.scale(pygame.image.load(
            "images/explosionpurple.png"), (40, 35))
        # enemy two (blue) images and animation loaded here
        Assets.ENEMY_2_IMAGE = pygame.image.load("images/enemy2.png")
        Assets.ENEMY_2_ANIMATION = [pygame.transform.scale(
            pygame.image.load("images/enemy2.png"), (40, 35)),
            pygame.transform.scale(pygame.image.load("images/enemy2_2.png"), (40, 35))]
        Assets.ENEMY_2_DEATH = pygame.transform.scale(pygame.image.load(
            "images/explosionblue.png"), (40, 35))
        Assets.BACK_GROUND = pygame.image.load("images/space.png")
        # enemy three (green) images and animation loaded here
        Assets.ENEMY_3_IMAGE = pygame.image.load("images/enemy3.png")
        Assets.ENEMY_3_ANIMATION = [pygame.transform.scale(pygame.image.load(
            "images/enemy3.png"), (40, 35)),
            pygame.transform.scale(pygame.image.load("images/enemy3_2.png"), (40, 35))]
        Assets.ENEMY_3_DEATH = pygame.transform.scale(pygame.image.load(
            "images/explosiongreen.png"), (40, 35))
        # sound loaded here
        Assets.MYSTERY_SOUND = pygame.mixer.Sound("sounds/mystery.wav")
        Assets.SHOOT_SOUND = pygame.mixer.Sound("sounds/shoot.wav")
        Assets.ENEMY_SHOOT_SOUND = pygame.mixer.Sound("sounds/shoot2.wav")
        Assets.DEATH_SOUND = pygame.mixer.Sound("sounds/invaderkilled.wav")
