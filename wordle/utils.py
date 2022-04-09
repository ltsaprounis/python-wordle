"""Utils functions for the wordle game"""

TERMINAL_FORMAT = {
    "end_format": "\x1b[0m",
    "correct": "\x1b[30;30;42m",
    "partially_correct": "\x1b[30;30;43m",
    "wrong": "\x1b[30;30;47m",
}

QWERTY_LAYOUT = {
    "Q": (0, 0),
    "W": (0, 1),
    "E": (0, 2),
    "R": (0, 3),
    "T": (0, 4),
    "Y": (0, 5),
    "U": (0, 6),
    "I": (0, 7),
    "O": (0, 8),
    "P": (0, 9),
    "A": (1, 0),
    "S": (1, 1),
    "D": (1, 2),
    "F": (1, 3),
    "G": (1, 4),
    "H": (1, 5),
    "J": (1, 6),
    "K": (1, 7),
    "L": (1, 8),
    "Z": (2, 0),
    "X": (2, 1),
    "C": (2, 2),
    "V": (2, 3),
    "B": (2, 4),
    "N": (2, 5),
    "M": (2, 6),
}


def decorate_string(text: str, start_format: str, end_format: str) -> str:
    """Format a string"""
    return start_format + text + end_format


def decorate_correct(text: str, format_dict: dict = TERMINAL_FORMAT):
    """Format a correct string"""
    return decorate_string(
        text, start_format=format_dict["correct"], end_format=format_dict["end_format"]
    )


def decorate_partially_correct(text: str, format_dict: dict = TERMINAL_FORMAT):
    """Format a partially correct string"""
    return decorate_string(
        text,
        start_format=format_dict["partially_correct"],
        end_format=format_dict["end_format"],
    )


def decorate_wrong(text: str, format_dict: dict = TERMINAL_FORMAT):
    """Format a wrong string"""
    return decorate_string(
        text, start_format=format_dict["wrong"], end_format=format_dict["end_format"]
    )


def display_keyboard_str(
    correct_set: set = set(),
    partially_correct_set: set = set(),
    wrong_set: set = set(),
    keyboard_layout: dict = QWERTY_LAYOUT,
    format_dict: dict = TERMINAL_FORMAT,
) -> None:
    """Prints the keyboard with hints on the characters used"""
    number_of_keyboard_lines = max([val[0] for val in keyboard_layout.values()]) + 1
    keyboard_lines_list = [[] for _ in range(number_of_keyboard_lines)]

    for letter, pos in keyboard_layout.items():
        if letter in correct_set:
            keyboard_lines_list[pos[0]].insert(
                pos[1], decorate_correct(text=letter, format_dict=format_dict)
            )
        elif letter in partially_correct_set:
            keyboard_lines_list[pos[0]].insert(
                pos[1], decorate_partially_correct(text=letter, format_dict=format_dict)
            )
        elif letter in wrong_set:
            keyboard_lines_list[pos[0]].insert(
                pos[1], decorate_wrong(text=letter, format_dict=format_dict)
            )
        else:
            keyboard_lines_list[pos[0]].insert(pos[1], letter)

    keyboard_str = ""
    for keyboard_line in keyboard_lines_list:
        keyboard_str += " ".join(keyboard_line) + "\n"

    return keyboard_str


def read_5letter_word_file(path):
    """Read the 5 letter word file"""
    with open(path, "r") as file:
        words = file.read().splitlines()

    return [word.upper() for word in words]
