package main

import (
	"fmt"
	"math"
	"os"

	"image/color"

	"github.com/wcharczuk/go-chart/v2"
	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
	"gonum.org/v1/plot/vg"
)

func sgn(x float64) float64 {
	if x < 0 {
		return -1.0
	} else {
		return 1.0
	}
}

// Функция для создания матрицы C и вектора d
func createCandD(A [][]float64, b []float64) ([][]float64, []float64) {
	v := 1.0
	gm := 0.0

	n := len(A)
	lambda := make([]float64, n)
	C := make([][]float64, n)
	d := make([]float64, n)

	for i := 0; i < n; i++ {
		lambda[i] = -(sgn(A[i][i]) * v) / (gm + math.Abs(A[i][i]))
	}

	for i := 0; i < n; i++ {
		C[i] = make([]float64, n)
		for j := 0; j < n; j++ {
			if i == j {
				C[i][j] = 1 + lambda[i]*A[i][j]
			} else {
				C[i][j] = lambda[i] * A[i][j]
			}
		}
		d[i] = -lambda[i] * b[i]
	}
	return C, d
}

// Проверка сходимости
func hasFirstConverged(v1 []float64, v2 []float64, tolerance float64) bool {
	for i := range v1 {
		if math.Abs(v1[i]-v2[i]) > tolerance {
			return false
		}
	}
	return true
}

func hasSecondConverged(x []float64, A [][]float64, b []float64, tolerance float64) bool {
	converde := true
	for i := 0; i < len(A); i++ {
		sum := 0.0
		for j := 0; j < len(x); j++ {
			sum += A[i][j] * x[j]
		}
		if math.Abs(sum-b[i]) > tolerance {
			converde = false
		}
	}
	return converde
}

// Метод Гаусса-Зейделя
func gaussSeidel(A [][]float64, b []float64, initialGuess []float64, tolerance float64, maxIterations int) []float64 {
	C, d := createCandD(A, b)
	x := make([]float64, len(initialGuess))
	copy(x, initialGuess)

	n := len(A)
	for k := 0; k < maxIterations; k++ {
		xNew := make([]float64, n)
		copy(xNew, x) // Сохраняем текущие значения для проверки сходимости

		for i := 0; i < n; i++ {
			sum := 0.0
			for j := 0; j < n; j++ {
				if i != j {
					// Используем новые значения для уже пересчитанных переменных на текущем шаге
					sum += C[i][j] * x[j]
				}
			}
			// Обновляем значение x_i^(k)
			x[i] = sum + d[i]
		}

		// Проверяем сходимость
		if hasFirstConverged(x, xNew, tolerance) && hasSecondConverged(x, A, b, tolerance) {
			fmt.Printf("Решение сошлось на %d итерации\n", k+1)
			return x
		}
	}

	fmt.Println("Не удалось достичь сходимости за указанное количество итераций")
	return x
}

func jordanGauss(matrix [][]float64, b []float64) []float64 {
	n := len(matrix)

	// Прямой ход метода Гаусса
	for i := 0; i < n; i++ {
		// Нормализуем текущую строку
		pivot := matrix[i][i]
		for j := 0; j < n; j++ {
			matrix[i][j] /= pivot
		}
		b[i] /= pivot

		// Обнуляем остальные строки
		for k := 0; k < n; k++ {
			if i != k {
				factor := matrix[k][i]
				for j := 0; j < n; j++ {
					matrix[k][j] -= factor * matrix[i][j]
				}
				b[k] -= factor * b[i]
			}
		}
	}

	return b
}

func iterationsGaussSeidel(A [][]float64, b []float64, initialGuess []float64, tolerance float64, maxIterations int) int64 {
	C, d := createCandD(A, b)
	x := make([]float64, len(initialGuess))
	copy(x, initialGuess)

	n := len(A)
	for k := 0; k < maxIterations; k++ {
		xNew := make([]float64, n)
		copy(xNew, x) // Сохраняем текущие значения для проверки сходимости

		for i := 0; i < n; i++ {
			sum := 0.0
			for j := 0; j < n; j++ {
				if i != j {
					// Используем новые значения для уже пересчитанных переменных на текущем шаге
					sum += C[i][j] * x[j]
				}
			}
			// Обновляем значение x_i^(k)
			x[i] = sum + d[i]
		}

		// Проверяем сходимость
		if hasFirstConverged(x, xNew, tolerance) && hasSecondConverged(x, A, b, tolerance) {
			fmt.Printf("Решение c точностью %f сошлось на %d итерации\n", tolerance, k+1)
			for i, val := range x {
				fmt.Printf("x%d = %.6f\n", i+1, val)
			}
			fmt.Println("-----------------------------------------")
			return int64(k + 1)
		}
	}
	fmt.Println("Не удалось достичь сходимости за указанное количество итераций")
	return 0
}

func createIterationChart(filename string, accuracy, iterations []float64) error {
	// Создание бар-чарта
	graph := chart.BarChart{
		Title: "Количество итераций, необходимых для достижения заданной точности",
		Background: chart.Style{
			Padding: chart.Box{
				Top:    100,
				Bottom: 20,
			},
		},
		Height:   512,
		BarWidth: 124,
		Bars: []chart.Value{
			{Value: iterations[0], Label: fmt.Sprintf("%.3f", accuracy[0])},
			{Value: iterations[1], Label: fmt.Sprintf("%.3f", accuracy[1])},
			{Value: iterations[2], Label: fmt.Sprintf("%.3f", accuracy[2])},
			{Value: iterations[3], Label: fmt.Sprintf("%.3f", accuracy[3])},
		},
	}

	// Создаем файл для сохранения графика
	f, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer f.Close()

	// Рисуем график и сохраняем его в файл
	err = graph.Render(chart.PNG, f)
	if err != nil {
		return err
	}

	fmt.Printf("График успешно сохранен в файл %s\n", filename)
	return nil
}

