import argparse

import h3m_constants
import common_functions

file = ''
# common_functions.gen_text_files()
parser = argparse.ArgumentParser(prog='HOMM_map_scanner',
                                 description=h3m_constants.description)
parser.add_argument('filepath', help='Takes path to a map file', type=str)

detail_group = parser.add_argument_group('Global settings',
                                         'Settings which define the general level of detalization')
detail = detail_group.add_mutually_exclusive_group(required=True)
detail.add_argument('-n', '--none', action='store_true',
                    help='Sets all blocks to "none" detalization')
detail.add_argument('-b', '--brief', action='store_true',
                    help='Sets all blocks to "brief" detalization')
detail.add_argument('-s', '--standard', action='store_true',
                    help='Sets all blocks to "standard" detalization')
detail.add_argument('-e', '--extended', action='store_true',
                    help='Sets all blocks to "extended" detalization')

specification_group = parser.add_argument_group('Separate settings',
                                                'Settings which specify separate blocks by \
                                                overwriting the global settings\n \
                                                Each parameter must have an argument in range of 0..3:\n \
                                                0 - None, 1 - Brief, 2 - Standard, 3 - Extended')
specification_group.add_argument('--format', choices=range(4),
                                 help="Changes formats' detalization to a specified one")
specification_group.add_argument('--size', choices=range(4),
                                 help="Changes size's detalization to a specified one")
specification_group.add_argument('--info', choices=range(4),
                                 help="Changes info's detalization to a specified one")
specification_group.add_argument('--players', choices=range(4),
                                 help="Changes players' detalization to a specified one")
specification_group.add_argument('--victory_cond', choices=range(4),
                                 help="Changes victory conditions' detalization to a specified one")
specification_group.add_argument('--loss_cond', choices=range(4),
                                 help="Changes loss conditions' detalization to a specified one")
specification_group.add_argument('--teams', choices=range(4),
                                 help="Changes teams' detalization to a specified one")
specification_group.add_argument('--heroes', choices=range(4),
                                 help="Changes heroes' detalization to a specified one")

args = parser.parse_args()

if args.filepath:
    try:
        data = common_functions.gzip_file_to_hex_bytes(args.filepath)
    except FileNotFoundError:
        print(args.filepath, "file does not exist")
    except IsADirectoryError:
        print("A file was expected but the directory was found")
    except Exception:
        print("Unknown error. Please, try again.")
    else:
        param = [0] * len(h3m_constants.blocks)
        try:
            common_functions.scan_file(data, h3m_constants.blocks, param)
        except RuntimeError:
            print(args.filepath, "is not a correct map file")
        except Exception:
            print("Unknown error. Please, try again.")
        else:
            print()
            if args.none:
                param = [0] * len(h3m_constants.blocks)
            if args.brief:
                param = [1] * len(h3m_constants.blocks)
            if args.standard:
                param = [2] * len(h3m_constants.blocks)
            if args.extended:
                param = [3] * len(h3m_constants.blocks)
            if args.format is not None:
                param[h3m_constants.matches['format']] = args.format
            if args.size is not None:
                param[h3m_constants.matches['size']] = args.size
            if args.info is not None:
                param[h3m_constants.matches['info']] = args.info
            if args.players is not None:
                param[h3m_constants.matches['players']] = args.players
            if args.victory_cond is not None:
                param[h3m_constants.matches['victory_cond']] = args.victory_cond
            if args.loss_cond is not None:
                param[h3m_constants.matches['loss_cond']] = args.loss_cond
            if args.teams is not None:
                param[h3m_constants.matches['teams']] = args.teams
            common_functions.scan_file(data, h3m_constants.blocks, param)
