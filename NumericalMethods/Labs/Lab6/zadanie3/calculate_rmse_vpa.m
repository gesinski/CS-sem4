function [dates, y, rmse_values, M, c_vpa, ya] = calculate_rmse_vpa()
% W tej funkcji obliczenia wykonywane są na zmiennych vpa, jednakże spośród
% zwracanych zmiennych tylko c_vpa jest wektorem zmiennych vpa.
%
% Funkcja calculate_rmse_vpa:
% 1) Wyznacza pierwiastek błędu średniokwadratowego w zależności od stopnia
%    aproksymacji wielomianowej danych przedstawiających produkcję energii.
% 2) Wyznacza i przedstawia na wykresie aproksymację wielomianową wysokiego
%    stopnia danych przedstawiających produkcję energii.
% Dla kraju C oraz źródła energii S:
% dates - wektor energy_2025.C.S.Dates (daty pomiaru produkcji energii)
% y - wektor energy_2025.C.S.EnergyProduction (poziomy miesięcznych produkcji energii)
% rmse_values(i,1) - RMSE wyznaczony dla wektora y i wielomianu i-tego stopnia
%     Rozmiar kolumnowego wektora wynosi length(y)-1.
% M - stopień wielomianu aproksymacyjnego przedstawionego na wykresie
% c_vpa - współczynniki wielomianu aproksymacyjnego przedstawionego na wykresie:
%       c = [c_M; ...; c_1; c_0]
% ya - wartości wielomianu aproksymacyjnego wyznaczone dla punktów danych
%       (rozmiar wektora ya powinien być taki sam jak rozmiar wektora y)

    digits(120); % określa liczbę cyfr dziesiętnych w zmiennych vpa

    M = 90; % stopień wielomianu aproksymacyjnego

    load energy_2025

    dates = energy_2025.Spain.Bioenergy.Dates; 
    y = energy_2025.Spain.Bioenergy.EnergyProduction; 

    % Przycięcie wektora danych ze względu na limit czasu obliczeń 
    % w Matlab Grader.
    %trim = 80;
    %if(numel(y)>trim)
    %    dates = dates(1:trim,1);
    %    y = y(1:trim,1);
    %end

    N = numel(y);
    degrees = 1:N-1;
    %degrees = [N-10, N-1];

    x_vpa = linspace(vpa(0),vpa(1),N)';
    y_vpa = vpa(y);

    rmse_values = zeros(numel(degrees),1);

    % Oblicz RMSE dla każdego stopnia
    id = 1;
    for m = degrees
        c = polyfit_qr_vpa(x_vpa, y_vpa, m);
        c = c(end:-1:1);
        app_y = polyval_vpa(c, x_vpa);
        rmse_values(id,1) = double(sqrt(mean((y_vpa - app_y).^2)));
        id = id + 1;
    end

    % Aproksymacja wielomianu wysokiego stopnia (dla wykresu)
    c_vpa = polyfit_qr_vpa(x_vpa, y_vpa, M);
    c_vpa = c_vpa(end:-1:1); % odwrócenie kolejności wektora c_vpa: dostosowanie do polyval

    ya = polyval_vpa(c_vpa, x_vpa);

    x = double(x_vpa);
    ya = double(ya); % konwersja vpa->double dla wykresu i formatu zwracanych danych

    figure;
    subplot(2,1,1);
    plot(degrees, rmse_values, 'b-', 'LineWidth', 2, 'MarkerFaceColor', 'cyan');
    title('RMSE w zależności od stopnia wielomianu');
    xlabel('Stopień wielomianu');
    ylabel('RMSE');
    grid on;

    subplot(2,1,2);
    plot(dates, y, 'k.-', 'LineWidth', 1.2); hold on;
    plot(dates, ya, 'r--', 'LineWidth', 2);
    title(['Porównanie danych oryginalnych z wartościami wielomianu aproksymacyjnego', num2str(M)]);
    xlabel('Data');
    ylabel('Produkcja energii');
    legend('Dane rzeczywiste', ['Aproksymacja M = ', num2str(M)], 'Location', 'best');
end


function y = polyval_vpa(coefficients, x)
% Oblicza wartość wielomianu w punktach x dla współczynników coefficients.
% Obliczenia wykonywane są na zmiennych vpa.
% coefficients – wektor współczynników wielomianu w kolejności od najwyższej potęgi
% x – wektor argumentów (zmienne vpa)
% y – wektor wartości wielomianu (zmienne vpa)

    n = length(coefficients);
    y = vpa(zeros(size(x)));  % inicjalizacja wyniku jako vpa

    for i = 1:n
        y = y .* x + coefficients(i);  % schemat Hornera
    end
end

function c_vpa = polyfit_qr_vpa(x, y, M)
    % Wyznacza współczynniki wielomianu aproksymacyjnego stopnia M
    % z zastosowaniem rozkładu QR.
    % c_vpa - kolumnowy wektor wsp. wielomianu c_vpa = [c_0; ...; c_M]
    %         zawierający zmienne vpa.

    A = vpa(zeros(numel(x),M+1)); % macierz Vandermonde o rozmiarze [n,M+1]
    for i = 1:M+1
        A(:, i) = x.^(i-1);   
    end
    [q1, r1] = qr(A, 0); % economy QR factorization
    c_vpa = vpa(r1 \ (q1.' * y));
end