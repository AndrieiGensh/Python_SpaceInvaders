import Space_invaders
import unittest
import random


class EnemyGroupTest (unittest.TestCase):

    enemygroup = Space_invaders.EnemyGroup()

    def test_level_changes(self):
        """
        Test how the movement of enemies changes depending on the current game level
        """
        self.enemygroup = Space_invaders.EnemyGroup()
        self.enemygroup.level_changes(10)
        self.assertEqual(self.enemygroup.move_time, 600 - 20*10)

    def test_reset(self):
        """
        Tests the functionality of the reset method for the enemy group
        """
        self.enemygroup.direction = 10
        self.enemygroup.move_time = 0
        self.enemygroup.left_right_speed = -500

        self.enemygroup.reset_group_params()

        self.assertEqual(self.enemygroup.direction, 1)
        self.assertEqual(self.enemygroup.move_time, 600)
        self.assertEqual(self.enemygroup.left_right_speed, 30)
        self.assertTrue((self.enemygroup.right_column_index == 9) and (self.enemygroup.left_column_index == 0))

        index = random.randint(0, 29)

        self.assertTrue(self.enemygroup.enemies_list[int(index/10)][int(index%10)] is None)

    def test_check_borders(self):
        """
        Tests the behavior of the borders checking method. Simulated situation -
        there is only one enemy left alive
        """
        index = random.randint(0, 29)

        self.enemygroup.reset_group_params()

        self.enemygroup.enemies_list[int(index/10)][int(index%10)] = Space_invaders.Enemy(int(index/10),int(index%10))

        self.enemygroup.check_border_columns()

        self.assertTrue((self.enemygroup.right_column_index == int(index%10))
                        and (self.enemygroup.left_column_index == int(index%10)))

    def test_movement_speed_changes(self):
        """
        Tests how an enemy's movement speed changes, depending on
        how many of then left alive
        """

        self.enemygroup.reset_group_params()

        self.assertTrue(self.enemygroup.move_time == 600)

        self.enemygroup.alive_enemies_count = 10

        self.enemygroup.update()

        self.assertTrue(self.enemygroup.move_time == (600 - 15 * (30 - 10)))
