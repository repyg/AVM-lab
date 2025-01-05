import matplotlib.pyplot as plt

points = [
    (-3.0, 12.10),  # 1
    (-2.5, 7.73),   # 2
    (-2.0, 4.08),   # 3
    (-1.5, 1.11),   # 4
    (-1.0, -1.12),  # 5
    (-0.5, -2.91),  # 6
    (0.0, -4.18),   # 7
    (0.5, -5.05),   # 8
    (1.0, -5.58),   # 9
    (1.5, -5.92),   # 10
    (2.0, -6.00),   # 11
    (2.5, -5.95),   # 12
    (3.0, -5.95),   # 13
    (3.5, -6.05)    # 14
]

# Разделение координат для удобства построения
x_values, y_values = zip(*points)

# Создаем график
plt.figure(figsize=(8, 5))
plt.scatter(x_values, y_values, color='blue', marker='D', label='Экспериментальные точки')

# Настройки графика
plt.title("Экспериментальные точки")
plt.xlabel("ось x")
plt.ylabel("ось y")
plt.grid(True)
plt.legend()

# Сохранение графика в файл
plt.savefig('experimental_points.png', format='png')  # Сохранение файла в формате PNG
plt.show()
