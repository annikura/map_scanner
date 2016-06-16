def __write_into_file(filename, data):
    file = open(filename, "w")
    for line in data:
        file.write(line + "\n")
    file.close()


def difficulties_gen():
    a = ['Easy', 'Normal', 'Hard', 'Expert', 'Impossible']
    __write_into_file('difficulties.txt', a)


def behavior_gen():
    a = ['Random', 'Warrior', 'Builder', 'Explorer']
    __write_into_file('behavior.txt', a)


def format_gen():
    a = ['14-RoE', '21-AB', '28-SoD', '51-WoG']
    __write_into_file('formats.txt', a)


def players_gen(size=8):
    a = ['Red', 'Blue', 'Tan', 'Green', 'Orange', 'Purple', 'Teal', 'Pink']
    a += [''] * (size - len(a))
    __write_into_file('players.txt', a)


def town_types_gen(size=256):
    a = ['Castle', 'Rampart', 'Tower', 'Inferno', 'Necropolis',
         'Dungeon', 'Stronghold', 'Fortress', 'Conflux']
    a += [''] * (size - len(a) - 1)
    a.append('Random Town')
    __write_into_file('town_types.txt', a)


def victory_conditions_gen(size=256):
    a = [
        'Acquire a specific artifact',
        'Accumulate creatures',
        'Accumulate resources',
        'Upgrade a specific town',
        'Build a grail structure',
        'Defeat a specific Hero',
        'Capture a specific town',
        'Defeat a specific monster',
        'Flag all creature dwelling',
        'Flag all mines',
        'Transport a specific artifact'
    ]
    a += [''] * (size - len(a) - 1)
    a.append("None")
    __write_into_file('victory_conditions.txt', a)


def loss_conditions_gen(size=256):
    a = [
        'Lose a specific town',
        'Lose a specific hero',
        'Time expires'
    ]
    a += [''] * (size - len(a) - 1)
    a.append("None")
    __write_into_file('loss_conditions.txt', a)


def resources_gen():
    a = ["Wood", "Mercury", "Ore", "Sulfur", "Crystal", "Gems", "Gold"]
    __write_into_file('resources.txt', a)


def hall_levels_gen():
    a = ["Town", "City", "Capitol"]
    __write_into_file('hall_levels.txt', a)


def castle_levels_gen():
    a = ["Fort", "Citadel", "Castle"]
    __write_into_file('castle_levels.txt', a)


def fractions_gen():
    a = ["Castle", "Rampart", "Tower",
         "Inferno", "Necropolis", "Dungeon",
         "Stronghold", "Fortress", "Conflux"]
    __write_into_file('fractions.txt', a)
