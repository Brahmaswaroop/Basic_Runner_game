import pygame

def disp_score(screen, start_time):
    # To show the score
    time = pygame.time.get_ticks() - start_time

    score_font = pygame.font.Font(None, 50)
    score_surf = score_font.render(f"Score: {time//1000}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    pygame.draw.rect(screen, (0, 230, 250), score_rect, 0)
    screen.blit(score_surf, score_rect)

