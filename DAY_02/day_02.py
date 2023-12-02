from functools import reduce
from typing import Union, Tuple, List, Dict, NamedTuple
from collections import namedtuple
def check_sets_validity(game_sets: List[str], game_settings: Dict) -> bool:
    parameters = list(game_settings.keys())
    for parameter in parameters:
        max_number = game_settings.get(parameter)
        cubes_by_parameter = get_cubes_by_parameter(game_sets, parameter)
        if max(cubes_by_parameter) > max_number:
            return False
    return True

def get_cubes_by_parameter(game_sets: List[str], parameter: str) -> List[int]:
    gathered_cubes = []
    for cubes_by_turn in game_sets:
        if parameter in cubes_by_turn:
            gathered_cubes.append(int(cubes_by_turn.replace(parameter, '')))
    return gathered_cubes



def get_game_info(game: str, delimiters: NamedTuple) -> Tuple[str, List[str]]:
    game_id, cubes_sets = game.split(delimiters.game_delimiter)
    game_id = int(game_id.removeprefix(delimiters.game_name))
    cubes_sets = cubes_sets.split(delimiters.cubes_set_delimiter)
    cubes_sets = list(reduce(
                            lambda a, b: a + b,
                            list(map(
                                    lambda x: x.split(delimiters.cube_delimiter),
                                    cubes_sets
                                    ))))
    return game_id, cubes_sets



settings = {'red': 12, 'blue': 14, 'green': 13}
Delimiters = namedtuple('Game_Delimiter', 'game_delimiter game_name '
                                          'cubes_set_delimiter cube_delimiter')
game_delimiters = Delimiters(':', 'Game', ';', ',')

def check_game_validity(game: str, game_settings: Dict, game_delimiters: NamedTuple) -> Tuple:
    game_id, cubes_sets = get_game_info(game, game_delimiters)
    is_valid_game = check_sets_validity(cubes_sets, settings)
    return game_id, is_valid_game

with open('./day_02_input', 'r') as f:
    valid_games = []
    for line in f:
        valid_games.append(check_game_validity(line, settings, game_delimiters))
    print(sum([x[0] for x in valid_games if x[1]]))