"ההתנגשות בין הדמות הראשית לאוייבים"
import pygame
import random

#פה אני מגידרה את הקול שמסיים את המשחק
pygame.mixer.init()
game_over_sound = pygame.mixer.Sound("GameOverSound.wav")


def run_game_with_collision():
    # פה נשים את כל הקוד של הדמות + אויבים + התנגשות
    """המיקומים PLAYER_X UPLAYER_Y"""
    player_x = 300  # מיקום אופקי (שמאל-ימין)
    player_y = 500  # מיקום אנכי (למטה במסך)
    "הגודל של הדמות PLATER_SIZE"
    player_size = 50  # גודל של הריבוע (רוחב וגובה)
    "מהירות התזוזה player_speed"
    player_speed = 2  # מהירות התזוזה בכל לחיצה
    enemy_x = 100  # מיקום אופקי של האויב (אפשר גם להתחיל רנדומלי)
    enemy_y = 0  # מתחיל למעלה
    enemy_size = 50  # אותו גודל כמו הדמות הראשית
    enemy_speed = 1  # כמה פיקסלים הוא יורד בכל פריים
    enemy_radius = 25  # רדיוס המעגל
    pygame.init()  # הפעולה מפעילה את מערכות המשחק
    font = pygame.font.SysFont(None,50) #גודל הפונט בשביל השניות שירוצו במסך
    screen = pygame.display.set_mode((800, 600))  # פותחת את חלון המשחק בגודל שניתן
    running = True
    while (running):
        time_of_game = pygame.time.get_ticks() /1000 #השניות שלוקח עד שנפסלים
        # מנקה את המסך בכל פריים כי ממלא את כל המסך בצבע הזה לפני שמציירים דברים חדשים
        screen.fill((255, 182, 193))
        "אני יוצרת מין תמונה כזאת של הזמן ליד המסך שסופר לי כמה זמן עד שאני נפסלת "
        timer_text = font.render(f"{int(time_of_game)} s", True, (255, 0, 255))
        screen.blit(timer_text, (10, 10))  # מציג את הזמן בפינה שמאלית עליונה
        """ 
        רשימה של אירועים שקורים במשחק עמו לחיצה על פתור, סגירת החלון 
        אם סוגרים את החלון יוצאים מהלולאה ויוצאים מהמשחק כלומר QUIT
        """
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
        keys = pygame.key.get_pressed()
        """
        פה אני בעצם שמה את המקשים, אם השמאלי לחוץ מורידה מX
        וכן הלאה
        בנוסף החלק השני בתנאים זה כדי לוודא שהדמות לא יוצאת מהמסך
        """
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed  # הזזה שמאלה
        if (keys[pygame.K_RIGHT]) and player_x < 800 - player_size:
            player_x += player_speed  # הזזה ימינה
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed  # הזזה למעלה
        if (keys[pygame.K_DOWN]) and player_y < 600 - player_size:
            player_y += player_speed  # הזזה למטה
        enemy_y += enemy_speed  # בכל פעם שפריים עובר האויב יורד קצת למטה
        if enemy_y > 600:  # בודקת אם האויב עבר את המסך
             enemy_y = 0
             enemy_x = random.randint(0, 800)  # כדי שיופיע כל פעם במקום שונה
        """
        player_x < enemy_x < player_x + player_size → האם האויב בתוך גבולות האופק של הדמות?
        player_y < enemy_y < player_y + player_size → האם האויב בתוך גבולות הגובה של הדמות?
אם שתי התנאים נכונים → האויב "בתוך" הדמות →        
        """
        if (player_x < enemy_x < player_x + player_size) and (player_y < enemy_y < player_y + player_size):
            game_over_sound.play()
            # מפסיקה את המשחק אבל מראה מסך סיום
            font = pygame.font.SysFont(None, 72)
            # יצירת טקסט עם הזמן שעבר עד הפגיעה
            final_time_text = font.render( f"{int(time_of_game)} SEC", True, (255, 0, 255))
            screen.blit(final_time_text, (335, 320))  # מתחת ל-GAME OVER
            text = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(text, (250, 250))
            #screen.blits(time_of_game,(0,0,250))
            pygame.display.update()
            pygame.time.delay(2000)  # מחכה 2 שניות לפני שסוגרת
            running = False

        "עכשיו אני מציירת את האויב כעיגול כחול"
        pygame.draw.circle(screen, (0, 0, 255), (enemy_x, enemy_y), enemy_radius)
        pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_size, player_size))  # ריבוע ציור הדמות
        pygame.display.update()  # זה בעצם אומר סיימתי עכשיו תציג את כל מה שיצרתי

if __name__ == "__main__":
    run_game_with_collision()


