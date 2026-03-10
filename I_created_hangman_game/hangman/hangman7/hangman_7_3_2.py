def check_win(secret_word, old_letters_guessed):
    """
    הפונקציה מקבלת את המילה הסודית ואת האותיות שניחשו
    ובכך עוברת על המילה ורואה אם היא מוחזרת שלמה
    :param secret_word: המילה הסודית שצריך לנחש
    :param old_letters_guessed: האותויות שכבר ניחשו
    :type secret_word: str
    :type old_letters_guessed: list
    :return: האם הצליחו לנחש את המילה
    :rtype: bool
    """
    secret_word = secret_word.lower()  # ממירה את כל המילה לאותיות קטנות
    old_letters_guessed_lower = []
    for letter in old_letters_guessed:
        old_letters_guessed_lower.append(letter.lower())  # ממיר את כל אות לאות קטנה
    for letter in secret_word:
        if letter not in old_letters_guessed_lower:
            return False
    return True

def main():
    secret_word = "friends"
    old_letters_guessed = ['m', 'p', 'j', 'i', 's', 'k']
    print(check_win(secret_word, old_letters_guessed))
    #False
    secret_word = "yes"
    old_letters_guessed = ['d', 'g', 'e', 'i', 's', 'k', 'y']
    print(check_win(secret_word, old_letters_guessed))
    #True

if __name__ == '__main__':
    main()