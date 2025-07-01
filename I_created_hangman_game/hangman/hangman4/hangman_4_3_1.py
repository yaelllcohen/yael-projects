guess_letter = input("enter a letter: ")
guess_letter = guess_letter.lower()
if 'a'<= guess_letter <= 'z' and len(guess_letter)==1 :
    print(guess_letter)
elif guess_letter.isalpha() and len(guess_letter) > 1 :
    print('E1')
elif not('a'<= guess_letter <= 'z') and len(guess_letter) == 1 :
    print('E2')
else:
    print('E3')
