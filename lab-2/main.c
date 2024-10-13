#include <stdio.h>
#include <math.h>
#include <stdlib.h>

double function(double x) {
    return -0.16 + 4.84 * x + 0.67 * pow(x, 2) + 7.29 * sin(x);
}

double functionDerivative(double x, double epsilon){
    return (function(x+epsilon/2) - function(x-epsilon/2))/epsilon;
}

int iterationsBisectionMethod(double a, double b, double epsilon){
    int iterations = 0;
    double c;
    while ((b - a) / 2 > epsilon) {
        c = (a + b) / 2;
        if (function(c) == 0.0) {
            break;
        } else if (function(a) * function(c) < 0) {
            b = c;
        } else {
            a = c;
        }
        iterations++;
    }
    return iterations;
}

int iterationsNewtonMethod(double x0, double epsilon){
    int iterations = 0;
    double x = x0;
    double delta_x;
    do {
        delta_x = function(x) / functionDerivative(x, epsilon);
        x = x - delta_x;
        iterations++;
    } while (fabs(delta_x) > epsilon);
    return iterations;
}

void plotGraph(){
    FILE *temp = fopen("data.dat", "w"), *table = fopen("table2.dat", "w");

    fprintf(table, "+--------+-----------+\n");
    fprintf(table, "|   x    |     y     |\n");
    fprintf(table, "+--------+-----------+\n");

    for (double x = -10; x <= 10; x += 0.5) {
        double y = function(x);
        fprintf(temp, "%lf %lf\n", x, y);
        fprintf(table, "| %6.2lf | %9.5lf |\n", x, y);  // Форматирование значений x и y
    }
    fprintf(table, "+--------+-----------+\n\n");

    fprintf(table, "+--------------------------------------------+\n");
    fprintf(table, "|        Приближенные значения и интервалы   |\n");
    fprintf(table, "|        локализации каждого корня           |\n");
    fprintf(table, "+----------+----------------+----------------+\n");
    fprintf(table, "|    i     |        1       |        2       |\n");
    fprintf(table, "+----------+----------------+----------------+\n");
    fprintf(table, "|   x_i    |      -8.4      |        0       |\n");
    fprintf(table, "+----------+----------------+----------------+\n");
    fprintf(table, "|   a_i    |      -10       |       -1       |\n");
    fprintf(table, "+----------+----------------+----------------+\n");
    fprintf(table, "|   b_i    |       -5       |        4       |\n");
    fprintf(table, "+----------+----------------+----------------+\n");

    fclose(temp);
    fclose(table);

    FILE *gnuplot = popen("gnuplot -persistent", "w");
    fprintf(gnuplot, "set title 'График функции y=f(x)'\n");
    fprintf(gnuplot, "set xlabel 'ось x'\n");
    fprintf(gnuplot, "set ylabel 'ось y'\n");

    fprintf(gnuplot, "set xzeroaxis lt -1\n");
    fprintf(gnuplot, "set yzeroaxis lt -1\n");

    fprintf(gnuplot, "plot 'data.dat' using 1:2 with lines title 'y = f(x)'\n");
    fclose(gnuplot);
}

void bisectionMethod(double a, double b, int n){
    FILE *file = fopen("bisection_table.txt", "a+");
    fprintf(file, "+----------------------------------------------------------------------------------------+\n");
    fprintf(file, "|                          Метод половинного деления (x_%d)                               |\n",n);
    fprintf(file, "+-----------+----------+----------+------------+------------+---------------+------------+\n");
    fprintf(file, "|    a_1    |    c_1   |   b_1    |   f(a_1)   |   f(c_1)   | f(a_1)*f(c_1) | (b_1-a_1)/2|\n");
    fprintf(file, "+-----------+----------+----------+------------+------------+---------------+------------+\n");

    double halfInterval = (b - a) / 2;
    while (halfInterval > 0.00001 || function(halfInterval) > 0.00001){
        double c = (a + b) / 2;
        double fa = function(a);
        double fc = function(c);
        double product = fa * fc;
        halfInterval = (b - a) / 2;

        fprintf(file, "| %9.5lf | %8.5lf | %8.5lf | %10.5lf | %10.5lf | %13.5lf | %10.5lf |\n",
                a, c, b, fa, fc, product, halfInterval);
        
        if (product < 0) {
            b = c;
        } else {
            a = c;
        }
    }
    fprintf(file, "+-----------+----------+----------+------------+------------+---------------+------------+\n\n");
    fclose(file);
}

