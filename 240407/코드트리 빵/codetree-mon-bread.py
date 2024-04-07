import sys
from collections import deque

n, m = map(int, sys.stdin.readline().split())
ground = []
for i in range(n):
    ground.append(list(map(int, sys.stdin.readline().split())))

convenience_store = []
people = [[-1, -1] for _ in range(m)]
for i in range(m):
    convenience_store.append(list(map(lambda x: int(x) - 1, sys.stdin.readline().split())))

dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]
BASECAMP = 1
EMPTY = 0
CANNOT = -1
ARRIVED = 0

def get_closest_basecamp(cx, cy):
    global n, m, ground, BASECAMP, CANNOT

    queue = deque([[cx, cy]])
    visited = [[False for _ in range(n)] for _ in range(n)]
    
    basecamp = [-1, -1]
    while queue:
        nx, ny = queue.popleft()
        visited[nx][ny] = True

        if ground[nx][ny] == BASECAMP:
            basecamp = [nx, ny]
            break

        for i in range(4):
            if 0 <= nx + dx[i] < n and 0 <= ny + dy[i] < n and ground[nx + dx[i]][ny + dy[i]] != CANNOT and not visited[nx + dx[i]][ny + dy[i]]:
                queue.append([nx + dx[i], ny + dy[i]])

    return basecamp


def go_to_basecamp(time):
    global n, m, convenience_store, people, ground, CANNOT

    closest_basecamp = get_closest_basecamp(convenience_store[time][0], convenience_store[time][1])
    people[time] = closest_basecamp

    ground[closest_basecamp[0]][closest_basecamp[1]] = CANNOT


def get_next_coordinate(px, py, cx, cy):
    global n, m, ground, BASECAMP, CANNOT

    queue = deque([[px, py]])
    visited = [[[] for _ in range(n)] for _ in range(n)]
    visited[px][py].append([px, py])

    nxt = [-1, -1]
    while queue:
        nx, ny = queue.popleft()

        if nx == cx and ny == cy:
            nxt = visited[nx][ny][1]
            break

        for i in range(4):
            if 0 <= nx + dx[i] < n and 0 <= ny + dy[i] < n and ground[nx + dx[i]][ny + dy[i]] != CANNOT and len(visited[nx + dx[i]][ny + dy[i]]) == 0:
                queue.append([nx + dx[i], ny + dy[i]])
                visited[nx + dx[i]][ny + dy[i]].extend(visited[nx][ny])
                visited[nx + dx[i]][ny + dy[i]].append([nx + dx[i], ny + dy[i]])

    return nxt


def go_to_store():
    global n, m, convenience_store, people, ground, ARRIVED

    arrived = []
    for i in range(m):
        if people[i] == [-1, -1] or people[i] == convenience_store[i]:
            continue

        people[i] = get_next_coordinate(people[i][0], people[i][1], convenience_store[i][0], convenience_store[i][1])

        if people[i] == convenience_store[i]:
            arrived.append(people[i])
            ARRIVED += 1

    return arrived


t = 0
while ARRIVED < m:
    arrived = go_to_store()

    for x, y in arrived:
        ground[x][y] = CANNOT

    if t < m:
        go_to_basecamp(t)
   

    # for i in range(n):
    #     print(ground[i])

    # print(arrived, ARRIVED)
    # print(people)
    # print()

    t += 1

print(t)