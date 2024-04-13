# n * n

# 꼬리잡기놀이. 3명 이상 한 팀.
# 맨 앞 사람: 머리사람
# 맨 뒤 사람: 꼬리사람
# 각 팀은 게임에서 주어진 이동선만 따라서 이동.
# 각 팀의 이동 선 끝이 이어져있다. 이동선은 서로 겹치지 X


# 격자 크기 n, 팀 개수 m, 라운드 수 k
# 0 빈칸, 1 머리사람, 2 나머지 사람, 3 꼬리사람, 4 이동 선
# 이동 선의 각 칸은 반드시 2개의 인접한 칸만 존재, 하나의 이동 선에는 하나의 팀만 존재.

import sys
from collections import deque

EMPTY = 0
FRONT = 1
ECT = 2
END = 3
LINE = 4
X = 0
Y = 1

n, m, k = map(int, sys.stdin.readline().split())
ground = []

for i in range(n):
    ground.append(list(map(int, sys.stdin.readline().split())))

lines_info = []
team = []

result = 0

def bfs(x, y):
    global n, ground, team, END, lines_info
    queue = deque([[x, y]])

    dx = [0, 0, -1, 1]
    dy = [1, -1, 0, 0]

    end = -1
    tmp = []

    visited = [[False for _ in range(n)] for _ in range(n)]
    visited[x][y] = True
    tmp.append([x, y])

    while queue:
        nx, ny = queue.popleft()

        if ground[nx][ny] == END:
            end = len(tmp) - 1

        for i in range(4):
            if 0 <= nx + dx[i] < n and 0 <= ny + dy[i] < n and not visited[nx + dx[i]][ny + dy[i]] and \
                    ground[nx + dx[i]][ny + dy[i]] != EMPTY and ground[nx + dx[i]][ny + dy[i]] <= ground[nx][ny] + 1:
                visited[nx + dx[i]][ny + dy[i]] = True
                queue.append([nx + dx[i], ny + dy[i]])
                tmp.append([nx + dx[i], ny + dy[i]])

    lines_info.append(tmp)
    return end


for i in range(n):
    for j in range(n):

        if ground[i][j] == FRONT:
            end = bfs(i, j)
            team.append([0, end, FRONT])

# print(lines_info)
# 한 라운드 단계

# 1. 각 팀은 머리사람을 따라서 한 칸 이동.
def move():
    global team, ground, n, lines_info, FRONT

    for i in range(len(team)):
        front, end, type = team[i]

        length = len(lines_info[i])
        if type == FRONT:
            front = (front - 1) % length
            end = (end - 1) % length
        else:
            front = (front + 1) % length
            end = (end + 1) % length

        team[i] = [front, end, type]

    # print(team)



# 2. 각 라운드마다 공이 정해진 선을 따라 던져진다.
#  round 1 ~ n : 왼 -> 오
#  round n + 1 ~ 2n: 아 -> 위
#  round 2n + 1 ~ 3n : 오 -> 왼
#  round 3n + 1 ~ 4n : 위 -> 아
#  round 4n 부터는 처음부터 반복

# 3. 공이 던져지는 경우, 해당 선에 사람이 있으면 최초 만나는 사람만이 점수 얻음.
#    점수는 머리사람을 시작으로 K번째 사람이면 K**2 점수 얻음.
#    공을 획득한 팀의 경우 머리사람과 꼬리사람이 바뀐다! (방향도 바뀜)

def throw_ball(origin_time):
    global n, ground, lines_info, team, result, FRONT

    origin_time = origin_time % (4 * n)
    time = origin_time % n
    isOver = False
    # print(f"origin_time {origin_time} time {time}")
    for i in range(len(lines_info)):
        tmp = []
        if team[i][2] == FRONT:
            if team[i][0] < team[i][1]:
                tmp = lines_info[i][team[i][0]: team[i][1] + 1]
            else:
                tmp = lines_info[i][team[i][0]:] + lines_info[i][: team[i][1] + 1]
        else:
            if team[i][0] > team[i][1]:
                tmp = lines_info[i][team[i][1]: team[i][0] + 1]
            else:
                tmp = lines_info[i][team[i][1]:] + lines_info[i][: team[i][0] + 1]
            tmp = list(reversed(tmp))
        # print(f"tmp {tmp} {origin_time}")

        if 0 <= origin_time < n:
            for j in range(n):
                for h in range(len(tmp)):
                    # print(f"1번 time {time} j {j} {tmp[h]}")
                    if [time, j] == tmp[h]:
                        result += (h + 1) ** 2
                        # print(f"result {result} {i}번째 team {time, j} {team[i]} {tmp}")
                        isOver = True

                        team[i][0], team[i][1] = team[i][1], team[i][0]
                        if team[i][2] == FRONT:
                            team[i][2] = END
                        else:
                            team[i][2] = FRONT
                        break
                if isOver:
                    break
            if isOver:
                break

        elif n <= origin_time < 2 * n:
            # print(tmp, isOver)
            for j in range(n - 1, -1, -1):
                for h in range(len(tmp)):
                    # print(f"2번 time {time} j {j} {tmp}")
                    if [j, time] == tmp[h]:
                        result += (h + 1) ** 2
                        # print(f"result {result} {i}번째 team {j, time} {team[i]} {tmp}")

                        isOver = True
                        team[i][0], team[i][1] = team[i][1], team[i][0]
                        if team[i][2] == FRONT:
                            team[i][2] = END
                        else:
                            team[i][2] = FRONT
                        break
                if isOver:
                    break
            if isOver:
                break
        elif 2 * n <= origin_time < 3 * n:

            for j in range(n - 1, -1, -1):
                for h in range(len(tmp)):
                    # print(f"3번 time {time} j {j} {tmp}")
                    if [(n - 1) - time, j] == tmp[h]:
                        result += (h + 1) ** 2
                        isOver = True
                        team[i][0], team[i][1] = team[i][1], team[i][0]
                        if team[i][2] == FRONT:
                            team[i][2] = END
                        else:
                            team[i][2] = FRONT
                        break
                if isOver:
                    break
            if isOver:
                break
        else:

            for j in range(0, n,):
                for h in range(len(tmp)):
                    # print(f"4번 time {time} j {j} {tmp}")
                    if [j, (n - 1) - time] == tmp[h]:
                        result += (h + 1) ** 2
                        isOver = True
                        team[i][0], team[i][1] = team[i][1], team[i][0]
                        if team[i][2] == FRONT:
                            team[i][2] = END
                        else:
                            team[i][2] = FRONT
                        break
                if isOver:
                    break
            if isOver:
                break


for i in range(k):
    move()
    throw_ball(i)

print(result)



'''
7 2 10
3 2 1 0 0 0 0
4 0 4 0 2 1 4
4 4 4 0 2 0 4
0 0 0 0 3 0 4
0 0 4 4 4 0 4
0 0 4 0 0 0 4
0 0 4 4 4 4 4
'''