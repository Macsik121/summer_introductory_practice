import numpy as np
import matplotlib.pyplot as plt

# Лучшая практика - сразу преобразовывать исходный список данных в список numpy
x = np.array([0, 0, 1, 2, 3, 3, 2, 1, 0])
y = np.array([3, 4, 6, 6, 4, 3, 1, 1, 3])
x2 = np.concatenate((np.arange(0.1, 1, .1), np.arange(1, 5)), axis=None)
y2 = np.array([1/i for i in x2])
x3 = np.arange(0, 5)
y3 = np.array([i ** 2 for i in x3])

# Если передаётся один аргумент - ось Ox генерируется автоматически
# Если передаётся два - ось Ox = первый аргумент
# plt.plot(x, y)

# функция plot также имеет аргумент, определяющий тип линии
# plt.plot(x, y, ':', x2, y2, '-.')

# lines = plt.plot(x2, y2, x3, y3)
# метод setp (p - properties) позваляет устанавливать или менять свойства графика(с помощью класса Lines2D)
# Первым аргументом идёт график, свойства которого надо поменять, а следующими - свойства
# plt.setp(lines, linestyle='-.')

# Можно менять цвет графиков
# lines = plt.plot(x2, y2, ':r', x3, y3, 'g-.', color=(1, 0, 1, .3))

# Также можно менять маркеры в точках пересечения с x и y
# lines = plt.plot(
#   x2, y2, '<:m', x3, y3, 'c-.>',
#   # color=(1, 0, 1, .86),
#   # marker='<',
# )

# Можно менять цвет заливки маркеров
# lines = plt.plot(
#   x2, y2, '<:m', x3, y3, 'c-.>',
#   # color=(1, 0, 1, .86),
#   # marker='<',
#   markerfacecolor='b'
# )

# Все параметры оформления графика можно задавать через метод .setp()
# plt.setp(lines[0], linewidth=10, color='y')

# Задача с экзамена по математике за 2-ой семестр - задача для того, чтобы показать fill_between
# y4 = [((i - 1) ** 2 + 1) for i in x3]
# y5 = [2] * len(x3)
# plt.fill_between(
#   x3, y4, y5,
# #  [True] * 3 + [False] * 2
# )

# fill_between пример
x = np.arange(-2 * np.pi, 2 * np.pi, .1)
y = np.cos(x)
r = np.sqrt(y ** 2 + np.sin(x) ** 2)
plt.plot(x, y)
plt.fill_between(x, y, where=(y < 0), color=(0, 1, 0, .5))
plt.fill_between(x, y, where=(y > 0), color=(1, 0, 0, .5))

plt.grid()
plt.show()
