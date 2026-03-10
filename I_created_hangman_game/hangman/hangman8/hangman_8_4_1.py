def print_hangman(num_of_tries):
    """
    הפעולה מחזירה את מצב האיש התלוי בכל ניסיון שלא הצליח
    :param num_of_tries: כמות הנסיונות שלא הצליחו
    :type num_of_tries: int
    :return: מצה האיש התלוי כמות הנסיונות שלא הצליחו
    :rtype: str
    """
    if num_of_tries == 1:
        return """
x-------x
        """
    elif num_of_tries == 2:
        return """  
x-------x
|
|
|
|
|"""
    elif num_of_tries == 3:
        return """  
x-------x
|       |
|       0
|
|
|"""
    elif num_of_tries == 4:
        return """  
x-------x
|       |
|       0
|       |
|
|"""
    elif num_of_tries == 5:
        return r"""  
x-------x
|       |
|       0
|      /|\
|
|"""
    elif num_of_tries == 6:
        return r"""  
x-------x
|       |
|       0
|      /|\
|      /
|"""
    elif num_of_tries == 7:
        return r"""  
x-------x
|       |
|       0
|      /|\
|      / \
|"""

def main():
    num_of_tries = 1
    print(print_hangman(num_of_tries))

if __name__ == '__main__' :
    main()
