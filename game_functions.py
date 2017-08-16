import sys
from time import sleep
from random import randint

import pygame

from bullet import Bullet
from alien import Alien
from item import Item


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship
                      , aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship
                      , aliens, bullets, mouse_x, mouse_y):
    """플레이어가 Play 버튼을 클릭하고 게임이 진행중이지 않을 때 새 게임을 시작합니다."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 게임 설정을 리셋합니다.
        ai_settings.initialize_dynamic_settings()

        # 마우스 커서를 숨깁니다.
        pygame.mouse.set_visible(False)

        # 게임 기록을 리셋합니다.
        stats.reset_stats()
        stats.game_active = True

        # 점수판 이미지를 리세삽니다.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 외게인과 탄환 리스트를 비웁니다.
        aliens.empty()
        bullets.empty()

        # 외계인 함대를 새로 만들고 우주선을 중앙에 배치합니다.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet, if limit not reached yet."""
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """화면에 있는 이미지를 업데이트하고 새 화면에 그립니다."""
    # Redraw the screen, each pass through the loop.
    screen.fill(ai_settings.bg_color)
    
    # Redraw all bullets, behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # 점수를 표시합니다.
    sb.show_score()

    # 게임이 진행 중이지 않다면 Play 버튼을 그립니다.
    if not stats.game_active:
        play_button.draw_button()

    # 가장 최근에 그린 화면을 표시합니다.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, items):
    """Update position of bullets, and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, items)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, items):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.

    if items:
        # item 가져오기
        item = items[0]

        # item flag 가 true 이면 사라지지 않는 초강력 탄환
        # if item.flag:
            # collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
        # else:
            # collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

        print(item.flag)

    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(aliens) == 0:
        # 함대 전체를 격추했다면 다음 단계를 시작합니다.
        bullets.empty()
        ai_settings.increase_speed()

        # 단계를 올립니다.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)
        create_item(ai_settings, screen, items)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
        
def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet, and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """우주선이 외계인과 충돌했을 때"""
    if stats.ships_left > 0:
        # ships_left 를 줄입니다.
        stats.ships_left -= 1

        # 점수판을 업데이트 합니다.
        sb.prep_ships()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
    # 외계인과 탄환 리스트를 비웁니다.
    aliens.empty()
    bullets.empty()
    
    # Create a new fleet, and center the ship.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    
    # Pause.
    sleep(0.5)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """화면 맨 아래에 도달한 외계인이 있는지 검사합니다."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 외계인과 우주선이 충돌했을 때와 똑같이 반응합니다.
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Check if the fleet is at an edge,
      then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def update_items(ai_settings, screen, ship, items):
    """아이템 위치 업데이트"""
    screen_rect = screen.get_rect()
    if items:
        item = items[0]
        item_rect = item.get_rect()

        # 아이템이 바닥에 도달하면 아이템을 지운다.
        if screen_rect.bottom <= item_rect.bottom:
            items.empty()

        # 아이템이 함선과 만나는지 체크
        collisions = pygame.sprite.groupcollide(item, ship, True, False)

        if collisions:
            item.flag = True
        else:
            item.flag = False


def get_number_aliens_x(ai_settings, alien_width):
    """한 줄에 들어갈 외계인 숫자를 계산합니다."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """화면에 외계인이 몇 줄이 들어갈 수 있는지 계산합니다."""
    available_space_y = (ai_settings.screen_height -
                            (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_item(ai_settings, screen, items):
    """아이템을 만들고 랜덤으로 떨어트린다."""
    item = Item(ai_settings, screen)
    random_number = randint(0, 8)

    item.x = item.margin + 2 * item.margin * random_number
    item.rect.x = item.x
    item.rect.y = item.rect.height * 2
    items.add(item)


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """외계인을 만들고 줄 안에 넣습니다."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


# def create_alien(ai_settings, screen, aliens):
    # 외계인을 랜덤으로 떨어트리는 것
    # alien = Alien(ai_settings, screen)
    # alien_width = alien.rect.width
    # random_number = randint(0, 8)

    # alien.x = alien_width + 2 * alien_width * random_number
    # alien.rect.x = alien.x
    # alien.rect.y = alien.rect.height * 2
    # aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """외계인 함대 전체를 만듭니다."""
    # 외계인을 하나 만들고 한 줄에 표시할 외계인 숫자를 결정합니다.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
        alien.rect.height)
    
    # 외계인 한 줄을 만듭니다.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                row_number)
    # alien = Alien(ai_settings, screen)
    # create_alien(ai_settings, screen, aliens)

def check_high_score(stats, sb):
    """최고 점수보다 높은지 확인합니다."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()