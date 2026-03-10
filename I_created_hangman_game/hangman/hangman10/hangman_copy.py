def start_the_game():
    """
    הפונקציה מציגה את מסך הפתיחה של המשחק איש תלוי
    :return: None
    """
    print(r""" 
        Welcome to the game Hangman
         _    _   
        | |  | | 
        | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
        |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
        | |  | | (_| | | | | (_| | | | | | | (_| | | | |
        |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                             __/ | 
                            |___/
        how the hangman look int the start: 
        x-------x
        |
        |
        |
        |
        |   
                            """)
    """
       לפי סעיף 2 מבקשים לבקש מהשחקן את נתיב הקובץ המכיל את המילים
       ואת המיקום של המילה שהוא רוצה לבחור מרשימת המילים
       """
    file_path = input("הזן את נתיב הקובץ המכיל את המילים: ")
    index = int(input("הזן את המיקום (אינדקס) של המילה שברצונך לבחור: "))
    """
    לפי הפונקציה הראשית playgame נמצא את המילה שצריך להחזיר
    ונחזיר את כמות האותיות ככה _ _ _ ...
    """
    different_words, secret_word = choose_word(file_path, index)
    print('_ ' * len(secret_word))
    play_game(file_path, index)

def print_how_the_hangman_look(tries):
    """
    הפונקציה מציגה את המצב של האיש התלוי על פי מספר הניסיונות הכושלים
    """
    hangman_states = [
        """
        x-------x
        |
        |
        |
        |
        |
        """,
        """
        x-------x
        |       |
        |       0
        |
        |
        |
        """,
        """
        x-------x
        |       |
        |       0
        |       |
        |
        |
        """ ,
        r"""
        x-------x
        |       |
        |       0
        |      /|\
        |
        |
        """,
        r"""
        x-------x
        |       |
        |       0
        |      /|\
        |      /
        |
        """,
        r"""
        x-------x
        |       |
        |       0
        |      /|\
        |      / \
        """
    ]
    return hangman_states[tries - 1]

def choose_word(file_path, index):
    """
    הפונקציה מקבלת נתיב לקובץ שמכיל מילים ומיקום המילה שצריך להחזיר
    index זה המילה שצריך להחזיר
    מחזירים כטאפל את האינדקס של המילה וכמות המילים שלא חוזרות על עצמן
    :param file_path: קובץ עם רשימת מילים
    :type file_path: file
    :param index: מיקום המילה שצריך להחזיר
    :type index: int
    :return: כמות המילים שלא חוזרות על עצמן והמילה במיקום index
    :rtype: tuple
    """
    with open(file_path, "r") as file:
        words = file.read().split(' ')

    index = (index - 1) % len(words)  # חישוב מעגלי
    the_word_to_return = words[index]  # אינדקס חוקי
    different_words = 0
    words_that_was = []

    for word in words :
        if not(word in words_that_was):
            different_words+=1
        words_that_was.append(word)
    tuple_of_the_word_and_diff_word = (different_words, the_word_to_return)
    """
    יכולתי במקום הלולאה לעשות
    different_words = len(set(words))
    כי המתודה set מחזירה רשימה ללא כפילויות
    """
    return tuple_of_the_word_and_diff_word

def show_hidden_word(secret_word, old_letters_guessed):
    """
    הפונקציה מקבלת את המילה שצריך לנחש ואת רשימת האותיות שכבר ניחשו
    אם אחת מאותיות שניחשו נמצאת במילה נוסיף אותה למחרוזת כך ש
    אם ניחשו מהמילה word את w ואת d זה יראה כך:
    w _ _ d
    :param secret_word: המילה הסודית שצריך לנחש
    :param old_letters_guessed: האותיות שכבר ניחשו
    :type secret_word: str
    :type old_letters_guessed: list
    :return:את האותיות מתוך הרשימה במיקום המתאים
    :rtype: str
    """
    part_of_the_word = ""
    for letter in secret_word:
        if letter in old_letters_guessed :
            part_of_the_word += letter +" "
        else:
            part_of_the_word += '_ '
    return part_of_the_word[:-1]

def check_valid_input(letter_guessed, old_letters_guessed):
    """
    בודק אם האות שהוזנה תקינה ולא הוזנה כבר בעבר
    :param letter_guessed: האות שהוזנה
    :param old_letters_guessed: רשימת האותיות שהוזנו
    :return: True אם תקין, False אם לא
    """
    if len(letter_guessed) != 1 or not letter_guessed.isalpha():
        print("X - לא תקין!")
        return False
    elif letter_guessed in old_letters_guessed:
        print("X - האות כבר הוזנה!")
        return False
    else:
        return True


def play_game(file_path, index):
    """
     הפונקציה מקבלת נתיב לקובץ שמכיל מילים ומיקום המילה שצריך להחזיר
    index זה המילה שצריך להחזיר
    מחזירים כטאפל את האינדקס של המילה וכמות המילים שלא חוזרות על עצמן
    :param file_path: קובץ עם רשימת מילים
    :type file_path: file
    :param index: מיקום המילה שצריך להחזיר
    :type index: int
    :return: כמות המילים שלא חוזרות על עצמן והמילה במיקום index
    :rtype: tuple
    """
    different_words, secret_word = choose_word(file_path, index)
    if not secret_word:
        return  # אם לא הצלחנו לבחור מילה, לא נמשיך במשחק
    old_letters_guessed = []  # רשימה של האותיות שכבר ניחשו
    attempt_left = 5 # מספר הניסיונות שנותרו, בהתחלה זה 6
    while attempt_left > 0:
        letter_guessed = input("guess letter: ").lower()
        """
        אם האות תקינה אני מוסיפה לרשימה
        """
        is_vaild = check_valid_input(letter_guessed, old_letters_guessed)
        if is_vaild:
            old_letters_guessed.append(letter_guessed)  # הוספת האות לרשימה

            if letter_guessed not in secret_word:
                attempt_left -= 1
                print("X - not true")

        else:
            print(is_vaild)
        print(old_letters_guessed)
        print(print_how_the_hangman_look(6 - attempt_left))
        current_word = show_hidden_word(secret_word, old_letters_guessed)
        print(current_word)
        if '_' not in current_word:
            print("Good job, you did it!")
            break

    if '_' in current_word:
        print("you lose, the word was: ", secret_word)


def main():
    start_the_game()


if __name__ == '__main__' :
    main()