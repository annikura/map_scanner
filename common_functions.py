import generators
import gzip


def gen_text_files():
    generators.behavior_gen()
    generators.difficulties_gen()
    generators.format_gen()
    generators.loss_conditions_gen()
    generators.players_gen()
    generators.town_types_gen()
    generators.victory_conditions_gen()
    generators.resources_gen()
    generators.castle_levels_gen()
    generators.hall_levels_gen()
    generators.fractions_gen()


def gzip_file_to_hex_bytes(filename):
    file = open(filename, "rb")
    string = gzip.decompress(file.read())
    hex_bytes = []
    for i in range(len(string)):
        h = hex(string[i])[2:]
        if len(h) == 1:
            h = '0' + h
        hex_bytes.append(h)
    return hex_bytes


def scan_file(data, functions, param):
    pointer = 0
    for i in range(len(functions)):
        pointer = functions[i](pointer, data, param[i])
    # if pointer != len(data):
