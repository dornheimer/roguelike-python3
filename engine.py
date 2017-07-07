import libtcodpy as libtcod

from entity import Entity
from fov_functions import initialize_fov, recompute_fov
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all


def main():
    """Main game loop.
    Initializes console(s), creates game and FOV maps and runs main loop with
    calls to render functions and input handlers.

    Contains:
        * Parameters for screen, room generator, FOV and tile colors
        * List of instances of the Entity class
    """
    ### Variables
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    #fov_algorithm = 0
    #fov_light_walls = True
    fov_radius = 10

    ### Colors
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    ### Entities
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow)
    entities = [npc, player]

    ### Console
    # libtcod.console_set_custom_font('terminal10x16_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_set_custom_font('terminal16x16_gs_ro.png', libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(screen_width, screen_height, 'rl-py3', False)
    con = libtcod.console_new(screen_width, screen_height)

    ### Game map
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    ### Main loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius)

        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width,
                    screen_height, colors)

        fov_recompute = False

        libtcod.console_flush()
        clear_all(con, entities)

        # Player input
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            # Check if tile is passable
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

                # Recompute FOV everytime the player moves
                fov_recompute = True

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
