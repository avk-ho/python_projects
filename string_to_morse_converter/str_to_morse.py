# https://www.udemy.com/course/100-days-of-code/learn/lecture/23076578#overview

# https://en.wikipedia.org/wiki/Morse_code

### Rules ###

# dot "▄" # 1 unit
# dash "▄▄▄" # 3 units
# 1 units space between part of a character
# 3 units space between characters
# 7 units space between words

from assets import *

### Functions ###

# Take a string and format it to be converted into morse code
def format_input(str):
    formatted_input = str.upper()

    return formatted_input


# Take a string and convert it into morse code
# Will leave unrecognized characters as is
def convert_to_morse(str):
    converted_str = []

    for char in str:
        if char in CHARACTERS:
            char = MORSE_CHARACTERS[char]

        converted_str.append(char)
        converted_str.append("   ") # 3 units space

    converted_str = "".join(converted_str).rstrip()

    return converted_str


### Converter ###
continue_loop = True

while continue_loop:
    str_input = input("Please input the text (only latin alphabet and numbers) to translate into morse: ")
    formatted_input = format_input(str_input)
    converted_input = convert_to_morse(formatted_input)
    print(converted_input)

    continue_input = input("Do you want to continue converting ? Type 'y' to keep converting: ")
    if continue_input != "y":
        continue_loop = False