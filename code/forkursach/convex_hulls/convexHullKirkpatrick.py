from collections import namedtuple
from random import randint

Point = namedtuple('Point', 'x y')


def flipped(points):
    return [Point(-point.x, -point.y) for point in points]


def quickselect(ls, index, lo=0, hi=None, depth=0):
    if hi is None:
        hi = len(ls) - 1
    if lo == hi:
        return ls[lo]
    if len(ls) == 0:
        return 0
    pivot = randint(lo, hi)
    ls = list(ls)
    ls[lo], ls[pivot] = ls[pivot], ls[lo]
    cur = lo
    for run in range(lo+1, hi+1):
        if ls[run] < ls[lo]:
            cur += 1
            ls[cur], ls[run] = ls[run], ls[cur]
    ls[cur], ls[lo] = ls[lo], ls[cur]
    if index < cur:
        return quickselect(ls, index, lo, cur-1, depth+1)
    elif index > cur:
        return quickselect(ls, index, cur+1, hi, depth+1)
    else:
        return ls[cur]


def bridge(points, vertical_line):
    candidates = set()
    if len(points) == 2:
        return tuple(sorted(points))
    pairs = []
    modify_s = set(points)
    while len(modify_s) >= 2:
        pairs += [tuple(sorted([modify_s.pop(), modify_s.pop()]))]
    if len(modify_s) == 1:
        candidates.add(modify_s.pop())
    slopes = []
    for pi, pj in pairs[:]:
        if pi.x == pj.x:
            pairs.remove((pi, pj))
            candidates.add(pi if pi.y > pj.y else pj)
        else:
            slopes += [(pi.y-pj.y)/(pi.x-pj.x)]
    median_index = len(slopes)//2 - (1 if len(slopes) % 2 == 0 else 0)
    median_slope = quickselect(slopes, median_index)
    small = {pairs[i] for i, slope in enumerate(slopes) if slope < median_slope}
    equal = {pairs[i] for i, slope in enumerate(slopes) if slope == median_slope}
    large = {pairs[i] for i, slope in enumerate(slopes) if slope > median_slope}
    max_slope = max(point.y-median_slope*point.x for point in points)
    max_set = [point for point in points if point.y-median_slope*point.x == max_slope]
    left = min(max_set)
    right = max(max_set)
    if left.x <= vertical_line < right.x:
        return left, right
    if right.x <= vertical_line:
        candidates |= {point for _, point in large | equal}
        candidates |= {point for pair in small for point in pair}
    if left.x > vertical_line:
        candidates |= {point for point, _ in small | equal}
        candidates |= {point for pair in large for point in pair}
    return bridge(candidates, vertical_line)


def connect(lower, upper, points):
    if lower == upper:
        return [lower]
    max_left = quickselect(points, len(points)//2-1)
    min_right = quickselect(points, len(points)//2)
    left, right = bridge(points, (max_left.x + min_right.x)/2)
    points_left = {left} | {point for point in points if point.x < left.x}
    points_right = {right} | {point for point in points if point.x > right.x}
    return connect(lower, left, points_left) + connect(right, upper, points_right)


def upper_hull(points):
    lower = min(points)
    lower = max({point for point in points if point.x == lower.x})
    upper = max(points)
    points = {lower, upper} | {p for p in points if lower.x < p.x < upper.x}
    return connect(lower, upper, points)


def convex_hull(init_points):
    points = [Point(p[0], p[1]) for p in init_points]
    upper = upper_hull(points)
    lower = flipped(upper_hull(flipped(points)))
    if upper[-1] == lower[0]:
        del upper[-1]
    if upper[0] == lower[-1]:
        del lower[-1]
    return upper + lower
