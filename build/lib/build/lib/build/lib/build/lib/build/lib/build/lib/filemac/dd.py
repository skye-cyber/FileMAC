import os


fl = 'home/skye/video/test'
tmp = 'tmp'
path = os.path.split(fl)[0]
file = os.path.split(fl)[1]
print(path)
print(os.path.join(path, tmp, file))
print(os.path.splitext(fl))
