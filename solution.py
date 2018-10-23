"""
Rozwiązania do laboratorium 1 z Obrazowania Biomedycznego.
"""
import numpy as np

"""
3 - Kwadrat
"""
def square(size, side, start):
    image = np.zeros((size, size)).astype(np.uint8)
    image[start[0]:start[0]+side, start[0]:start[0]+side] = 255
    return image

"""
3 - Koło
"""
def midcircle(size):
    image = np.zeros((size, size)).astype(np.uint8)
    mid = (size[0] // 2, size[1] // 2)
    rsq = (min(size) // 4) ** 2
    for i in range(size[0]):
        for j in range(size[1]):
            eq = (i - mid[0])**2 + (j - mid[1])**2
            if eq <= rsq:
                image[i,j] = 255
    return image

"""
3 - Szachownica.
"""
def checkerboard(size):
    side_size = size // 8
    image = np.zeros(size).astype(np.uint8)
    for i in range(i):
        for j in range(j):
            origin_i = i * side_size
            origin_j = j * side_size
            if (i + j) % 2 == 0:
                image[origin_i:origin_i + side_size, origin_j:origin_j + side_size] = 255
    return image
                
            

"""
4 - Interpolacja najbliższych sąsiadów.
"""
def nn_interpolation(source, new_size):
    pass

"""
5 - Interpolacja dwuliniowa
"""
def bilinear_interpolation(source, new_size):
    pass
