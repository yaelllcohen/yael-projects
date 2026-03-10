import pygame

def run_main_player():
    """המיקומים PLAYER_X UPLAYER_Y"""
    player_x = 300  # מיקום אופקי (שמאל-ימין)
    player_y = 500   # מיקום אנכי (למטה במסך)
    "הגודל של הדמות PLATER_SIZE"
    player_size = 50   # גודל של הריבוע (רוחב וגובה)
    "מהירות התזוזה player_speed"
    player_speed = 3   # מהירות התזוזה בכל לחיצה
    pygame.init()  # הפעולה מפעילה את מערכות המשחק
    screen = pygame.display.set_mode((800, 600))  # פותחת את חלון המשחק בגודל שניתן
    running = True
    while(running):
        """ 
        רשימה של אירועים שקורים במשחק עמו לחיצה על פתור, סגירת החלון 
        אם סוגרים את החלון יוצאים מהלולאה ויוצאים מהמשחק כלומר QUIT
        """
        for event in pygame.event.get():
           if(event.type == pygame.QUIT):
              running = False
        keys = pygame.key.get_pressed()
        """
        פה אני בעצם שמה את המקשים, אם השמאלי לחוץ מורידה מX
        וכן הלאה
        בנוסף החלק השני בתנאים זה כדי לוודא שהדמות לא יוצאת מהמסך
        """
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed #הזזה שמאלה
        if(keys[pygame.K_RIGHT]) and player_x < 800 - player_size:
            player_x += player_speed #הזזה ימינה
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed #הזזה למעלה
        if(keys[pygame.K_DOWN]) and player_y < 600 - player_size:
            player_y += player_speed #הזזה למטה

        screen.fill((255, 182, 193)) #צבע הרקע
        pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_size, player_size)) #ריבוע ציור הדמות
        pygame.display.update() #זה בעצם אומר סיימתי עכשיו תציג את כל מה שיצרתי

if __name__ == "__main__":
    run_main_player()
