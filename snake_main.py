import game_display
import game_parameters
import snake
from game_display import GameDisplay
from bomb import Bomb
import bomb
from snake import Snake
import apple
from typing import *


class Game:
    Hight = game_parameters.HEIGHT
    Width = game_parameters.WIDTH
    Apple_color = 'green'  # TODO האם צריך לרשום את זה מחוץ לאינט או בתוכו
    Snake_color = 'Black'
    Bomb_color = 'red'
    Blast_color = 'orange'

    def __init__(self):
        self.snake = Snake()  # TODO change to now see
        self.__bomb = None
        self.__apples = []
        self.__score = 0

    def in_board(self, x, y):
        """
        function that tell if we are in the board
        :param col: object row
        :param row: object row
        :return: True if in the board and False else
        """
        in_Width = -1 < x and x < self.Width
        in_Hight = -1 < y and y < self.Hight
        return in_Width and in_Hight

    def bomb_blasts(self) -> List[Tuple]:
        blast = list()
        if self.__bomb.get_time() < 0:
            blast = self.__bomb.blast_cords()
        return blast

    def cell_empty(self, x, y) -> bool:
        """
        check if cell is empty
        :param x: row number of object
        :param y: col number of object
        :return: True ig cell empty and False if not
        """
        all: List = []
        all += self.snake.get_locations()
        all += [apple.get_location for apple in self.__apples]
        if self.__bomb:
            all += self.__bomb.blast_cords()
            all += self.__bomb.get_location()
        if (x, y) in all:
            return False
        return True

    def draw(self, gd):
        for loc in self.snake.get_locations():
            gd.draw_cell(loc[0], loc[1], self.Snake_color)
        for apple_row, apple_col in self.apples_cells():
            gd.draw_cell(apple_row, apple_col, self.Apple_color)
        if self.__bomb.get_time() > 0:
            bomb_row = self.__bomb.get_location()[0]
            bomb_col = self.__bomb.get_location()[1]
            gd.draw_cell(bomb_row, bomb_col, self.Bomb_color)
        else:
            blast_cords_list = self.__bomb.blast_cords()
            for blast_row, blast_col in blast_cords_list:
                if self.in_board(blast_row, blast_col):
                    gd.draw_cell(blast_row, blast_col, self.Blast_color)

    ##### snake part  #####

    def get_snake(self):
        return self.snake

    def set_initial_snake(self) -> None:
        self.snake.add_new_head((10, 10))
        self.snake.add_new_head((9, 10))
        self.snake.add_new_head((8, 10))

    def move_snake(self):
        """
        moves snake one step in given direction.
        :param movekey: Key of move in snake to activate
        :return: True upon success, False otherwise
        """
        tail = self.snake.move()
        row_head = self.snake.get_head()[0]
        col_head = self.snake.get_head()[1]
        # בדיקה האם הנחש הגיע לתא שנמצא ברשימה השחורה או אם חרג מהלוח
        if self.__bomb and (row_head, col_head) == self.__bomb.get_location or \
                (row_head, col_head) in self.__bomb.blast_cords or \
                row_head > self.Hight or row_head < 0 or \
                col_head > self.Width or col_head < 0:
            return
        return tail

    def eat_apple(self, tail):
        self.snake.add_to_tail(tail)

    ####### Bomb part  #########

    def get_bomb(self):
        return self.__bomb

    def add_bomb(self) -> None:
        while not self.__bomb:
            bomb: Bomb = Bomb()
            bomb.set_bomb()
            x, y = bomb.get_location()
            if self.cell_empty(x, y) and self.in_board(x, y):
                self.__bomb = bomb


    def bomb_cells(self) -> List[Tuple]:
        bomb_list = list()
        for bomb in self.__bomb:
            bomb_list.append(bomb.get_location())
        return bomb_list

    def remove_bomb(self) -> None:
        self.__bomb = None

    ######## apple part  #########

    def set_score(self, score) -> None:
        self.__score += score

    def get_score(self) -> int:
        return self.__score

    def apples_list(self):
        return self.__apples

    def remove_apple(self, apple) -> None:
        self.__apples.remove(apple)

    def add_apples(self) -> None:
        """
        function that sets 3 apple in self.__apples
        :return: None
        """
        while len(self.__apples) < 3:
            iphon = apple.Apple()
            iphon.set_apple()
            iphon.set_color(self.Apple_color)
            (x, y) = iphon.get_location()
            if self.cell_empty(x, y) and self.in_board(x,
                                                       y):  # TODO function that collactiong the snake and bomb cells
                self.__apples.append(iphon)

    def apples_cells(self) -> List[Tuple]:
        """
        :return: return apples cells
        """
        apples_list = list()
        for apple in self.__apples:
            apple_row = apple.get_location()[0]
            apple_col = apple.get_location()[1]
            apples_list.append((apple_row, apple_col))
        return apples_list


def main_loop(gd: GameDisplay) -> None:
    game = Game()
    game.set_initial_snake()
    game.add_bomb()
    gd.show_score(game.get_score())
    game.add_apples()
    count_increase = 0
    tail = None
    while True:
        snake = game.get_snake()
        bomb = game.get_bomb()
        apples = game.apples_list()

        # Getting input from the user
        key_clicked = gd.get_key_clicked()
        if key_clicked:
            snake.set_orientation(key_clicked)

        # If the snake ate an apple in the previous round - we will add the tail
        if count_increase > 0 and tail:
            game.eat_apple(tail)
            count_increase -= 1

        # The snake is advanced in the direction defined for it
        # + saving tha removed tail
        tail = snake.move()

        # check if snake run into himself or run into bomb or run out of board
        if snake.get_head() in snake.get_locations()[1:] or\
                snake.get_head() == bomb.get_location or\
                not game.in_board(snake.get_head()[0], snake.get_head()[0]):
            # TODO board with game over
            break

        # check if snake eat an apple
        for apple in apples:
            if snake.get_head() == apple.get_location():
                count_increase += 3
                game.set_score(apple.get_score())
                game.remove_apple(apple)

        bomb.time_getting_smaller()
        # if bomb time up
        if bomb.get_time() <= 0:
            # if bomb finish her life (blast == radius)
            if -bomb.get_time() > bomb.get_redius():
                game.remove_bomb()
            # if not - check if it's blast hit something
            else:
                # if blast hit the snake
                if set(snake.get_locations()) & set(bomb.blast_cords()):
                    break
                for apple in apples:
                    # if blast hit an apple
                    if apple.get_location() in bomb.blast_cords():
                        game.remove_apple(apple)

        gd.show_score(game.get_score())
        game.draw(gd)
        game.add_bomb()
        game.add_apples()
        gd.end_round()
