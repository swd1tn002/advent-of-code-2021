# Player 1 starting position: 5
# Player 2 starting position: 8

p1_pos = 5
p2_pos = 8

p1_score = 0
p2_score = 0

next_dice = 1


def roll_thrice(dice):
    return dice * 3 + 3, dice + 3


turn = 0

while p1_score < 1_000 and p2_score < 1_000:
    rolls, next_dice = roll_thrice(next_dice)

    if turn % 2 == 0:
        p1_pos = (p1_pos - 1 + rolls) % 10 + 1
        p1_score += p1_pos
        print(f'P1 moves to {p1_pos} with total score {p1_score}')
    else:
        p2_pos = (p2_pos - 1 + rolls) % 10 + 1
        p2_score += p2_pos
        print(f'P2 moves to {p2_pos} with total score {p2_score}')

    turn += 1

print(p1_score, p2_score)
print(turn * 3)

print(f'Part 1: {min(p1_score, p2_score) * turn * 3}')
