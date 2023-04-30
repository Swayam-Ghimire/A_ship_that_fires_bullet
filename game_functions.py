import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep


def change_fleet_direction(setting, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += setting.fleet_drop_speed
    setting.fleet_direction *= -1


def check_fleet_edges(setting, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(setting, aliens)
            break


def get_number_rows(setting, ship_height, alien_height):
    available_space_y = (setting.height - (alien_height) - ship_height)
    number_rows = int(available_space_y / (3 * alien_height))
    return number_rows


""" This function make no of rows. Here available_space_y means how much space is left after excluding ship height
and 2 times alien height(we need a little space to get time to shoot the bullet.To calculate the number of rows we can 
fit on the screen, we write our available_space_y and number_rows calculations into the function get_number_rows(), 
which is similar to get_number_aliens_x(). """


def get_number_aliens_x(setting, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = setting.width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(setting, screen, aliens, alien_number, row_number, ship):
    """Create an alien and place it in the row."""
    alien = Alien(setting, screen, ship)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


"""alien.rect.y is looped for number_rows times ie 2 times. This line updates the row position in which alien fleet is 
created. Similar to alien.x. 
1st case: row_number = 0 that means fleet of alien is created leaving the aliens height from the top.
2nd case: row_number = 1 that means fleet of alien is created leaving the 3 * aliens height from the top."""


def create_fleet(setting, screen, aliens, ship):
    """Creating the first row of alien."""
    alien = Alien(setting, screen, ship)
    number_rows = get_number_rows(setting, ship.rect.height, alien.rect.height)
    number_alien_x = get_number_aliens_x(setting, alien.rect.width)
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(setting, screen, aliens, alien_number, row_number, ship)


"""1st loop vaneko y ko position ie row number ko loop ani 2nd vaneko alien ko x ko position ma alien number ko loop"""


def fire_bullets(bullets, setting, screen, ship):
    # Create the new bullet and add it to bullets group
    if len(bullets) < setting.bullets_allowed:
        new_bullet = Bullet(setting, screen, ship)
        bullets.add(new_bullet)


def check_key_down_event(ship, event, bullets, screen, setting):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:  # 2 ota thicho vane kasari duitei event ganinxa
        # up ra right key thichda kheri ani space thicho vane bullet niskinxa tara aru combination ma chai niskinna
        # kina?
        fire_bullets(bullets, setting, screen, ship)


def check_key_up_event(ship, event):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ship, setting, screen, bullets, stats, play_button, aliens, sb):
    """Checks for keyboard and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, setting, screen, ship, aliens, bullets, sb)
        elif event.type == pygame.KEYDOWN:
            # print(pygame.KEYDOWN)
            # When we press the key the event is said to be KEYDOWN
            check_key_down_event(ship, event, bullets, screen, setting)
        elif event.type == pygame.KEYUP:
            # print(pygame.KEYUP)
            # when we lift our finger up after pressing key, then the event is said to be KEYUP
            check_key_up_event(ship, event)


def check_play_button(stats, play_button, mouse_x, mouse_y, setting, screen, ship, aliens, bullets, sb):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        setting.initialize_dynamic_settings()
        # checks whether the mouse is clicked on play_button object which was at the middle of the screen and if yes returns True.
        pygame.mouse.set_visible(False)  # make mouse cursor not visible on the surface.
        aliens.empty()
        bullets.empty()
        create_fleet(setting, screen, aliens, ship)
        ship.center_ship()
        stats.reset_stats()
        stats.game_active = True
        sb.prep_ships()


def update_screen(setting, screen, ship, bullets, aliens, play_button, stats, sb):
    # Redraw the screen
    screen.fill(setting.bg_color)
    # Make the most recently drawn screen visible.
    # Redraw all the bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # Draw the score info
    sb.show_score()
    ship.blitme()  # blitme because only one image needed to be updated
    aliens.draw(screen)  # we use draw because multiple image should be updated and drawn on the screen.
    if not stats.game_active:
        play_button.draw_button()
        sb.prep_score()
        sb.prep_level()
    pygame.display.flip()


def update_bullets(bullets, aliens, setting, screen, ship, stats, sb):
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_alien_bullet_collision(bullets, aliens, setting, screen, ship, stats, sb)


def check_alien_bullet_collision(bullets, aliens, setting, screen, ship, stats, sb):
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # collisions will be the key value pair of bullet and alien that collided.
    """
    In the case of pygame.sprite.groupcollide(bullets, aliens, True, True), the function checks for collisions between 
    all the bullet sprites in the bullets group and all the alien sprites in the aliens group. If any bullet sprite 
    collides with any alien sprite, the function removes both sprites from their respective groups, as specified by the 
    third and fourth arguments.
    """
    if collisions:
        for aliens in collisions.values():
            stats.score += setting.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        setting.increase_speed()  # increases the speed of everything after all aliens vanishes by hitting with bullet
        create_fleet(setting, screen, aliens, ship)
        stats.level += 1
        sb.prep_level()


def update_aliens(aliens, setting, ship, stats, bullets, screen, sb):
    """
     Check if the fleet is at an edge,
     and then update the postions of all aliens in the fleet.
     """
    check_fleet_edges(setting, aliens)
    aliens.update()
    check_alien_ship_collision(ship, aliens, setting, stats, screen, bullets, sb)
    check_aliens_bottom(setting, stats, screen, ship, aliens, bullets)


def check_alien_ship_collision(ship, aliens, setting, stats, screen, bullets, sb):
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(setting, stats, screen, ship, aliens, bullets, sb)


def ship_hit(setting, stats, screen, ship, aliens, bullets, sb):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1
        sb.prep_ships()
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        # Create a new fleet and center the ship.
        sleep(0.5)  # Pause.
        create_fleet(setting, screen, aliens, ship)
        ship.center_ship()
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)  # make mouse cursor visible on the surface
        stats.score = 0
        stats.level = 1


def check_aliens_bottom(setting, stats, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(setting, stats, screen, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
