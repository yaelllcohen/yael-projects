def check_valid_input(letter_guessed, old_letters_guessed):
    """
    this function check if the guessed leter is valid,
    if more then 2 letters false
    if its not in english letter false
    if the letter guessed is already at old letter guessed
    else true
    :param letter_guessed:the letter that guessed at input
    :param old_letters_guessed: the letters that already was guessted
    :type letter_guessed: string
    :type old_letters_guessed: list
    :return: if the letter_guessed is vaild
    :rtype: bool
    """
    letter_guessed = letter_guessed.lower()
    if len(letter_guessed) > 1:
        return False
    elif not ('a' <= letter_guessed <= 'z') and len(letter_guessed) == 1:
        return False
    elif letter_guessed in old_letters_guessed :
        return False;
    elif letter_guessed.isalpha() and len(letter_guessed) == 1 and not(letter_guessed in old_letters_guessed):
        return True

def main():
    old_letters = ['a', 'b', 'c']
    print(check_valid_input('C', old_letters))
    #False
    print(check_valid_input('ep', old_letters))
    #False
    print(check_valid_input('$', old_letters))
    #False
    print(check_valid_input('s', old_letters))
    #True

if __name__ == '__main__' :
    main();