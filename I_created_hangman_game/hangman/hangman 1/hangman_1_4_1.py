print("Welcome to the game Hangman")
print(""" 
  _    _   
 | |  | | 
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ | 
                     |___/""")
import random
random_guessing_attempts= random.randint(5,10)
print(random_guessing_attempts)