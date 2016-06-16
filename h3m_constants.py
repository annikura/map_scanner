import h3m_functions

blocks = [
    h3m_functions.format_block,
    h3m_functions.size_block,
    h3m_functions.info_block,
    h3m_functions.players_block,
    h3m_functions.victory_cond_block,
    h3m_functions.loss_cond_block,
    h3m_functions.teams_block
]

matches = {
    'format': 0,
    'size': 1,
    'info': 2,
    'players': 3,
    'victory_cond': 4,
    'loss_cond': 5,
    'teams': 6
}

description = 'Prints the info about the given HOMM map according to the input parameters' \
              '\nWARNING!\n' \
              '\t\tThe "extended" format may contain some spoilers about town\'s, ' \
              'creature\'s, hero\'s location or some other info which may be odd'
