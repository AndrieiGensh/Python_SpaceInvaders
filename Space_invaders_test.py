"""Tests for Space_invaders EnemyGroup module"""

import Space_invaders
import assets
import pygame
import unittest
import random


class EnemyGroupTest(unittest.TestCase):
    def setUp(self):
        self.enemygroup = Space_invaders.EnemyGroup()
        # load the assets so that the tests could run properly
        assets.Assets.load()

    def test_level_changes(self):
        self.enemygroup.level_changes(10)
        self.assertEqual(self.enemygroup.move_time, 600 - 20 * 10)

    def test_reset(self):
        self.enemygroup.direction = 10
        self.enemygroup.move_time = 0
        self.enemygroup.left_right_speed = -500
        self.enemygroup.reset_group_parameters()
        self.assertEqual(self.enemygroup.direction, 1)
        self.assertEqual(self.enemygroup.move_time, 600)
        self.assertEqual(self.enemygroup.left_right_speed, 30)
        self.assertTrue(self.enemygroup.right_column_index == 9)
        self.assertTrue(self.enemygroup.left_column_index == 0)
        index = random.randint(0, 29)
        self.assertIsNone(self.enemygroup.enemies_list[int(index / 10)][int(index % 10)])

    def test_check_borders(self):
        index = random.randint(0, 29)
        self.enemygroup.reset_group_parameters()
        self.enemygroup.enemies_list[int(index / 10)][int(index % 10)] = Space_invaders.Enemy(
            int(index / 10), int(index % 10))
        self.enemygroup.check_border_columns()
        self.assertTrue(self.enemygroup.right_column_index == int(index % 10))
        self.assertTrue(self.enemygroup.left_column_index == int(index % 10))

    def test_add_internal(self):
        self.enemygroup.empty()
        for row in range(2):
            for column in range(4):
                self.enemygroup.add(Space_invaders.Enemy(row, column))
        amount = 0
        for potential_enemy in self.enemygroup:
            if isinstance(potential_enemy, Space_invaders.Enemy):
                amount += 1
        self.assertEqual(amount, 8)

    def test_remove_internal(self):
        self.enemygroup.reset_group_parameters()
        for i in range(self.enemygroup.rows):
            for j in range(self.enemygroup.columns):
                new_enemy = Space_invaders.Enemy(i, j)
                self.enemygroup.add(new_enemy)

        for row in range(2):
            for column in range(4):
                self.enemygroup.enemies_list[row][column].kill()
        self.assertEquals(self.enemygroup.alive_enemies_count, 22)
        self.assertTrue(len(self.enemygroup.alive_indexes) == 22)


if __name__ == '__main__':
    unittest.main()
