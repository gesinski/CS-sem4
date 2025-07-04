function [xvec,xdif,xsolution,ysolution,iterations] = velocity_secant()
% Wyznacza miejsce zerowe funkcji velocity_difference metodą siecznych.
% xvec - wektor z kolejnymi przybliżeniami miejsca zerowego;
%   xvec(1)=x2 przy założeniu, że x0 i x1 są punktami startowymi
% xdif - wektor różnic kolejnych przybliżeń miejsca zerowego
%   xdif(i) = abs(xvec(i+1)-xvec(i));
% xsolution - obliczone miejsce zerowe
% ysolution - wartość funkcji velocity_difference wyznaczona dla f=xsolution
% iterations - liczba iteracji wykonana w celu wyznaczenia xsolution

x0 = 1; % pierwszy punkt startowy metody siecznych
x1 = 40; % drugi punkt startowy metody siecznych
ytolerance = 1e-12;% tolerancja wartości funkcji w przybliżonym miejscu zerowym.
% Warunek abs(f1(xsolution))<ytolerance określa jak blisko zera ma znaleźć
% się wartość funkcji w obliczonym miejscu zerowym funkcji f1(), aby obliczenia
% zostały zakończone.
max_iterations = 1000; % maksymalna liczba iteracji wykonana przez alg. bisekcji

f0 = velocity_difference(x0);
f1 = velocity_difference(x1);

xvec = [];
xdif = [];
xsolution = Inf;
ysolution = Inf;
iterations = max_iterations;

for ii=1:max_iterations
    x2 = x1 - ((f1 * (x1 - x0)) / (f1 - f0));
    xvec(ii,1) = x2;
    f2 = velocity_difference(x2);
    if(abs(f2)<ytolerance)
         xsolution = x2;
         ysolution = f2;
         iterations = ii;
         break
    else
        x0 = x1;
        x1 = x2;
        f0 = f1;
        f1 = f2;
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
title('Kolejne przybliżenia miejsca zerowego - Metoda Siecznych');
grid on;

% Dolny wykres: xdif w skali logarytmicznej
subplot(2,1,2);
semilogy(1:length(xdif), xdif);
xlabel('Numer iteracji');
ylabel('Różnice przybliżeń miejsca zerowego');
title('Różnice między kolejnymi przybliżeniami - Metoda Siecznych');
grid on;


end

function velocity_delta = velocity_difference(t)
% t - czas od startu rakiety
    if t <= 0
        error('Podany czas jest mniejszy lub równy zero.')
    end
    u = 2000;
    m0 = 150000;
    q = 2700;
    g = 1.622;
    M = 700;

    v = u * log(m0 / (m0 - q * t)) - g * t;

    velocity_delta = v - M;

end