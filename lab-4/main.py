import numpy as np

# Данные из таблицы
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

# Выбираем нужные точки для интерполяции
lagrange_points = [points[0], points[6], points[12]]  # индексы 1, 7, 13
newton_points = [points[0], points[4], points[9], points[12]]  # индексы 1, 5, 10, 13

# Функция для полинома Лагранжа
def lagrange_interpolation(xs, points):
    def L(k, x):
        xk, _ = points[k]
        result = 1
        for i, (xi, _) in enumerate(points):
            if i != k:
                result *= (x - xi) / (xk - xi)
        return result
    
    # Вычисляем y для каждого x в списке xs
    return [(x, sum(y * L(k, x) for k, (xk, y) in enumerate(points))) for x in xs]

# Функция для полинома Ньютона
def newton_interpolation(xs, points):
    def divided_differences(points):
        n = len(points)
        coef = np.zeros([n, n])
        for i, (_, y) in enumerate(points):
            coef[i][0] = y

        for j in range(1, n):
            for i in range(n - j):
                xi, _ = points[i]
                xj, _ = points[i + j]
                coef[i][j] = (coef[i + 1][j - 1] - coef[i][j - 1]) / (xj - xi)

        return coef[0]

    coefs = divided_differences(points)
    results = []
    for x in xs:
        result = coefs[0]
        for i in range(1, len(points)):
            term = coefs[i]
            for j in range(i):
                term *= (x - points[j][0])
            result += term
        results.append((x, result))
    return results

# Пример использования
x_test = [x for x, _ in points]  # список значений x для вычислений

# Вычисляем результаты для полиномов Лагранжа и Ньютона
lagrange_results = lagrange_interpolation(x_test, lagrange_points)
newton_results = newton_interpolation(x_test, newton_points)

# Выводим результаты в формате исходных точек
print("Результаты интерполяции полиномом Лагранжа:")
for x, y in lagrange_results:
    print(f"x = {x:.2f}, y = {y:.2f}")

print("\nРезультаты интерполяции полиномом Ньютона:")
for x, y in newton_results:
    print(f"x = {x:.2f}, y = {y:.2f}")
