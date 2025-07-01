function [xvec,xdif,xsolution,ysolution,iterations] = impedance_bisection()
% Wyznacza miejsce zerowe funkcji impedance_difference metodą bisekcji.
% xvec - wektor z kolejnymi przybliżeniami miejsca zerowego, gdzie xvec(1)= (a+b)/2
% xdif - wektor różnic kolejnych przybliżeń miejsca zerowego
%   xdif(i) = abs(xvec(i+1)-xvec(i));
% xsolution - obliczone miejsce zerowe
% ysolution - wartość funkcji impedance_difference wyznaczona dla f=xsolution
% iterations - liczba iteracji wykonana w celu wyznaczenia xsolution

a = 1; % lewa granica przedziału poszukiwań miejsca zerowego
b = 10; % prawa granica przedziału poszukiwań miejsca zerowego
ytolerance = 1e-12; % tolerancja wartości funkcji w przybliżonym miejscu zerowym.
% Warunek abs(f1(xsolution))<ytolerance określa jak blisko zera ma znaleźć
% się wartość funkcji w obliczonym miejscu zerowym funkcji f1(), aby obliczenia
% zostały zakończone.
max_iterations = 1000; % maksymalna liczba iteracji wykonana przez alg. bisekcji

fa = impedance_difference(a);
fb = impedance_difference(b);

xvec = [];
xdif = [];
xsolution = Inf;
ysolution = Inf;
iterations = max_iterations;

for ii=1:max_iterations
    c = (a + b)/2;
    xvec(ii,1) = c;
    fc = impedance_difference(c);
    if(abs(fc)<ytolerance)
         xsolution = c;
         ysolution = fc;
         iterations = ii;
         break
    else 
        if fa * fc < 0
            b = c;
        else
            a = c;
        end
    end

end
    xdif = abs(diff(xvec));

% Tworzenie wspólnego wykresu z dwoma panelami (subplotami)
figure;

% Górny wykres: xvec w skali liniowej
subplot(2,1,1);
plot(1:length(xvec), xvec);
xlabel('Numer iteracji');
ylabel('Przybliżenie miejsca zerowego');
title('Kolejne przybliżenia miejsca zerowego - Metoda Bisekcji');
grid on;

% Dolny wykres: xdif w skali logarytmicznej
subplot(2,1,2);
semilogy(1:length(xdif), xdif);
xlabel('Numer iteracji');
ylabel('Różnice przybliżeń miejsca zerowego');
title('Różnice między kolejnymi przybliżeniami - Metoda Bisekcji');
grid on;


end

function impedance_delta = impedance_difference(f)
% Wyznacza moduł impedancji równoległego obwodu rezonansowego RLC pomniejszoną o wartość M.
% f - częstotliwość
    if f <= 0
        error('Podana częstotliwość jest mniejsza lub równa zero.')
    end
    R = 525;
    C = 7e-5;
    L = 3;
    M = 75;

    Z = 1 / (sqrt(1/(R^2) + (2*pi*f*C - 1 / (2*pi*f*L))^2));

    impedance_delta = Z - M;

end