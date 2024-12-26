import pygame
from .level_loader import load_level_data


def build_main_menu(screen, display_size, game_active, alpha_val=0):
    # Create a transparent surface for the main menu
    main_menu_surface = pygame.Surface(display_size, pygame.SRCALPHA)
    main_menu_surface_rect = main_menu_surface.get_rect()
    difficulty = "medium"

    if not game_active:
        # Load player sprite with error handling
        try:
            start_menu_surf = pygame.image.load(
                "./game_files/Stage_backgrounds/start_menu_background.png").convert_alpha()
            start_menu_surf = pygame.transform.smoothscale(start_menu_surf, display_size)
            start_menu_surf.set_alpha(alpha_val)
        except pygame.error as e:
            print(f"Error loading image: {e}")
            return alpha_val  # Exit function and preserve alpha state

        # Scale and position the image
        start_menu_rect = start_menu_surf.get_rect(topleft=(0, 0))

        # Clamp alpha value to prevent errors
        alpha_val = min(alpha_val, 255)

        # Add text for instructions
        font = pygame.font.Font(None, 40)  # Default font
        message = font.render("Press SPACE to Start", True, (255, 255, 255))
        message.set_alpha(alpha_val)  # Set text alpha
        message_rect = message.get_rect(center=(display_size[0] / 2, display_size[1] / 1.25))

        # Draw the combined surface to the screen
        main_menu_surface.blit(start_menu_surf, start_menu_rect)
        main_menu_surface.blit(message, message_rect)
        screen.blit(main_menu_surface, main_menu_surface_rect)

        # Increase alpha for fade-in effect
        if alpha_val < 255:
            alpha_val += 3  # Adjust this for faster/slower fade

    else:
        alpha_val = 0  # Reset alpha when the game becomes active

    # Return updated alpha value
    return alpha_val, load_level_data(difficulty)
