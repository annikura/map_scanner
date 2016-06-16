
bool_size = 1
players_cnt = 8
f = ''
roe = "RoE\n"
ab = "AB\n"
active_players = []
fractions_available = []


def __get_int(pointer, data, num_size=4, add=True):
    a = [data[pointer + i] for i in range(num_size)]
    number = ''
    for i in range(len(a)):
        number = a[i] + number
    if add:
        return int(number, 16), pointer + num_size
    return int(number, 16)


def __get_string(pointer, data, len_size=4, add=True):
    length, pointer = __get_int(pointer, data, len_size)
    string = ''
    for i in range(length):
        string += bytes([__get_int(pointer, data, num_size=1, add=False)]).decode('cp1251')
        pointer += 1

    if add:
        return string, pointer
    return string


def __get_fileline(filename, line_index):
    file = open(filename)
    line = file.readlines()[line_index]
    file.close()
    return line


def __get_coordinates(pointer, data, coordinate_size=1, add=True):
    x, pointer = __get_int(pointer, data, coordinate_size)
    y, pointer = __get_int(pointer, data, coordinate_size)
    z, pointer = __get_int(pointer, data, coordinate_size)
    if add:
        return x, y, z, pointer
    return x, y, z


def format_block(pointer, data, print_param=1, format_size=4, rubbish=1):  # rubbish - hero existence flag
    format_int, pointer = __get_int(pointer, data, num_size=format_size)
    file = open('formats.txt')
    output = 'None'
    for line in file:
        separator = line.find('-')
        format_id = int(line[:separator])
        format_name = line[separator + 1:]
        if format_id == format_int:
            output = format_name
            break
    file.close()
    if output == 'None':
        exit(RuntimeError)
    global f
    f = output  # since the content of the file depends on the game format, we should store it more global
    if print_param > 0:
        print("Format:")
        print("\t" + output, end='')
    return pointer + rubbish


def size_block(pointer, data, print_param=1,
               size_size=4, layers_size=1, rubbish=0):
    size, pointer = __get_int(pointer, data, size_size)
    levels, pointer = __get_int(pointer, data, layers_size)
    if print_param > 0:
        print("Map size:")
        print("\t" + str(size))
        print("Layers:")
        print("\t" + str(levels + 1) + "-layered")
    return pointer + rubbish


def info_block(pointer, data, print_param=1,
               diff_size=1, rubbish=0):
    name, pointer = __get_string(pointer, data)
    desc, pointer = __get_string(pointer, data)
    diff, pointer = __get_int(pointer, data, diff_size)
    if print_param > 0:
        print("Name:")
        try:
            print("\t" + name)
        except UnicodeError:
            print("\tNot available. Name contains invalid characters")
        print("Description:")
        try:
            print("\t" + desc)
        except UnicodeError:
            print("\tNot available. Description contains invalid characters")
        print("Difficulty:")
        print("\t" + __get_fileline('difficulties.txt', diff), end='')
    return pointer + rubbish


