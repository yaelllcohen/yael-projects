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

def main():
    secret_word = "mammals"
    old_letters_guessed = ['s', 'p', 'j', 'i', 'm', 'k']
    print(show_hidden_word(secret_word, old_letters_guessed))
    #m _ m m _ _ s

if __name__ == '__main__' :
    main()