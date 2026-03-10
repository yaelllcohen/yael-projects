HANGMAN_PHOTOS = ['''
x-------x   
''', '''
x-------x   
|       |
|       0
|      
|      
|     
''', '''
x-------x   
|       |
|       0
|       |
|      
|     
''', '''
x-------x   
|       |
|       0
|      /|
|      
|     
''', '''
x-------x   
|       |
|       0
|      /|\\
|      
|     
''', '''
x-------x   
|       |
|       0
|      /|\\
|      / 
|     
''', '''
x-------x   
|       |
|       0
|      /|\\
|      / \\
|     
''']


def print_hangman(tries_left):
    print(HANGMAN_PHOTOS[6 - tries_left])


def check_valid_input(letter_guessed, old_letters_guessed):
    """
    בודק אם האות שהוזנה תקינה ולא הוזנה כבר בעבר
    :param letter_guessed: האות שהוזנה
    :param old_letters_guessed: רשימת האותיות שהוזנו
    :return: True אם תקין, False אם לא
    """
    if len(letter_guessed) != 1 or not letter_guessed.isalpha():
        print("X")
        return False
    if letter_guessed in old_letters_guessed:
        print("X")
        return False
    return True


def show_hidden_word(secret_word, old_letters_guessed):
    """
    מציגה את המילה הסודית כשהיא מכילה את האותיות שניחשו, ושאר האותיות עם קווים תחתונים.
    """
    return " ".join([letter if letter in old_letters_guessed else "_" for letter in secret_word])


def choose_word(file_path, index):
    with open(file_path, 'r') as f:
        words = f.read().split()
    return words[index]


def play_game():
    # שלב קבלת נתיב הקובץ והמילה
    file_path = input("Enter file path: ")
    index = int(input("Enter index: "))
    secret_word = choose_word(file_path, index)

    old_letters_guessed = []  # רשימת האותיות שניחשו
    tries_left = 6  # מספר הניסיונות שנותרו

    print("Let's start!")
    while tries_left > 0:
        print_hangman(tries_left)  # הצגת תמונת האיש התלוי
        print(show_hidden_word(secret_word, old_letters_guessed))  # הצגת המילה המוסתרת

        letter_guessed = input("Guess a letter: ").lower()  # המרת הקלט לאות קטנה

        if check_valid_input(letter_guessed, old_letters_guessed):
            old_letters_guessed.append(letter_guessed)  # הוספת האות לרשימה

            if letter_guessed not in secret_word:
                tries_left -= 1  # אם ניחוש שגוי, מצמצמים את הניסיונות
        else:
            print("X")

        if "_" not in show_hidden_word(secret_word, old_letters_guessed):  # אם המילה נחשפה
            print("WIN!")
            break

    if tries_left == 0:
        print("You lose! The word was:", secret_word)


play_game()
