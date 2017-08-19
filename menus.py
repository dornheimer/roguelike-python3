import libtcodpy as libtcod


def menu(con, header, options, width, screen_width, screen_height):
    """Show menu window in center of the screen."""
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    # Calculate total height for the header (after auto-wrap) and one more line per option
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # Create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # Print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.lightest_grey)
    libtcod.console_set_color_control(libtcod.COLCTRL_1, libtcod.lighter_sepia, libtcod.black)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # Print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = f'%c({chr(letter_index)})%c{option_text}' % (libtcod.COLCTRL_1, libtcod.COLCTRL_STOP)
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # Blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)


def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
    """Show a menu with each item of the inventory as an option."""
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []

        for item in player.inventory.items:
            if item in player.equipment.equipped:
                libtcod.console_set_color_control(libtcod.COLCTRL_3, libtcod.darker_grey, libtcod.black)
                options.append(f'%c{item.name} (equipped)%c' % (libtcod.COLCTRL_3, libtcod.COLCTRL_STOP))
            else:
                libtcod.console_set_color_control(libtcod.COLCTRL_2, libtcod.lightest_grey, libtcod.black)
                options.append(f'%c{item.name}%c' % (libtcod.COLCTRL_2, libtcod.COLCTRL_STOP))

    menu(con, header, options, inventory_width, screen_width, screen_height)


def equipment_menu(con, header, player, equipment_menu_width, screen_width, screen_height):
    """Show what items the player has equipped on the equipment slots."""
    header_height = libtcod.console_get_height_rect(con, 0, 0, equipment_menu_width, screen_height, header)
    height = header_height + 10

    window = libtcod.console_new(equipment_menu_width, height)

    libtcod.console_set_default_foreground(window, libtcod.lightest_grey)

    libtcod.console_set_color_control(libtcod.COLCTRL_1, libtcod.lighter_sepia, libtcod.black)
    libtcod.console_set_color_control(libtcod.COLCTRL_2, libtcod.dark_grey, libtcod.black)
    libtcod.console_set_color_control(libtcod.COLCTRL_3, libtcod.light_han, libtcod.black)
    libtcod.console_set_color_control(libtcod.COLCTRL_4, libtcod.dark_magenta, libtcod.black)


    slots = [
            (player.equipment.main_hand, 'Main hand'),
            (player.equipment.off_hand, 'Off hand'),
            (player.equipment.torso, 'Torso'),
            (player.equipment.head, 'Head'),
            (player.equipment.coat, 'Coat'),
            (player.equipment.ring_l, 'Ring (left)'),
            (player.equipment.ring_r, 'Ring (right)'),
            (player.equipment.special, 'Special')
    ]

    libtcod.console_print_rect_ex(window, 0, 1, equipment_menu_width, height, libtcod.BKGND_NONE,
                                    libtcod.LEFT, header)

    line = header_height + 1
    letter_index = ord('a')

    for slot, slot_desc in slots:
        equippable_name = '%cEmpty.%c' % (libtcod.COLCTRL_2, libtcod.COLCTRL_STOP)
        index_prefix = f'%c({chr(letter_index)})%c'% (libtcod.COLCTRL_1, libtcod.COLCTRL_STOP)

        if slot is not None:
            equippable_name = f'%c{slot.name} %c{slot.equippable}%c' % (libtcod.COLCTRL_3, libtcod.COLCTRL_4, libtcod.COLCTRL_STOP)
            equippable_stats = str(slot.equippable)

        libtcod.console_print_rect_ex(window, 0, line, equipment_menu_width, height, libtcod.BKGND_NONE,
                                        libtcod.LEFT, '{0}{1}: {2}'.format(index_prefix, slot_desc, equippable_name))
        line += 1
        letter_index += 1

    x = int(screen_width / 2 - equipment_menu_width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, equipment_menu_width, height, 0, x, y, 1.0, 0.7)


def main_menu(con, background_image, screen_width, screen_height):
    """Main menu screen with options to choose from."""
    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                            'DEEPGLOW')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE, libtcod.CENTER,
                            'by iiu')

    menu(con, '', ['new game', 'continue last game', 'quit'], 24, screen_width, screen_height)


def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    """Show level up menu with option to choose from."""
    options = ['Constitution (+20 HP, from {0})'.format(player.fighter.max_hp),
                'Strength (+1 attack, from {0})'.format(player.fighter.power),
                'Agility (+1 defense, from {0})'.format(player.fighter.defense)]

    menu(con, header, options, menu_width, screen_width, screen_height)


def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    """Show character_screen with basic information."""
    window = libtcod.console_new(character_screen_width, character_screen_height)

    libtcod.console_set_default_foreground(window, libtcod.lightest_grey)
    libtcod.console_set_color_control(libtcod.COLCTRL_1, libtcod.dark_magenta, libtcod.black)


    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                    libtcod.LEFT, 'Character Information')

    player_level = f'Level: %c{player.level.current_level}%c' % (libtcod.COLCTRL_1, libtcod.COLCTRL_STOP)
    libtcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                    libtcod.LEFT, player_level)

    player_experience = f'Experience: %c{player.level.current_xp}%c' % (libtcod.COLCTRL_1, libtcod.COLCTRL_STOP)
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                    libtcod.LEFT, player_experience)

    player_experience_to_next_level = f'Experience to level: %c{player.level.experience_to_next_level}%c' % (libtcod.COLCTRL_1, libtcod.COLCTRL_STOP)
    libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                    libtcod.LEFT, player_experience_to_next_level)

    player_maximum_hp = f'Maximum HP: %c{player.fighter.max_hp}%c' % (libtcod.COLCTRL_1, libtcod.COLCTRL_STOP)
    libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                    libtcod.LEFT, player_maximum_hp)

    player_attack = f'Attack: %c{player.fighter.power}%c' % (libtcod.COLCTRL_1, libtcod.COLCTRL_STOP)
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                    libtcod.LEFT, player_attack)

    player_defense = f'Defense: %c{player.fighter.defense}%c' % (libtcod.COLCTRL_1, libtcod.COLCTRL_STOP)
    libtcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                    libtcod.LEFT, player_defense)

    x = int(screen_width / 2 - character_screen_width / 2)
    y = int(screen_height / 2 - character_screen_height / 2)
    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)


def message_box(con, header, width, screen_width, screen_height):
    """Show message box."""
    menu(con, header, [], width, screen_width, screen_height)


def description_box(con, description, width, screen_width, screen_height, x, y):
    """Show box at specific location with description of entity."""
    height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, description)
    window = libtcod.console_new(width, height)

    libtcod.console_set_default_foreground(window, libtcod.lightest_grey)

    if description:
        libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, description)
        libtcod.console_blit(window, 0, 0, width, height, 0, x, y - height, 1.0, 0.7)