def players_block(pointer, data, print_param=1,
                  behavior_size=1, settings_size=1,
                  types_size=2, type_size=1, rubbish=0, frac_num=9):
    level_limit = 0
    humans = []
    comps = []
    humncomps = []
    global active_players, fractions_available
    active_players = []
    if f != roe:
        level_limit, pointer = __get_int(pointer, data, num_size=1)
    for player in range(players_cnt):
        f_human, pointer = __get_int(pointer, data, bool_size)
        f_comp, pointer = __get_int(pointer, data, bool_size)

        if f_human and not f_comp:
            humans.append(player)
        if f_comp and not f_human:
            comps.append(player)
        if f_comp and f_human:
            humncomps.append(player)
        if f_comp or f_human:
            active_players.append(player)
            behavior, pointer = __get_int(pointer, data, behavior_size)
            if f != roe and f != ab:
                f_town_settings, pointer = __get_int(pointer, data, settings_size)  # dunno what it is yet
            fractions_available.append(__get_int(pointer, data, types_size, add=False))
            pointer += types_size
            if f != roe:
                f_random_town, pointer = __get_int(pointer, data, bool_size)
            f_main_town, pointer = __get_int(pointer, data, bool_size)
            if f_main_town:
                if f != roe:
                    f_create_town_hero, pointer = __get_int(pointer, data, bool_size)
                    main_town_type, pointer = __get_int(pointer, data, type_size)
                x, y, z, pointer = __get_coordinates(pointer, data)
            f_rand_hero, pointer = __get_int(pointer, data, bool_size)
            hero_type, pointer = __get_int(pointer, data, num_size=1)
            if hero_type != 255:  # if hero type == FF than there is no any hero
                face_num, pointer = __get_int(pointer, data, num_size=1)
                try:
                    name, pointer = __get_string(pointer, data)
                except UnicodeError:
                    name = "Hero name contains invalid symbols"
                if f != roe:
                    pointer += 1  # rubbish byte
                    heroes_cnt, pointer = __get_int(pointer, data)
                    for hero in range(heroes_cnt):
                        hero_id, pointer = __get_int(pointer, data, num_size=1)
                        try:
                            hero_name, pointer = __get_string(pointer, data)
                        except UnicodeError:
                            print("Hero name contains invalid symbols")
                        else:
                            hero_name = "Unknown"
            else:
                if f != roe:
                    pointer += 5  # !!! 5 odd bytes seem to be for hero id and
                # his name length even if there is no any hero
        else:  # ToDo: fix nums
            pointer += 6
            if f != roe and f != ab:
                pointer += 1
            if f != roe:
                pointer += 6
            # !!! don't like it. Thinking. Nevertheless,
            # if player is inactive (neither human nor computer can play for it),
            # we always have 13 odd bytes UPD: not always, only in WoG and SoD formats
    if print_param > 0:
        print("Players:")
        print("\tThere are", len(active_players), "active players:")
        print("\t\t" + str(len(humans)) + " can be played by human players only")
        print("\t\t" + str(len(comps)) + " can be played by computer players only")
        print("\t\t" + str(len(humncomps)) + " can be played both by human and computer players")
        if print_param > 1:
            if level_limit != 0:
                print("\tHeroes' level limit:", level_limit)
            print("\tPlayers' specifications:")
            for player in active_players:
                player_colour = __get_fileline('players.txt', player)
                print("\t\t" + player_colour, end='')
                print("\t\t\tCan be played by ", end='')
                if player in humans:
                    print("human only")
                if player in humncomps:
                    print("human or computer")
                if player in comps:
                    print("computer only")
                print("\t\t\tFractions available:")
                string = ''
                cnt_fracs = 0
                for i in range(frac_num):
                    if (fractions_available[player] // (2 ** i)) % 2:
                        cnt_fracs += 1
                        string += "\t\t\t\t" + __get_fileline('fractions.txt', i)
                if cnt_fracs == frac_num:
                    string = "\t\t\t\tRandom fraction or any\n"
                print(string, end='')

    return pointer + rubbish


def victory_cond_block(pointer, data, print_param=1, rubbish=0):  # ToDo: get info about the towns and monsters
    cond, pointer = __get_int(pointer, data, num_size=1)
    if print_param > 0:
        print("Special victory condition:")
        print("\t" + __get_fileline('victory_conditions.txt', cond), end='')
    if cond != 255:  # if cond == 255 than there is no any special victory condition
        f_standard_ending, pointer = __get_int(pointer, data, bool_size)
        f_comp_available, pointer = __get_int(pointer, data, bool_size)
        if cond == 0:  # acquire a specific artifact
            artifact_num, pointer = __get_int(pointer, data, num_size=1)
            artifact = __get_fileline('artifacts.txt', artifact_num)
            if print_param > 1:
                print("\tArtifact:")
                print("\t\t" + artifact, end='')
        if cond == 1:  # accumulate creatures
            unit_code, pointer = __get_int(pointer, data, num_size=2)
            unit_name = __get_fileline('units.txt', unit_code)
            quantity, pointer = __get_int(pointer, data)
            if print_param > 1:
                print("\tUnit type:")
                print("\t\t" + unit_name, end='')
                print("\tQuantity:")
                print("\t\t" + str(quantity))
        if cond == 2:  # accumulate resources
            resource_code, pointer = __get_int(pointer, data, num_size=1)
            resource = __get_fileline('resources.txt', resource_code)
            quantity, pointer = __get_int(pointer, data)
            if print_param > 1:
                print("\tResource:")
                print("\t\t" + resource, end='')
                print("\tQuantity:")
                print("\t\t" + str(quantity))
        if cond == 3:  # upgrade a specific town
            x, y, z, pointer = __get_coordinates(pointer, data)
            hall_level_code, pointer = __get_int(pointer, data, num_size=1)
            hall_level = __get_fileline('hall_levels.txt', hall_level_code)
            castle_level_code, pointer = __get_int(pointer, data, num_size=1)
            castle_level = __get_fileline('castle_levels.txt', castle_level_code)
            if print_param > 2:
                print("\tTown location:")
                print("\t\tWidth:", x, "Length:", y, "Level:", z)
                print("\tHall level:")
                print("\t\t" + hall_level, end='')
                print("\tCastle level:")
                print("\t\t" + castle_level, end='')
        if cond == 4:  # build a grail structure
            x, y, z, pointer = __get_coordinates(pointer, data)
            if print_param > 2:
                print("\tTown location:")
                print("\t\tWidth:", x, "Length:", y, "Level:", z)
        if cond == 5:  # defeat a specific hero
            x, y, z, pointer = __get_coordinates(pointer, data)
            if print_param > 2:
                print("\tHero start location:")
                print("\t\tWidth:", x, "Length:", y, "Level:", z)
        if cond == 6:  # capture a specific town
            x, y, z, pointer = __get_coordinates(pointer, data)
            if print_param > 2:
                print("\tTown location:")
                print("\t\tWidth:", x, "Length:", y, "Level:", z)
        if cond == 7:  # defeat a specific monster
            x, y, z, pointer = __get_coordinates(pointer, data)
            print("\tMonster location:")
            print("\t\tWidth:", x, "Length:", y, "Level:", z)
        if cond == 8:  # flag all creatures dwelling
            pointer += 0
        if cond == 9:  # flag all mines
            pointer += 0
        if cond == 10:  # transport a specific artifact
            artifact_code, pointer = __get_int(pointer, data, num_size=1)
            artifact = __get_fileline('artifacts.txt', artifact_code)
            x, y, z, pointer = __get_coordinates(pointer, data)
            if print_param > 2:
                print("\tArtifact:")
                print("\t\t" + artifact, end='')
                print("\tTown location:")
                print("\t\tWidth:", x, "Length:", y, "Level:", z)
        if print_param > 1:
            print("\tAdditional info:")
            if f_standard_ending:
                print("\t\tStandard ending is also available")
            else:
                print("\t\tStandard ending is not available")
            if f_comp_available:
                print("\t\tSpecial condition is also available for computer players")
            else:
                print("\t\tSpecial condition is available for human players only")
    return pointer + rubbish


def loss_cond_block(pointer, data, print_param=1, rubbish=0):
    cond, pointer = __get_int(pointer, data, num_size=1)
    if print_param > 0:
        print("Special loss condition:")
        print("\t" + __get_fileline('loss_conditions.txt', cond), end='')
    if cond != 255:  # if cond == 255 than there is no any special loss condition
        if cond == 0:  # lose a specific town
            x, y, z, pointer = __get_coordinates(pointer, data)
            if print_param > 2:
                print("\tTown location:")
                print("\t\tWidth:", x, "Length:", y, "Level:", z)
        if cond == 1:  # lose a specific hero
            x, y, z, pointer = __get_coordinates(pointer, data)
            if print_param > 2:
                print("\tHero location:")
                print("\t\tWidth:", x, "Length:", y, "Level:", z)
        if cond == 2:  # time expires
            time_exp, pointer = __get_int(pointer, data, num_size=2)
            if print_param > 1:
                print("\t\tIn", time_exp // 28, "months,", time_exp % 28 // 7,
                      "weeks and",  time_exp % 28 % 7, "days")
    return pointer + rubbish


def teams_block(pointer, data, print_param=1, rubbish=0):
    teams_cnt, pointer = __get_int(pointer, data, num_size=1)
    if print_param > 0:
        print("Teams:")
        if teams_cnt == 0:
            print("\tNo teams")
        else:
            print("\tThere are", teams_cnt, "teams")
    if teams_cnt != 0:
        if print_param > 1:
            for i in range(teams_cnt):
                print("\tteam", i + 1, ":")
                for j in range(players_cnt):
                    team_num = __get_int(pointer + j, data, num_size=1, add=False)
                    if team_num == i and j in active_players:
                        print("\t\t" + __get_fileline('players.txt', j), end='')
        pointer += players_cnt
    return pointer + rubbish
