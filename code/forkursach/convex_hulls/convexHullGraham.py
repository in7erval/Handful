from functools import cmp_to_key


class Point:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y


# Расстояние между двумя точками
def dist_sq(p1, p2):
    return ((p1.x - p2.x) * (p1.x - p2.x) +
            (p1.y - p2.y) * (p1.y - p2.y))


# Определение ориентации трёх точек
# (перекрестное произведение векторов pq и qr)
def orientation(p, q, r):
    val = ((q.y - p.y) * (r.x - q.x) -
           (q.x - p.x) * (r.y - q.y))
    if val == 0:
        return 0  # коллинеарны
    elif val > 0:
        return 1  # по часовой
    else:
        return 2  # против часовой


# Сравнение двух точек для сортировки
def compare(p1, p2):
    global p0
    o = orientation(p0, p1, p2)
    if o == 0:
        return -1 if dist_sq(p0, p2) >= dist_sq(p0, p1) else 1
    else:
        return -1 if o == 2 else 1


def convex_hull(input_points: list) -> list:
    # Конвертируем в класс Point
    points = [Point(point[0], point[1]) for point in input_points]
    n = len(input_points)
    # Находим минимальную точку
    min_y = points[0].y
    min_i = 0
    for i in range(1, n):
        y = points[i].y
        if ((y < min_y) or
                (min_y == y and points[i].x < points[min_i].x)):
            min_y = points[i].y
            min_i = i

    points[0], points[min_i] = points[min_i], points[0]

    # Сортируем массив
    global p0
    p0 = points[0]
    points = sorted(points, key=cmp_to_key(compare))

    m = 1  # Начальный размер нового массива
    # Удаляем лишние точки
    for i in range(1, n):
        while ((i < n - 1) and
               (orientation(p0, points[i], points[i + 1]) == 0)):
            i += 1
        points[m] = points[i]
        m += 1
    if m < 3:
        return None

    S = [points[0], points[1], points[2]]
    for i in range(3, m):
        while ((len(S) > 1) and
               (orientation(S[-2], S[-1], points[i]) != 2)):
            S.pop()
        S.append(points[i])

    return [(p.x, p.y) for p in S]

