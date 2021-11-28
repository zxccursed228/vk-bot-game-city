import random


class Lobby:
    def __init__(self, user1, user2):
        self.user_ids = [user1, user2]
        self.current_turn = random.randint(0, 1)
        self.used_cities = []
        self.last_letter = None

    def get_active_player_id(self):
        return self.user_ids[self.current_turn]

    def get_inactive_player_id(self):
        return self.user_ids[1 - self.current_turn]

    def is_correct_letter(self, letter):
        return self.last_letter == letter

    def change_ll(self, city):
        incorrectect_last_letters = ['ы', 'ь', "ъ", "ё"]
        for letter in city[::-1]:
            if letter not in incorrectect_last_letters:
                self.last_letter = letter
                break

    def change_cur_turn(self):
        self.current_turn = 1 - self.current_turn