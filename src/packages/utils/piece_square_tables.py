piece_evaluation: dict[str, float] = {
    "K": 20,
    "Q": 9,
    "R": 5,
    "B": 3.3,
    "N": 3.2,
    "P": 1,
}


wP_table = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    [0.1, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.1],
    [0.05, 0.05, 0.1, 0.25, 0.25, 0.1, 0.05, 0.05],
    [0.0, 0.0, 0.0, 0.2, 0.2, 0.0, 0.0, 0.0],
    [0.05, -0.05, -0.1, 0.0, 0.0, -0.1, -0.05, 0.05],
    [0.05, 0.1, 0.1, -0.2, -0.2, 0.1, 0.1, 0.05],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
]

wN_table = [
    [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5],
    [-0.4, -0.2, 0.0, 0.0, 0.0, 0.0, -0.2, -0.4],
    [-0.3, 0.0, 0.1, 0.15, 0.15, 0.1, 0.0, -0.3],
    [-0.3, 0.05, 0.15, 0.2, 0.2, 0.15, 0.05, -0.3],
    [-0.3, 0.0, 0.15, 0.2, 0.2, 0.15, 0.0, -0.3],
    [-0.3, 0.05, 0.1, 0.15, 0.15, 0.1, 0.05, -0.3],
    [-0.4, -0.2, 0.0, 0.05, 0.05, 0.0, -0.2, -0.4],
    [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5],
]


wB_table = [
    [-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2],
    [-0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1],
    [-0.1, 0.0, 0.05, 0.1, 0.1, 0.05, 0.0, -0.1],
    [-0.1, 0.05, 0.05, 0.1, 0.1, 0.05, 0.05, -0.1],
    [-0.1, 0.0, 0.1, 0.1, 0.1, 0.1, 0.0, -0.1],
    [-0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, -0.1],
    [-0.1, 0.05, 0.0, 0.0, 0.0, 0.0, 0.05, -0.1],
    [-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2],
]


wR_table = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05],
    [-0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.05],
    [-0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.05],
    [-0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.05],
    [-0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.05],
    [-0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.05],
    [0.0, 0.0, 0.0, 0.05, 0.05, 0.0, 0.0, 0.0],
]


wQ_table = [
    [-0.2, -0.1, -0.1, -0.05, -0.05, -0.1, -0.1, -0.2],
    [-0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1],
    [-0.1, 0.0, 0.05, 0.05, 0.05, 0.05, 0.0, -0.1],
    [-0.05, 0.0, 0.05, 0.05, 0.05, 0.05, 0.0, -0.05],
    [0.0, 0.0, 0.05, 0.05, 0.05, 0.05, 0.0, -0.05],
    [-0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.0, -0.1],
    [-0.1, 0.0, 0.05, 0.0, 0.0, 0.0, 0.0, -0.1],
    [-0.2, -0.1, -0.1, -0.05, -0.05, -0.1, -0.1, -0.2],
]

