import os
img_objs = '/home/skye/Software Engineering/Y2/SEM2/RV/SPE 2210 Client Side Programming Year II Semester II_1.png'
name = img_objs.split('/')[-1]
print(name)
print(os.path.dirname(img_objs))
print(os.path.abspath(img_objs))
print("\033[5;97;1m Hello")
