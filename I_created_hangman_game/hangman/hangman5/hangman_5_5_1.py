def is_valid_input(letter_guessed):
    """
    this function check if the guessed letter is valid
     if she only from 1 letter in english
    :param letter_guessed: the guess letter for the game hangman
    :type letter_guessed: string
    :return: if the letter is valid
    :rtype: bool
    """
    letter_guessed = letter_guessed.lower()
    if 'a' <= letter_guessed <= 'z' and len(letter_guessed) == 1:
        return True
    elif letter_guessed.isalpha() and len(letter_guessed) > 1:
        return False
    elif not ('a' <= letter_guessed <= 'z') and len(letter_guessed) == 1:
        return False
    else:
        return False
#def main():
#    print(is_valid_input('a'))  # True
#    print(is_valid_input('A'))  # True
#    print(is_valid_input('$'))  # False
#    print(is_valid_input("ab"))  # False
#    print(is_valid_input("app$"))  # False


#if __name__ == '__main__':
#    main()
