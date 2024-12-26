import pygame

def build_main_menu(screen, display_size, game_active, alpha_val):
    # Create a transparent surface for the main menu
    main_menu_surface = pygame.Surface(display_size, pygame.SRCALPHA)
    main_menu_surface_rect = main_menu_surface.get_rect()

    if not game_active:
        # Load player sprite with error handling
        try:
            player_stand = pygame.image.load("./game_files/charSkin1.png").convert_alpha()
        except pygame.error as e:
            print(f"Error loading image: {e}")
            return alpha_val  # Exit function and preserve alpha state

        # Scale and position the image
        player_stand = pygame.transform.rotozoom(player_stand, 0, 1.5)
        player_stand_rect = player_stand.get_rect(center=(display_size[0] / 2, display_size[1] / 2))

        # Apply fade effect with alpha transparency
        main_menu_surface.fill((124, 159, 192, alpha_val))  # Background with fading alpha
        main_menu_surface.blit(player_stand, player_stand_rect)  # Player sprite

        # Add text for instructions
        font = pygame.font.Font(None, 40)  # Default font
        message = font.render("Press SPACE to Start", True, (0, 0, 0))
        message.set_alpha(alpha_val)  # Set text alpha
        message_rect = message.get_rect(center=(display_size[0] / 2, display_size[1] / 1.5))
        main_menu_surface.blit(message, message_rect)

        # Draw the combined surface to the screen
        screen.blit(main_menu_surface, main_menu_surface_rect)

        # Increase alpha for fade-in effect
        if alpha_val < 255:
            alpha_val += 2  # Adjust this for faster/slower fade

    else:
        alpha_val = 0  # Reset alpha when the game becomes active

    # Return updated alpha value
    return alpha_val
