% Коэффициенты уравнения
a0 = -1.951;
a1 = 0.010;
a2 = 0.970;
a3 = 0.143;
a4 = -0.054;


% Начальные параметры
x0 = -3.9;
y0 = -1.4;
dx = 0.05;
x_target = -3.3; %-3.3

f = @(x, y) a0 + a1 * x + a2 * x^2 + a3 * y + a4 * y * x;
% Вычисления методами
[e_x, e_y, e_c] = euler('euler.txt', x0, y0, x_target, dx, f);

[em_x, em_y, em_c] = euler_mod('euler_mod.txt', x0, y0, x_target, dx, f);
[em2_x, em2_y, em2_c] = euler_mod('euler_mod_dop.txt', x0, y0, x_target, dx/2, f);
[em4_x, em4_y, em4_c] = euler_mod('euler_mod_dop.txt', x0, y0, x_target, dx/4, f);
[em6_x, em6_y, em6_c] = euler_mod('euler_mod_dop.txt', x0, y0, x_target, dx/6, f);
[em8_x, em8_y, em8_c] = euler_mod('euler_mod_dop.txt', x0, y0, x_target, dx/8, f);

points = [em_c, em2_c, em4_c, em6_c, em8_c];
em_Y = [em_y(end), em2_y(end), em4_y(end), em6_y(end), em8_y(end)];

[ek_x, ek_y, ek_c] = euler_koshi('euler_koshi.txt', x0, y0, x_target, dx, f);
[rk_x, rk_y, rk_c] = runge_kutt('runge_kutt.txt', x0, y0, x_target, dx, f);
[rk2_x, rk2_y, rk2_c] = runge_kutt('runge_kutt_2.txt', x0, y0, x_target, dx/10, f);

% Абсолютные ошибки
[e_mistake, ek_mistake, rk_mistake] = absolut_mistake(e_y, ek_y, rk_y, rk2_y);

% Ошибки по точкам
mistakes = mistake_by_points(points, em_Y, rk2_y);

% Построение графика №1
figure; 

plot(e_x, e_y, '-r', 'LineWidth', 2); 
hold on; 

plot(ek_x, ek_y, '--g', 'LineWidth', 2); 
plot(rk_x, rk_y, ':b', 'LineWidth', 2); 
plot(rk2_x, rk2_y, '-.k', 'LineWidth', 2); 

legend('Метод Эйлера', 'Метод Эйлера-Коши', ...
       'Метод Рунге-Кутта', 'Метод Рунге-Кутта (dx=0,005)', 'Location', 'best');

xlabel('x'); 
ylabel('y'); 

title('Сравнение численных методов решения');

grid on;

hold off;
saveas(gcf, 'comparison_plot.png');

% Построение графика №2
figure;

plot(rk2_x, rk2_y, '-b', 'LineWidth', 1);
hold on;

plot(em_x, em_y, '--y', 'LineWidth', 1);
plot(em2_x, em2_y, '-.b', 'LineWidth', 1);
plot(em4_x, em4_y, ':r', 'LineWidth', 1);
plot(em6_x, em6_y, '.g', 'LineWidth', 1);
plot(em8_x, em8_y, '-r', 'LineWidth', 1);

legend('РК (dx=0,005)', 'МЭ (dx=0,05)', 'МЭ (dx=0,025)', 'МЭ (dx=0,0125)' ...
    , 'МЭ (dx=0,008333)', 'МЭ (dx=0,00625)')

xlabel('x'); 
ylabel('y'); 

title('График зависимостей y=y(x)');

grid on;

hold off;
saveas(gcf, 'comparison_plot2.png');

% Построение столбчатой диаграммы
errors = [e_mistake, ek_mistake, rk_mistake]; % Абсолютные ошибки
methods = {'Э', 'ЭК', 'РК'}; % Названия методов

% Построение столбчатой диаграммы
figure; 
bar(errors, 'FaceColor', [0.2 0.6 0.8]); 

set(gca, 'XTickLabel', methods, 'FontSize', 12); 
xlabel('Метод решения', 'FontSize', 14); 
ylabel('Абсолютная ошибка', 'FontSize', 14); 

title('Зависимость абсолютной ошибки от метода', 'FontSize', 16);

grid on;

saveas(gcf, 'absolute_error_bar_chart.png'); 

% Построение графика №3
figure; % Создаём новое окно для графика
plot(points, mistakes, '-k', 'LineWidth', 2); % Линия чёрного цвета с толщиной 2

% Подписи осей
xlabel('Количество точек интегрирования', 'FontSize', 14); % Подпись оси X
ylabel('Абсолютная ошибка', 'FontSize', 14); % Подпись оси Y

% Заголовок графика
title('Зависимость абсолютной ошибки от количества точек интегрирования', 'FontSize', 16);

% Настройка осей
grid on; % Включение сетки
axis tight; % Автоматическое поджатие осей под данные

