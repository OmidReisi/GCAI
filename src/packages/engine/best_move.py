from .move_evaluation import get_move_evaluation
from .random_move import get_random_move
from .engine_move import is_move_draw
from ..move import Move

from concurrent.futures import ProcessPoolExecutor, as_completed
import pygame
import sys
import json


def get_best_move(
    valid_moves: list[Move],
    board_state: list[list[str]],
    board_hash: int,
    turn_to_move: str,
    king_pos: tuple[int, int],
    castle_rights: dict[str, bool],
    opponent_king_pos: tuple[int, int],
    opponent_castle_rights: dict[str, bool],
    openings: list[dict[str, str | list[str]]],
    opening_index: int,
    last_move: Move | None,
    zobrist_hash_keys: dict[str, int],
    hash_table: dict[str, float],
    hash_list: list[int],
    fifty_move_rule: int,
    depth: int,
) -> Move | None:
    """finding and returning the best move based on the possition.

    Args:
        valid_moves (list[Move]): valid_moves
        board_state (list[list[str]]): board_state
        board_hash (int): board_hash
        turn_to_move (str): turn_to_move
        king_pos (tuple[int, int]): king_pos
        castle_rights (dict[str, bool]): castle_rights
        opponent_king_pos (tuple[int, int]): opponent_king_pos
        opponent_castle_rights (dict[str, bool]): opponent_castle_rights
        openings (list[dict[str, str | list[str]]]): openings
        opening_index (int): opening_index
        last_move (Move | None): last_move
        zobrist_hash_keys (dict[str, int]): zobrist_hash_keys
        hash_table (dict[str, float]): hash_table
        hash_list (list[int]): hash_list
        fifty_move_rule (int): fifty_move_rule
        depth (int): depth

    Returns:
        Move | None:
    """

    best_moves: list[Move] = []
    secondary_moves: list[Move] = []

    min_max_eval = float("inf") if turn_to_move == "b" else -float("inf")

    if len(valid_moves) == 0:
        return None

    if len(openings) != 0:
        move_list: list[Move] = []
        for opening in openings:
            if len(opening["moves"]) > opening_index:
                move_to_add = Move.from_notation(
                    opening["moves"][opening_index],
                    board_state,
                    turn_to_move,
                    last_move,
                    castle_rights,
                    king_pos,
                )
                if move_to_add is not None:
                    move_list.append(move_to_add)

        if len(move_list) > 0:
            return get_random_move(move_list)

    with ProcessPoolExecutor() as executer:
        eval_results = [
            executer.submit(
                get_move_evaluation,
                move,
                board_state,
                board_hash,
                turn_to_move,
                king_pos,
                castle_rights,
                opponent_king_pos,
                opponent_castle_rights,
                zobrist_hash_keys,
                hash_table,
                depth,
            )
            for move in valid_moves
        ]

        for result in as_completed(eval_results):

            event = pygame.event.wait(timeout=1)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return None

            move_eval, move_hash, move = result.result()
            move_hash = int(move_hash)

            if move_hash not in hash_table:
                hash_table[move_hash] = move_eval
            else:
                update_hashed_moves_count()

            if turn_to_move == "b" and move_eval < min_max_eval:
                if is_move_draw(
                    # board_state,
                    # turn_to_move,
                    move,
                    move_hash,
                    hash_list,
                    fifty_move_rule,
                    # opponent_king_pos,
                    # opponent_castle_rights,
                ):
                    secondary_moves.append(move)
                    continue
                best_moves = [move]
                min_max_eval = move_eval
            elif turn_to_move == "w" and move_eval > min_max_eval:
                if is_move_draw(
                    # board_state,
                    # turn_to_move,
                    move,
                    move_hash,
                    hash_list,
                    fifty_move_rule,
                    # opponent_king_pos,
                    # opponent_castle_rights,
                ):
                    secondary_moves.append(move)
                    continue
                best_moves = [move]
                min_max_eval = move_eval

            elif move_eval == min_max_eval:
                best_moves.append(move)

        # for index, result in enumerate(eval_results):
        #     event = pygame.event.wait(timeout=1)
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         sys.exit()
        #     move = valid_moves[index]
        #     move_eval, move_hash = result.result()
        #     if move_hash not in hash_table:
        #         hash_table[move_hash] = move_eval
        #
        #     # for move in valid_moves:
        #     #
        #     #     move_eval = get_move_evaluation(
        #     #         move,
        #     #         board_state,
        #     #         board_hash,
        #     #         turn_to_move,
        #     #         king_pos,
        #     #         castle_rights,
        #     #         opponent_king_pos,
        #     #         opponent_castle_rights,
        #     #         zobrist_hash_keys,
        #     #         hash_table,
        #     #         depth,
        #     #     )
        #     #
        #     if turn_to_move == "b" and move_eval < min_max_eval:
        #         if -1000 < move_eval <= -1.5 and is_move_draw(
        #             board_state,
        #             turn_to_move,
        #             move,
        #             move_hash,
        #             hash_list,
        #             fifty_move_rule,
        #             opponent_king_pos,
        #             opponent_castle_rights,
        #         ):
        #             secondary_moves.append(move)
        #             continue
        #         best_moves = [move]
        #         min_max_eval = move_eval
        #     elif turn_to_move == "w" and move_eval > min_max_eval:
        #         if 1.5 <= move_eval < 1000 and is_move_draw(
        #             board_state,
        #             turn_to_move,
        #             move,
        #             move_hash,
        #             hash_list,
        #             fifty_move_rule,
        #             opponent_king_pos,
        #             opponent_castle_rights,
        #         ):
        #             secondary_moves.append(move)
        #             continue
        #         best_moves = [move]
        #         min_max_eval = move_eval
        #
        #     elif move_eval == min_max_eval:
        #         best_moves.append(move)
        #
    # print(time.perf_counter() - start_time)
    # if len(best_moves) == 0:
    #     print("secondary_moves")
    #     return get_random_move(secondary_moves)

    if turn_to_move == "w" and min_max_eval < 0 and len(secondary_moves) > 0:
        return get_random_move(secondary_moves)

    if turn_to_move == "b" and min_max_eval > 0 and len(secondary_moves) > 0:
        return get_random_move(secondary_moves)

    if len(best_moves) == 0:
        return get_random_move(secondary_moves)

    return get_random_move(best_moves)


def update_hashed_moves_count() -> None:
    """increase the number of hashed moves counter by 1

    Args:

    Returns:
        None:
    """

    with open(r"./packages/utils/hashed_moves_counter.json", "r") as json_file:
        counter = json.load(json_file)
        counter["count"] += 1

    with open(r"./packages/utils/hashed_moves_counter.json", "w") as json_file:
        json.dump(counter, json_file, indent=2)
