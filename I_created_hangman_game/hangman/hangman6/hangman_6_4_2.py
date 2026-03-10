

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

def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
    the function add thr letter guessed to the old letters guessed only if its a vaild letter
    else it will print x
    the function is helped with the function check_valid_input and set the old letters
    if the guessed letter is added to the old letters it will return true else false
    :param letter_guessed: the letter who guessed
    :param old_letters_guessed: the letters that already guessed
    :type letter_guessed: basestring
    :type old_letters_guessed: list
    :return: if the guessed latter added to the old letters
    :rtype: bool
    """
    if(check_valid_input(letter_guessed, old_letters_guessed)):
        old_letters_guessed+= letter_guessed
        return True
    else :
        print('X')
        print(old_letters_guessed)
        return False

def main() :
    old_letters = ['a', 'p', 'c', 'f']
    print(try_update_letter_guessed('A', old_letters))
    #X
    #a -> c -> f -> p
    #False
    print(try_update_letter_guessed('s', old_letters))
    #True
    #old_letters
    #['a', 'p', 'c', 'f', 's']
    print(try_update_letter_guessed('$', old_letters))
    #X
    #a -> c -> f -> p -> s
    #False
    print(try_update_letter_guessed('d', old_letters))
    #True
    #old_letters
    #['a', 'p', 'c', 'f', ‘s’, 'd']

if __name__ == '__main__' :
    main()