wK_middle_game_table = [
    [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
    [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
    [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
    [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
    [-0.2, -0.3, -0.3, -0.4, -0.4, -0.3, -0.3, -0.2],
    [-0.1, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.1],
    [0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2],
    [0.2, 0.3, 0.1, 0.0, 0.0, 0.1, 0.3, 0.2],
]


wK_end_game_table = [
    [-0.5, -0.4, -0.3, -0.2, -0.2, -0.3, -0.4, -0.5],
    [-0.3, -0.2, -0.1, 0.0, 0.0, -0.1, -0.2, -0.3],
    [-0.3, -0.1, 0.2, 0.3, 0.3, 0.2, -0.1, -0.3],
    [-0.3, -0.1, 0.3, 0.4, 0.4, 0.3, -0.1, -0.3],
    [-0.3, -0.1, 0.3, 0.4, 0.4, 0.3, -0.1, -0.3],
    [-0.3, -0.1, 0.2, 0.3, 0.3, 0.2, -0.1, -0.3],
    [-0.3, -0.3, 0.0, 0.0, 0.0, 0.0, -0.3, -0.3],
    [-0.5, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.5],
]


bP_table = [
    [-0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0],
    [-0.05, -0.1, -0.1, 0.2, 0.2, -0.1, -0.1, -0.05],
    [-0.05, 0.05, 0.1, -0.0, -0.0, 0.1, 0.05, -0.05],
    [-0.0, -0.0, -0.0, -0.2, -0.2, -0.0, -0.0, -0.0],
    [-0.05, -0.05, -0.1, -0.25, -0.25, -0.1, -0.05, -0.05],
    [-0.1, -0.1, -0.2, -0.3, -0.3, -0.2, -0.1, -0.1],
    [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5],
    [-0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0],
]


bN_table = [
    [0.5, 0.4, 0.3, 0.3, 0.3, 0.3, 0.4, 0.5],
    [0.4, 0.2, -0.0, -0.05, -0.05, -0.0, 0.2, 0.4],
    [0.3, -0.05, -0.1, -0.15, -0.15, -0.1, -0.05, 0.3],
    [0.3, -0.0, -0.15, -0.2, -0.2, -0.15, -0.0, 0.3],
    [0.3, -0.05, -0.15, -0.2, -0.2, -0.15, -0.05, 0.3],
    [0.3, -0.0, -0.1, -0.15, -0.15, -0.1, -0.0, 0.3],
    [0.4, 0.2, -0.0, -0.0, -0.0, -0.0, 0.2, 0.4],
    [0.5, 0.4, 0.3, 0.3, 0.3, 0.3, 0.4, 0.5],
]


bB_table = [
    [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
    [0.1, -0.05, -0.0, -0.0, -0.0, -0.0, -0.05, 0.1],
    [0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, 0.1],
    [0.1, -0.0, -0.1, -0.1, -0.1, -0.1, -0.0, 0.1],
    [0.1, -0.05, -0.05, -0.1, -0.1, -0.05, -0.05, 0.1],
    [0.1, -0.0, -0.05, -0.1, -0.1, -0.05, -0.0, 0.1],
    [0.1, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 0.1],
    [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2],
]


bR_table = [
    [-0.0, -0.0, -0.0, -0.05, -0.05, -0.0, -0.0, -0.0],
    [0.05, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 0.05],
    [0.05, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 0.05],
    [0.05, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 0.05],
    [0.05, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 0.05],
    [0.05, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 0.05],
    [-0.05, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.05],
    [-0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0],
]


bQ_table = [
    [0.2, 0.1, 0.1, 0.05, 0.05, 0.1, 0.1, 0.2],
    [0.1, -0.0, -0.0, -0.0, -0.0, -0.05, -0.0, 0.1],
    [0.1, -0.0, -0.05, -0.05, -0.05, -0.05, -0.05, 0.1],
    [0.05, -0.0, -0.05, -0.05, -0.05, -0.05, -0.0, -0.0],
    [0.05, -0.0, -0.05, -0.05, -0.05, -0.05, -0.0, 0.05],
    [0.1, -0.0, -0.05, -0.05, -0.05, -0.05, -0.0, 0.1],
    [0.1, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 0.1],
    [0.2, 0.1, 0.1, 0.05, 0.05, 0.1, 0.1, 0.2],
]

bK_middle_game_table = [
    [-0.2, -0.3, -0.1, -0.0, -0.0, -0.1, -0.3, -0.2],
    [-0.2, -0.2, -0.0, -0.0, -0.0, -0.0, -0.2, -0.2],
    [0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.1],
    [0.2, 0.3, 0.3, 0.4, 0.4, 0.3, 0.3, 0.2],
    [0.3, 0.4, 0.4, 0.5, 0.5, 0.4, 0.4, 0.3],
    [0.3, 0.4, 0.4, 0.5, 0.5, 0.4, 0.4, 0.3],
    [0.3, 0.4, 0.4, 0.5, 0.5, 0.4, 0.4, 0.3],
    [0.3, 0.4, 0.4, 0.5, 0.5, 0.4, 0.4, 0.3],
]


bK_end_game_table = [
    [0.5, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.5],
    [0.3, 0.3, -0.0, -0.0, -0.0, -0.0, 0.3, 0.3],
    [0.3, 0.1, -0.2, -0.3, -0.3, -0.2, 0.1, 0.3],
    [0.3, 0.1, -0.3, -0.4, -0.4, -0.3, 0.1, 0.3],
    [0.3, 0.1, -0.3, -0.4, -0.4, -0.3, 0.1, 0.3],
    [0.3, 0.1, -0.2, -0.3, -0.3, -0.2, 0.1, 0.3],
    [0.3, 0.2, 0.1, -0.0, -0.0, 0.1, 0.2, 0.3],
    [0.5, 0.4, 0.3, 0.2, 0.2, 0.3, 0.4, 0.5],
]