% Сохранение графика (опционально)
saveas(gcf, 'absolute_error_vs_points.png');

% Метод Эйлера
function [X, Y, count] = euler(filename, x, y, x_target, dx, f)
    fileID = fopen(filename, 'w');
    fprintf(fileID, 'x\t\t\ty\t\t\tK1\n');
    X = [];
    Y = [];
    count = 0;
    while x < x_target
        K1 = dx * f(x, y);
        fprintf(fileID, '%.3f\t%.6f\t%.6f\n', x, y, K1);
        X(end+1) = x;
        Y(end+1) = y;
        x = x + dx;
        y = y + K1;
        count = count + 1;
    end
    fclose(fileID);
end

% Модифицированный метод Эйлера
function [X, Y, count] = euler_mod(filename, x, y, x_target, dx, f)
    fileID = fopen(filename, 'w');
    fprintf(fileID, 'x\t\t\ty\t\t\tK1\t\t\tK2\n');
    X = [];
    Y = [];
    count = 0;
    
    while x < x_target
        % Если следующий шаг превышает x_target, корректируем шаг dx
        if x + dx > x_target
            dx = x_target - x;
        end
        
        K1 = (dx / 2) * f(x, y);
        K2 = dx * f(x + dx / 2, y + K1);
        fprintf(fileID, '%.3f\t%.6f\t%.6f\t%.6f\n', x, y, K1, K2);
        X(end+1) = x;
        Y(end+1) = y;
        x = x + dx;
        y = y + K2;
        count = count + 1;
    end
    
    % Записываем финальную точку (если не попали точно)
    if abs(x - x_target) < 1e-10
        X(end+1) = x_target;
        Y(end+1) = y;
    end
    
    fclose(fileID);
end

% Метод Эйлера-Коши
function [X, Y, count] = euler_koshi(filename, x, y, x_target, dx, f)
    fileID = fopen(filename, 'w');
    fprintf(fileID, 'x\t\t\ty\t\t\tK1\t\t\tK2\n');
    X = [];
    Y = [];
    count = 0;
    while x < x_target
        K1 = dx * f(x, y);
        K2 = dx * f(x + dx, y + K1);
        fprintf(fileID, '%.3f\t%.6f\t%.6f\t%.6f\n', x, y, K1, K2);
        X(end+1) = x;
        Y(end+1) = y;
        x = x + dx;
        y = y + (K1 + K2) / 2;
        count = count + 1;
    end
    fclose(fileID);
end

% Метод Рунге-Кутты
function [X, Y, count] = runge_kutt(filename, x, y, x_target, dx, f)
    fileID = fopen(filename, 'w');
    fprintf(fileID, 'x\t\t\ty\t\t\tK1\t\t\tK2\t\t\tK3\t\t\tK4\n');
    X = [];
    Y = [];
    count = 0;
    while x < x_target
        K1 = dx * f(x, y);
        K2 = dx * f(x + dx/2, y + K1/2);
        K3 = dx * f(x + dx/2, y + K2/2);
        K4 = dx * f(x + dx, y + K3);
        fprintf(fileID, '%.3f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\n', x, y, K1, K2, K3, K4);
        X(end+1) = x;
        Y(end+1) = y;
        x = x + dx;
        y = y + (1/6) * (K1 + 2*K2 + 2*K3 + K4);
        count = count + 1;
    end
    fclose(fileID);
end

% Абсолютные ошибки
function [e_mistake, ek_mistake, rk_mistake] = absolut_mistake(e_y, ek_y, rk_y, rk2_y)
    e_mistake = round(abs(rk2_y(end) - e_y(end)), 5);
    ek_mistake = round(abs(rk2_y(end) - ek_y(end)), 5);
    rk_mistake = round(abs(rk2_y(end) - rk_y(end)), 5);
    fileID = fopen('mistakes.txt', 'w');
    fprintf(fileID, 'Метод решения\tАбсолютная ошибка\n');
    fprintf(fileID, 'Э\t\t\t\t%.5f\nЭК\t\t\t\t%.5f\nРК\t\t\t\t%.5f\n', e_mistake, ek_mistake, rk_mistake);
    fclose(fileID);
end

% Ошибки по точкам
function mistakes = mistake_by_points(points, em_Y, rk2_y)
    mistakes = [];
    fileID = fopen('mistakes_by_points.txt', 'w');
    fprintf(fileID, 'Количество точек\tАбсолютная ошибка\n');
    for i = 1:length(points)
        mistake = round(abs(rk2_y(end) - em_Y(i)), 5);
        mistakes(end+1) = mistake; %#ok<AGROW>
        fprintf(fileID, '%d\t\t\t\t\t%.5f\n', points(i), mistake);
        disp(['Ошибка на шаге ', num2str(i), ': ', num2str(mistake)]);
    end
    fclose(fileID);
    disp('Массив ошибок:');
    disp(mistakes);
end



