import random
import sys


class Main:
    max_width = 5
    max_height = 5
    character_alive = True
    character_won = False
    monster_awake = False
    monster_awakened = False
    monster_moves_per_turn = 2

    def __init__(self):
        self.display_menu()
        self.reset_current_game()

    def reset_current_game(self):
        self.monster_position = [1, 1]
        self.trap_position = [0, 1]
        self.flask_position = [1, 0]

    def reset_all_settings(self):
        self.character_alive = True
        self.character_won = False
        self.monster_awake = False
        self.monster_awakened = False

    def place_character(self):
        self.character_position = [0, 0]

    def place_monster(self):
        self.monster_position = [random.randint(0, self.max_width - 1), random.randint(0, self.max_height - 1)]
        if self.coordinate_collision('monster', 'player'):
            self.place_monster()
        elif self.coordinate_collision('monster', 'flask'):
            self.place_monster()
        elif self.coordinate_collision('monster', 'trap'):
            self.place_monster()
        else:
            return True
        return True

    def place_trap(self):
        self.trap_position = [random.randint(0, self.max_width - 1), random.randint(0, self.max_height - 1)]
        if self.coordinate_collision('trap', 'player'):
            self.place_trap()
        elif self.coordinate_collision('trap', 'flask'):
            self.place_trap()
        elif self.coordinate_collision('trap', 'monster'):
            self.place_trap()
        else:
            return True
        return True

    def place_flask(self):
        self.flask_position = [random.randint(0, self.max_width - 1), random.randint(0, self.max_height - 1)]
        if self.coordinate_collision('flask', 'player'):
            self.place_flask()
        elif self.coordinate_collision('flask', 'monster'):
            self.place_flask()
        elif self.coordinate_collision('flask', 'trap'):
            self.place_flask()
        else:
            return True
        return True

    def display_menu(self):
        menu_list = ['Start New Game', '[Save Game]', '[Load Game]', 'Customize Setup', 'Exit']
        print('Type the number of your choice')
        print()
        for i in range(1, len(menu_list) + 1):
            print(str(i) + ' ' + menu_list[i - 1])
        choice = input('Your Choice: ')
        self.menu_choice(choice)

    def coordinate_collision(self, coord1, coord2):
        if coord1 == 'monster':
            first = self.monster_position
        elif coord1 == 'flask':
            first = self.flask_position
        elif coord1 == 'trap':
            first = self.trap_position
        elif coord1 == 'player':
            first = self.character_position
        else:
            return None

        if coord2 == 'monster':
            second = self.monster_position
        elif coord2 == 'flask':
            second = self.flask_position
        elif coord2 == 'trap':
            second = self.trap_position
        elif coord2 == 'player':
            second = self.character_position
        else:
            return None

        if coord1 == coord2:
            return None

        if first[0] == second[0] and first[1] == second[1]:
            return True
        else:
            return False

    def start_new_game(self):
        self.reset_all_settings()
        self.reset_current_game()
        self.setup_game()

    def setup_game(self):
        self.place_character()
        self.place_flask()
        self.place_monster()
        self.place_trap()
        self.draw_grid()

    def menu_choice(self, choice):
        try:
            choice = int(choice)
        except ValueError:
            choice = 0
        if (choice == 1):
            self.start_new_game()
        elif (choice == 2):
            pass
        elif (choice == 3):
            pass
        elif (choice == 4):
            pass
        elif (choice == 5):
            sys.exit(0)

        else:
            print('That wasn\'t a valid option. Try again.')
            self.display_menu()

    def collision_check(self):
        if self.coordinate_collision('player', 'monster'):
            self.character_alive = False
            return True
        elif self.coordinate_collision('player', 'flask'):
            self.character_won = True
            return True
        elif self.coordinate_collision('player', 'trap'):
            self.monster_awakened = True
            self.trap_position = [-1, -1]
            return True
        return False

    def check_boundary(self, new_x, new_y):
        min_width = 0
        min_height = 0
        if new_x < min_width or new_x == self.max_width or new_y < min_height or new_y == self.max_height:
            return False
        else:
            return True

    def player_move(self, choice):
        current_x = self.character_position[0]
        current_y = self.character_position[1]
        if choice == 'W' or choice == 'w':
            if not self.check_boundary(current_x, current_y - 1):
                return False
            else:
                self.character_position = [current_x, current_y - 1]
                return True
        elif choice == 'A' or choice == 'a':
            if not self.check_boundary(current_x - 1, current_y):
                return False
            else:
                self.character_position = [current_x - 1, current_y]
                return True
        elif choice == 'S' or choice == 's':
            if not self.check_boundary(current_x, current_y + 1):
                return False
            else:
                self.character_position = [current_x, current_y + 1]
                return True
        elif choice == 'D' or choice == 'd':
            if not self.check_boundary(current_x + 1, current_y):
                return False
            else:
                self.character_position = [current_x + 1, current_y]
                return True
        else:
            return False

    def move_monster(self):
        moves_left = self.monster_moves_per_turn
        while moves_left > 0:
            mon_x = self.monster_position[0]
            mon_y = self.monster_position[1]
            player_x = self.character_position[0]
            player_y = self.character_position[1]

            if player_x - mon_x != 0:
                if player_x - mon_x < 0:
                    self.monster_position = [mon_x - 1, mon_y]
                else:
                    self.monster_position = [mon_x + 1, mon_y]
            else:
                if player_y - mon_y < 0:
                    self.monster_position = [mon_x, mon_y - 1]
                else:
                    self.monster_position = [mon_x, mon_y + 1]
            moves_left = moves_left - 1


    def draw_grid(self):
        if self.character_won == True:
            print('You have beaten Monster! Congratulations!')
            choice = input('Press any key to return to the menu or press enter to exit:')
            if choice:
                self.display_menu()
        elif self.character_alive == False:
            print('You have been eaten by the Monster!')
            choice = input('Press any key to return to the menu or press enter to exit:')
            if choice:
                self.display_menu()
        else:
            height = self.max_height
            width = self.max_width

            for y in range(0, height):
                for x in range(0, width):
                    y = str(y)
                    x = str(x)

                    char_x = str(self.character_position[0])
                    char_y = str(self.character_position[1])
                    if (str(self.monster_position[0]) == x and str(
                            self.monster_position[1]) == y and self.monster_awake == True):
                        sys.stdout.write('M')
                    elif (char_x == x and char_y == y):
                        sys.stdout.write('X')
                    elif (str(self.trap_position[0]) == x and str(self.trap_position[1]) == y):
                        sys.stdout.write('T')
                    elif (str(self.flask_position[0]) == x and str(self.flask_position[1]) == y):
                        sys.stdout.write('F')
                    else:
                        # sys.stdout.write('?')
                        print('?', end='')
                print()
            print()
            print('Move using WASD')
            choice = input('Move: ')
            if self.player_move(choice) == False:
                print('Not a valid move')
                self.draw_grid()
            else:
                if self.monster_awake:
                    self.move_monster()
                if self.collision_check():
                    if self.monster_awakened:
                        self.monster_awake = True
                        print('You awoke the Monster!')
                        self.monster_awakened = False
                self.draw_grid()


monster = Main()
