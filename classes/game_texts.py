import pygame
import time

def disp_score(screen, start_time, bonus=0):
    # To show the score
    time_score = pygame.time.get_ticks() - start_time
    score = time_score//1000 + bonus
    score_font = pygame.font.Font(None, 50)
    score_surf = score_font.render(f"Score: {score}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    pygame.draw.rect(screen, (0, 230, 250), score_rect, 0)
    screen.blit(score_surf, score_rect)
    return score

def countdown_timer(screen, background_surf, countdown_time):
    count_font = pygame.font.Font(None, 150)
    for count in range(countdown_time, 0, -1):  # Countdown from countdown_time to 1
        text = count_font.render(str(count), True, "black")  # Render countdown number
        text_rect = text.get_rect(center=(screen.get_size()[0] // 2, screen.get_size()[1] // 2))
        screen.blit(background_surf, (0, 0))
        screen.blit(text, text_rect)  # Display the countdown text
        pygame.display.flip()  # Update the display
        time.sleep(1)  # Wait for 1 second

    # Display "GO!" at the end of countdown
    text = count_font.render("GO!", True, "black")
    text_rect = text.get_rect(center=(screen.get_size()[0] // 2, screen.get_size()[1] // 2))
    screen.blit(background_surf, (0, 0))
    screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(1)  # Pause briefly before starting the game
