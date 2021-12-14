class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# поиск самой левой нижней точки
def left_index(points):
    minn = 0
    for i in range(1, len(points)):
        if points[i].x < points[minn].x or \
                (points[i].x == points[minn].x and
                 points[i].y > points[minn].y):
            minn = i
    return minn


# аналогично orientation в алгоритме Грэхема
def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - \
          (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0
    elif val > 0:
        return 1
    return -1


def convex_hull(init_points):
    n = len(init_points)
    if n < 3:
        return
    points = [Point(p[0], p[1]) for p in init_points]

    l = left_index(points)

    hull = []

    p = l
    q = 0
    while True:
        hull.append(p)
        q = (p + 1) % n
        for i in range(n):
            if (orientation(points[p],
                            points[i], points[q]) == 2):
                q = i
        p = q
        if p == l:
            break
    return [(points[i].x, points[i].y) for i in hull]
