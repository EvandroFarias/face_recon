import os


DEFAULT_PATH = os.path.dirname(os.path.abspath(__file__))


with open(f'{DEFAULT_PATH}\\sizes.txt') as f:
    SIZES = f.readline().split(',')
    for index, size in enumerate(SIZES):
         SIZES[size] = int(size)
         if int(size) < 150:
              SIZES[index] = 150

print(SIZES)