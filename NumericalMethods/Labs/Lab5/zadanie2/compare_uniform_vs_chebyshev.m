function [N, x_uniform, y_fine_uniform, x_chebyshev, y_fine_chebyshev] = ...
        compare_uniform_vs_chebyshev()
% Funkcja ilustruje porównanie działania interpolacji wielomianowej funkcji
% Rungego wyznaczonej dla a) węzłów rozmieszczonych równomiernie,
% b) węzłów Czebyszewa.
% N - liczba węzłów interpolacji wynosi z przedziału [12,20].
% Funkcja zwraca następujące wektory wierszowe:
% x_uniform - węzły interpolacji rozmieszczone równomiernie
% y_fine_uniform - interpolacja wielomianowa wyznaczona dla
%   równomiernie rozmieszczonych węzłów interpolacji
% x_chebyshev - węzły Czebyszewa
% y_fine_chebyshev - interpolacja wielomianowa wyznaczona dla węzłów Czebyszewa

    N = 16; % liczba węzłów interpolacji

    % Gęsta siatka punktów do testowania interpolacji
    x_fine = linspace(-1, 1, 1000);

    % funkcja Rungego
    runge_function = @(x) 1 ./ (1 + 25 * x.^2);
    y_fine_reference = runge_function(x_fine);

    % 1. węzły równomiernie rozmieszczone
    x_uniform = linspace(-1, 1, N);
    % obliczenie wartości funkcji w węzłach
    y_uniform = runge_function(x_uniform);
    y_uniform = y_uniform(:);
    % wyznaczenie macierzy Vandermonde'a
    V_uniform = get_vandermonde_matrix(x_uniform);
    % wyznaczenie współczynników wielomianu interpolacyjnego
    coeff_uniform =  V_uniform\y_uniform;
    % odwrócenie kolejności wsp. wielomianów: dostosowanie do polyval
    coeff_uniform = coeff_uniform(end:-1:1);
    % wyznaczenie wartości wielomianu w punktach testowych
    y_fine_uniform = polyval(coeff_uniform, x_fine);

    % 2. węzły Czebyszewa II rodzaju
    x_chebyshev = get_chebyshev_nodes(N);
    y_chebyshev = runge_function(x_chebyshev);
    y_chebyshev = y_chebyshev(:);
    V_chebyshev = get_vandermonde_matrix(x_chebyshev); 
    coeff_chebyshev = V_chebyshev\y_chebyshev; 
    coeff_chebyshev = coeff_chebyshev (end:-1:1);
    y_fine_chebyshev = polyval(coeff_chebyshev, x_fine);

    % 3. Wykresy
    subplot(2,1,1);
    plot(x_fine, y_fine_reference, 'k--', 'LineWidth', 2, 'DisplayName', 'Funkcja wzorcowa');
    hold on;
    
    plot(x_fine, y_fine_uniform, 'm', 'DisplayName', ['Interpolacja N = ', num2str(N)]);
    plot(x_uniform, y_uniform, 'mo', 'DisplayName', ['Wartości w węzłach. N = ', num2str(N)]);
    hold off ;
    legend show;
    legend('Location', 'eastoutside')
    title('Interpolacja równomiernie rozmieszczonych węzłów');
    xlabel('x');
    ylabel('y');

    subplot(2,1,2);
    plot(x_fine, y_fine_reference, 'k--', 'LineWidth', 2, 'DisplayName', 'Funkcja wzorcowa');
    hold on;

    plot(x_fine, y_fine_chebyshev, 'b', 'DisplayName', ['Interpolacja N = ', num2str(N)]);
    plot(x_chebyshev, y_chebyshev, 'bo', 'DisplayName', ['Wartości w węzłach. N = ', num2str(N)]);
    hold off ;
    legend show;
    legend('Location', 'eastoutside')
    title('Interpolacja  węzłów Czebyszewa');
    xlabel('x');
    ylabel('y');

    set(gcf, 'Position', [1000 500 2000 1500]);
end

function x = get_chebyshev_nodes(N)
    % Węzły Czebyszewa drugiego rodzaju wyznaczone w przedziale [-1, 1]
    x = zeros(N, 1);
    for k = 1:N
        x(k) = cos((k - 1)/(N - 1) * pi);
    end
end

function V = get_vandermonde_matrix(x)
    % Buduje macierz Vandermonde’a na podstawie wektora węzłów interpolacji x.
    N = length(x);
    V = ones(N, N);
    for i = 2:N
        V(:, i) = x.^(i-1);
    end
end