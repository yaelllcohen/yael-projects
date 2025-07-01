import pygame
import random

def run_enemies():
    enemy_x = 100       # מיקום אופקי של האויב (אפשר גם להתחיל רנדומלי)
    enemy_y = 0         # מתחיל למעלה
    enemy_size = 50     # אותו גודל כמו הדמות שלך
    enemy_speed = 2     # כמה פיקסלים הוא יורד בכל פריים
    enemy_radius = 25   # רדיוס המעגל
    pygame.init()  # הפעולה מפעילה את מערכות המשחק
    screen = pygame.display.set_mode((800, 600)) #גודל חלון המשחק
    running = True
    while(running):
        # מנקה את המסך בכל פריים כי ממלא את כל המסך בצבע הזה לפני שמציירים דברים חדשים
        screen.fill((255, 182, 193))
        """ 
            רשימה של אירועים שקורים במשחק עמו לחיצה על פתור, סגירת החלון 
            אם סוגרים את החלון יוצאים מהלולאה ויוצאים מהמשחק כלומר QUIT
            """
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
        enemy_y += enemy_speed #בכל פעם שפריים עובר האויב יורד קצת למטה
        "עכשיו אני מציירת את האויב כעיגול כחול"
        pygame.draw.circle(screen, (0, 0, 255), (enemy_x, enemy_y), enemy_radius)
        if enemy_y > 600: #בודקת אם האויב עבר את המסך
            enemy_y = 0
            enemy_x = random.randint(0, 800) #כדי שיופיע כל פעם במקום שונה
        pygame.display.update()

if __name__ == "__main__":
    run_enemies()