func tableGaussSeidel(A [][]float64, b []float64, initialGuess []float64, tolerance float64, maxIterations int) [][]float64 {
	C, d := createCandD(A, b)
	x := make([]float64, len(initialGuess))
	copy(x, initialGuess)

	n := len(A)
	history := make([][]float64, 0) // Для хранения истории значений переменных

	for k := 0; k < maxIterations; k++ {
		xNew := make([]float64, n)
		copy(xNew, x) // Сохраняем текущие значения для проверки сходимости

		for i := 0; i < n; i++ {
			sum := 0.0
			for j := 0; j < n; j++ {
				if i != j {
					// Используем новые значения для уже пересчитанных переменных на текущем шаге
					sum += C[i][j] * x[j]
				}
			}
			// Обновляем значение x_i^(k)
			x[i] = sum + d[i]
		}

		// Сохраняем текущие значения переменных в историю
		history = append(history, append([]float64(nil), x...))

		// Проверяем сходимость
		if hasFirstConverged(x, xNew, tolerance) && hasSecondConverged(x, A, b, tolerance) {
			return history
		}
	}
	return history
}

func createLinePlot(history [][]float64) error {
	// Создание нового графика
	p := plot.New()
	p.Title.Text = "График изменения всех элементов вектора решения системы от номера итерации при точности e=0.1"
	p.X.Label.Text = "Итерации"
	p.Y.Label.Text = "Значение переменной"

	// Количество переменных
	n := len(history[0])

	// Определяем цвета для 6 линий (RGBA)
	colors := []color.RGBA{
		{R: 0, G: 0, B: 255, A: 255},   // Синий для x1
		{R: 255, G: 0, B: 0, A: 255},   // Красный для x2
		{R: 0, G: 255, B: 0, A: 255},   // Зелёный для x3
		{R: 255, G: 0, B: 255, A: 255}, // Фиолетовый для x4
		{R: 255, G: 165, B: 0, A: 255}, // Оранжевый для x5
		{R: 0, G: 255, B: 255, A: 255}, // Голубой для x6
	}

	// Массив для легенды
	labels := []string{"x1", "x2", "x3", "x4", "x5", "x6"}

	// Данные для каждой переменной
	for i := 0; i < n; i++ {
		pts := make(plotter.XYs, len(history))
		for k := 0; k < len(history); k++ {
			pts[k].X = float64(k + 1) // Номер итерации
			pts[k].Y = history[k][i]  // Значение переменной на итерации k
		}

		// Создание линии для каждой переменной
		line, err := plotter.NewLine(pts)
		if err != nil {
			return err
		}

		// Назначаем цвет для линии
		line.Color = colors[i%len(colors)]
		p.Add(line)

		// Добавляем линии в легенду
		p.Legend.Add(labels[i], line)
	}

	// Настройка отображения легенды
	p.Legend.Top = true

	// Сохранение графика в файл
	if err := p.Save(10*vg.Inch, 5*vg.Inch, "gauss_seidel_plot.png"); err != nil {
		return err
	}

	return nil
}

func main() {
	// Матрица коэффициентов
	A := [][]float64{
		{16.8, 1.9, -8.8, 6.0, -9.9, -10.5},
		{-7.1, 11.8, 8.3, 2, -0.7, -5.1},
		{-3.0, -2.7, 18.2, 0.8, 2.1, 11.2},
		{-0.5, -5.3, -5.1, 9.6, 1.6, 3.3},
		{-6.0, 6.9, 7.3, 7.5, 18.3, 9.3},
		{12.3, -10.5, 13.5, -8.4, -4.8, 19.0},
	}

	// Вектор свободных членов
	b := []float64{0.04, -41.39, 37.51, 22.60, -28.28, 56.97}

	// Начальное приближение
	initialGuess := []float64{1.5, 1.9, 0.1, -0.3, -1.0, 1.9}

	accuracy := []float64{0.1, 0.02, 0.005, 0.001}
	iterations := make([]int64, len(A))

	// Параметры
	tolerance := 1e-5
	maxIterations := 100

	for i, acc := range accuracy {
		iterations[i] = iterationsGaussSeidel(A, b, initialGuess, acc, maxIterations)
	}
	history := tableGaussSeidel(A, b, initialGuess, 0.1, maxIterations)
	// Решаем систему методом Гаусса-Зейделя
	solutionGaussSeidel := gaussSeidel(A, b, initialGuess, tolerance, maxIterations)
	solutionJordanGauss := jordanGauss(A, b)

	// Выводим результат
	fmt.Println("Решение Гаусса-Зейделя:")
	for i, val := range solutionGaussSeidel {
		fmt.Printf("x%d = %.6f\n", i+1, val)
	}
	fmt.Println("Решение Жордана-Гаусса:")
	for i, val := range solutionJordanGauss {
		fmt.Printf("x%d = %.6f\n", i+1, val)
	}

	floatIterations := make([]float64, len(iterations))
	for i, v := range iterations {
		floatIterations[i] = float64(v)
	}

	// Вызов функции для создания графика
	err := createIterationChart("iterations_chart.png", accuracy, floatIterations)
	if err != nil {
		panic(err)
	}

	if err := createLinePlot(history); err != nil {
		panic(err)
	}
}
