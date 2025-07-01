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


def main():
    # שמירת הקובץ בתיקייה הנוכחית של הפרויקט
    file_path = "words.txt"  # הקובץ ייווצר באותה תיקייה כמו קובץ הסקריפט
    file = open(file_path, 'w')
    file.write("hangman song most broadly is a song hangman work music work broadly is typically")
    file.close()
    print(choose_word(file_path, 3))
    #(9, 'most')
    print(choose_word(file_path, 15))
    #(9, 'hangman')

if __name__ == '__main__' :
    main()