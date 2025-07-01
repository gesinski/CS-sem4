function [dates, y, rmse_values, M, c, ya] = calculate_rmse()
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
% c - współczynniki wielomianu aproksymacyjnego przedstawionego na wykresie:
%       c = [c_M; ...; c_1; c_0]
% ya - wartości wielomianu aproksymacyjnego wyznaczone dla punktów danych
%       (rozmiar wektora ya powinien być taki sam jak rozmiar wektora y)

    M = 90; % stopień wielomianu aproksymacyjnego (dla wykresu)

    load energy_2025

    dates = energy_2025.Spain.Bioenergy.Dates; 
    y = energy_2025.Spain.Bioenergy.EnergyProduction; 

    N = numel(y);
    degrees = 1:N-1;

    x = linspace(0,1,N)';

    rmse_values = zeros(numel(degrees),1);

    for m = degrees
        temp_c = polyfit_qr(x, y, m);
        temp_c = temp_c(end:-1:1); 
        app_y = polyval(temp_c, x);
        rmse_values(m) = sqrt(mean((y - app_y).^2));
    end

    % Aproksymacja wielomianu wysokiego stopnia (dla wykresu)
    c = polyfit_qr(x, y, M);
    c = c(end:-1:1); % odwrócenie kolejności wektora c: dostosowanie do polyval

    ya = polyval(c, x);

    figure;

    % Górny wykres - RMSE
    subplot(2,1,1);
    plot(degrees, rmse_values, 'b-', 'MarkerSize', 4);
    title('RMSE w zależności od stopnia wielomianu aproksymacyjnego');
    xlabel('Stopień wielomianu');
    ylabel('RMSE');
    grid on;

    % Dolny wykres - dane i aproksymacja
    subplot(2,1,2);
    plot(dates, y, 'b-', 'DisplayName', 'Dane oryginalne'); hold on;
    plot(dates, ya, 'r--', 'LineWidth', 2, 'DisplayName', sprintf('Wielomian stopnia %d', M));
    title('Porównanie danych oryginalnych z wartościami wielomianu aproksymacyjnego');
    xlabel('Data');
    ylabel('Produkcja energii [TWh]');
    legend('Location', 'best');
    grid on;

end

function c = polyfit_qr(x, y, M)
    % Wyznacza współczynniki wielomianu aproksymacyjnego stopnia M
    % z zastosowaniem rozkładu QR.
    % c - kolumnowy wektor wsp. wielomianu c = [c_0; ...; c_M]

    A = zeros(numel(x),M+1); % macierz Vandermonde o rozmiarze [n,M+1]
    for i = 1:M+1
        A(:, i) = x.^(i-1);   
    end
    [q1, r1] = qr(A, 0); % economy QR factorization
    c = r1 \ (q1.' * y);
end
