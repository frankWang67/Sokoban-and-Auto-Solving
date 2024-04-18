import random

# 定义地图大小
width = 8
height = 8

# 初始化地图，全部填充为墙壁（1）
map = [[1 for _ in range(width)] for _ in range(height)]

# 随机选择一个起始点
start_x = random.randint(1, width - 2)
start_y = random.randint(1, height - 2)

# 将起始点设为通路（0）
map[start_y][start_x] = 0

# 深度优先搜索函数
def dfs(x, y):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx * 2, y + dy * 2
        if 1 <= nx < width-1 and 1 <= ny < height-1 and map[ny][nx] == 1:
            map[y + dy][x + dx] = 0
            map[ny][nx] = 0
            dfs(nx, ny)

# 从起始点开始深度优先搜索
dfs(start_x, start_y)

# 输出地图
for row in map:
    print(row)