void newtonMethod(double initial_guess, int n){
    FILE *file = fopen("newton_table.txt", "a+");
    fprintf(file, "+------------------------------------------------------------+\n");
    fprintf(file, "|                   Метод Ньютона (x_%d)                      |\n", n);
    fprintf(file, "+-----------+------------+-------------+---------------------+\n");
    fprintf(file, "|    x_n    |   f(x_n)   |  f'(x_n)    |  f(x_n)/f'(x_n)     |\n");
    fprintf(file, "+-----------+------------+-------------+---------------------+\n");

    double x_n = initial_guess;
    while (1) {
        double f_xn = function(x_n);
        double f_prime_xn = functionDerivative(x_n, 0.00001);
        double delta_x = f_xn / f_prime_xn;

        fprintf(file, "| %9.5lf | %10.5lf | %11.5lf | %19.5lf |\n", x_n, f_xn, f_prime_xn, delta_x);
        x_n = x_n - delta_x;
        if (fabs(delta_x) < 0.00001) {
            break;
        }
    }
    fprintf(file, "+-----------+------------+-------------+---------------------+\n\n");
    fclose(file);
}

void table(){
    FILE *file = fopen("table3.dat", "w"), *table  = fopen("table.dat", "w");
    double epsilons[] = {0.1, 0.01, 0.001, 0.0001, 0.00001};
    double logs[] = {-1.0, -2.0, -3.0, -4.0, -5.0};
    int bisection_iterations_x1[5], bisection_iterations_x2[5];
    int newton_iterations_x1[5], newton_iterations_x2[5];

    for (int i = 0; i < 5; i++) {
        bisection_iterations_x1[i] = iterationsBisectionMethod(-10, -5, epsilons[i]);
        bisection_iterations_x2[i] = iterationsBisectionMethod(-1, 4, epsilons[i]);
        newton_iterations_x1[i] = iterationsNewtonMethod(-10, epsilons[i]);  
        newton_iterations_x2[i] = iterationsNewtonMethod(-1, epsilons[i]); 
    }

    fprintf(file, "+---------------+--------+-----------------------------------------------------------------------------------------------------------+\n");
    fprintf(file, "|               |        |                                            Количество итераций                                            |\n");
    fprintf(file, "|  Точность (ε) | Log(ε) |--------------------------------+--------------------+--------------------------------+--------------------+\n");
    fprintf(file, "|               |        | Метод половинного деления (x1) | Метод Ньютона (x1) | Метод половинного деления (x2) | Метод Ньютона (x2) |\n");
    fprintf(file, "+---------------+--------+--------------------------------+--------------------+--------------------------------+--------------------+\n");
    for (int i = 0; i < 5; i++) {
        fprintf(file, "|  %12.5f | %6.2f |   %28d |%19d |  %29d | %18d |\n", epsilons[i], logs[i], bisection_iterations_x1[i], newton_iterations_x1[i], 
        bisection_iterations_x2[i], newton_iterations_x2[i]);
        fprintf(table, "%f %f %d %d %d %d\n", epsilons[i], logs[i], bisection_iterations_x1[i], newton_iterations_x1[i], 
        bisection_iterations_x2[i], newton_iterations_x2[i]);
    }
    fprintf(file, "+---------------+--------+--------------------------------+--------------------+--------------------------------+--------------------+\n");
    fclose(file);
    fclose(table);

    FILE *gnuplot = popen("gnuplot -persistent", "w");
    
    if (gnuplot == NULL) {
        printf("Ошибка при открытии Gnuplot.\n");
        exit(1);
    }
    
    fprintf(gnuplot, "set title 'Количество итераций для x1 и x2'\n");
    fprintf(gnuplot, "set xlabel 'Log(eps)'\n");
    fprintf(gnuplot, "set ylabel 'Количество итераций'\n");
    fprintf(gnuplot, "set grid\n");
    fprintf(gnuplot, "set key left top\n");

    fprintf(gnuplot, "plot 'table.dat' using 2:3 with linespoints title 'Bisection_x1', "
                     "'table.dat' using 2:4 with linespoints title 'Newton_x1'\n");
    

    fflush(gnuplot);
    
    FILE *gnuplot1 = popen("gnuplot -persistent", "w");
    
    if (gnuplot1 == NULL) {
        printf("Ошибка при открытии Gnuplot.\n");
        exit(1);
    }

    fprintf(gnuplot1, "set title 'Количество итераций для x1 и x2'\n");
    fprintf(gnuplot1, "set xlabel 'Log(eps)'\n");
    fprintf(gnuplot1, "set ylabel 'Количество итераций'\n");
    fprintf(gnuplot1, "set grid\n");
    fprintf(gnuplot1, "set key left top\n");
    fprintf(gnuplot1, "plot 'table.dat' using 2:5 with linespoints title 'Bisection_x2', "
                     "'table.dat' using 2:6 with linespoints title 'Newton_x2'\n");
                     
    fflush(gnuplot1);
    pclose(gnuplot);
    pclose(gnuplot1);
}

int main() {
    //  plotGraph();
    // bisectionMethod(-10, -5, 1);
    // bisectionMethod(-1, 4, 2);   
    // newtonMethod(-10, 1);
    // newtonMethod(-1, 2);
    table();
    return 0;
}
