# -*- coding: utf-8 -*-

def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)


def story_points(start):
    for i in range(10):
        result = fibonacci(i)
        if result >= start:
            break
    return result
