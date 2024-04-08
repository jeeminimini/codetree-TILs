import sys
import heapq

# n*n 격자
# 격자에는 무기. 빈 격자에 플레이어 위치. 초기 능력치 가짐. 초기 능력치는 모두 다름
n, m, k = map(int, sys.stdin.readline().split())
ground = []
ground_player = [[-1 for _ in range(n)] for _ in range(n)]
player = []

for i in range(n):
    ground.append(list(map(lambda x: [int(x) * -1] if int(x) > 0 else [], sys.stdin.readline().split())))

NO_GUN = 0
# x, y, d(방향), s(초기 능력치), 총
for i in range(m):
    x, y, d, s = map(int, sys.stdin.readline().split())
    x -= 1
    y -= 1
    player.append([x, y, d, s, NO_GUN])
    ground_player[x][y] = i

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
X = 0
Y = 1
DIR = 2
HTH = 3
GUN = 4
NONE = -1
points = [0 for _ in range(m)]


# 빨간 배경의 숫자: 총 - 공격력, 플레이어 - 초기 능력치
# 노란 배경의 숫자: 플레이어 번호

# 절차

def print_all(num):
    global n, player, ground, dx, dy, points, X, Y, DIR, HTH, GUN, NONE, points, ground_player, NO_GUN

    print(f"<{num}>")
    print(f"player {player}")
    print("ground")
    for i in range(n):
        print(ground[i])
    print("ground_player")
    for i in range(n):
        print(ground_player[i])

    print()


def move_player(num):
    global n, player, ground, dx, dy, points, X, Y, DIR, HTH, GUN, NONE, points, ground_player, NO_GUN

    # 1-1. 첫번째 플레이어부터 본인의 방향대로 한 칸 이동.
    # 격자 벗어나는 경우 정반대 방향으로 바꿔서 1만큼 이동.
    if not (0 <= player[num][X] + dx[player[num][DIR]] < n and 0 <= player[num][Y] + dy[player[num][DIR]] < n):
        player[num][DIR] = (player[num][DIR] + 2) % 4

    new_x = player[num][X] + dx[player[num][DIR]]
    new_y = player[num][Y] + dy[player[num][DIR]]
    ground_player[player[num][X]][player[num][Y]] = NONE

    # print(f"new_x {new_x} new_y {new_y}")
    # print_all(1)
    # 2-1. 만약 이동한 방향에 플레이어 없으면, 총이 있는지 확인.
    # 총이 있으면, 총 획득
    # 이미 총이 있었다면, 더 공격력이 쎈 총 획득. 나머지 총들은 해당 격자에 둠.

    if ground_player[new_x][new_y] == NONE:  # 플레이어 없으면
        if player[num][GUN] != NO_GUN:
            heapq.heappush(ground[new_x][new_y], player[num][GUN] * -1)
        if len(ground[new_x][new_y]) > 0:
            player[num][GUN] = heapq.heappop(ground[new_x][new_y]) * -1
        ground_player[new_x][new_y] = num
        player[num][X] = new_x
        player[num][Y] = new_y
        # print_all(2)
    else:  # 플레이어 있으면
        # 2-2-1. 만약 이동한 방향에 플레이어 있으면, 두 플레이어 싸움
        # (해당 플레이어 초기 능력치 + 총의 공격력)이 더 큰 플레이어가 이김.
        # 만약 수치가 같으면 초기 능력치가 더 높은 플레이어가 이김.

        other = ground_player[new_x][new_y]
        winner = -1
        loser = -1
        if player[num][HTH] + player[num][GUN] > player[other][HTH] + player[other][GUN]:
            winner = num
            loser = other
        elif player[num][HTH] + player[num][GUN] < player[other][HTH] + player[other][GUN]:
            winner = other
            loser = num
        else:
            if player[num][HTH] > player[other][HTH]:
                winner = num
                loser = other
            else:
                winner = other
                loser = num

        # 이긴 플레이어는 각 플레이어의 (해당 플레이어 초기 능력치 + 총의 공격력) 차이만큼 포인트 획득.
        points[winner] += (player[winner][HTH] + player[winner][GUN]) - (player[loser][HTH] + player[loser][GUN])

        # print_all(3)
        # 2-2-2. 진 플레이어는 본인 총을 격자에 내려놓고, 해당 플레이어 원래 방향대로 한 칸 이동.
        # 만약 이동하려는 칸에 플레이어 있거나 격자 범위 밖이면, 오른쪽으로 90도 회전해서 빈 칸이 보이는 순간 이동.
        # 만약 그 칸에 총있으면, 가장 공격력이 높은 총 획득. 나머지 격자에 내려놓음.
        if player[loser][GUN] != NO_GUN:
            heapq.heappush(ground[new_x][new_y], player[loser][GUN] * -1)
        player[loser][GUN] = NO_GUN

        for i in range(4):
            if 0 <= new_x + dx[(player[loser][DIR] + i) % 4] < n and 0 <= new_y + dy[(player[loser][DIR] + i) % 4] < n and ground_player[new_x + dx[(player[loser][DIR] + i) % 4]][new_y + dy[(player[loser][DIR] + i) % 4]] == NONE:
                # print(f"요기 {player[loser][DIR]} {[(player[loser][DIR] + i) % 4]}")
                player[loser][DIR] = (player[loser][DIR] + i) % 4
                break

        if len(ground[new_x + dx[player[loser][DIR]]][new_y + dy[player[loser][DIR]]]) > 0:
            player[loser][GUN] = heapq.heappop(ground[new_x + dx[player[loser][DIR]]][new_y + dy[player[loser][DIR]]]) * -1

        ground_player[player[winner][X]][player[winner][Y]] = NONE
        ground_player[player[loser][X]][player[loser][Y]] = NONE
        player[winner][X] = new_x
        player[winner][Y] = new_y
        player[loser][X] = new_x + dx[player[loser][DIR]]
        player[loser][Y] = new_y + dy[player[loser][DIR]]
        ground_player[new_x][new_y] = winner
        ground_player[new_x + dx[player[loser][DIR]]][new_y + dy[player[loser][DIR]]] = loser

        # print_all(4)
        # 2-2-3. 이긴 플레이어는 승리한 칸에서 원래 있던 총과 비교해서 가장 공격력 높은 총 획득하고, 나머지는 격자에 내려놓음.
        if player[winner][GUN] != NO_GUN:
            heapq.heappush(ground[new_x][new_y], player[winner][GUN] * -1)
        if len(ground[new_x][new_y]) > 0:
            player[winner][GUN] = heapq.heappop(ground[new_x][new_y]) * -1

        # print_all(5)


for i in range(k):
    # print(f"-----{i}-----")
    for j in range(m):
        move_player(j)

print(" ".join(map(str, points)))