from bingo import read_bingo_input, check_winner, find_winner, find_loser, calculate_score


def test_read_bingo_numbers():
    numbers, _ = read_bingo_input()
    assert numbers[0] == 67
    assert numbers[-1] == 33


def test_read_bingo_boards():
    _, boards = read_bingo_input()

    assert len(boards) == 100
    assert boards[0] == [[12, 75, 58, 21, 87],
                         [55, 80, 14, 63, 17],
                         [37, 35, 76, 92, 56],
                         [72, 68, 51, 19, 38],
                         [91, 60, 34, 30, 88]]


def test_check_winner_horizontal():
    board = [[12, 75, 58, 21, 87],
             [55, 80, 14, 63, 17],
             [37, 35, 76, 92, 56],
             [72, 68, 51, 19, 38],
             [91, 60, 34, 30, 88]]

    assert check_winner(board, [72, 68, 51, 19]) == False
    assert check_winner(board, [72, 68, 51, 19, 38]) == True


def test_check_winner_vertical():
    board = [[12, 75, 58, 21, 87],
             [55, 80, 14, 63, 17],
             [37, 35, 76, 92, 56],
             [72, 68, 51, 19, 38],
             [91, 60, 34, 30, 88]]

    assert check_winner(board, [75, 80, 35, 68]) == False
    assert check_winner(board, [75, 80, 35, 68, 60]) == True


def test_find_winner():
    boards = [
        [[1, 2], [3, 4]],
        [[5, 6], [7, 8]],
        [[9, 10], [11, 12]]
    ]
    winner, marked = find_winner(boards, [1, 4, 9, 12, 5, 7, 8, 10, 11])
    assert winner == [[5, 6], [7, 8]]
    assert marked == [1, 4, 9, 12, 5, 7]


def test_find_loser():
    boards = [
        [[1, 2], [3, 4]],
        [[5, 6], [7, 8]],
        [[9, 10], [11, 12]]
    ]
    loser, marked = find_loser(
        boards, [1, 9, 2, 10, 3, 4, 5, 6, 7, 8, 12, 5, 7, 8, 10, 11])
    assert loser == [[5, 6], [7, 8]]
    assert marked == [1, 9, 2, 10, 3, 4, 5, 6]


def test_calculate_score():
    board = [
        [14, 21, 17, 24,  4],
        [10, 16, 15,  9, 19],
        [18,  8, 23, 26, 20],
        [22, 11, 13,  6,  5],
        [2,  0, 12,  3,  7]
    ]
    marked = [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24]
    score = calculate_score(board, marked)
    assert score == 4_512
