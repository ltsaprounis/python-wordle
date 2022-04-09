"""The wordle game"""

import os
import random

from wordle import utils
import wordle

VALID_WORDS = utils.read_5letter_word_file(
    os.path.join(os.path.dirname(wordle.__file__), "datasets/5-letter-words.txt")
)


class WordleGame:
    """The wordle game"""

    def __init__(
        self,
        target_word: str = None,
        max_tries: int = 5,
        valid_words: list = VALID_WORDS,
        random_seed: int = None,
        format_dict: dict = utils.TERMINAL_FORMAT,
        keyboard_layout: dict = utils.QWERTY_LAYOUT,
    ) -> None:
        self.max_tries = max_tries
        self.format_dict = format_dict
        self.keyboard_layout = keyboard_layout
        self.random_seed = random_seed
        self.valid_words = valid_words
        self.target_word = target_word

        # Initialise private attributes here:
        self._tries_remaining = max_tries
        self._used_words = []
        self._used_words_str = ""
        self._correct_letters_set = set()
        self._partially_correct_letters_set = set()
        self._wrong_letters_set = set()
        self._random = random.Random(random_seed)
        self._success = False
        self.target_word_ = self.generate_target_word(target_word)
        self._target_word_letter_pos = self.get_letter_pos_dict(self.target_word_)

    @property
    def tries_remaining(self):
        """Remaining tries"""
        return self._tries_remaining

    def game_status_string(self):
        """Get the game status string"""
        keyboard_str = utils.display_keyboard_str(
            correct_set=self._correct_letters_set,
            partially_correct_set=self._partially_correct_letters_set,
            wrong_set=self._wrong_letters_set,
            keyboard_layout=self.keyboard_layout,
            format_dict=self.format_dict,
        )
        return "\n" + self._used_words_str + "\n" + keyboard_str + "\n"

    def user_input(self):
        """Get user input."""
        return input(self.game_status_string())

    def check_word_valid(self, word: str):
        """Check wheter a word is valid."""
        return word.upper() in self.valid_words

    def generate_target_word(self, target_word: str):
        """Generates a target word and checks the validity if it is provided."""
        if target_word is not None and not self.check_word_valid(target_word):
            raise ValueError(f"Target word {target_word.upper()} is not a valid word")
        elif target_word is not None:
            return target_word.upper()
        else:
            return self._random.choice(self.valid_words).upper()

    @staticmethod
    def get_letter_pos_dict(word):
        """Get a dictionary of the position of each letter in a word"""
        return {
            letter: {i for i, w in enumerate(word) if w == letter}
            for letter in set(word)
        }

    def format_word(self, word, letters_status):
        """Format a word based on the letter status list"""
        formatted_word = ""
        for i in range(len(letters_status)):
            status = letters_status[i]
            if status == "correct":
                formatted_word += utils.decorate_correct(
                    word[i], format_dict=self.format_dict
                )
            elif status == "partially_correct":
                formatted_word += utils.decorate_partially_correct(
                    word[i], format_dict=self.format_dict
                )
            elif status == "wrong":
                formatted_word += utils.decorate_wrong(
                    word[i], format_dict=self.format_dict
                )
            else:
                raise ValueError("{status} is not a valid word status")

        return formatted_word

    def process_wrong_valid_word(self, word: str):
        """Process a wrong word that is valid"""
        letters_pos = self.get_letter_pos_dict(word)
        letters_status = ["wrong" for _ in range(len(word))]
        for letter, pos in letters_pos.items():
            if letter not in self._target_word_letter_pos.keys():
                self._wrong_letters_set.add(letter)
            else:
                pos_intersection = pos.intersection(
                    self._target_word_letter_pos[letter]
                )
                if len(pos_intersection) != 0:
                    for i in pos_intersection:
                        letters_status[i] = "correct"
                        self._correct_letters_set.add(letter)
                else:
                    letters_status[min(pos)] = "partially_correct"
                    self._partially_correct_letters_set.add(letter)

        self._used_words_str += (
            self.format_word(word=word, letters_status=letters_status) + "\n"
        )

    def single_round(self):
        """Play a single wordle round."""
        word = self.user_input().upper().replace(" ", "")
        if word == self.target_word_:
            self._used_words_str += utils.decorate_correct(word)
            self._correct_letters_set.update(set(word))
            self._success = True
        elif not self.check_word_valid(word):
            print(f">> {word} is not a real word")
        elif word in self._used_words:
            print(f">> You have already used {word}")
        else:
            self.process_wrong_valid_word(word)
            self._tries_remaining -= 1
            self._used_words.append(word)

    def play(self):
        """Play the game."""
        while self._tries_remaining > 0 and not self._success:
            self.single_round()

        if self._success:
            print("\n>> Congrats, you won!")
            print(self.game_status_string())
        else:
            print(f"\n>> You lost... the word was {self.target_word_}")
            print(self.game_status_string())
